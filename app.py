import streamlit as st
import google.generativeai as genai
import os
from dotenv import load_dotenv
import json
import PyPDF2 as pdf

load_dotenv() ## load all env variables

genai.configure(api_key=os.getenv('GOOGLE_API_KEY'))

def get_gemini_response(input):
    model = genai.GenerativeModel('gemini-pro')
    response = model.generate_content(input)
    return response.text

def input_pdf_text(upload_file):
    reader = pdf.PdfReader(upload_file)
    text = ""
    for page in range(len(reader.pages)):
        page = reader.pages[page]
        text += str(page.extract_text())
    return text

# Creating Prompt Template

input_prompt = """

Hey! Act like a skilled or an experienced ATS (Applicant Tracking System)
with a deep understanding of technology, software enginering, data science, data analytics and cybersecurity. 
Your task is to evaluate resume based on the job description. You must consider that the job market is very competitive and you should provide best assistance for improving the resumes. 
Assign the percentage matching based on the job description and the missing keywords with high accuracy. You
resume: {text}
descriptions: {jd}

I want the response in one single string having the structure {{"JD Match": "%", "Missing Keywords: []", "Profile Summary": ""}}

"""

## Streamlit App

st.title("ATS Management")
st.text("Improve Resume with ATS")
jd = st.text_area("Paste the job description for a specific company")
upload_file = st.file_uploader("Upload Your Resume", type="pdf", help="Please upload PDF only")
submit = st.button("Submit")

if submit:
    if upload_file is not None:
        text = input_pdf_text(upload_file)
        response = get_gemini_response(input_prompt)
        st.subheader(response)