# student1_extractor/s1_agent_task.py
from crewai import Agent, Task, LLM
from student1_extractor.s1_tool import advanced_pdf_reader

local_llm = LLM(model="ollama/llama3.1", base_url="http://localhost:11434")

resume_parser_agent = Agent(
    role='Senior Data Extraction Specialist',
    goal='Read the physical document and extract the Name and Skills strictly into XML tags.',
    backstory=(
        "You are an elite NLP parsing agent. You possess strict attention to detail. "
        "You never hallucinate fake data like 'John Doe'. If a name is missing, you state 'Name Not Found'. "
        "You ALWAYS output your final answer wrapped in secure XML tags."
    ),
    tools=[advanced_pdf_reader],
    llm=local_llm,
    verbose=True
)

extract_skills_task = Task(
    description=(
        "1. YOU MUST USE the 'advanced_pdf_reader' tool to read this exact file: '{resume_path}'.\n"
        "2. Deeply analyze the text returned by the tool.\n"
        "3. Find the Candidate's Real Name.\n"
        "4. Extract a comma-separated list of their hard technical skills (languages, frameworks, databases, cloud).\n\n"
        "CRITICAL DIRECTIVE - YOU MUST OUTPUT EXACTLY THIS FORMAT AND NOTHING ELSE:\n"
        "<NAME>The Candidate Name</NAME>\n"
        "<SKILLS>Skill 1, Skill 2, Skill 3</SKILLS>"
    ),
    expected_output="Candidate name and skills enclosed in strict XML tags.",
    agent=resume_parser_agent
)