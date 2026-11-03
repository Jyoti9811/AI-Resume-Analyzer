import streamlit as ui
from google import genai
import pypdf as pdf  # <-- SWITCHED TO THE MODERN LIBRARY
import os
from dotenv import load_dotenv

# Load secret API keys
load_dotenv()

# Initialize the Google GenAI Client
# Load secret API keys
load_dotenv()

# Fetch the key safely from your local .env file
api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    ui.error("⚠️ GEMINI_API_KEY not found! Please check your .env file.")
    ui.stop()

# Initialize the Google GenAI Client securely
client = genai.Client(api_key=api_key)

def get_gemini_response(resume_text, job_description, prompt_type):
    """Sends data to Gemini AI using the correct google-genai package path."""

    if prompt_type == "score":
        full_prompt = f"""
        You are an expert HR Manager and Technical Recruiter. 
        Evaluate the following Resume against the Job Description.
        
        Resume: {resume_text}
        Job Description: {job_description}
        
        Provide a percentage match score (e.g., 75%), a list of missing keywords, 
        and a 3-sentence summary of how well the candidate fits.
        """
    elif prompt_type == "improve":
        full_prompt = f"""
        You are a career coach. Look at this Resume and Job Description.
        Suggest exactly 3 actionable ways the candidate can improve their resume 
        or what projects they should add to match this job description better.
        
        Resume: {resume_text}
        Job Description: {job_description}
        """
        
    response = client.models.generate_content(
        model='gemini-3.8-flash',
        contents=full_prompt,
    )
    return response.text

def extract_text_from_pdf(uploaded_file):
    """Reads the uploaded PDF file using the updated pypdf syntax."""
    reader = pdf.PdfReader(uploaded_file)
    text = ""
    for page in reader.pages:  # Modern loop syntax for pypdf
        text += page.extract_text() or ""
    return text

# --- STREAMLIT UI DESIGN ---
ui.set_page_config(page_title="AI Resume Analyzer", layout="centered")
ui.title("🤖 AI Resume Analyzer & Job Fit Predictor")
ui.subheader("Evaluate your profile against any tech job description using AI")

# Input fields
job_desc = ui.text_area("Paste the Job Description Here:", height=150)
uploaded_file = ui.file_uploader("Upload your Resume (PDF format only):", type=["pdf"])

if uploaded_file is not None:
    ui.success("Resume uploaded successfully!")

# Buttons for action
col1, col2 = ui.columns(2)

with col1:
    if ui.button("Calculate Match Score 📊"):
        if uploaded_file and job_desc:
            with ui.spinner("Analyzing with AI..."):
                resume_text = extract_text_from_pdf(uploaded_file)
                result = get_gemini_response(resume_text, job_desc, "score")
                ui.markdown("### Analysis Result:")
                ui.write(result)
        else:
            ui.error("Please upload a resume and paste a job description first.")

with col2:
    if ui.button("How to Improve Resume 💡"):
        if uploaded_file and job_desc:
            with ui.spinner("Generating suggestions..."):
                resume_text = extract_text_from_pdf(uploaded_file)
                result = get_gemini_response(resume_text, job_desc, "improve")
                ui.markdown("### Actionable Suggestions:")
                ui.write(result)
        else:
            ui.error("Please upload a resume and paste a job description first.")







