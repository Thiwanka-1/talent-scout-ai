import os
import logging

# =====================================================================
# THE OLLAMA HIJACK: Forces 100% Local Execution, blocks OpenAI crashes
# =====================================================================
os.environ["OPENAI_API_KEY"] = "sk-fake-dummy-key"
os.environ["OPENAI_API_BASE"] = "http://localhost:11434/v1"
os.environ["OPENAI_MODEL_NAME"] = "llama3.1"
# =====================================================================

from crewai import Crew, Process
from core_utils import AdvancedDataProcessor

from student1_extractor.s1_agent_task import resume_parser_agent, extract_skills_task
from student2_matcher.s2_agent_task import skill_matcher_agent, compare_skills_task
from student3_interviewer.s3_agent_task import interview_creator_agent, generate_questions_task
from student4_reporter.s4_agent_task import report_writer_agent, write_report_task

def run_talent_scout_pipeline(resume_file_path, job_description):
    logging.info("=== INITIATING PHASE 1: EXTRACTION CREW ===")
    
    # Phase 1 extracts raw text into XML
    crew_phase_1 = Crew(
        agents=[resume_parser_agent, skill_matcher_agent],
        tasks=[extract_skills_task, compare_skills_task],
        process=Process.sequential, 
        verbose=True,
        cache=False
    )
    
    crew_phase_1.kickoff(inputs={
        'resume_path': resume_file_path, 
        'job_description': job_description
    })
    
    # =================================================================
    # THE DETERMINISTIC BRIDGE: Extracting direct task outputs!
    # This mathematically guarantees Agent 1's data is never overwritten.
    # =================================================================
    output_1 = getattr(extract_skills_task.output, 'raw', '')
    output_2 = getattr(compare_skills_task.output, 'raw', '')
    
    c_name = AdvancedDataProcessor.extract_xml_tag(output_1, "NAME") or "Extraction Failed"
    c_skills = AdvancedDataProcessor.extract_xml_tag(output_1, "SKILLS") or ""
    j_skills = AdvancedDataProcessor.extract_xml_tag(output_2, "JOB_SKILLS") or ""
    
    # Do deterministic fuzzy math in Python
    match_pct, missing_list = AdvancedDataProcessor.fuzzy_skill_matcher(c_skills, j_skills)
    missing_str = ", ".join(missing_list) if missing_list else "None! Candidate is a 100% perfect match."
    
    logging.info(f"BRIDGE COMPLETE: {c_name} scored {match_pct}%")
    logging.info("=== INITIATING PHASE 2: SYNTHESIS CREW ===")
    
    # Phase 2 writes the report using the hardcoded Python math
    crew_phase_2 = Crew(
        agents=[interview_creator_agent, report_writer_agent],
        tasks=[generate_questions_task, write_report_task],
        process=Process.sequential, 
        verbose=True,
        cache=False
    )
    
    # Inject exact values into the prompts
    crew_phase_2.kickoff(inputs={
        'candidate_name': c_name,
        'candidate_skills': c_skills if c_skills else "No skills extracted",
        'missing_skills': missing_str,
        'match_percentage': str(match_pct),
        'interview_questions': "Will be populated by Task 3 context." 
    })
    
    # Extract the questions and return the payload to the UI
    output_3 = getattr(generate_questions_task.output, 'raw', '')
    questions = AdvancedDataProcessor.extract_xml_tag(output_3, "QUESTIONS") or "Questions failed to generate."
    
    # Assemble the final string for the UI (Agent 4 already saved it to disk)
    final_ui_markdown = f"""
    # 📄 Candidate Evaluation Report
    **Candidate:** {c_name}
    **Match:** {match_pct}%
    
    **Verified Skills:** {c_skills}
    **Missing Competencies:** {missing_str}
    
    ### Targeted Interview Strategy:
    {questions}
    """
    return final_ui_markdown