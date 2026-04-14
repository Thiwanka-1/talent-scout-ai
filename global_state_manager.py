import json
import os
from typing import Dict, Any

class GlobalStateManager:
    """
    Advanced State Management System for Multi-Agent Workflows.
    Ensures zero context loss by persisting agent memory to a physical JSON database.
    """
    STATE_FILE = 'outputs/global_state.json'

    @staticmethod
    def initialize_state() -> None:
        """Creates a fresh, empty state database for a new run."""
        os.makedirs('outputs', exist_ok=True)
        initial_state = {
            "candidate_name": "UNKNOWN",
            "candidate_skills": [],
            "job_skills_required": [],
            "match_percentage": 0.0,
            "missing_skills": [],
            "interview_questions": "Not generated yet."
        }
        with open(GlobalStateManager.STATE_FILE, 'w', encoding='utf-8') as f:
            json.dump(initial_state, f, indent=4)
        print("[STATE MANAGER] Database Initialized Successfully.")

    @staticmethod
    def update_state(key: str, value: Any) -> str:
        """Safely updates a specific key in the global state."""
        try:
            with open(GlobalStateManager.STATE_FILE, 'r', encoding='utf-8') as f:
                state = json.load(f)
            
            state[key] = value
            
            with open(GlobalStateManager.STATE_FILE, 'w', encoding='utf-8') as f:
                json.dump(state, f, indent=4)
            return f"SUCCESS: Global state '{key}' updated successfully."
        except Exception as e:
            return f"CRITICAL STATE ERROR: {str(e)}"

    @staticmethod
    def get_state() -> Dict[str, Any]:
        """Retrieves the current global state."""
        try:
            with open(GlobalStateManager.STATE_FILE, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception:
            return {}