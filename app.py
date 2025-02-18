from flask import Flask, render_template, request, send_from_directory
import os
import pdfplumber
import re
import json
from werkzeug.utils import secure_filename

app = Flask(__name__)

UPLOAD_FOLDER = "uploads"
ALLOWED_EXTENSIONS = {"pdf"}
HISTORY_FILE = "history.json"
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

CORE_SKILLS = {"python", "java", "react", "flask", "fastapi", "mongodb", "postgresql"}
SOFT_SKILLS = {"team player", "hardworking", "leadership", "communication", "problem-solving"}

def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS

def extract_text_from_pdf(filepath):
    text = ""
    with pdfplumber.open(filepath) as pdf:
        for page in pdf.pages:
            text += page.extract_text() + "\n"
    return text.strip()

# Function to extract email from text
def extract_email(text):
    email_match = re.search(r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}", text)
    if email_match:
        return email_match.group(0)
    return "Not found"

# Function to extract name from email (before @ symbol) and remove digits
def extract_name_from_email(email):
    if email != "Not found":
        name_part = email.split("@")[0]  # Get the part before '@'
        # Remove digits and keep only alphabetic characters
        name_part = ''.join([char for char in name_part if char.isalpha()])
        return name_part
    return "Not found"

# Function to extract skills (core and soft)
def extract_skills(text):
    words = set(text.lower().split())
    core_skills = list(CORE_SKILLS.intersection(words))
    soft_skills = list(SOFT_SKILLS.intersection(words))
    return core_skills, soft_skills

# Function to rate the resume based on skills
def rate_resume(core_skills, soft_skills):
    score = 0
    if len(core_skills) > 3:
        score += 5
    if len(soft_skills) > 1:
        score += 3
    return min(score, 10)

# Suggest improvements based on missing core skills
def suggest_improvements(core_skills):
    missing_skills = CORE_SKILLS.difference(core_skills)
    return f"Consider learning: {', '.join(missing_skills)}" if missing_skills else "No improvements needed"

# Save the extracted data to history.json
def save_to_history(data):
    history = []
    if os.path.exists(HISTORY_FILE):
        with open(HISTORY_FILE, "r") as file:
            history = json.load(file)

    history.append(data)
    with open(HISTORY_FILE, "w") as file:
        json.dump(history, file, indent=4)

# Load history data from history.json
def load_history():
    if os.path.exists(HISTORY_FILE):
        with open(HISTORY_FILE, "r") as file:
            return json.load(file)
    return []

@app.route("/", methods=["GET", "POST"])
def index():
    extracted_data = {}

    if request.method == "POST":
        if "pdf_doc" not in request.files:
            return render_template("index.html", data={"error": "No file uploaded"}, history=load_history())

        file = request.files["pdf_doc"]

        if file.filename == "":
            return render_template("index.html", data={"error": "No file selected"}, history=load_history())

        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            filepath = os.path.join(app.config["UPLOAD_FOLDER"], filename)
            file.save(filepath)

            extracted_text = extract_text_from_pdf(filepath)
            
            # Extract email first
            email = extract_email(extracted_text)
            
            # Extract name from email
            name = extract_name_from_email(email)
            
            core_skills, soft_skills = extract_skills(extracted_text)
            resume_rating = rate_resume(core_skills, soft_skills)
            improvement_areas = suggest_improvements(core_skills)

            extracted_data = {
                "name": name,
                "email": email,
                "core_skills": core_skills,
                "soft_skills": soft_skills,
                "resume_rating": resume_rating,
                "improvement_areas": improvement_areas,
                "filename": filename,
            }

            save_to_history(extracted_data)

    return render_template("index.html", data=extracted_data, history=load_history())

@app.route("/uploads/<filename>")
def uploaded_file(filename):
    return send_from_directory(app.config["UPLOAD_FOLDER"], filename)

if __name__ == "__main__":
    app.run(debug=True)
