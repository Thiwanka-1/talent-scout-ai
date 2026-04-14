# student2_matcher/s2_agent_task.py
from crewai import Agent, Task, LLM

local_llm = LLM(model="ollama/llama3.1", base_url="http://localhost:11434")

skill_matcher_agent = Agent(
    role='Lead Technical Evaluator',
    goal='Parse complex job descriptions into clean, atomic technical keywords.',
    backstory=(
        "You are an AI trained to read paragraphs of job requirements and distill them "
        "down to single, atomic technical keywords. You ignore soft skills like 'teamwork' and 'communication'. "
        "You output strictly in XML."
    ),
    tools=[], # Tools removed so it doesn't get distracted by JSON loops
    llm=local_llm,
    verbose=True
)

compare_skills_task = Task(
    description=(
        "Read the following raw Job Description:\n"
        "'{job_description}'\n\n"
        "ACTION STEPS:\n"
        "1. Ignore all educational requirements and soft skills.\n"
        "2. Extract ONLY the hard technical technologies (e.g., Python, React, Docker, AWS, MySQL).\n"
        "3. Format them as a simple, comma-separated list of individual words.\n\n"
        "CRITICAL DIRECTIVE - YOU MUST OUTPUT EXACTLY THIS FORMAT AND NOTHING ELSE:\n"
        "<JOB_SKILLS>Python, React, AWS, Docker</JOB_SKILLS>"
    ),
    expected_output="Job skills enclosed in strict <JOB_SKILLS> XML tags.",
    agent=skill_matcher_agent
)