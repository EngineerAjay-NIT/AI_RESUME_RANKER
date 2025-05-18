import streamlit as st
import PyPDF2
import spacy

nlp = spacy.load("en_core_web_md")

st.title("AI Resume Ranker")
st.write("Upload your resume and paste a job description to get a match score.")

# Upload resume
resume_file = st.file_uploader("Upload Resume (PDF)", type=["pdf"])

# Paste job description
job_description = st.text_area("Paste Job Description Here")

def extract_text_from_pdf(pdf_file):
    reader = PyPDF2.PdfReader(pdf_file)
    text = ""
    for page in reader.pages:
        text += page.extract_text()
    return text

def calculate_similarity(resume_text, job_text):
    resume_doc = nlp(resume_text)
    job_doc = nlp(job_text)
    return resume_doc.similarity(job_doc)

if resume_file and job_description:
    resume_text = extract_text_from_pdf(resume_file)
    similarity = calculate_similarity(resume_text, job_description)
    st.metric("Match Score", f"{similarity * 100:.2f}%")

    if similarity > 0.8:
        st.success("Great match! Your resume aligns well.")
    elif similarity > 0.5:
        st.warning("Moderate match. Try customizing your resume more.")
    else:
        st.error("Low match. Consider rewriting your resume for this role.")
