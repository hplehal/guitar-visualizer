"""
audio/pitch_detector.py - Librosa with harmonic filtering
"""

import numpy as np
import librosa
from typing import List, Dict, Optional
import time


class PitchDetector:
    """Detects single notes and chords using librosa"""
    
    def __init__(self, sample_rate: int = 44100):
        self.sample_rate = sample_rate
        self.min_freq = 60.0
        self.max_freq = 1400.0
        
        # Chord detection timing
        self.last_note_time = 0
        self.chord_time_threshold = 0.05  # Notes within 50ms = chord
        self.pending_notes = []           # Notes waiting to be classified
        
        self.note_names = ['C', 'C#', 'D', 'D#', 'E', 'F', 
                          'F#', 'G', 'G#', 'A', 'A#', 'B']
    
    def detect_pitch(self, audio_data: np.ndarray) -> dict:
        """Main detection - handles single notes and chords"""
        amplitude = np.sqrt(np.mean(audio_data ** 2))
        
        if amplitude < 0.02:
            return self._empty_result(amplitude)
        
        # Try pyin first (best for single notes)
        single_note = self._detect_single_note(audio_data, amplitude)
        
        if single_note:
            return single_note
        
        # Try chord detection
        chord = self._detect_chord(audio_data, amplitude)
        
        if chord:
            return chord
        
        return self._empty_result(amplitude)
    
    def _detect_single_note(self, audio_data: np.ndarray, amplitude: float) -> Optional[dict]:
        """Detect single note using pyin"""
        try:
            f0, voiced_flag, voiced_probs = librosa.pyin(
                audio_data,
                fmin=self.min_freq,
                fmax=self.max_freq,
                sr=self.sample_rate
            )
        except Exception:
            return None
        
        if voiced_flag is None or not np.any(voiced_flag):
            return None
        
        valid_pitches = f0[voiced_flag]
        valid_probs = voiced_probs[voiced_flag]
        
        if len(valid_pitches) == 0:
            return None
        
        best_idx = np.argmax(valid_probs)
        frequency = valid_pitches[best_idx]
        confidence = valid_probs[best_idx]
        
        # Higher confidence threshold for single notes
        if confidence < 0.6:
            return None
        
        if np.isnan(frequency) or not (self.min_freq <= frequency <= self.max_freq):
            return None
        
        note_info = self._frequency_to_note(frequency)
        
        return {
            'is_chord': False,
            'notes': [note_info['note']],
            'note_names': [note_info['note_name']],
            'frequencies': [float(frequency)],
            'note_numbers': [note_info['note_number']],
            'amplitude': amplitude,
            'confidence': float(confidence),
            'has_note': True,
            'note': note_info['note'],
            'note_number': note_info['note_number'],
            'frequency': float(frequency),
        }
    
    def _detect_chord(self, audio_data: np.ndarray, amplitude: float) -> Optional[dict]:
        """Detect chord using piptrack with harmonic filtering"""
        try:
            pitches, magnitudes = librosa.piptrack(
                y=audio_data,
                sr=self.sample_rate,
                fmin=self.min_freq,
                fmax=self.max_freq,
                threshold=0.1
            )
        except Exception:
            return None
        
        # Extract strong pitches
        detected = self._extract_strong_pitches(pitches, magnitudes)
        
        if not detected:
            return None
        
        # KEY FIX: Remove harmonics!
        filtered = self._remove_harmonics(detected)
        
        if not filtered:
            return None
        
        # If only one note after filtering, it's a single note
        if len(filtered) == 1:
            return {
                'is_chord': False,
                'notes': [filtered[0]['note']],
                'note_names': [filtered[0]['note_name']],
                'frequencies': [filtered[0]['frequency']],
                'note_numbers': [filtered[0]['note_number']],
                'amplitude': amplitude,
                'confidence': 0.6,
                'has_note': True,
                'note': filtered[0]['note'],
                'note_number': filtered[0]['note_number'],
                'frequency': filtered[0]['frequency'],
            }
        
        # Multiple notes after filtering = actual chord!
        return {
            'is_chord': True,
            'notes': [n['note'] for n in filtered],
            'note_names': [n['note_name'] for n in filtered],
            'frequencies': [n['frequency'] for n in filtered],
            'note_numbers': [n['note_number'] for n in filtered],
            'amplitude': amplitude,
            'confidence': 0.7,
            'has_note': True,
            'note': filtered[0]['note'],
            'note_number': filtered[0]['note_number'],
            'frequency': filtered[0]['frequency'],
        }
    
    def _remove_harmonics(self, notes: List[Dict], tolerance: float = 8.0) -> List[Dict]:
        """
        Remove harmonics from detected notes
        Keeps only the fundamental frequencies
        """
        if len(notes) <= 1:
            return notes
        
        # Sort by frequency (lowest = most likely fundamental)
        sorted_notes = sorted(notes, key=lambda x: x['frequency'])
        keep = []
        
        for i, note in enumerate(sorted_notes):
            is_harmonic = False
            
            # Check against all lower notes
            for lower in sorted_notes[:i]:
                if self._is_harmonic(note['frequency'], lower['frequency'], tolerance):
                    is_harmonic = True
                    break
            
            if not is_harmonic:
                keep.append(note)
        
        return keep
    
    def _is_harmonic(self, freq: float, fundamental: float, tolerance: float = 8.0) -> bool:
        """Check if freq is a harmonic of fundamental"""
        for multiplier in range(2, 8):  # 2nd through 7th harmonic
            harmonic = fundamental * multiplier
            if abs(freq - harmonic) < tolerance:
                return True
        return False
    
    def _extract_strong_pitches(self, pitches: np.ndarray, magnitudes: np.ndarray) -> List[Dict]:
        """Extract significant pitches from piptrack"""
        detected = []
        max_magnitude = np.max(magnitudes)
        
        if max_magnitude == 0:
            return []
        
        absolute_minimum = 5.0

        for t in range(pitches.shape[1]):
            for freq_bin in range(pitches.shape[0]):
                magnitude = magnitudes[freq_bin, t]
                pitch = pitches[freq_bin, t]
                
                if magnitude > max_magnitude * 0.3 and pitch > 0:
                    if self.min_freq <= pitch <= self.max_freq:
                        note_info = self._frequency_to_note(pitch)
                        note_info['magnitude'] = float(magnitude)
                        detected.append(note_info)
        
        if not detected:
            return []
        
        # Deduplicate
        deduped = self._deduplicate_notes(detected)
        deduped.sort(key=lambda x: x['magnitude'], reverse=True)
        return deduped[:6]  # Keep top 6 before harmonic filtering
    
    def _deduplicate_notes(self, notes: List[Dict]) -> List[Dict]:
        """Remove notes too close in frequency"""
        if not notes:
            return []
        
        unique = []
        used = set()
        
        for i, note in enumerate(notes):
            if i in used:
                continue
            
            group = [note]
            for j, other in enumerate(notes):
                if i != j and j not in used:
                    if abs(note['frequency'] - other['frequency']) < 5:
                        group.append(other)
                        used.add(j)
            
            best = max(group, key=lambda x: x['magnitude'])
            unique.append(best)
            used.add(i)
        
        return unique
    
    def _frequency_to_note(self, frequency: float) -> Dict:
        """Convert Hz to note info"""
        semitones_from_a4 = 12 * np.log2(frequency / 440.0)
        note_number = int(round(69 + semitones_from_a4))
        octave = (note_number // 12) - 1
        note_index = note_number % 12
        note_name = self.note_names[note_index]
        
        return {
            'note': f"{note_name}{octave}",
            'note_name': note_name,
            'note_number': note_number,
            'octave': octave,
            'frequency': float(frequency)
        }
    
    def _empty_result(self, amplitude: float) -> dict:
        """Empty result when nothing detected"""
        return {
            'is_chord': False,
            'notes': [],
            'note_names': [],
            'frequencies': [],
            'note_numbers': [],
            'amplitude': float(amplitude),
            'confidence': 0.0,
            'has_note': False,
            'note': None,
            'note_number': None,
            'frequency': 0.0,
        }
    
    def identify_chord(self, note_numbers: List[int]) -> Optional[str]:
        """Identify chord name from MIDI note numbers"""
        if len(note_numbers) < 2:
            return None
        
        normalized = sorted(set([n % 12 for n in note_numbers]))
        
        if len(normalized) < 2:
            return None
        
        root = normalized[0]
        root_name = self.note_names[root]
        intervals = set([(n - root) % 12 for n in normalized])
        
        patterns = {
            frozenset([0, 4, 7]):     "Major",
            frozenset([0, 3, 7]):     "Minor",
            frozenset([0, 4, 7, 11]): "Major 7",
            frozenset([0, 3, 7, 10]): "Minor 7",
            frozenset([0, 4, 7, 10]): "Dominant 7",
            frozenset([0, 3, 6]):     "Diminished",
            frozenset([0, 4, 8]):     "Augmented",
            frozenset([0, 5, 7]):     "Sus4",
            frozenset([0, 2, 7]):     "Sus2",
            frozenset([0, 7]):        "Power (5th)",
        }
        
        for pattern, name in patterns.items():
            if pattern.issubset(intervals):
                return f"{root_name} {name}"
        
        note_list = [self.note_names[n] for n in normalized]
        return f"{root_name} ({', '.join(note_list)})"