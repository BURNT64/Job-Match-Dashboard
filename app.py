# app.py
# run with: streamlit run app.py

import streamlit as st
import docx2txt
import PyPDF2
from wordcloud import WordCloud
from matcher import compare_texts


st.set_page_config(page_title="Job Match Dashboard", layout="wide")

st.title("Job Match Dashboard")
st.write("Upload your CV and paste a job description to see how well they match.")

jd_text = st.text_area("Paste Job Description Here")

uploaded_file = st.file_uploader("Upload your CV", type=["pdf", "docx"])

if st.button("Analyze") and jd_text and uploaded_file:
    # Extract text from CV
    if uploaded_file.type == "application/pdf":
        reader = PyPDF2.PdfReader(uploaded_file)
        cv_text = "".join([page.extract_text() for page in reader.pages if page.extract_text()])
    else:
        cv_text = docx2txt.process(uploaded_file)

    # Compare
    results = compare_texts(cv_text, jd_text)

    st.subheader("Results")

    # Show metrics
    col1, col2, col3 = st.columns(3)
    col1.metric("Hybrid Score", f"{results['hybrid_score']:.2f}%")
    col2.metric("Keyword Score", f"{results['keyword_score']:.2f}%")
    col3.metric("Semantic Score", f"{results['semantic_score']:.2f}%")

    st.write("**Matching Skills:**", ", ".join(results["matched_skills"]) if results["matched_skills"] else "None")
    st.write("**Missing Skills:**", ", ".join(results["missing_skills"]) if results["missing_skills"] else "None")
