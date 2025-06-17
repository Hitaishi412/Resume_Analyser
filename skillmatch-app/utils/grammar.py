from flask import Flask, request, jsonify
from language_tool_python import LanguageToolPublicAPI

app = Flask(__name__)
tool = LanguageToolPublicAPI('en-US')  # You can change locale if needed


@app.route('/grammar-check', methods=['POST'])
def grammar_check():
    data = request.get_json()
    input_text = data.get("text", "")

    if not input_text.strip():
        return jsonify({"error": "Missing or empty 'text' field"}), 400

    # Check grammar
    matches = tool.check(input_text)

    # Format grammar suggestions
    suggestions = []
    for match in matches:
        suggestions.append({
            "message": match.message,
            "suggestions": match.replacements,
            "offset": match.offset,
            "error_length": match.errorLength,
            "context": match.context,
            "rule": match.ruleId
        })

    return jsonify({
        "original_text": input_text,
        "error_count": len(suggestions),
        "grammar_issues": suggestions
    })


if __name__ == '__main__':
    app.run(debug=True)
