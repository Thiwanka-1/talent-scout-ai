from crewai.tools import tool
from global_state_manager import GlobalStateManager

@tool("get_missing_skills_from_db")
def get_missing_skills_from_db(dummy_arg: str = "fetch") -> str:
    """Fetches the list of missing skills directly from the global database."""
    state = GlobalStateManager.get_state()
    missing = state.get("missing_skills", [])
    if not missing:
        return "CANDIDATE IS PERFECT. NO MISSING SKILLS. Ask advanced architecture questions."
    return f"MISSING SKILLS TO TEST: {', '.join(missing)}"

@tool("save_interview_questions_to_db")
def save_interview_questions_to_db(questions_markdown: str) -> str:
    """Saves the final generated interview questions to the global database."""
    GlobalStateManager.update_state("interview_questions", questions_markdown)
    return "SUCCESS: Questions saved to database."