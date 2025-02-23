from flask import Flask, render_template, jsonify, send_file, request, redirect, url_for
from flask import session
from pdf_generator import generate_pdf  # Import PDF generator
import pandas as pd
import os
from datetime import datetime
import random

app = Flask(__name__)

app.secret_key = 'your_secret_key'

# File paths
CSV_FILE = "static/disability_data.csv"
SAVED_CSV_FOLDER = "saved_csvs/updated_df.csv"

# Ensure CSV file and folder exist
if not os.path.exists(SAVED_CSV_FOLDER):
    os.makedirs(SAVED_CSV_FOLDER)

global_df = pd.DataFrame({
    "Disorder": [
        "Autism", "Autism", "Autism", "Autism", "Autism", "Autism",
        "Specific Learning Disabilities", "Specific Learning Disabilities", "Specific Learning Disabilities",
        "Emotional & Behavioral Disorders", "Emotional & Behavioral Disorders", "Emotional & Behavioral Disorders"
    ],
    "Signs": [
        "Sensitivity to change - They may get upset by minor changes or changes to their routine.",
        "Sensitivity to change - They may get upset by minor changes or changes to their routine.",
        "Difficulty initiating social interactions",
        "Sensory hypersensitivity - They may have unusual reactions to how things smell, taste, look, feel, or sound.",
        "Delayed speech or language development",
        "Dyslexia - challenges in understanding and working with language– including phonemic awareness and phonics",
        "Auditory Processing Disorder - challenges hearing small sound differences in words.",
        "Dyscalculia - struggle with key concepts like bigger vs. smaller, doing basic math problems and/or more abstract math, spacial relations.",
        "Dysgraphia - challenge with handwriting, which can interfere with learning to spell words in writing and speed of writing text",
        "Anxiety - Having angry outbursts",
        "Anxiety - Withdrawing and not wanting to do things they used to enjoy",
        "Depression - Difficulty completing assignments"
    ],
    "Suggestions": [
        "Alerting to changes - Inform the student about upcoming changes in routine or activities in advance to prepare them.",
        "Structured environment - Create a predictable classroom routine with visual schedules and clear expectations.",
        "Social skills development - Incorporate structured social interaction activities to support communication and social skills.",
        "Sensory accommodations - Provide fidget toys, noise-cancelling headphones, or designated quiet spaces to manage sensory overload.",
        "Use pictures, symbols, and visual cues to support communication and understanding.",
        "Repeat directions in multiple ways and use step-by-step instructions.",
        "Combine verbal and visual instruction with participatory activities.",
        "Incorporate different senses like touch, sight, and hearing to reinforce learning.",
        "Use paper with raised or different-colored lines to help form letters and use graph paper to help line up math problems.",
        "Check-in with students regularly to assess their emotional state.",
        "Help students break down large tasks into smaller, manageable steps.",
        "Speak to teachers about potential accommodations like extra time on assignments or reduced workload."
    ]
})

