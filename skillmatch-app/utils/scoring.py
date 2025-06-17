from flask import Flask, request, jsonify

app = Flask(__name__)

WEIGHTS = {
    "skill_match": 0.35,
    "keyword_match": 0.2,
    "formatting": 0.15,
    "grammar": 0.15,
    "readability": 0.15
}

IDEAL_READABILITY_GRADE = 8

def score_ats_style(metrics):
    skill_score = metrics.get("skill_match_score", 0)
    keyword_score = metrics.get("keyword_match_score", 0)
    grammar_errors = metrics.get("grammar_error_count", 0)
    formatting_issues = metrics.get("formatting_issue_count", 0)
    readability_grade = metrics.get("readability_grade", 12)  # higher = harder to read

    # ---- Normalize each score ----
    grammar_score = max(0, 100 - grammar_errors * 4)     # 4 point penalty per error
    formatting_score = max(0, 100 - formatting_issues * 5)
    readability_score = max(0, 100 - abs(readability_grade - IDEAL_READABILITY_GRADE) * 7)

    # ---- Calculate weighted score ----
    final_score = (
        skill_score * WEIGHTS["skill_match"] +
        keyword_score * WEIGHTS["keyword_match"] +
        formatting_score * WEIGHTS["formatting"] +
        grammar_score * WEIGHTS["grammar"] +
        readability_score * WEIGHTS["readability"]
    )

    # ---- ATS-like Feedback ----
    feedback = []
    if skill_score < 60:
        feedback.append("Include more job-relevant skills to improve alignment.")
    if keyword_score < 50:
        feedback.append("Add more keywords from the job description.")
    if grammar_score < 80:
        feedback.append("Fix grammar or spelling errors for professionalism.")
    if formatting_score < 85:
        feedback.append("Improve section formatting, spacing, or bullet consistency.")
    if readability_score < 75:
        feedback.append("Simplify sentence structure to improve clarity.")

    return {
        "final_score": round(final_score, 2),
        "breakdown": {
            "skill_match_score": skill_score,
            "keyword_match_score": keyword_score,
            "formatting_score": formatting_score,
            "grammar_score": grammar_score,
            "readability_score": readability_score
        },
        "feedback": feedback
    }

@app.route('/score', methods=['POST'])
def score():
    data = request.get_json()

    required_fields = [
        "skill_match_score",
        "keyword_match_score",
        "grammar_error_count",
        "formatting_issue_count",
        "readability_grade"
    ]

    if not all(field in data for field in required_fields):
        return jsonify({"error": f"Missing fields. Required: {required_fields}"}), 400

    result = score_ats_style(data)
    return jsonify(result)

if __name__ == '__main__':
    app.run(debug=True)
