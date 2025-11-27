# Dog-brain Document Chatbot

![Main](./image.jpg)

A powerful document chatbot that leverages natural language processing models to upload, summarize, translate, and answer questions about your documents. Built with Flask and PyTorch, Dog-brain provides an intuitive web interface for document analysis.

## Features

- **Document Upload**: Support for .docx, .pdf, and .txt files
- **Intelligent Summarization**: Automatic summarization using T5 model
- **Text Translation**: Translate text using T5 translation model
- **Question Answering**: Answer questions about document content using RoBERTa QA model
- **Web Interface**: Clean and user-friendly web UI
- **REST API**: Full API support for integration
- **Docker Support**: Easy deployment with Docker Compose

## Prerequisites

- Python 3.7+
- PyTorch (with CUDA support for GPU acceleration)
- Docker (optional, for containerized deployment)

## Installation

### Option 1: Local Setup

1. **Clone the repository**:

   ```bash
   git clone https://github.com/tungtt30/Dog-brain.git
   cd Dog-brain
   ```

2. **Install dependencies**:

   ```bash
   pip install -r requirements.txt
   ```

3. **Ensure model files are in place**:
   - `backend/models/summ_model/` (T5 summarization model)
   - `backend/models/trans_model/` (T5 translation model)
   - QA model downloads automatically (deepset/roberta-base-squad2)

### Option 2: Docker Setup

1. **Build and run with Docker Compose**:
   ```bash
   docker-compose up --build
   ```

## Configuration

Edit `backend/app_config.json` to configure device settings:

```json
{
  "device": "cuda" // Use "cpu" for CPU-only execution
}
```

## Running the Application

1. **Navigate to the backend directory**:

   ```bash
   cd backend
   ```

2. **Run the Flask app**:

   ```bash
   python app.py
   ```

3. **Open your browser** and go to `http://localhost:5000`

## Usage

1. **Upload Document**: Click "Upload" and select a .docx, .pdf, or .txt file
2. **Summarize**: Click "Summarize" to get a summary of the uploaded document or input text
3. **Translate**: Enter text and click "Translate" to translate it
4. **Ask Questions**: Type a question about the document and click "Ask" to get an answer

## API Endpoints

- `GET /`: Main web interface
- `POST /upload`: Upload document file
- `POST /summ`: Summarize document or text
- `POST /trans`: Translate text
- `POST /ask`: Ask questions about uploaded document
- `GET /status`: Check if document is loaded

### API Examples

**Upload a document**:

```bash
curl -X POST -F "file=@document.docx" http://localhost:5000/upload
```

**Ask a question**:

```bash
curl -X POST -H "Content-Type: application/json" \
  -d '{"question": "What is the main topic?"}' \
  http://localhost:5000/ask
```

## Architecture

- **Backend**: Flask web server with REST API
- **Models**:
  - Summarization: Local T5 model
  - Translation: Local T5 model
  - QA: RoBERTa-base-squad2 from Hugging Face
- **Frontend**: HTML/CSS/JavaScript
- **File Processing**: Supports .docx, .pdf, .txt files

## Troubleshooting

- Ensure CUDA is installed if using GPU acceleration
- Check that model directories exist and contain required files
- Verify port 5000 is not in use
- For Docker issues, ensure Docker Desktop is running

## Contributing

Contributions are welcome! Please feel free to submit issues or pull requests to improve Dog-brain.

## License

This project is licensed under the MIT License.
