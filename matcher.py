import spacy
from sentence_transformers import SentenceTransformer, util

# Load spaCy model for lemmatization
nlp = spacy.load("en_core_web_sm")

# Load sentence transformer for semantic similarity
sem_model = SentenceTransformer("all-MiniLM-L6-v2")

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


def normalize_text(text: str):
    """Tokenize, lemmatize, lowercase the text into keywords."""
    doc = nlp(text.lower())
    return {token.lemma_ for token in doc if token.is_alpha}


def expand_aliases(keywords: set):
    """Expand keywords with their known aliases."""
    expanded = set(keywords)
    for base, synonyms in ALIASES.items():
        if base in keywords or any(s in keywords for s in synonyms):
            expanded.add(base)
            expanded.update(synonyms)
    return expanded


def keyword_score(cv_text: str, jd_text: str):
    """Calculate keyword overlap score."""
    cv_keywords = expand_aliases(normalize_text(cv_text))
    jd_keywords = expand_aliases(normalize_text(jd_text))

    matched = jd_keywords.intersection(cv_keywords)
    missing = jd_keywords - cv_keywords

    # Weighted scoring
    total_weight = sum(SKILL_WEIGHTS.get(skill, 1) for skill in jd_keywords)
    matched_weight = sum(SKILL_WEIGHTS.get(skill, 1) for skill in matched)

    score = (matched_weight / total_weight * 100) if total_weight > 0 else 0

    return score, list(matched), list(missing)


def semantic_score(cv_text: str, jd_text: str):
    """Calculate semantic similarity score using embeddings."""
    cv_emb = sem_model.encode(cv_text, convert_to_tensor=True)
    jd_emb = sem_model.encode(jd_text, convert_to_tensor=True)
    sim = util.cos_sim(cv_emb, jd_emb)
    return float(sim) * 100  # scale to 0-100


def compare_texts(cv_text: str, jd_text: str):
    """
    Compare CV text and JD text.
    Returns hybrid score, keyword score, semantic score, matched skills, and missing skills.
    """
    kw_score, matched, missing = keyword_score(cv_text, jd_text)
    sem_score = semantic_score(cv_text, jd_text)

    # Hybrid: 50% keyword + 50% semantic
    hybrid_score = (kw_score * 0.5) + (sem_score * 0.5)

    return {
        "hybrid_score": hybrid_score,
        "keyword_score": kw_score,
        "semantic_score": sem_score,
        "matched_skills": matched,
        "missing_skills": missing
    }

