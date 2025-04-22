from flask import Flask, render_template, request, redirect, url_for, session
from flask_sqlalchemy import SQLAlchemy
from werkzeug.utils import secure_filename
from werkzeug.security import check_password_hash, generate_password_hash
from flask import request, render_template, redirect, url_for, flash
import os

from models import db, User, Candidate
from flask_migrate import Migrate

app = Flask(__name__)
app.secret_key = 'your-secret-key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['UPLOAD_FOLDER'] = 'uploads'
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

migrate = Migrate(app, db)

db.init_app(app)

# ======================== Routes ============================

@app.route('/')
def index():
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()

        if user and check_password_hash(user.password, password):  # Use hashed password check
            session['user_id'] = user.id
            session['role'] = user.role
            return redirect(url_for('admin'))
        else:
            return "Invalid username or password"
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))

@app.route('/upload', methods=['GET', 'POST'])
def upload():
    if request.method == 'POST':
        file = request.files['resume']
        if file:
            filename = secure_filename(file.filename)
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(filepath)

            # FAKE analysis (you can replace with GPT/spaCy code)
            candidate = Candidate(
                name="Jane Doe",
                email="jane@example.com",
                phone="1234567890",
                experience="3 years in software dev",
                skills="Python, Flask",
                education="B.Sc Computer Science",
                certifications="AWS Certified",
                score=88.0,
                ranking=1,
                status="Qualified"
            )
            db.session.add(candidate)
            db.session.commit()

            return redirect(url_for('result', id=candidate.id))
    return render_template('upload.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        role = request.form.get('role', 'admin')  # Default to 'admin' if not passed

        # Debug prints
        print("Form Data:", request.form)
        print("Form Type:", type(request.form))
        print("Username:", username)
        print("Password:", password)
        print("Role:", role)

        # Check if username already exists
        existing_user = User.query.filter_by(username=username).first()
        if existing_user:
            flash('Username already exists. Please choose another.', 'error')
            return redirect(url_for('register'))

        # Hash the password before saving
        hashed_password = generate_password_hash(password)

        # Create new user with role from form (should be 'admin')
        new_user = User(username=username, password=hashed_password, role=role)
        db.session.add(new_user)
        db.session.commit()

        flash('Admin registered successfully!', 'success')
        return redirect(url_for('login'))

    return render_template('register.html')


@app.route('/result/<int:id>')
def result(id):
    candidate = Candidate.query.get_or_404(id)
    return render_template('result.html', candidate=candidate)

@app.route('/admin')
def admin():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    candidates = Candidate.query.order_by(Candidate.ranking.asc()).all()
    return render_template('admin.html', candidates=candidates)

@app.route('/candidate/<int:id>')
def view_candidate(id):
    candidate = Candidate.query.get_or_404(id)
    return render_template('view_candidate.html', candidate=candidate)

# ======================== Run ============================

if __name__ == '__main__':
    with app.app_context():
        db.create_all()

        # Create admin user if not exists (run this block only once)
        from models import User,db
        if not User.query.filter_by(username='admin').first():
            admin = User(username='admin', password=generate_password_hash('admin123'), role='admin')
            db.session.add(admin)
            db.session.commit()
            print("Admin user created.")
        else:
            print("Admin user already exists.")

    app.run(debug=True)
