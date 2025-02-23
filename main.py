from flask import Flask, render_template, request, jsonify, send_file
from pdf_generator import generate_pdf  # Import PDF generator

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/submit', methods=['POST'])
def submit():
    # Get form data
    file = request.files.get('ieps')
    file_name = file.filename if file else "No file uploaded"

    disability = request.form.get('disabilities')
    grade = request.form.get('grade')
    lesson_topic = request.form.get('lesson-topic')
    learning_objective = request.form.get('learning-objective')
    assistance = request.form.getlist('assistance')

    # Store form data in a dictionary
    form_data = {
        "File": file_name,
        "Disability": disability,
        "Assistance": ", ".join(assistance) if assistance else "None",
        "Grade Level": grade,
        "Lesson Topic": lesson_topic,
        "Learning Objective": learning_objective
    }

    # Generate PDF
    pdf_filename = generate_pdf(form_data)

    return jsonify({"message": "Form submitted successfully!", "pdf": pdf_filename})

@app.route('/download-pdf')
def download_pdf():
    """ Serves the generated PDF for download """
    pdf_path = "generated_pdfs/Lesson_Plan.pdf"
    return send_file(pdf_path, as_attachment=True)

if __name__ == '__main__':
    app.run(debug=True)
