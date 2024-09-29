from flask import Flask, render_template, request, redirect, url_for, jsonify, session
import csv
import os
from flask_cors import CORS
from authlib.integrations.flask_client import OAuth
from dotenv import find_dotenv, load_dotenv
from functools import wraps
import json

app = Flask(__name__)
CORS(app)

# Load environment variables
ENV_FILE = load_dotenv(dotenv_path="Static/auth0/.env")
if ENV_FILE:
    load_dotenv(ENV_FILE)

app.secret_key = os.getenv("APP_SECRET_KEY")

oauth = OAuth(app)

# Register Auth0 with OAuth
oauth.register(
    "auth0",
    client_id=os.getenv("AUTH0_CLIENT_ID"),
    client_secret=os.getenv("AUTH0_CLIENT_SECRET"),
    client_kwargs={
        "scope": "openid profile email",
    },
    server_metadata_url=f'https://{os.getenv("AUTH0_DOMAIN")}/.well-known/openid-configuration'
)

# Helper to ensure user is logged in
def requires_auth(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if "user" not in session:
            return redirect(url_for("login"))
        return f(*args, **kwargs)
    return decorated

@app.route('/')
def index():
    # Pass session directly to the template for flexibility
    return render_template('index.html', session=session)

@app.route('/login')
def login():
    return oauth.auth0.authorize_redirect(redirect_uri=url_for("callback", _external=True))

@app.route('/callback', methods=['GET', 'POST'])
def callback():
    token = oauth.auth0.authorize_access_token()
    # Debugging: Print token to check its structure
    print("Token received:", token)
    
    # Store the token in the session (this includes user info)
    session["user"] = token
    
    return redirect(url_for('maintenance_request'))  # Redirect to maintenance request after login

@app.route('/logout')
def logout():
    session.clear()
    return redirect(f"https://{os.getenv('AUTH0_DOMAIN')}/v2/logout?returnTo={url_for('index', _external=True)}&client_id={os.getenv('AUTH0_CLIENT_ID')}")

@app.route('/maintenance-request', methods=['GET', 'POST'])
@requires_auth
def maintenance_request():
    if request.method == 'POST':
        student_id = request.form.get('student_id')
        building = request.form.get('building')
        category = request.form.get('category')
        description = request.form.get('description')

        result = model_reply(student_id, building, category, description)

        csv_file_path = 'maintenance_requests.csv'
        file_exists = os.path.isfile(csv_file_path)

        with open(csv_file_path, mode='a', newline='') as csv_file:
            csv_writer = csv.writer(csv_file)
            if not file_exists:
                csv_writer.writerow(['Student ID', 'Building', 'Category', 'Description'])
            csv_writer.writerow([student_id, building, category, description])

        return redirect(url_for('success'))

    return render_template('maintenance_request.html')

@app.route('/success')
@requires_auth
def success():
    return render_template('success.html')

if __name__ == '__main__':
    app.run(debug=True)