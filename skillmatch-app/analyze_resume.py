from flask_cors import CORS
from flask import Flask, request, jsonify
from utils import skill_matcher, keyword_matcher, grammar, readability, formatting, scoring

app = Flask(__name__)  # ✅ Only one instance
CORS(app)

# Root route for browser testing
@app.route('/', methods=['GET'])
def home():
    return "✅ Resume Analyzer API is running. Send a POST request to /analyze."


@app.route('/analyze', methods=['POST'])
def analyze_resume():
    data = request.get_json()
    resume_text = data.get('resume_text', '')
    jd_text = data.get('jd_text', '')

    if not resume_text or not jd_text:
        return jsonify({"error": "Both 'resume_text' and 'jd_text' are required."}), 400

    skills_result = skill_matcher.match_skills_from_text(resume_text, jd_text)
    keyword_result = keyword_matcher.match_keywords_from_text(resume_text, jd_text)
    grammar_result = grammar.check_grammar(resume_text)
    readability_result = readability.calculate_readability(resume_text)
    formatting_result = formatting.check_formatting(resume_text)

    scoring_input = {
        "skill_match_score": skills_result.get("match_score", 0),
        "keyword_match_score": keyword_result.get("match_score", 0),
        "grammar_error_count": grammar_result.get("error_count", 0),
        "readability_grade": readability_result.get("flesch_kincaid_grade", 12),
        "formatting_issue_count": formatting_result.get("formatting_issue_count", 0)
    }

    final_score = scoring.score_ats_style(scoring_input)

    return jsonify({
        "skill_match": skills_result,
        "keyword_match": keyword_result,
        "grammar": grammar_result,
        "readability": readability_result,
        "formatting": formatting_result,
        "final_score": final_score
    })


if __name__ == '__main__':
    app.run(debug=True, port=5000)
