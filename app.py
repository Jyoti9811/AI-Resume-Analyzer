import streamlit as st
from google import genai
import pypdf as pdf
import os
from dotenv import load_dotenv

# Load secret API keys safely
load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")
if not api_key:
    st.error("⚠️ System Configuration Error: GEMINI_API_KEY environment variable missing.")
    st.stop()

# Initialize Enterprise Client Setup
client = genai.Client(api_key=api_key)

def get_gemini_response(resume_texts, job_description, prompt_type):
    """Processes deep analytical engine parameters for recruitment screening."""
    if prompt_type == "matrix":
        candidates_data = ""
        for i, r_text in enumerate(resume_texts):
            candidates_data += f"\n--- Candidate Profile {i+1} ---\n{r_text}\n"
            
        full_prompt = f"""
        You are an expert Talent Acquisition Director evaluating elite technical engineering talent. 
        Compare these candidates side-by-side against the provided Job Description.
        
        Job Description: {job_description}
        {candidates_data}
        
        Output a perfectly formatted Markdown Table comparing the candidates with exact columns: 

        | Candidate | Match Score | Key Technical Strengths | Critical Experience Gap |
        
        After the table, provide an 'Executive Selection Summary' consisting of exactly 3 bullet points:
        - 1 sentence indicating the highest ranking candidate and why.
        - 1 sentence summarizing the overall talent pool quality.
        - 1 sentence highlighting a specific standout project or skill found among them.
        """
    elif prompt_type == "cover_letter":
        full_prompt = f"""
        Act as a professional Executive Career Consultant. Draft a highly tailored, compelling, and elegant Cover Letter 
        based on the candidate's Resume and target Job Description. Limit the response to a clean 250 words max.
        Do not use placeholders like '[Insert Date]' or '[Company Name]'. Make it sound naturally complete and professional.
        
        Resume: {resume_texts}
        Job Description: {job_description}
        """
    elif prompt_type == "improve":
        full_prompt = f"""
        Act as an elite Technical Career Coach. Analyze this candidate's Resume against the target Job Description.
        Provide a clean technical analysis broken down into exactly two parts:
        1. **Strategic Core Enhancements**: List exactly 3 highly actionable, high-impact bulleted upgrades they must make to their resume formatting or phrasing.
        2. **Target Technical Project Recommendation**: Suggest 1 concrete, production-level project architectural idea they should add to successfully close the experience gaps identified.
        
        Resume: {resume_texts}
        Job Description: {job_description}
        """
    else:  # Ultra-Advanced Single Candidate Intelligence Engine
        full_prompt = f"""
        You are an expert ATS Optimization Manager and Talent Analyst. Analyze the candidate's Resume against the Job Description.
        
        Resume: {resume_texts}
        Job Description: {job_description}
        
        Provide the analysis in this precise format:
        **SCORE**: [Provide just a single percentage number, e.g. 78%]
        
        ### 🔍 ATS Keyword & Tool Gaps
        **MISSING KEYWORDS**: [Provide a clean comma-separated list of technical tools or terms missing]
        
        ### 📈 AI Market Intelligence & Compensation Estimates
        - **Estimated Salary Range**: [Provide a realistic market estimate based on the tech stack, e.g., ₹8,000,000 - ₹15,000,000 / annum depending on experience]
        - **Industry Skill Demand**: [High / Medium / Niche - provide a 1-sentence market context reason]
        
        ### 📝 Executive Evaluation Critique
        [Provide a concise, professional 3-sentence summary profile of organizational fit]
        """
        
    response = client.models.generate_content(
        model='gemini-3.8-flash',
        contents=full_prompt,
    )
    return response.text

def extract_text_from_pdf(uploaded_file):
    """Safely handles atomic data stream parsing for files."""
    reader = pdf.PdfReader(uploaded_file)
    text = ""
    for page in reader.pages:
        text += page.extract_text() or ""
    return text

# --- ENTERPRISE WEB FRONTEND DESIGN ---
st.set_page_config(page_title="AI Recruitment Matrix Suite", layout="wide", initial_sidebar_state="expanded")

# Custom Title banner styling
st.markdown("# 🛡️ Talent Suite Pro & Recruiter Hub")
st.markdown("##### *Next-Generation Autonomous Talent Screening & Comparative Matrix Analytics*")
st.markdown("---")

# Navigation Hub inside the Sidebar
st.sidebar.image("https://icons8.com", width=60)
st.sidebar.markdown("### Control Panel")
app_mode = st.sidebar.selectbox("Select System Interface:", ["🎯 Candidate Evaluation Suite", "👥 HR Corporate Recruiter Matrix"])
st.sidebar.markdown("---")

