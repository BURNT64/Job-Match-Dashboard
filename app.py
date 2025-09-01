# app.py
import streamlit as st
import re
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from wordcloud import WordCloud
import matplotlib.pyplot as plt
import pdfminer.high_level
import docx

# ---------- Helper functions ----------
def clean_text(text):
    return re.sub(r'\W+', ' ', text).lower()

def extract_text_from_pdf(file):
    return pdfminer.high_level.extract_text(file)

def extract_text_from_docx(file):
    doc = docx.Document(file)
    return " ".join([para.text for para in doc.paragraphs])

def get_keywords(text):
    words = clean_text(text).split()
    return set(words)

def compare_texts(cv_text, jd_text):
    cv_text = clean_text(cv_text)
    jd_text = clean_text(jd_text)

    vectorizer = CountVectorizer().fit_transform([cv_text, jd_text])
    vectors = vectorizer.toarray()
    score = cosine_similarity([vectors[0]], [vectors[1]])[0][0]

    # Keyword overlap
    cv_keywords = get_keywords(cv_text)
    jd_keywords = get_keywords(jd_text)
    matched = cv_keywords & jd_keywords
    missing = jd_keywords - cv_keywords

    return score, matched, missing

# ---------- Streamlit App ----------
st.title("Job Match Dashboard")

st.write("Upload your CV and paste a job description to see how well they match.")

jd_text = st.text_area("Paste Job Description Here")

uploaded_cv = st.file_uploader("Upload your CV", type=["pdf", "docx"])

if st.button("Analyze") and jd_text and uploaded_cv:
    # Extract CV text
    if uploaded_cv.type == "application/pdf":
        cv_text = extract_text_from_pdf(uploaded_cv)
    else:
        cv_text = extract_text_from_docx(uploaded_cv)

    score, matched, missing = compare_texts(cv_text, jd_text)

    st.metric("Match Score", f"{score:.2%}")

    st.write(" **Matching Skills:**", ", ".join(sorted(matched)))
    st.write(" **Missing Skills:**", ", ".join(sorted(missing)))

    # Word cloud for missing skills
    if missing:
        st.write("### Missing Skills Word Cloud")
        wordcloud = WordCloud(width=600, height=400, background_color="white").generate(" ".join(missing))
        fig, ax = plt.subplots()
        ax.imshow(wordcloud, interpolation="bilinear")
        ax.axis("off")
        st.pyplot(fig)