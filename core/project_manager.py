"""
Project and session management
"""

from pathlib import Path


class ProjectManager:
    """Manages session projects"""
    
    def __init__(self, projects_dir: str = "projects"):
        self.projects_dir = Path(projects_dir)
        self.projects_dir.mkdir(exist_ok=True)
    
    def create_session(self) -> str:
        """Create a new session folder"""
        # TODO: Create unique session ID
        # TODO: Create session directory
        # TODO: Initialize metadata
        pass
    
    def get_all_sessions(self):
        """Get all saved sessions"""
        # TODO: Load all session metadata
        pass
    
    def load_metadata(self, session_id: str):
        """Load metadata for a session"""
        # TODO: Read metadata.json
        pass
    
    def save_metadata(self, session_id: str, metadata: dict):
        """Save metadata for a session"""
        # TODO: Write metadata.json
        pass
