from flask import Flask, render_template, request, redirect
import mysql.connector
from datetime import datetime
import os

app = Flask(__name__)

# MySQL database connection
db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="Univers!ty23",
    database="hospital"
)

@app.route('/')
def index():
    return render_template('index.html', show_title=True)


@app.route('/patients')
def get_patients():
    cursor = db.cursor()
    cursor.execute("SELECT * FROM patients")
    patients = cursor.fetchall()
    cursor.close()
    return render_template('patients.html', patients=patients)

@app.route('/patients/add', methods=['GET', 'POST'])
def add_patient():
    if request.method == 'POST':
        # Retrieve form data
        first_name = request.form.get('first_name')
        last_name = request.form.get('last_name')
        date_of_birth = request.form.get('date_of_birth')
        gender = request.form.get('gender')
        address = request.form.get('address')
        phone_number = request.form.get('phone_number')
        email = request.form.get('email')
        condition = request.form.get('condition')
        prescription = request.form.get('prescription')

        cursor = db.cursor()
        query = "INSERT INTO patients (first_name, last_name, date_of_birth, gender, address, phone_number, email, `condition`, prescription) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)"
        values = (first_name, last_name, date_of_birth, gender, address, phone_number, email, condition, prescription)

        cursor.execute(query, values)
        db.commit()
        cursor.close()

        return redirect('/patients')  # Redirect to the patients' list page
    else:
        return render_template('add_patient.html')




@app.route('/patients/delete/<int:patient_id>', methods=['DELETE'])
def delete_patient(patient_id):
    if request.method == 'DELETE':
        cursor = db.cursor()
        query = "DELETE FROM patients WHERE id = %s"
        value = (patient_id,)
        cursor.execute(query, value)
        db.commit()
        cursor.close()
        return "Patient deleted successfully"
    else:
        return "Method not allowed"

@app.route('/patients/<int:patient_id>')
def patient_info(patient_id):
    cursor = db.cursor()
    query = "SELECT * FROM patients WHERE id = %s"
    value = (patient_id,)
    cursor.execute(query, value)
    patient = cursor.fetchone()
    cursor.close()

    return render_template('patient_info.html', patient=patient)







if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 5000))
    host = '0.0.0.0'
    
    # Use Gunicorn to run the app
    cmd = f"gunicorn --bind={host}:{PORT} --threads=4 app.py:startapp()"
    os.system(cmd)