#global vars
inputdata = {
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
    global global_df

    #df = pd.read_csv(SAVED_CSV_FOLDER)
    #df = pd.read_csv(SAVED_CSV_FOLDER, delimiter=",", quotechar='"')
    #df = pd.read_csv(SAVED_CSV_FOLDER, quoting=3)
    print(global_df)

    indx = get_random_index(global_df)

    dis1 = global_df['Disorder'].iloc[indx]
    dis2 = global_df['Disorder'].iloc[indx - 1]
    dis3 = global_df['Disorder'].iloc[indx + 1]

    sin1 = global_df['Signs'].iloc[indx]
    sin2 = global_df['Signs'].iloc[indx - 1]
    sin3 = global_df['Signs'].iloc[indx + 1]

    sug1 = global_df['Suggestions'].iloc[indx]
    sug2 = global_df['Suggestions'].iloc[indx - 1]
    sug3 = global_df['Suggestions'].iloc[indx + 1]

    print(dis1)


#Render the templates

@app.route('/', methods=['GET', 'POST'])
def index():
    #if request.method == 'POST':
        
    if request.method == 'GET':
        return render_template('index.html')


@app.route('/grade.html', methods=['GET', 'POST'])
def grade():
    global inputdata

    return render_template('grade.html')


@app.route('/store_lesson_data', methods=['POST'])
def store_lesson_data():
    # Get the data from the request
    data = request.get_json()

    # You can store this data in a database or a session
    inputdata["grade"] = request.form.get('grade')
    inputdata["lessonTopic"] = request.form.get('lesson_topic')
    inputdata["learningObjective"] = request.form.get('lesson_objective')

    # Return a success message
    return jsonify({'message': 'Lesson data stored successfully!'})




    #return jsonify({"message": "Lesson details updated successfully!", "inputdata": inputdata})

@app.route('/lessonOutOne.html', methods=['GET', 'POST'])
def render1():
    global lessout1  # Allow modification of global variable

    if request.method == 'POST':  # If the user submits the lesson plan
        lessout1 = request.form.get("lessonPlan", "")  # Save it dynamically

    select_suggestion()  # Ensure this runs before rendering
    return render_template(
        'lessonOutOne.html',
        dis1_var=dis1 or "N/A",
        dis2_var=dis2 or "N/A",
        dis3_var=dis3 or "N/A",
        sin1_var=sin1 or "N/A",
        sin2_var=sin2 or "N/A",
        sin3_var=sin3 or "N/A",
        sug1_var=sug1 or "N/A",
        sug2_var=sug2 or "N/A",
        sug3_var=sug3 or "N/A"
    )

@app.route('/lessonOutTwo.html', methods=['GET', 'POST'])
def render2():
    global lessout2  # Allow modification of global variable

    if request.method == 'POST':  # If the user submits the lesson plan
        lessout2 = request.form.get("lessonPlan", "")  # Save it dynamically

    select_suggestion()  # Ensure this runs before rendering
    return render_template(
        'lessonOutTwo.html',
        dis1_var=dis1 or "N/A",
        dis2_var=dis2 or "N/A",
        dis3_var=dis3 or "N/A",
        sin1_var=sin1 or "N/A",
        sin2_var=sin2 or "N/A",
        sin3_var=sin3 or "N/A",
        sug1_var=sug1 or "N/A",
        sug2_var=sug2 or "N/A",
        sug3_var=sug3 or "N/A"
    )

@app.route('/lessonOutThree.html', methods=['GET', 'POST'])
def render3():
    global lessout3  # Allow modification of global variable
    if request.method == 'POST':  # If the user submits the lesson plan
        lessout3 = request.form.get("lessonPlan", "")  # Save it dynamically
    
    select_suggestion()  # Ensure this runs before rendering
    return render_template(
        'lessonOutThree.html',
        dis1_var=dis1 or "N/A",
        dis2_var=dis2 or "N/A",
        dis3_var=dis3 or "N/A",
        sin1_var=sin1 or "N/A",
        sin2_var=sin2 or "N/A",
        sin3_var=sin3 or "N/A",
        sug1_var=sug1 or "N/A",
        sug2_var=sug2 or "N/A",
        sug3_var=sug3 or "N/A"
    )

@app.route('/finaldisplay.html', methods=['GET', 'POST'])
def renderpdf():
    #return render_template('sim.html', w_var = water, t_var = temp, v_var = int(vege), d_var = int(decomp), h_var = int(herb), c_var = int(carn), year_var = year, grid = biomegrid, imageList=crucialList)
    return render_template('finaldisplay.html')



#OLD CODE

@app.route('/submit', methods=['POST'])
def submit():
    
    # Generate PDF
    pdf_filename = generate_pdf(inputdata, lessout1, lessout2, lessout3)

    return jsonify({"message": "Form submitted successfully!"})


@app.route('/download-pdf')
def download_pdf():
    """Serves the generated PDF for download"""
    pdf_path = "generated_pdfs/Lesson_Plan.pdf"
    return send_file(pdf_path, as_attachment=True)

if __name__ == '__main__':
    app.run(debug=True)
