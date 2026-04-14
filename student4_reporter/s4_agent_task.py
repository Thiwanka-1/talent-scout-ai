# student4_reporter/s4_agent_task.py
from crewai import Agent, Task, LLM
from student4_reporter.s4_tool import save_markdown_report

local_llm = LLM(model="ollama/llama3.1", base_url="http://localhost:11434")

report_writer_agent = Agent(
    role='Executive HR Reporter',
    goal='Format hard data into an Executive Markdown Report and save it to disk.',
    backstory=(
        "You are an Executive Technical Writer. You take raw, perfectly calculated data and format it beautifully. "
        "You NEVER invent data. You MUST use the 'save_markdown_report' tool to finalize your task."
    ),
    tools=[save_markdown_report],
    llm=local_llm,
    verbose=True
)

write_report_task = Task(
    description=(
        "You have been provided with VERIFIED MATHEMATICAL FACTS about the candidate.\n"
        "Candidate Name: {candidate_name}\n"
        "Overall Match: {match_percentage}%\n"
        "Extracted Candidate Skills: {candidate_skills}\n"
        "Missing Technical Skills: {missing_skills}\n\n"
        "Interview Strategy:\n{interview_questions}\n\n"
        "ACTION STEPS:\n"
        "1. Format all of this data into a beautiful, professional Markdown report.\n"
        "2. YOU MUST CALL the 'save_markdown_report' tool.\n"
        "3. Pass your entire Markdown string as 'markdown_content', and pass '{candidate_name}' as 'filename'."
    ),
    expected_output="A success message from the save tool.",
    agent=report_writer_agent
)