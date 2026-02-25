from flask import Flask, render_template, request, redirect, flash
from flask_sqlalchemy import SQLAlchemy
import string
import random
import requests # Used to verify if the URL is real

app = Flask(__name__)
app.secret_key = 'super_secret_key' # Needed for flash messages

# 3. Backend - Database ORM Configuration (SQLite + SQLAlchemy)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# ORM Model mapping to the Database table
class URLMap(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    original_url = db.Column(db.String(500), nullable=False)
    short_id = db.Column(db.String(10), unique=True, nullable=False)

# Create the database automatically
with app.app_context():
    db.create_all()

# --- Helper Functions ---
def generate_short_id():
    """Generates a random 6-character short ID."""
    characters = string.ascii_letters + string.digits
    return ''.join(random.choice(characters) for _ in range(6))

def is_valid_url(url):
    """Verifies if the URL is correct/reachable by sending a quick request."""
    try:
        response = requests.head(url, timeout=3, allow_redirects=True)
        return response.status_code < 400
    except requests.RequestException:
        return False

# --- Routes ---
@app.route('/', methods=['GET', 'POST'])
def home():
    shortened_url = None
    
    if request.method == 'POST':
        original_url = request.form.get('original_url')
        
        # Add http:// if the user forgot it
        if not original_url.startswith(('http://', 'https://')):
            original_url = 'http://' + original_url

        # Check if URL is real (Requirement: "Try to verify whether the URL... is correct")
        if not is_valid_url(original_url):
            flash('Error: The URL you entered does not exist or is unreachable.', 'danger')
            return render_template('home.html')

        # Check if we already shortened this URL to avoid duplicates
        existing_url = URLMap.query.filter_by(original_url=original_url).first()
        if existing_url:
            short_id = existing_url.short_id
        else:
            # Generate new short ID and save to database using ORM
            short_id = generate_short_id()
            new_entry = URLMap(original_url=original_url, short_id=short_id)
            db.session.add(new_entry)
            db.session.commit()

        shortened_url = request.host_url + short_id

    return render_template('home.html', shortened_url=shortened_url)

@app.route('/history')
def history():
    # Fetch all URLs from the database using ORM
    all_urls = URLMap.query.all()
    return render_template('history.html', urls=all_urls)

@app.route('/<short_id>')
def redirect_to_original(short_id):
    # Find the original URL in the database and redirect
    link = URLMap.query.filter_by(short_id=short_id).first_or_404()
    return redirect(link.original_url)

if __name__ == '__main__':
    app.run(debug=True)