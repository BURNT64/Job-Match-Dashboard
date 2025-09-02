# app.py
# run with streamlit run app.py

import streamlit as st
import docx2txt
import PyPDF2
import matplotlib.pyplot as plt
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
    score, matched, missing = compare_texts(cv_text, jd_text)

    st.subheader("Results")
    st.metric("Match Score", f"{score:.2f}%")

    st.write("**Matching Skills:**", ", ".join(matched) if matched else "None")
    st.write("**Missing Skills:**", ", ".join(missing) if missing else "None")

    # Bar chart
    st.subheader("Skills Match Breakdown")
    skills = matched + missing
    values = [1] * len(matched) + [0] * len(missing)

    fig, ax = plt.subplots()
    ax.bar(skills, values, color=["green" if v else "red" for v in values])
    ax.set_ylabel("Match (1=yes, 0=no)")
    ax.set_title("Matched vs Missing Skills")
    st.pyplot(fig)

    # Word cloud for missing skills
    if missing:
        st.subheader("Missing Skills Word Cloud")
        wordcloud = WordCloud(width=800, height=400, background_color="white").generate(" ".join(missing))
        fig, ax = plt.subplots()
        ax.imshow(wordcloud, interpolation="bilinear")
        ax.axis("off")
        st.pyplot(fig)