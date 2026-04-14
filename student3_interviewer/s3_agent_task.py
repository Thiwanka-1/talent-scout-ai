# student3_interviewer/s3_agent_task.py
from crewai import Agent, Task, LLM

local_llm = LLM(model="ollama/llama3.1", base_url="http://localhost:11434")

interview_creator_agent = Agent(
    role='Senior Engineering Manager',
    goal='Generate highly technical, scenario-based interview questions based on missing skills.',
    backstory=(
        "You are a battle-tested Engineering Manager. You write practical, scenario-based questions "
        "that test a candidate's ability to solve real-world problems. You format your output in clean XML."
    ),
    tools=[],
    llm=local_llm,
    verbose=True
)

generate_questions_task = Task(
    description=(
        "The mathematical evaluation system has determined the candidate is MISSING the following skills:\n"
        "[{missing_skills}]\n\n"
        "ACTION STEPS:\n"
        "1. Write exactly 3 scenario-based technical questions. Each question must target at least one of the missing skills.\n"
        "2. Provide a brief 'Evaluation Criteria' for each question explaining what to look for in a good answer.\n\n"
        "CRITICAL DIRECTIVE - YOU MUST OUTPUT EXACTLY THIS FORMAT AND NOTHING ELSE:\n"
        "<QUESTIONS>\n"
        "### Question 1: [Skill Name]\n[Scenario text]\n**Evaluation:** [Criteria]\n\n"
        "### Question 2: [Skill Name]\n[Scenario text]\n**Evaluation:** [Criteria]\n\n"
        "### Question 3: [Skill Name]\n[Scenario text]\n**Evaluation:** [Criteria]\n"
        "</QUESTIONS>"
    ),
    expected_output="3 interview questions wrapped in <QUESTIONS> XML tags.",
    agent=interview_creator_agent
)