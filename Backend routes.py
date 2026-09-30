from fastapi import APIRouter, UploadFile, File, HTTPException
import fitz  # PyMuPDF
import os
from dotenv import load_dotenv
import google.generativeai as genai

load_dotenv()

router = APIRouter()

# Gemini Setup - Team 210PocketSmart
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
if GEMINI_API_KEY:
    genai.configure(api_key=GEMINI_API_KEY)
    model = genai.GenerativeModel("gemini-1.5-flash")
else:
    model = None

def extract_text_from_pdf(pdf_bytes):
    """PDF la irunthu text edukkum function"""
    doc = fitz.open(stream=pdf_bytes, filetype="pdf")
    text = ""
    for page in doc:
        text += page.get_text()
    return text

@router.get("/")
def home():
    return {"message": "LegalEaseAI Backend Running", "team_id": "210PocketSmart"}

@router.post("/simplify")
async def simplify_document(file: UploadFile = File(...)):
    try:
        if not file.filename.endswith('.pdf'):
            raise HTTPException(status_code=400, detail="Only PDF allowed")

        # 1. PDF read pannu
        pdf_bytes = await file.read()
        legal_text = extract_text_from_pdf(pdf_bytes)

        if not legal_text.strip():
            raise HTTPException(status_code=400, detail="PDF is empty")

        # 2. Gemini ku anuppa prompt
        if not model:
            raise HTTPException(status_code=500, detail="Gemini API Key missing in .env")

        prompt = f"""
        You are LegalEaseAI - An AI Legal Assistant for team 210PocketSmart.
        
        Task: Simplify this legal document.
        1. Give Title
        2. Give 5 Points Summary in simple English + Tamil mixed
        3. List Risks / Important Clauses
        4. Give Simplified Version of full document (easy language)

        Legal Document:
        {legal_text[:8000]}
        """

        response = model.generate_content(prompt)
        
        return {
            "team_id": "210PocketSmart",
            "filename": file.filename,
            "original_length": len(legal_text),
            "simplified_result": response.text
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/chat")
async def chat_with_doc(question: str, context: str):
    """Document pathi doubt ketka"""
    try:
        prompt = f"""
        Context: {context[:4000]}
        User Question: {question}
        Answer as a friendly legal assistant in simple language.
        Team: 210PocketSmart
        """
        response = model.generate_content(prompt)
        return {"answer": response.text}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
