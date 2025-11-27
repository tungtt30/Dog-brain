# Dog-brain Document Chatbot Guide

## Overview

Dog-brain is a cute document chatbot that allows users to upload Word documents (.docx), summarize their content, translate text, and ask questions based on the document using natural language processing models.

## Features

- 📄 Document Upload: Supports .docx file uploads
- ✨ Summarization: Automatically summarizes uploaded documents using T5 model
- 🌐 Translation: Translates text using T5 translation model
- ❓ Question Answering: Answers questions about the document content using RoBERTa QA model
- 🐰 Web Interface: Simple and adorable web UI

## Prerequisites

- Python 3.7+
- PyTorch (with CUDA support for GPU acceleration)
- Docker (optional, for containerized deployment)

## Installation

### Option 1: Local Setup

1. Clone the repository:

   ```bash
   git clone https://github.com/tungtt30/Dog-brain.git
   cd Dog-brain
   ```

2. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

3. Ensure model files are in place:
   - `backend/models/summ_model/` (T5 summarization model)
   - `backend/models/trans_model/` (T5 translation model)
   - QA model downloads automatically (deepset/roberta-base-squad2)

### Option 2: Docker Setup

1. Build and run with Docker Compose:
   ```bash
   docker-compose up --build
   ```

## Configuration

- Edit `backend/app_config.json` to change device settings:
  ```json
  {
    "device": "cuda" // or "cpu"
  }
  ```

## Running the Application

1. Navigate to the backend directory:

   ```bash
   cd backend
   ```

2. Run the Flask app:

   ```bash
   python app.py
   ```

3. Open your browser and go to `http://localhost:5000`

## Usage

1. **Upload Document**: Click "Upload" and select a .docx file
2. **Summarize**: Click "Summerize" to get a summary of the uploaded document
3. **Translate**: Enter text and click "Translate" to translate it
4. **Ask Questions**: Type a question about the document and click "Ask" to get an answer

## API Endpoints

- `GET /`: Main web interface
- `POST /upload`: Upload document file
- `POST /summ`: Summarize document or text
- `POST /trans`: Translate text
- `POST /ask`: Ask questions about uploaded document
- `GET /status`: Check if document is loaded

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

Feel free to submit issues or pull requests to improve Dog-brain! 🐶
