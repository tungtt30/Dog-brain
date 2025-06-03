from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
from utils.file_reader import read_docx
from model_func.summarizer import summ
from model_func.translate import trans
from model_func.qa import answer_question

import sys
sys.stdout.reconfigure(encoding='utf-8')

app = Flask(__name__, static_url_path='', static_folder='static', template_folder='templates')
CORS(app)

# Global variable để lưu nội dung tài liệu
document_content = ""

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    global document_content
    try:
        if 'file' not in request.files:
            return jsonify({"error": "Không có file được tải lên"}), 400
        
        file = request.files['file']
        if file.filename == '':
            return jsonify({"error": "Chưa chọn file"}), 400
            
        if file and file.filename.endswith('.docx'):
            document_content = read_docx(file)
            if document_content:
                return jsonify({
                    "message": "Tải file thành công!", 
                    "content_length": len(document_content)
                })
            else:
                return jsonify({"error": "Không thể đọc nội dung file"}), 400
        
        return jsonify({"error": "Chỉ hỗ trợ file .docx"}), 400
    
    except Exception as e:
        return jsonify({"error": f"Lỗi khi xử lý file: {str(e)}"}), 500

@app.route('/trans', methods=['POST'])
def translate():
    try:
        data = request.json
        if not data or 'question' not in data:
            return jsonify({"error": "Thiếu dữ liệu câu hỏi"}), 400
            
        question = data.get("question", "")
        if not question.strip():
            return jsonify({"error": "Câu hỏi không được để trống"}), 400
            
        answer = trans(question)
        return jsonify({"answer": answer})
    
    except Exception as e:
        return jsonify({"error": f"Lỗi khi dịch: {str(e)}"}), 500

@app.route('/summ', methods=['POST'])
def summary():
    try:
        data = request.json
        if not data or 'question' not in data:
            return jsonify({"error": "Thiếu dữ liệu"}), 400
            
        question = data.get("question", "")
        
        # Nếu có document content, summarize nó thay vì question
        if document_content:
            answer = summ(document_content)
        else:
            if not question.strip():
                return jsonify({"error": "Chưa có tài liệu để tóm tắt"}), 400
            answer = summ(question)
            
        return jsonify({"answer": answer})
    
    except Exception as e:
        return jsonify({"error": f"Lỗi khi tóm tắt: {str(e)}"}), 500

@app.route('/ask', methods=['POST'])
def ask_question():
    global document_content
    try:
        data = request.json
        if not data or 'question' not in data:
            return jsonify({"error": "Thiếu câu hỏi"}), 400
            
        question = data.get("question", "")
        if not question.strip():
            return jsonify({"error": "Câu hỏi không được để trống"}), 400
            
        if not document_content:
            return jsonify({"error": "Vui lòng tải tài liệu lên trước khi hỏi"}), 400
            
        # Sử dụng model Q&A để trả lời dựa trên document content
        answer = answer_question(document_content, question)
        
        if not answer or answer.strip() == "":
            answer = "Xin lỗi, tôi không tìm thấy thông tin liên quan trong tài liệu."
            
        return jsonify({"answer": answer})
    
    except Exception as e:
        return jsonify({"error": f"Lỗi khi trả lời câu hỏi: {str(e)}"}), 500

@app.route('/status', methods=['GET'])
def get_status():
    """Endpoint để kiểm tra trạng thái tài liệu đã tải"""
    return jsonify({
        "document_loaded": bool(document_content),
        "document_length": len(document_content) if document_content else 0
    })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)