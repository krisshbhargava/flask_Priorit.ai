from flask import Flask, render_template, request, redirect, url_for, jsonify, session
import csv
import os
from flask_cors import CORS
from authlib.integrations.flask_client import OAuth
from dotenv import find_dotenv, load_dotenv
from functools import wraps
import json
from Models.test_models import model_reply
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import sessionmaker, declarative_base

app = Flask(__name__)
CORS(app)

db_config = {
    'host' : '127.0.0.1',
    'user' : 'root',
    'password' : 'sqlMeHackGT@0924',
    'database' : 'test_schema'
}

DATABASE_URI = 'mysql+mysqlconnector://root:sqlMeHackGT0924@localhost/test_schema'

engine = create_engine(DATABASE_URI)
Base = declarative_base()

class MaintenanceRequestA(Base):
    __tablename__ = 'general_information'
    issue_id = Column(Integer, primary_key = True, autoincrement = True)
    student_id = Column(Integer)
    building_type = Column(String)
    department = Column(String)
    issue_type = Column(String)
    certainty = Column(Integer)

class MaintenanceRequestB(Base):
    __tablename__ = 'manual_check'
    issue_id = Column(Integer, primary_key = True, autoincrement = True)
    student_id = Column(Integer)
    building_type = Column(String)
    department = Column(String)
    description = Column(String)

class MaintenanceRequestC(Base):
    __tablename__ = 'kitchen_bath_priority'
    issue_id = Column(Integer, primary_key = True, autoincrement = True)
    student_id = Column(Integer)
    building_type = Column(String)
    issue_type = Column(String)
    priority = Column(Integer)

class MaintenanceRequestD(Base):
    __tablename__ = 'light_electrical_priority'
    issue_id = Column(Integer, primary_key = True, autoincrement = True)
    student_id = Column(Integer)
    building_type = Column(String)
    issue_type = Column(String)
    priority = Column(Integer)

class MaintenanceRequestE(Base):
    __tablename__ = 'general_maintenance'
    issue_id = Column(Integer, primary_key = True, autoincrement = True)
    student_id = Column(Integer)
    building_type = Column(String)
    issue_type = Column(String)
    priority = Column(Integer)

Session = sessionmaker(bind=engine)

priorities = {"0":["HVAC Problems", "Leaky Faucet", "Wall Damage"], "1":["Mold", "Broken Shower Head", "Request for Bed Lofting"], "2":["Fire Alarm", "Flooding Toilet", "Lock and Key"]}

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

def findPriority(msg):
    for i in range(len(priorities)):
        if msg in priorities.get(str(i)):
            # print(priorities.get(str(i)))
            return str(i)
        


@app.route('/maintenance-request', methods=['GET', 'POST'])

@requires_auth
def maintenance_request():
    if request.method == 'POST':
        student_id = request.form.get('student_id')
        building = request.form.get('building')
        category = request.form.get('category')
        description = request.form.get('description')

        result = model_reply(student_id, building, category, description)

        session = Session()

        if int(result[4]) == 1:
            new_request = MaintenanceRequestA(
                student_id = int(result[0]),
                building_type = str(result[1]),
                department = str(result[2]),
                issue_type = str(result[3]),
                certainty = int(result[4])
            )
            session.add(new_request)
            session.commit()

            if str(result[2]) == "kitchenDF":
                print(new_request.issue_id)
                new_request2 = MaintenanceRequestC(
                    issue_id = new_request.issue_id,
                    student_id = new_request.student_id,
                    building_type = new_request.building_type,
                    issue_type = new_request.issue_type,
                    priority = int(findPriority(new_request.issue_type)) + 1
                )
                session.add(new_request2)
            elif str(result[2]) == "electricalDF":
                new_request2 = MaintenanceRequestD(
                    issue_id = new_request.issue_id,
                    student_id = new_request.student_id,
                    building_type = new_request.building_type,
                    issue_type = new_request.issue_type,
                    priority = int(findPriority(new_request.issue_type)) + 1
                )
                session.add(new_request2)
            elif str(result[2]) == "roomDF":
                new_request2 = MaintenanceRequestE(
                    issue_id = new_request.issue_id,
                    student_id = new_request.student_id,
                    building_type = new_request.building_type,
                    issue_type = new_request.issue_type,
                    priority = int(findPriority(new_request.issue_type)) + 1
                )
                session.add(new_request2)
            
            

        elif int(result[4]) == 0:
            new_request = MaintenanceRequestB(
                student_id = int(result[0]),
                building_type = str(result[1]),
                department = str(result[2]),
                description = str(result[5])
            )
            session.add(new_request)
        
        elif int(result[4]) == -1:
            return render_template('maintenance_request.html')


        session.commit()
        session.close()

        return redirect(url_for('success'))

    return render_template('maintenance_request.html')

@app.route('/success')
@requires_auth
def success():
    return render_template('success.html')

@app.route('/admin')
@requires_auth
def admin():
    # Restrict access to a specific email address (krissh.bhargava@gmail.com)
    user_email = session['user']['userinfo']['email']

    if user_email != 'krissh.bhargava@gmail.com':
        return "Unauthorized Access", 403  # HTTP 403 Forbidden

    # Read maintenance requests from the CSV file
    csv_file_path = 'maintenance_requests.csv'
    maintenance_requests = []

    if os.path.exists(csv_file_path):
        with open(csv_file_path, mode='r') as csv_file:
            csv_reader = csv.DictReader(csv_file)
            for row in csv_reader:
                maintenance_requests.append(row)

    return render_template('admin.html', maintenance_requests=maintenance_requests)

if __name__ == '__main__':
    Base.metadata.create_all(engine)
    app.run(debug=True)