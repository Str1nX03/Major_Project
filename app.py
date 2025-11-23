import os
import sqlite3
import json
from flask import Flask, render_template, request, redirect, url_for, session, flash
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from dotenv import load_dotenv
from src.agents.assistant_agent import AssistantAgent
from src.agents.testing_agent import TestingAgent
from src.agents.tutoring_agent import TutoringAgent

# Load environment variables
load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv("FLASK_SECRET_KEY", "super_secret_dev_key")

# --- Database Config ---
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# --- Database Models ---
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(150), nullable=False)
    # Relationship to access courses easily
    courses = db.relationship('Course', backref='author', lazy=True)

class Course(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    topic = db.Column(db.String(150), nullable=False)
    subject = db.Column(db.String(150), nullable=False)
    standard = db.Column(db.Integer, nullable=False)
    
    # Storing large text content
    intro = db.Column(db.Text, nullable=True)
    links = db.Column(db.Text, nullable=True)
    
    # Storing Dicts as JSON strings
    lessons_json = db.Column(db.Text, nullable=True) 
    tests_json = db.Column(db.Text, nullable=True)

# Initialize Database within Application Context
with app.app_context():
    db.create_all()

# --- Helpers ---
def check_auth():
    """Helper to check if user is logged in."""
    if 'user_id' not in session:
        return False
    return True

# --- Routes ---

@app.route('/')
def home():
    """Landing Page"""
    return render_template('landing.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    """Registration Page"""
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        if not username or not password:
            flash("Username and password are required.", "error")
            return redirect(url_for('register'))

        # Check if user already exists
        user_exists = User.query.filter_by(username=username).first()
        if user_exists:
            flash("Username already exists. Please choose another.", "error")
            return redirect(url_for('register'))

        # Create new user with hashed password
        hashed_password = generate_password_hash(password, method='pbkdf2:sha256')
        new_user = User(username=username, password=hashed_password)
        
        try:
            db.session.add(new_user)
            db.session.commit()
            flash("Registration successful! Please login.", "success")
            return redirect(url_for('login'))
        except Exception as e:
            flash("An error occurred during registration.", "error")
            return redirect(url_for('register'))

    return render_template('login.html', mode='register')

@app.route('/login', methods=['GET', 'POST'])
def login():
    """Login/Signin Page"""
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        user = User.query.filter_by(username=username).first()

        if user and check_password_hash(user.password, password):
            session['user_id'] = user.id
            session['username'] = user.username
            flash(f"Welcome back, {user.username}!", "success")
            return redirect(url_for('dashboard'))
        else:
            flash("Invalid username or password.", "error")
            return redirect(url_for('login'))
            
    return render_template('login.html', mode='login')

@app.route('/logout')
def logout():
    session.clear()
    flash("You have been logged out.", "info")
    return redirect(url_for('home'))

@app.route('/dashboard')
def dashboard():
    """After Login - User Inputs Topic & Sees History"""
    if not check_auth():
        flash("Please login to access the dashboard.", "error")
        return redirect(url_for('login'))
    
    # Fetch user's previous courses (Newest first)
    user_courses = Course.query.filter_by(user_id=session['user_id']).order_by(Course.id.desc()).all()
    
    return render_template('dashboard.html', user=session.get('username'), courses=user_courses)

@app.route('/course/<int:course_id>')
def view_course(course_id):
    """View a saved course without regenerating"""
    if not check_auth():
        flash("Please login.", "error")
        return redirect(url_for('login'))
    
    course = Course.query.get_or_404(course_id)
    
    # Ensure user owns this course
    if course.user_id != session['user_id']:
        flash("Unauthorized access.", "error")
        return redirect(url_for('dashboard'))
    
    # Deserialize JSON strings back to Dicts
    lessons = json.loads(course.lessons_json) if course.lessons_json else {}
    tests = json.loads(course.tests_json) if course.tests_json else {}
    
    return render_template(
        'product.html',
        topic=course.topic,
        subject=course.subject,
        standard=course.standard,
        intro=course.intro,
        links=course.links,
        lessons=lessons,
        tests=tests
    )

@app.route('/product', methods=['POST'])
def product():
    """Product Page - Orchestrates all Agents"""
    if not check_auth():
        flash("Please login to access the content.", "error")
        return redirect(url_for('login'))

    # 1. Get User Input
    topic = request.form.get('topic')
    subject = request.form.get('subject')
    standard = request.form.get('standard')

    if not all([topic, subject, standard]):
        flash("All fields are required.", "error")
        return redirect(url_for('dashboard'))

    # --- CHECK HISTORY FIRST ---
    # If exact same request exists for this user, load it instead of generating
    existing_course = Course.query.filter_by(
        user_id=session['user_id'],
        topic=topic,
        subject=subject,
        standard=int(standard)
    ).first()
    
    if existing_course:
        flash("Loaded course from your history!", "success")
        return redirect(url_for('view_course', course_id=existing_course.id))

    try:
        # --- AGENT 1: ASSISTANT AGENT ---
        assistant = AssistantAgent()
        initial_state = {"standard": str(standard), "subject": subject, "topic": topic}
        assistant_output = assistant.graph.invoke(initial_state)
        
        instructions = assistant_output['instructions']
        topic_intro = assistant_output.get('topic_intro', 'No intro generated.')
        study_links = assistant_output.get('study_links', 'No links found.')

        # --- AGENT 2: TUTORING AGENT ---
        tutor = TutoringAgent()
        lessons = tutor.run(instructions, int(standard), subject, topic)

        # --- AGENT 3: TESTING AGENT ---
        tester = TestingAgent()
        tests = tester.run(lessons)
        
        # --- SAVE TO DATABASE ---
        new_course = Course(
            user_id=session['user_id'],
            topic=topic,
            subject=subject,
            standard=int(standard),
            intro=topic_intro,
            links=study_links,
            lessons_json=json.dumps(lessons), # Serialize dict to string
            tests_json=json.dumps(tests)      # Serialize dict to string
        )
        db.session.add(new_course)
        db.session.commit()
        
        flash("Course generated and saved to your history!", "success")

        return render_template(
            'product.html',
            topic=topic,
            subject=subject,
            standard=standard,
            intro=topic_intro,
            links=study_links,
            lessons=lessons,
            tests=tests
        )

    except Exception as e:
        flash(f"An error occurred during generation: {str(e)}", "error")
        print(f"Error: {e}")
        return redirect(url_for('dashboard'))

if __name__ == '__main__':
    app.run(debug=True)