# matcher.py
import re
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

def clean_text(text):
    return re.sub(r'\W+', ' ', text).lower()

def compare_texts(cv_text, jd_text):
    # Clean
    cv_text = clean_text(cv_text)
    jd_text = clean_text(jd_text)

    # Vectorize
    vectorizer = TfidfVectorizer()
    vectors = vectorizer.fit_transform([cv_text, jd_text])

    # Cosine similarity
    similarity = cosine_similarity(vectors[0], vectors[1])[0][0]
    return similarity

if __name__ == "__main__":
    # Example run
    cv = "Python developer with experience in data analysis and SQL"
    jd = "Looking for a software engineer with Python, SQL, and machine learning skills"
    
    score = compare_texts(cv, jd)
    print(f"Match Score: {score:.2f}")
