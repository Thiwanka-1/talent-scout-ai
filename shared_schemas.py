from pydantic import BaseModel, Field
from typing import List

class ResumeExtraction(BaseModel):
    candidate_name: str = Field(description="The exact full name of the candidate extracted from the resume.")
    technical_skills: List[str] = Field(description="A clean list of technical skills found in the resume.")

class SkillMatch(BaseModel):
    match_percentage: str = Field(description="The numerical match percentage, e.g., '80%'")
    missing_skills: List[str] = Field(description="A list of SINGLE WORD technical skills missing. e.g. ['AWS', 'GraphQL', 'PostgreSQL']. NEVER use sentences or bullet points.")

class InterviewPrep(BaseModel):
    scenario_questions: List[str] = Field(description="A list of exactly 3 scenario-based interview questions.")