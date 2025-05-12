from flask import Flask, request, jsonify
from flask_cors import CORS
from utils.file_reader import read_docx
from model.summarizer import summarize_text
from model.qa import answer_question

app = Flask(__name__)
CORS(app)

document_content = ""  # Save word content

@app.route('/upload', methods=['POST'])
def upload_file():
    global document_content
    file = request.files['file']
    if file and file.filename.endswith('.docx'):
        document_content = read_docx(file)
        return jsonify({"message": "File uploaded OK"})
    return jsonify({"error": "Only support .docx"}), 400

@app.route('/summarize', methods=['GET'])
def summarize():
    if not document_content:
        return jsonify({"error": "Not uploaded file yet"}), 400
    summary = summarize_text(document_content)
    return jsonify({"summary": summary})

@app.route('/ask', methods=['POST'])
def ask():
    data = request.json
    question = data.get("question", "")
    answer = answer_question(document_content, question)
    return jsonify({"answer": answer})

if __name__ == '__main__':
    app.run(debug=True)
