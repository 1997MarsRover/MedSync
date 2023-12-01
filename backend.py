from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from flask_sqlalchemy import SQLAlchemy
import random
import string




app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///medsync.db'
app.config['SECRET_KEY'] = '1111'  # Change this to a random secret key
db = SQLAlchemy(app)



# Define models
class Patient(db.Model):
    id = db.Column(db.String(10), primary_key=True)
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    identification_number = db.Column(db.String(20), unique=True, nullable=False)
    phone_number = db.Column(db.String(15))
    date_of_birth = db.Column(db.String(10))
    region = db.Column(db.String(50))
    city = db.Column(db.String(50))
    diagnostics = db.relationship('Diagnostics', backref='patient', lazy=True)

    def __init__(self, first_name, last_name, identification_number, phone_number, date_of_birth, region, city):
        self.id = self.generate_unique_id()
        self.first_name = first_name
        self.last_name = last_name
        self.identification_number = identification_number
        self.phone_number = phone_number
        self.date_of_birth = date_of_birth
        self.region = region
        self.city = city

    def generate_unique_id(self):
        # Generate a unique ID (for demonstration purposes)
        return ''.join(random.choices(string.ascii_uppercase + string.digits, k=8))

# Create the database tables
with app.app_context():
    db.create_all()

# Routes
@app.route('/')
def index():
    return render_template('landing_page.html')

from flask import request

@app.route('/medical_practitioner', methods=['GET', 'POST'])
def medical_practitioner():
    if request.method == 'POST':
        # Handle login logic here
        license = request.form.get('license')
        password = request.form.get('password')
        consent = request.form.get('consent')

        # Implement your authentication logic here (e.g., check against database)
        # For now, let's just print the values
        print(f"License: {license}, Password: {password}, Consent: {consent}")

        flash('Login logic goes here', 'info')
        # Redirect to the patient_home route upon successful login
        return redirect(url_for('patient_home', username='PatientName'))
    return render_template('medical_practitioner.html')

# Health Administrator Login Route
@app.route('/health_administrator_login', methods=['POST'])
def health_administrator_login():
    if request.method == 'POST':
        # Handle Health Administrator login logic here
        admin_username = request.form.get('admin_username')
        admin_password = request.form.get('admin_password')

        # Implement your authentication logic here (e.g., check against a dictionary)
        # For now, let's just print the values
        print(f"Admin Username: {admin_username}, Admin Password: {admin_password}")

        # Redirect to the health_administrator_home route upon successful login
        return redirect(url_for('health_administrator_home'))

    # Redirect back to the landing page if not a POST request
    return redirect(url_for('landing_page'))

# Replace 'your_api_endpoint' with the actual endpoint you want
@app.route('/api/region', methods=['GET', 'POST'])
def get_region_data():
    if request.method == 'POST':
        region_name = request.form.get('region')
        # Replace this with your actual data retrieval logic based on the selected region
        region_data = get_region_data_by_name(region_name)
        return jsonify(region_data)
    else:
        return render_template('health_administrator_home.html')

def get_region_data_by_name(region_name):
    # Replace this with your actual data retrieval logic based on the selected region
    # This function should return the region data in a structured format
    region_data = {
        'region_name': region_name,
        'population': 4397073,  # As of 2022
        'num_hospitals': 67,
        'medical_resources': 'High',
        'top_ailment': 'Respiratory Infections',
        'average_age': 28,
        'majority_gender': 'Female',
        'available_beds': 3200,
        'specialized_facilities': 'Cardiology, Oncology',
        'health_insurance_coverage': '75%',
        'common_health_risks': 'Malaria, Diabetes'
    }
    return region_data


@app.route('/health_administrator_home')
def health_administrator_home():
    # Render the Health Administrator Home page
    return render_template('health_administrator_home.html')

@app.route('/admin_home')
def admin_home():
    # Add logic for the admin home page
    return render_template('admin_home.html')


@app.route('/handle_patient_unid', methods=['GET', 'POST'])
def handle_patient_unid():
    if request.method == 'POST':
        patient_unid = request.form.get('patient_unid')
        # Add logic to handle patient UNid (e.g., retrieve patient details from the database)
        print(f"Patient's UNid: {patient_unid}")
        return redirect(url_for('patient_home', username='PatientName'))  # Redirect to patient home with a placeholder name
    return redirect(url_for('medical_practitioner')) 

@app.route('/patient_home/<username>')
def patient_home(username):
    # Fetch Diagnostics data for the patient
    patient = Patient.query.filter_by(id=username).first()
    diagnostics_data = patient.diagnostics if patient else []

    return render_template('patient_home.html', username=username, diagnostics_data=diagnostics_data)

@app.route('/add_new_patient', methods=['POST'])
def add_new_patient():
    if request.method == 'POST':
        # Handle new patient registration logic here
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        identification_number = request.form['identification_number']
        phone_number = request.form['phone_number']
        date_of_birth = request.form['date_of_birth']
        region = request.form['region']
        city = request.form['city']

        new_patient = Patient(
            first_name=first_name,
            last_name=last_name,
            identification_number=identification_number,
            phone_number=phone_number,
            date_of_birth=date_of_birth,
            region=region,
            city=city
        )

        db.session.add(new_patient)
        db.session.commit()

        flash('New Registration Confirmed. Unique Identifier: {}'.format(new_patient.id), 'success')

    return redirect(url_for('medical_practitioner'))


class Diagnostics(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date_of_diagnostic = db.Column(db.Date)
    ailment_diagnosed = db.Column(db.String)
    results = db.Column(db.String)
    facility = db.Column(db.String)
    type_of_diagnosis = db.Column(db.String)
    patient_id = db.Column(db.String(10), db.ForeignKey('patient.id'), nullable=False)




