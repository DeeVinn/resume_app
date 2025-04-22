import spacy
import docx
from pdfminer.high_level import extract_text
import openai

nlp = spacy.load("en_core_web_sm")

def parse_resume(file_path):
    text = ""
    
    if file_path.endswith('.pdf'):
        text = extract_text(file_path)
    elif file_path.endswith('.docx'):
        doc = docx.Document(file_path)
        for para in doc.paragraphs:
            text += para.text + "\n"
    
    # Use spaCy to process the text and extract entities like name, phone, etc.
    doc = nlp(text)
    contact_details = {
        "name": "",
        "email": "",
        "phone": "",
    }
    for ent in doc.ents:
        if ent.label_ == "PERSON":
            contact_details["name"] = ent.text
        elif ent.label_ == "EMAIL":
            contact_details["email"] = ent.text
        elif ent.label_ == "PHONE":
            contact_details["phone"] = ent.text

    return contact_details

def analyze_with_ai(text, job_description):
    prompt = f"Analyze the following resume and match it with this job description:\nResume: {text}\nJob Description: {job_description}\nPlease provide a score (out of 100) based on relevance."
    response = openai.Completion.create(
        engine="gpt-3.5-turbo",
        prompt=prompt,
        max_tokens=150
    )
    score = response['choices'][0]['text'].strip()
    return score

def send_notification(candidate_email, status):
    # Dummy email sending logic
    print(f"Sending email to {candidate_email} about status: {status}")

from flask import Flask, render_template, request, redirect, url_for, session
from models import db, User

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite'
app.config['SECRET_KEY'] = 'supersecretkey'
db.init_app(app)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()
        if user and user.password == password:
            session['user_id'] = user.id
            return redirect(url_for('upload_resume'))
        else:
            return "Invalid credentials"
    return render_template('login.html')
