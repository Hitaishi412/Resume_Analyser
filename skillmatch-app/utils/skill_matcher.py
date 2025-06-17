from flask import Flask, request, jsonify
import spacy
from difflib import SequenceMatcher

app = Flask(__name__)
nlp = spacy.load("en_core_web_sm")


def extract_skills(text):
    """Dynamically extract possible skills from text using noun phrases and filtering."""
    doc = nlp(text.lower())
    skills = set()

    for chunk in doc.noun_chunks:
        phrase = chunk.text.strip()
        if len(phrase.split()) <= 4 and not phrase.isnumeric():
            skills.add(phrase)

    return list(skills)


def similar(a, b):
    """Similarity score between two strings."""
    return SequenceMatcher(None, a.lower(), b.lower()).ratio()


def match_skills(resume_skills, jd_skills, threshold=0.6):
    """Match resume skills to JD skills using fuzzy matching."""
    matched = []
    missing = []

    for jd_skill in jd_skills:
        found = False
        for resume_skill in resume_skills:
            if similar(resume_skill, jd_skill) >= threshold:
                matched.append(jd_skill)
                found = True
                break
        if not found:
            missing.append(jd_skill)

    match_score = int((len(matched) / len(jd_skills)) * 100) if jd_skills else 0

    return {
        "matched_skills": matched,
        "missing_skills": missing,
        "match_score": match_score
    }


@app.route('/match', methods=['POST'])
def match_endpoint():
    data = request.get_json()
    resume_text = data.get('resume_text', '')
    jd_text = data.get('jd_text', '')

    if not resume_text or not jd_text:
        return jsonify({"error": "Both 'resume_text' and 'jd_text' are required."}), 400

    resume_skills = extract_skills(resume_text)
    jd_skills = extract_skills(jd_text)

    result = match_skills(resume_skills, jd_skills)
    result.update({
        "resume_skills_extracted": resume_skills,
        "jd_skills_extracted": jd_skills
    })

    return jsonify(result)


if __name__ == '__main__':
    app.run(debug=True)
