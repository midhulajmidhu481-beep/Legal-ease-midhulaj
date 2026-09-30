from flask import Flask, render_template, request
import fitz  # PyMuPDF
import google.generativeai as genai

app = Flask(__name__)

# Gemini API key - unga key podu
genai.configure(api_key="YOUR_GEMINI_API_KEY")
model = genai.GenerativeModel("gemini-1.5-flash")

def extract_text_from_pdf(pdf_file):
    doc = fitz.open(stream=pdf_file.read(), filetype="pdf")
    text = ""
    for page in doc:
        text += page.get_text()
    return text

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload():
    if 'file' not in request.files:
        return "No file uploaded"
    
    file = request.files['file']
    legal_text = extract_text_from_pdf(file)
