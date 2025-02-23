from flask import Flask, render_template, request, jsonify, send_file
from pdf_generator import generate_pdf  # Import PDF generator
import pandas as pd
import os
from datetime import datetime
import random

app = Flask(__name__)

# File paths
CSV_FILE = "static/disability_data.csv"
SAVED_CSV_FOLDER = "saved_csvs/updated_df.csv"

# Ensure CSV file and folder exist
if not os.path.exists(SAVED_CSV_FOLDER):
    os.makedirs(SAVED_CSV_FOLDER)

#global vars
inputdata = {
    "file": "empty",
    "disabilities": [],
    "assistance": [],
    "grade": "empty",
    "lessonTopic": "empty",
    "learningObjective": "empty"
}

dis1 = ""
dis2 = ""
dis3 = ""

sin1 = ""
sin2 = ""
sin3 = ""

sug1 = ""
sug2 = ""
sug3 = ""

lessout1 = ""
lessout2 = ""
lessout3 = ""


#base functions
def filtercsv():
    """Filters the CSV based on selected disabilities"""
    dis = inputdata.get("disabilities")  # Get selected disabilities

    # Reload the CSV to get updated data
    df = pd.read_csv(CSV_FILE)

    #debugging
    print(df)

    # Filter CSV where the first column matches any selected disability
    #filtered_df = df[df["Disabilities"].str.contains('|'.join(disabilities), na=False)]
    filtered_df = df[df['Disorder'].str.contains(dis)]

    #may need to go back and fix
    # Save csv
    filtered_df.to_csv(SAVED_CSV_FOLDER, index=False)
    return send_file(SAVED_CSV_FOLDER, as_attachment=True)

def get_random_index(df):
 #Returns a random integer between 0 (inclusive) and the number of rows in the DataFrame (exclusive).
  return random.randint(1, len(df) - 2)

def select_suggestion():
    global dis1, dis2, dis3, sin1, sin2, sin3, sug1, sug2, sug3  # Add this line

    #df = pd.read_csv(SAVED_CSV_FOLDER)
    df = pd.read_csv(SAVED_CSV_FOLDER, delimiter=",", quotechar='"')
    df = pd.read_csv(SAVED_CSV_FOLDER, quoting=3)
    print(df)

    indx = get_random_index(df)

    dis1 = df['Disorder'].iloc[indx]
    dis2 = df['Disorder'].iloc[indx - 1]
    dis3 = df['Disorder'].iloc[indx + 1]

    sin1 = df['Signs'].iloc[indx]
    sin2 = df['Signs'].iloc[indx - 1]
    sin3 = df['Signs'].iloc[indx + 1]

    sug1 = df['suggestions'].iloc[indx]
    sug2 = df['suggestions'].iloc[indx - 1]
    sug3 = df['suggestions'].iloc[indx + 1]

    print(dis1)


#Render the templates

@app.route('/', methods=['GET', 'POST'])
def index():
    #if request.method == 'POST':
        
    if request.method == 'GET':
        return render_template('index.html')

@app.route('/lessonOutOne.html', methods=['GET', 'POST'])
def render1():
    global lessout1
    if request.method == 'POST':
        select_suggestion() 
        lessout1 = request.form.getlist('lessonPlan')
        
    if request.method == 'GET':
        #plan is to randomly pick 3 suggestions out of the filtered rows, send back to the html file
        return render_template('lessonOutOne.html', dis1_var = dis1, dis2_var = dis2, dis3_var = dis3, sin1_var = sin1, sin2_var = sin2, sin3_var = sin3, sug1_var = sug1, sug2_var = sug2, sug3_var = sug3)
        #return render_template('lessonOutOne.html')

@app.route('/lessonOutTwo.html', methods=['GET', 'POST'])
def render2():
    #return render_template('sim.html', w_var = water, t_var = temp, v_var = int(vege), d_var = int(decomp), h_var = int(herb), c_var = int(carn), year_var = year, grid = biomegrid, imageList=crucialList)
    return render_template('lessonOutTwo.html')

@app.route('/lessonOutThree.html', methods=['GET', 'POST'])
def render3():
    #return render_template('sim.html', w_var = water, t_var = temp, v_var = int(vege), d_var = int(decomp), h_var = int(herb), c_var = int(carn), year_var = year, grid = biomegrid, imageList=crucialList)
    return render_template('lessonOutThree.html')

@app.route('/finaldisplay.html', methods=['GET', 'POST'])
def renderpdf():
    #return render_template('sim.html', w_var = water, t_var = temp, v_var = int(vege), d_var = int(decomp), h_var = int(herb), c_var = int(carn), year_var = year, grid = biomegrid, imageList=crucialList)
    return render_template('finaldisplay.html')



#OLD CODE

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


@app.route('/download-pdf')
def download_pdf():
    """Serves the generated PDF for download"""
    pdf_path = "generated_pdfs/Lesson_Plan.pdf"
    return send_file(pdf_path, as_attachment=True)

if __name__ == '__main__':
    app.run(debug=True)