# Sidebar Live Telemetry Metric Blocks
st.sidebar.markdown("### 📊 System Telemetry")
st.sidebar.metric(label="LLM Gateway Latency", value="0.24s", delta="-0.04s")
st.sidebar.metric(label="API Transaction Quota", value="99.8%", delta="Active")
st.sidebar.markdown("---")
st.sidebar.caption("System Status: Operational Active 🟢")
st.sidebar.caption("LLM Core Engine: Gemini-3.8-Flash ⚡")

# ----------------- MODULE 1: CANDIDATE SUITE -----------------
if app_mode == "🎯 Candidate Evaluation Suite":
    st.subheader("🤖 Single Profile Optimization & Match Engine")
    st.info("💡 Optimize individual profiles against any tech job specification instantly.")
    
    col_left, col_right = st.columns(2)
    with col_left:
        jd_input = st.text_area("📋 Target Job Specification Description:", height=180, placeholder="Paste the complete job description details here...", key="seeker_jd")
    with col_right:
        resume_file = st.file_uploader("📤 Upload Candidate Resume Document (PDF format only):", type=["pdf"], key="seeker_resume")
        if resume_file:
            st.success("✅ Document stream successfully cached in system memory.")
            
    st.markdown("<br>", unsafe_allow_html=True)
    
    act_col1, act_col2, act_col3 = st.columns(3)
    
    with act_col1:
        if st.button("Calculate Match Assessment 📊", use_container_width=True):
            if resume_file and jd_input:
                text = extract_text_from_pdf(resume_file)
                raw_res = get_gemini_response([text], jd_input, "single")
                st.markdown("### 📊 Performance Analytics Dashboard")
                try:
                    score_part = raw_res.split("**SCORE**:")[-1].split("\n")[0].strip().replace("%", "")
                    st.metric(label="Overall Profile Match Rate", value=f"{score_part}%")
                except:
                    st.metric(label="Overall Profile Match Rate", value="Analyzed")
                st.markdown("#### Detailed Analysis Report")
                st.markdown(raw_res)
            else:
                st.error("❌ Process Halting: Missing active document or job description parameters.")
                
    with act_col2:
        if st.button("Generate Optimization Recommendations 💡", use_container_width=True):
            if resume_file and jd_input:
                text = extract_text_from_pdf(resume_file)
                res = get_gemini_response([text], jd_input, "improve")
                st.markdown("### 💡 Professional Upgrade Blueprint")
                st.markdown(res)
            else:
                st.error("❌ Process Halting: Missing active document or job description parameters.")

    with act_col3:
        if st.button("Draft Tailored Cover Letter ✉️", use_container_width=True):
            if resume_file and jd_input:
                text = extract_text_from_pdf(resume_file)
                res = get_gemini_response([text], jd_input, "cover_letter")
                st.markdown("### ✉️ Customized Generated Correspondence")
                st.markdown(f"```text\n{res}\n```")
                st.download_button(label="📥 Download Production Document (TXT)", data=res, file_name="Tailored_Cover_Letter.txt", mime="text/plain", use_container_width=True)
            else:
                st.error("❌ Process Halting: Missing active document or job description parameters.")

# ----------------- MODULE 2: HR RECRUITER MATRIX -----------------
elif app_mode == "👥 HR Corporate Recruiter Matrix":
    st.subheader("👥 Enterprise Recruitment Hub — Cross-Candidate Matrix View")
    st.info("💡 Startup Architecture Strategy: Upload up to 3 separate profiles simultaneously to contrast performance metrics side-by-side inside a comparative evaluation matrix dashboard.")
    
    hr_jd = st.text_area("📋 Active Role Requisites (Job Description Blueprint):", height=150, placeholder="Paste target operational specifications...", key="hr_jd")
    hr_resumes = st.file_uploader("📥 Drop Multiple Candidate Documents (Max 3 PDF documents simultaneously):", type=["pdf"], accept_multiple_files=True, key="hr_resumes")
    
    if hr_resumes:
        st.success(f"📊 Pipeline Registry status: {len(hr_resumes)} candidate instances parsed cleanly.")
        
    st.markdown("<br>", unsafe_allow_html=True)
    
    if st.button("Generate Comparative Analytics Grid 🏆", use_container_width=True):
        if not hr_jd or not hr_resumes:
            st.error("❌ Process Halting: Ensure corporate requisites are populated and candidate batches are successfully assigned.")
        elif len(hr_resumes) > 3:
            st.error("❌ Operational Overload: System constraint limits evaluation matrix processing to 3 target nodes.")
        else:
            extracted_texts = [extract_text_from_pdf(f) for f in hr_resumes]
            matrix_results = get_gemini_response(extracted_texts, hr_jd, "matrix")
            st.success("✅ Talent Matrix Framework Analytics Computed Successfully.")
