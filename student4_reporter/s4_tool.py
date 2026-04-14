# student4_reporter/s4_tool.py
from crewai.tools import tool
import os
import logging

@tool("save_markdown_report")
def save_markdown_report(markdown_content: str, filename: str) -> str:
    """Saves the final synthesized Markdown string to the local hard drive."""
    try:
        os.makedirs('outputs', exist_ok=True)
        safe_filename = "".join(c for c in filename if c.isalnum() or c in (' ', '_', '-')).strip().replace(' ', '_')
        if not safe_filename:
            safe_filename = "evaluation_report"
            
        full_path = os.path.join('outputs', f"{safe_filename}.md")
        
        with open(full_path, 'w', encoding='utf-8') as f:
            f.write(markdown_content)
            
        logging.info(f"Report successfully secured at {full_path}")
        return f"CRITICAL SUCCESS: Report saved physically to {full_path}"
    except Exception as e:
        logging.error(f"Disk Write Error: {str(e)}")
        return f"SYSTEM ERROR: Failed to write to disk. {str(e)}"