from flask import Flask, render_template, request, jsonify, send_file
from pdf_generator import generate_pdf  # Import PDF generator
import pandas as pd
import os
from datetime import datetime

app = Flask(__name__)

# File paths
CSV_FILE = "static/disability_data.csv"
SAVED_CSV_FOLDER = "saved_csvs"

# Ensure CSV file and folder exist
if not os.path.exists(SAVED_CSV_FOLDER):
    os.makedirs(SAVED_CSV_FOLDER)

if not os.path.exists(CSV_FILE):
    pd.DataFrame(columns=["File", "Disabilities", "Assistance", "Grade Level", "Lesson Topic", "Learning Objective"]).to_csv(CSV_FILE, index=False)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/submit', methods=['POST'])
def submit():
    """Handles form submission and appends data to CSV"""
    # Get form data
    file = request.files.get('ieps')
    file_name = file.filename if file else "No file uploaded"

    disabilities = request.form.getlist('disabilities')  # Multiple selections
    grade = request.form.get('grade')
    lesson_topic = request.form.get('lesson-topic')
    learning_objective = request.form.get('learning-objective')
    assistance = request.form.getlist('assistance')

    # Store form data in a dictionary
    form_data = {
        "File": file_name,
        "Disabilities": ", ".join(disabilities) if disabilities else "None",
        "Assistance": ", ".join(assistance) if assistance else "None",
        "Grade Level": grade,
        "Lesson Topic": lesson_topic,
        "Learning Objective": learning_objective
    }


    # Generate PDF
    pdf_filename = generate_pdf(form_data)

    return jsonify({"message": "Form submitted successfully!", "pdf": pdf_filename, "csv": saved_csv_path})

@app.route('/generate', methods=['POST'])
def filter_suggestions():
    """Filters the CSV based on selected disabilities"""
    disabilities = request.form.getlist('disabilities')  # Get selected disabilities

    # Reload the CSV to get updated data
    df = pd.read_csv(CSV_FILE)

    # Filter CSV where the first column matches any selected disability
    filtered_df = df[df["Disabilities"].str.contains('|'.join(disabilities), na=False)]


    # Append new data to the original CSV
    #new_data = pd.DataFrame([form_data])
    #filtered_df.to_csv(CSV_FILE, mode='a', header=False, index=False)


    # Save filtered data with a timestamp
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filtered_csv_path = os.path.join(SAVED_CSV_FOLDER, f"filtered_results_{timestamp}.csv")
    filtered_df.to_csv(filtered_csv_path, index=False)

    return send_file(filtered_csv_path, as_attachment=True)

@app.route('/download-pdf')
def download_pdf():
    """Serves the generated PDF for download"""
    pdf_path = "generated_pdfs/Lesson_Plan.pdf"
    return send_file(pdf_path, as_attachment=True)

if __name__ == '__main__':
    app.run(debug=True)
