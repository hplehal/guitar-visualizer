"""
test_pitch_detector.py
======================
Live audio test for PitchDetector.
Plug in your guitar, run this script, and play notes/chords.

Requirements:
    pip install sounddevice numpy librosa scipy

Usage:
    python test_pitch_detector.py
    python test_pitch_detector.py --device 2       # use a specific input device
    python test_pitch_detector.py --list-devices   # see all available devices
    python test_pitch_detector.py --buffer 0.1     # change buffer size in seconds (default 0.15)
"""

import argparse
import sys
import time
import numpy as np

try:
    import sounddevice as sd
except ImportError:
    print("ERROR: sounddevice not installed. Run:  pip install sounddevice")
    sys.exit(1)

try:
    from pitch_detector import PitchDetector
except ImportError:
    print("ERROR: pitch_detector.py not found. Make sure it's in the same folder as this script.")
    sys.exit(1)


# ------------------------------------------------------------------ #
#  Helpers                                                            #
# ------------------------------------------------------------------ #

RESET  = "\033[0m"
BOLD   = "\033[1m"
GREEN  = "\033[92m"
YELLOW = "\033[93m"
CYAN   = "\033[96m"
RED    = "\033[91m"
DIM    = "\033[2m"

def colour(text, code):
    return f"{code}{text}{RESET}"

def print_result(result, elapsed_ms):
    if not result['has_note']:
        # Only print silence every ~20 frames to avoid spam
        return

    amp_bar_len = int(min(result['amplitude'] * 400, 30))
    amp_bar = "█" * amp_bar_len + colour("░" * (30 - amp_bar_len), DIM)
    conf_pct = int(result['confidence'] * 100)

    if result['is_chord']:
        chord_label = colour(f"CHORD  {result['chord_name'] or '?'}", YELLOW + BOLD)
        notes_str = "  ".join(result['notes'])
        freqs_str = "  ".join(f"{f:.1f}Hz" for f in result['frequencies'])
        print(f"\n{chord_label}")
        print(f"  Notes : {colour(notes_str, CYAN)}")
        print(f"  Freqs : {colour(freqs_str, DIM)}")
        print(f"  Conf  : {conf_pct}%   Vol: [{amp_bar}]   {elapsed_ms:.1f}ms")
    else:
        note_label = colour(f"NOTE   {result['note']}", GREEN + BOLD)
        freq_str = colour(f"{result['frequency']:.2f} Hz", DIM)
        print(f"{note_label}   {freq_str}   Conf: {conf_pct}%   Vol: [{amp_bar}]   {elapsed_ms:.1f}ms")


def list_devices():
    print("\nAvailable audio input devices:\n")
    devices = sd.query_devices()
    for i, dev in enumerate(devices):
        if dev['max_input_channels'] > 0:
            marker = " <-- default" if i == sd.default.device[0] else ""
            print(f"  [{i:2d}] {dev['name']}{colour(marker, GREEN)}")
    print()


# ------------------------------------------------------------------ #
#  Synthetic tests (no microphone needed)                             #
# ------------------------------------------------------------------ #

def make_sine(freq, sample_rate=44100, duration=0.15, amplitude=0.5):
    t = np.linspace(0, duration, int(sample_rate * duration), endpoint=False)
    return (amplitude * np.sin(2 * np.pi * freq * t)).astype(np.float64)

def make_chord(freqs, sample_rate=44100, duration=0.15, amplitude=0.4):
    t = np.linspace(0, duration, int(sample_rate * duration), endpoint=False)
    wave = sum(amplitude * np.sin(2 * np.pi * f * t) for f in freqs)
    wave /= np.max(np.abs(wave) + 1e-9)
    return (wave * amplitude).astype(np.float64)

def make_guitar_like(freq, sample_rate=44100, duration=0.15, amplitude=0.5):
    """Sine + harmonics to simulate a guitar-like timbre."""
    t = np.linspace(0, duration, int(sample_rate * duration), endpoint=False)
    wave = (
        amplitude       * np.sin(2 * np.pi * freq * t) +
        amplitude * 0.5 * np.sin(2 * np.pi * freq * 2 * t) +
        amplitude * 0.3 * np.sin(2 * np.pi * freq * 3 * t) +
        amplitude * 0.15* np.sin(2 * np.pi * freq * 4 * t)
    )
    wave /= np.max(np.abs(wave) + 1e-9)
    return (wave * amplitude).astype(np.float64)

