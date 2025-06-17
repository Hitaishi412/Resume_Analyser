from flask import Flask, request, jsonify
import textstat

app = Flask(__name__)

@app.route('/readability', methods=['POST'])
def calculate_readability():
    data = request.get_json()
    input_text = data.get("text", "")

    if not input_text.strip():
        return jsonify({"error": "Missing or empty 'text' field in request"}), 400

    readability_scores = {
        "flesch_reading_ease": textstat.flesch_reading_ease(input_text),
        "flesch_kincaid_grade": textstat.flesch_kincaid_grade(input_text),
        "smog_index": textstat.smog_index(input_text),
        "automated_readability_index": textstat.automated_readability_index(input_text),
        "coleman_liau_index": textstat.coleman_liau_index(input_text),
        "linsear_write_formula": textstat.linsear_write_formula(input_text),
        "dale_chall_score": textstat.dale_chall_readability_score(input_text),
        "difficult_words": textstat.difficult_words(input_text),
        "syllable_count": textstat.syllable_count(input_text),
        "lexicon_count": textstat.lexicon_count(input_text),
        "sentence_count": textstat.sentence_count(input_text),
        "readability_consensus": textstat.text_standard(input_text, float_output=False)
    }

    return jsonify(readability_scores)


if __name__ == '__main__':
    app.run(debug=True)
