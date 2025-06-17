from flask import Flask, render_template, request, redirect, url_for
from utils import file_handler, text_extractor, text_preprocessor, skill_matcher, keyword_matcher, readability, grammar, formatting, scoring

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'

@app.route('/', methods=['GET', 'POST'])
def upload_resume():
    if request.method == 'POST':
        file = request.files['resume']
        job_desc = request.form.get('job_desc')
        filename = file_handler.save_file(file, app.config['UPLOAD_FOLDER'])
        text = text_extractor.extract_text(filename)
        cleaned = text_preprocessor.preprocess(text)
        
        skills = skill_matcher.match_skills(cleaned)
        keywords = keyword_matcher.compare(cleaned, job_desc)
        read_scores = readability.get_scores(cleaned)
        grammar_issues = grammar.check(cleaned)
        formatting_issues = formatting.analyze(text)
        scores = scoring.calculate(skills, keywords, read_scores, grammar_issues, formatting_issues)
        
        return render_template('result.html', **scores)
    
    return '''
        <form method="POST" enctype="multipart/form-data">
            Upload Resume: <input type="file" name="resume"><br>
            Job Description: <textarea name="job_desc"></textarea><br>
            <input type="submit">
        </form>
    '''

if __name__ == '__main__':
    app.run(debug=True)
