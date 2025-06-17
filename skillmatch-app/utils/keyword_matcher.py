from flask import Flask, request, jsonify
import spacy
from difflib import SequenceMatcher

app = Flask(__name__)
nlp = spacy.load("en_core_web_sm")


def extract_keywords(text):
    """
    Extract meaningful keywords from text using noun phrases and filtering logic.
    These keywords could be skills, tools, technologies, or concepts.
    """
    doc = nlp(text.lower())
    keywords = set()

    for chunk in doc.noun_chunks:
        phrase = chunk.text.strip()
        if len(phrase.split()) <= 5 and not phrase.isnumeric():
            keywords.add(phrase)

    return list(keywords)


def similar(a, b):
    """Calculate similarity ratio between two strings."""
    return SequenceMatcher(None, a.lower(), b.lower()).ratio()


def match_keywords(resume_keywords, jd_keywords, threshold=0.65):
    """
    Compare resume keywords with job description keywords using fuzzy matching.
    """
    matched = []
    missing = []

    for jd_kw in jd_keywords:
        found = False
        for resume_kw in resume_keywords:
            if similar(resume_kw, jd_kw) >= threshold:
                matched.append(jd_kw)
                found = True
                break
        if not found:
            missing.append(jd_kw)

    match_score = int((len(matched) / len(jd_keywords)) * 100) if jd_keywords else 0

    return {
        "matched_keywords": matched,
        "missing_keywords": missing,
        "match_score": match_score
    }


@app.route('/keyword-match', methods=['POST'])
def keyword_match_endpoint():
    data = request.get_json()
    resume_text = data.get('resume_text', '')
    jd_text = data.get('jd_text', '')

    if not resume_text or not jd_text:
        return jsonify({"error": "Both 'resume_text' and 'jd_text' are required."}), 400

    resume_keywords = extract_keywords(resume_text)
    jd_keywords = extract_keywords(jd_text)

    result = match_keywords(resume_keywords, jd_keywords)
    result.update({
        "resume_keywords_extracted": resume_keywords,
        "jd_keywords_extracted": jd_keywords
    })

    return jsonify(result)


if __name__ == '__main__':
    app.run(debug=True)
