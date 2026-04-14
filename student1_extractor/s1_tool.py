# student1_extractor/s1_tool.py
from crewai.tools import tool
import os
import PyPDF2
import re
import logging

@tool("advanced_pdf_reader")
def advanced_pdf_reader(file_path: str) -> str:
    """
    Enterprise-grade PDF parsing tool with buffer handling and string normalization.
    Args: file_path (str): Absolute or relative path to the PDF document.
    """
    logging.info(f"Attempting to read document at: {file_path}")
    try:
        if not os.path.exists(file_path):
            error_msg = f"FILE NOT FOUND ERROR: The path {file_path} is invalid."
            logging.error(error_msg)
            return error_msg
            
        _, ext = os.path.splitext(file_path)
        extracted_text = ""
        
        if ext.lower() == '.pdf':
            with open(file_path, 'rb') as file:
                pdf_reader = PyPDF2.PdfReader(file)
                total_pages = len(pdf_reader.pages)
                logging.info(f"PDF identified. Extracting {total_pages} pages...")
                
                for page_num in range(total_pages):
                    page = pdf_reader.pages[page_num]
                    text = page.extract_text()
                    if text:
                        extracted_text += text + " "
        else:
            with open(file_path, 'r', encoding='utf-8') as file:
                extracted_text = file.read()
                
        # Clean text to prevent LLM token overflow
        normalized_text = re.sub(r'\s+', ' ', extracted_text).strip()
        logging.info(f"Successfully extracted {len(normalized_text)} characters.")
        
        return f"DOCUMENT CONTENT EXTRACTED SUCCESSFULLY:\n\n{normalized_text}"
        
    except Exception as e:
        logging.error(f"PDF Extraction Exception: {str(e)}")
        return f"CRITICAL SYSTEM ERROR during extraction: {str(e)}"