Resume Analysis Tool
This project is a Resume Analysis Tool built using Python, Flask, and various libraries like spacy, pdfplumber, and re for parsing resumes in PDF format and extracting useful data such as name, email, skills, and more. The tool provides resume rating based on core and soft skills and offers improvement suggestions.
Features
Resume Parsing: Extracts the name, email, core skills, and soft skills from the uploaded resume (in PDF format).
Resume Rating: Rates the resume based on core and soft skills.
Improvement Suggestions: Suggests skills to improve based on the missing core skills.
Resume History: Keeps track of previously uploaded resumes with a download link.
Web Interface: A simple web interface built using Flask and Tailwind CSS for users to upload resumes and view extracted data.
Tech Stack
Frontend: HTML, CSS (Tailwind), JavaScript
Backend: Python (Flask)
Libraries:
spacy for Named Entity Recognition (NER) to extract names.
pdfplumber for extracting text from PDF files.
re for regular expressions (used for extracting email).
Database: JSON file (history.json) to store previously uploaded resume data.
Run the Flask App
Make sure you're in the project directory, and then run the Flask app:
python app.py
This will start a local development server.
Access the Web App
Once the server is running, open a web browser and go to:
http://127.0.0.1:5000/
