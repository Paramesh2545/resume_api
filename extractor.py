import PyPDF2
import docx2txt
import tempfile
import re
import fitz  # PyMuPDF

def extract_text_from_pdf(file):
    try:
        # file is a file-like object → read bytes
        pdf_bytes = file.read()

        # open from bytes
        doc = fitz.open("pdf", pdf_bytes)
        text = ""
        for page in doc:
            text += page.get_text()
        return text
    except Exception as e:
        print("PDF Error:", e)
        return ""


def extract_text_from_docx(file):
    try:
        # Create a temporary file
        with tempfile.NamedTemporaryFile(delete=False, suffix=".docx") as tmp:
            tmp.write(file.read())
            tmp_path = tmp.name

        # Now pass the temp file path to docx2txt
        text = docx2txt.process(tmp_path)
        return text if text else ""
    except Exception as e:
        print("DOCX Error:", e)
        return ""
