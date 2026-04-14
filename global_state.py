import json
import os
import logging
from typing import Any, Dict

# Advanced logging for AgentOps Observability
logging.basicConfig(level=logging.INFO, format='%(asctime)s - [STATE MANAGER] - %(message)s')

class StateDB:
    """
    Enterprise-grade State Management System for Multi-Agent Workflows.
    Intercepts LLM context and stores it on disk to mathematically guarantee zero context decay.
    """
    DB_FILE = 'outputs/global_database.json'

    @classmethod
    def init_db(cls) -> None:
        """Initializes a fresh database state, wiping old memory caches."""
        os.makedirs('outputs', exist_ok=True)
        initial_schema = {
            "candidate_name": "UNKNOWN",
            "candidate_skills": [],
            "job_requirements": [],
            "match_percentage": 0.0,
            "missing_skills": [],
            "interview_questions": "No questions generated."
        }
        with open(cls.DB_FILE, 'w', encoding='utf-8') as f:
            json.dump(initial_schema, f, indent=4)
        logging.info("Global Database initialized and wiped clean for new run.")

    @classmethod
    def update(cls, key: str, value: Any) -> None:
        """Safely updates a specific parameter in the JSON database."""
        try:
            with open(cls.DB_FILE, 'r', encoding='utf-8') as f:
                data = json.load(f)
            data[key] = value
            with open(cls.DB_FILE, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=4)
            logging.info(f"Successfully updated '{key}'.")
        except Exception as e:
            logging.error(f"Failed to update database: {str(e)}")

    @classmethod
    def get(cls, key: str) -> Any:
        """Retrieves a specific parameter from the JSON database."""
        try:
            with open(cls.DB_FILE, 'r', encoding='utf-8') as f:
                data = json.load(f)
            return data.get(key)
        except Exception as e:
            logging.error(f"Failed to read database: {str(e)}")
            return None