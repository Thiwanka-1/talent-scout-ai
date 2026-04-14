import streamlit as st
import os
from main_orchestrator import run_talent_scout_pipeline

st.set_page_config(page_title="Talent-Scout AI", layout="wide")

# The Hijack must be loaded in the app process too just in case
os.environ["OPENAI_API_KEY"] = "sk-fake-dummy-key"
os.environ["OPENAI_API_BASE"] = "http://localhost:11434/v1"

st.title("🤖 Talent-Scout MAS")
st.markdown("### Enterprise Two-Phase Cognitive Architecture")
st.divider()

col1, col2 = st.columns(2)

with col1:
    uploaded_file = st.file_uploader("Upload PDF Resume", type=["pdf"])

with col2:
    job_desc = st.text_area("Paste Job Description", height=150)

if st.button("🚀 Execute Autonomous Analysis", type="primary", use_container_width=True):
    if uploaded_file and job_desc:
        os.makedirs('temp_uploads', exist_ok=True)
        file_path = os.path.join('temp_uploads', uploaded_file.name)
        
        with open(file_path, "wb") as f:
            f.write(uploaded_file.getbuffer())
            
        with st.status('Agents are reasoning... Check terminal for Core Utility logs.', expanded=True):
            final_markdown = run_talent_scout_pipeline(file_path, job_desc)
            
        st.success("✅ Architecture Executed Successfully!")
        st.balloons()
        
        with st.expander("📊 VIEW EXECUTIVE REPORT", expanded=True):
            st.markdown(final_markdown)
    else:
        st.error("Please upload a CV and paste a Job Description.")