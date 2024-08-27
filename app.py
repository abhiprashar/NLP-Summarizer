from flask import Flask, render_template, request
from login import summarize_text

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    return render_template('gui.html')

@app.route('/analyze', methods = ['GET', 'POST'])
def analyze():
    if request.method == 'POST':
        rawtext = request.form['rawtext']
        summary = summarize_text(rawtext)
    return render_template('summarizee.html', summary=summary)


if __name__ == "__main__":
    app.run(debug=True)