def run_synthetic_tests(detector):
    print(colour("\n=== Synthetic Tests (no microphone) ===\n", BOLD))

    tests = [
        # (label, audio, expected_note_or_chord)
        ("Silence",          np.zeros(6615),                                  "silence"),
        ("E2 (low E string)", make_guitar_like(82.41),                        "E2"),
        ("A2 (A string)",    make_guitar_like(110.00),                        "A2"),
        ("D3 (D string)",    make_guitar_like(146.83),                        "D3"),
        ("G3 (G string)",    make_guitar_like(196.00),                        "G3"),
        ("B3 (B string)",    make_guitar_like(246.94),                        "B3"),
        ("E4 (high e)",      make_guitar_like(329.63),                        "E4"),
        ("C Major chord",    make_chord([261.63, 329.63, 392.00]),             "C Major"),
        ("A Minor chord",    make_chord([220.00, 261.63, 329.63]),             "A Minor"),
        ("E Power chord",    make_chord([82.41, 123.47]),                     "E Power"),
        ("G Major chord",    make_chord([196.00, 246.94, 293.66, 392.00]),    "G Major"),
        ("D Major chord",    make_chord([146.83, 220.00, 293.66]),             "D Major"),
        ("Noisy signal",     np.random.normal(0, 0.005, 6615),               "silence/noise"),
    ]

    passed = 0
    failed = 0

    for label, audio, expected in tests:
        t0 = time.perf_counter()
        result = detector.detect_pitch(audio)
        elapsed = (time.perf_counter() - t0) * 1000

        if expected == "silence" or expected == "silence/noise":
            ok = not result['has_note']
            got = "silence" if not result['has_note'] else result.get('note') or str(result.get('notes'))
        elif expected.endswith("chord") or "Major" in expected or "Minor" in expected or "Power" in expected:
            ok = result['is_chord']
            got = result.get('chord_name') or str(result.get('notes'))
        else:
            ok = result.get('note', '').startswith(expected[:2])
            got = result.get('note') or "nothing"

        status = colour("PASS", GREEN) if ok else colour("FAIL", RED)
        print(f"  {status}  {label:<25} expected={expected:<15} got={got:<20} {elapsed:.1f}ms")

        if ok:
            passed += 1
        else:
            failed += 1

    print(f"\n  {colour(f'{passed} passed', GREEN)}, {colour(f'{failed} failed', RED if failed else DIM)}\n")
    return failed == 0


# ------------------------------------------------------------------ #
#  Live audio test                                                    #
# ------------------------------------------------------------------ #

def run_live_test(detector, device, buffer_seconds):
    sample_rate = 44100
    buffer_size = int(sample_rate * buffer_seconds)

    print(colour("\n=== Live Guitar Test ===", BOLD))
    print(f"  Sample rate : {sample_rate} Hz")
    print(f"  Buffer size : {buffer_size} samples ({buffer_seconds*1000:.0f} ms)")
    print(f"  Device      : {device if device is not None else 'default'}")
    print(colour("\n  Plug in your guitar and start playing!", CYAN))
    print(colour("  Press Ctrl+C to stop.\n", DIM))

    silence_counter = 0

    def callback(indata, frames, time_info, status):
        nonlocal silence_counter

        if status:
            print(colour(f"  [stream warning] {status}", RED))

        audio = indata[:, 0].astype(np.float64)

        t0 = time.perf_counter()
        result = detector.detect_pitch(audio)
        elapsed = (time.perf_counter() - t0) * 1000

        if not result['has_note']:
            silence_counter += 1
            # Print a dot every 20 silent frames so user knows it's alive
            if silence_counter % 20 == 0:
                print(colour(".", DIM), end="", flush=True)
        else:
            silence_counter = 0
            print_result(result, elapsed)

    try:
        with sd.InputStream(
            samplerate=sample_rate,
            channels=1,
            dtype='float32',
            blocksize=buffer_size,
            device=device,
            callback=callback,
        ):
            while True:
                time.sleep(0.1)

    except KeyboardInterrupt:
        print(colour("\n\n  Stopped.", DIM))
    except sd.PortAudioError as e:
        print(colour(f"\nAudio device error: {e}", RED))
        print("Try running with --list-devices to find the right device index,")
        print("then re-run with --device <number>")


# ------------------------------------------------------------------ #
#  Entry point                                                        #
# ------------------------------------------------------------------ #

def main():
    parser = argparse.ArgumentParser(description="Test PitchDetector with live guitar audio.")
    parser.add_argument("--list-devices", action="store_true",
                        help="List all available audio input devices and exit.")
    parser.add_argument("--device", type=int, default=None,
                        help="Audio input device index (from --list-devices).")
    parser.add_argument("--buffer", type=float, default=0.15,
                        help="Audio buffer size in seconds (default: 0.15).")
    parser.add_argument("--synthetic-only", action="store_true",
                        help="Only run synthetic tests, skip live audio.")
    args = parser.parse_args()

    if args.list_devices:
        list_devices()
        return

    detector = PitchDetector(sample_rate=44100)

    # Always run synthetic tests first
    all_passed = run_synthetic_tests(detector)

    if args.synthetic_only:
        sys.exit(0 if all_passed else 1)

    # Then go live
    run_live_test(detector, device=args.device, buffer_seconds=args.buffer)


if __name__ == "__main__":
    main()