from docx import Document

def read_docx(file_storage):
    doc = Document(file_storage)
    text = "\n".join([para.text for para in doc.paragraphs])
    return text
