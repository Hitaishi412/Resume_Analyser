from flask import Flask, request, jsonify
import re

app = Flask(__name__)

def check_formatting_issues(text):
    issues = []

    # Rule 1: Multiple spaces
    if re.search(r' {2,}', text):
        issues.append("Multiple consecutive spaces found.")

    # Rule 2: Inconsistent bullet points
    bullet_styles = re.findall(r'^(\s*[\-\*\u2022])', text, re.MULTILINE)
    if bullet_styles and len(set(bullet_styles)) > 1:
        issues.append("Inconsistent bullet styles (e.g., '-', '*', '•').")

    # Rule 3: No space after punctuation
    if re.search(r'[.,;:!?][^\s\n]', text):
        issues.append("Missing space after punctuation.")

    # Rule 4: Inconsistent capitalization in bullet points
    bullets = re.findall(r'^[\-\*\u2022]\s+(.*)', text, re.MULTILINE)
    if bullets:
        start_cases = [b[0].isupper() for b in bullets if b]
        if not all(start_cases) and any(start_cases):
            issues.append("Inconsistent capitalization in bullet points.")

    # Rule 5: Unusual indentation
    if re.search(r'^\s{5,}\S', text, re.MULTILINE):
        issues.append("Excessive indentation found.")

    # Rule 6: Long paragraphs
    paragraphs = text.split('\n\n')
    for p in paragraphs:
        if len(p.split()) > 120:
            issues.append("Very long paragraph detected — consider splitting.")

    return list(set(issues))


@app.route('/formatting-check', methods=['POST'])
def formatting_check():
    data = request.get_json()
    input_text = data.get("text", "")

    if not input_text.strip():
        return jsonify({"error": "Missing or empty 'text' field"}), 400

    issues = check_formatting_issues(input_text)

    return jsonify({
        "original_text": input_text,
        "formatting_issue_count": len(issues),
        "formatting_issues": issues
    })


if __name__ == '__main__':
    app.run(debug=True)
