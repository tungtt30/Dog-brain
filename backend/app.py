"""
Dog-brain Document Chatbot - Main Application
"""
import sys
from flask import Flask, request, jsonify, render_template
from flask_cors import CORS

from utils.file_reader import read_file_auto
from utils.document_manager import document_manager
from model_func.model_manager import summarizer_model, translator_model, qa_model

# Configure stdout encoding
sys.stdout.reconfigure(encoding='utf-8')

# Constants
MAX_FILE_SIZE = 10 * 1024 * 1024  # 10MB
ALLOWED_EXTENSIONS = {'.docx', '.pdf', '.txt'}

# Flask app setup
app = Flask(__name__, static_url_path='', static_folder='static', template_folder='templates')
CORS(app)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    """Upload and process a document file."""
    try:
        if 'file' not in request.files:
            return jsonify({"error": "No file provided"}), 400

        file = request.files['file']
        if not file.filename:
            return jsonify({"error": "No file selected"}), 400

        # Validate file extension
        if not any(file.filename.lower().endswith(ext) for ext in ALLOWED_EXTENSIONS):
            return jsonify({"error": "Unsupported file type. Only .docx, .pdf, .txt allowed"}), 400

        # Read and store document content
        content = read_file_auto(file)
        if content:
            document_manager.content = content
            return jsonify({
                "message": "File uploaded successfully",
                "content_length": len(content)
            })
        else:
            return jsonify({"error": "Failed to read file content"}), 400

    except Exception as e:
        return jsonify({"error": f"File processing error: {str(e)}"}), 500

@app.route('/trans', methods=['POST'])
def translate():
    """Translate text using the translation model."""
    try:
        data = request.get_json()
        if not data or 'question' not in data:
            return jsonify({"error": "Missing text data"}), 400

        text = data.get("question", "").strip()
        if not text:
            return jsonify({"error": "Text cannot be empty"}), 400

        translation = translator_model.translate(text)
        return jsonify({"answer": translation})

    except Exception as e:
        return jsonify({"error": f"Translation failed: {str(e)}"}), 500

@app.route('/summ', methods=['POST'])
def summary():
    """Summarize text or uploaded document."""
    try:
        data = request.get_json()
        if not data or 'question' not in data:
            return jsonify({"error": "Missing data"}), 400

        input_text = data.get("question", "").strip()

        # If document is loaded, summarize it; otherwise summarize the input text
        if document_manager.is_loaded:
            summary_text = document_manager.content
        else:
            if not input_text:
                return jsonify({"error": "No document loaded or text provided"}), 400
            summary_text = input_text

        summary = summarizer_model.summarize(summary_text)
        return jsonify({"answer": summary})

    except Exception as e:
        return jsonify({"error": f"Summarization failed: {str(e)}"}), 500

@app.route('/ask', methods=['POST'])
def ask_question():
    """Answer questions about the uploaded document."""
    try:
        data = request.get_json()
        if not data or 'question' not in data:
            return jsonify({"error": "Missing question"}), 400

        question = data.get("question", "").strip()
        if not question:
            return jsonify({"error": "Question cannot be empty"}), 400

        if not document_manager.is_loaded:
            return jsonify({"error": "Please upload a document first"}), 400

        # Use QA model to answer based on document content
        answer = qa_model.answer_question(document_manager.content, question)
        return jsonify({"answer": answer})

    except Exception as e:
        return jsonify({"error": f"Question answering failed: {str(e)}"}), 500

@app.route('/status', methods=['GET'])
def get_status():
    """Check the status of the uploaded document."""
    return jsonify(document_manager.get_status())

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
