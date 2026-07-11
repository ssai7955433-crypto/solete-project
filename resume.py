import streamlit as st
import os
from dotenv import load_dotenv
from groq import Groq
import PyPDF2

load_dotenv()
# Load Groq API key
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

def extract_text_from_pdf(uploaded_file):
    reader = PyPDF2.PdfReader(uploaded_file)
    text = ""
    for page in reader.pages:
        text += page.extract_text() + "\n"
    return text

def analyze_resume(text):
    prompt = f"""
    You are an AI Resume Analyzer.
    Resume Text: {text}
    Provide:
    1. Strengths
    2. Weaknesses
    3. Improvement Suggestions
    4. ATS Score (0–100)
    5. Missing Skills
    """
    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[{"role":"user","content":prompt}]
    )
    return response.choices[0].message.content

st.title("AI Resume Analyzer")
uploaded_file = st.file_uploader("Upload your Resume (PDF)", type="pdf")

if uploaded_file:
    resume_text = extract_text_from_pdf(uploaded_file)
    st.subheader("Extracted Resume Text")
    st.text(resume_text[:1000])  # preview first 1000 chars
    st.subheader("AI Feedback")
    feedback = analyze_resume(resume_text)
    st.write(feedback)
