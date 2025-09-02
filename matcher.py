import spacy

# Load English model for lemmatization
nlp = spacy.load("en_core_web_sm")

def lemmatize_keywords(text):
    """Lowercase, remove non-alpha tokens, and lemmatize words/phrases"""
    doc = nlp(text.lower())
    # Keep only alphabetic tokens that are not stop words
    return set([token.lemma_ for token in doc if token.is_alpha and not token.is_stop])

def compare_texts(cv_text, jd_text):
    """
    Compare CV and job description using keyword overlap.
    Returns:
        score (float): % of JD keywords found in CV
        matched (set): matching keywords
        missing (set): JD keywords not in CV
    """
    cv_keywords = lemmatize_keywords(cv_text)
    jd_keywords = lemmatize_keywords(jd_text)

    matched = cv_keywords & jd_keywords
    missing = jd_keywords - cv_keywords

    # Avoid division by zero
    score = len(matched) / len(jd_keywords) if jd_keywords else 0

    return score, matched, missing

# Example usage
if __name__ == "__main__":
    cv = "Python developer with experience in data analysis and SQL"
    jd = "Looking for a software engineer with Python, SQL, and machine learning skills"

    score, matched, missing = compare_texts(cv, jd)
    print(f"Match Score: {score:.2%}")
    print("Matching Keywords:", matched)
    print("Missing Keywords:", missing)
