from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
from utils.file_reader import read_docx
from model_func.summarizer import summ
from model_func.translate import trans

import sys
sys.stdout.reconfigure(encoding='utf-8')

app = Flask(__name__, static_url_path='', static_folder='static', template_folder='templates')
CORS(app)

document_content = ""

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    global document_content
    file = request.files['file']
    if file and file.filename.endswith('.docx'):
        document_content = read_docx(file)
        return jsonify({"message": "File uploaded OK"})
    return jsonify({"error": "Only support file .docx"}), 400

@app.route('/trans', methods=['POST'])
def translate():
    data = request.json
    question = data.get("question", "")
    # print("from server" + question)
    answer = trans(question)
    # print("res: ", answer)
    return jsonify({"answer": answer})

@app.route('/summ', methods=['POST'])
def summary():
    data = request.json
    question = data.get("question", "")
    # print("from server" + question)
    answer = summ(question)
    # print("res: ", answer)
    return jsonify({"answer": answer})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
