from fastapi import FastAPI, UploadFile, File
import extractor
import parser as resume_parser
app = FastAPI()

@app.get("/")
def root():
    return {"message": "Resume Parser API is running 🚀"}

@app.post("/parse-resume")
async def parse_resume(file: UploadFile = File(...)):
    filename = file.filename.lower()

    if filename.endswith(".pdf"):
        text = extractor.extract_text_from_pdf(file.file)
    elif filename.endswith(".docx"):
        text = extractor.extract_text_from_docx(file.file)
    else:
        return {"error": "Please upload PDF or DOCX files only."}

    parsed_data = resume_parser.parse_resume_text(text)

    return {
        "filename": file.filename,
        "parsed_details": parsed_data
    }
