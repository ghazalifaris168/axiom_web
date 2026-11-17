from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__, instance_relative_config=True)
app.config['SECRET_KEY'] = 'axiom-secret-key-2026'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///axiom.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    full_name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)
    subjects = db.Column(db.String(200), nullable=True)

    def __repr__(self):
        return f'<User {self.email}>'

@app.route('/')
def home():
    return render_template('main.html')  # Make sure your template file is named main.html

@app.route('/login', methods=['GET', 'POST'])
def login_page():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        
        # Find user by email
        user = User.query.filter_by(email=email).first()
        
        # Check if user exists AND password matches
        if user and user.password == password:
            # Successful login: redirect to study dashboard
            return redirect(url_for('study_dashboard'))
        else:
            # Failed login: reload login page with an error message
            return render_template('login.html', error="Incorrect email or password. Please try again.")
            
    return render_template('login.html')

@app.route('/study')
def study_dashboard():
    return render_template('study.html')


@app.route('/signup', methods=['GET', 'POST'])
def signup_page():
    if request.method == 'POST':
        full_name = request.form.get('full_name')
        email = request.form.get('email')
        password = request.form.get('password')
        
        selected_subjects = request.form.getlist('subjects')
        subjects_str = ", ".join(selected_subjects)

        new_user = User(
            full_name=full_name,
            email=email,
            password=password,
            subjects=subjects_str
        )

        db.session.add(new_user)
        db.session.commit()

        return redirect(url_for('login_page'))

    return render_template('signup.html')

if __name__ == '__main__':
    app.run(debug=True)