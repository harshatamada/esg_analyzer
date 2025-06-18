from flask import Flask, render_template, request, send_from_directory, redirect, url_for
import os
from backend.esg_analyzer import analyze_esg

app = Flask(__name__)

UPLOAD_FOLDER = os.path.join("backend", "data")
OUTPUT_FOLDER = os.path.join("backend", "outputs")

@app.route('/')
def index():
    return render_template("index.html")

@app.route('/analyze', methods=['POST'])
def analyze():
    file = request.files['file']
    if file:
        file_path = os.path.join(UPLOAD_FOLDER, file.filename)
        file.save(file_path)

        analyze_esg(file_path)

        return render_template("index.html",
                               summary_file="esg_summary.csv",
                               text_summary="company_esg_risk_summary.txt")
    return redirect(url_for('index'))

@app.route('/download/<filename>')
def download(filename):
    return send_from_directory(OUTPUT_FOLDER, filename, as_attachment=True)

if __name__ == '__main__':
    app.run(debug=True)
