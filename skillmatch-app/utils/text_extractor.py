from pdfminer.high_level import extract_text as extract_pdf_text
import docx

def extract_text(file_path):
    """
    Extracts text from PDF or DOCX file based on file extension.
    """
    if file_path.endswith(".pdf"):
        return extract_pdf_text(file_path)
    
    elif file_path.endswith(".docx"):
        doc = docx.Document(file_path)
        return "\n".join([para.text for para in doc.paragraphs])
    
    else:
        raise ValueError("Unsupported file type. Only PDF and DOCX are allowed.")
