import spacy

# Load spaCy model for lemmatization
nlp = spacy.load("en_core_web_sm")

# Synonyms / aliases mapping (can expand over time)
ALIASES = {
    "machine learning": ["ml", "ai", "artificial intelligence"],
    "developer": ["engineer", "programmer"],
    "python": ["python3", "python 3"],
    "sql": ["structured query language"],
    "excel": ["spreadsheet", "microsoft excel"]
}

# Example weights for key skills (optional)
SKILL_WEIGHTS = {
    "python": 3,
    "machine learning": 3,
    "sql": 2,
    "excel": 1,
    "developer": 2,
    "engineer": 2
}


def normalize_text(text):
    """Tokenize, lemmatize, lowercase the text into keywords."""
    doc = nlp(text.lower())
    return {token.lemma_ for token in doc if token.is_alpha}


def expand_aliases(keywords):
    """Expand keywords with their known aliases."""
    expanded = set(keywords)
    for base, synonyms in ALIASES.items():
        if base in keywords or any(s in keywords for s in synonyms):
            expanded.add(base)
            expanded.update(synonyms)
    return expanded


def compare_texts(cv_text, jd_text):
    """Compare CV text and JD text, return score and matched/missing skills."""

    cv_keywords = expand_aliases(normalize_text(cv_text))
    jd_keywords = expand_aliases(normalize_text(jd_text))

    matched = jd_keywords.intersection(cv_keywords)
    missing = jd_keywords - cv_keywords

    # Weighted scoring
    total_weight = sum(SKILL_WEIGHTS.get(skill, 1) for skill in jd_keywords)
    matched_weight = sum(SKILL_WEIGHTS.get(skill, 1) for skill in matched)

    score = (matched_weight / total_weight * 100) if total_weight > 0 else 0

    return score, list(matched), list(missing)
