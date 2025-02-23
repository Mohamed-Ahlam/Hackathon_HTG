import os  # Ensure 'os' module is imported
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from datetime import datetime

def generate_pdf(inputdata, lessout1, lessout2, lessout3):
    """Creates a PDF lesson plan based on inputdata dictionary"""

    # Ensure output directory exists
    output_dir = "generated_pdfs"
    os.makedirs(output_dir, exist_ok=True)

    pdf_filename = os.path.join(output_dir, "Lesson_Plan.pdf")

    c = canvas.Canvas(pdf_filename, pagesize=letter)
    width, height = letter

    # Set font
    c.setFont("Times-Roman", 12)

    # Title
    c.setFont("Times-Bold", 16)
    title = f"{datetime.today().strftime('%Y-%m-%d')} - Lesson Plan"
    c.drawCentredString(width / 2, height - 50, title)

    # Subtitle
    c.setFont("Times-Bold", 14)
    lesson_topic = inputdata.get("lessonTopic", "Lesson Topic Not Provided")
    grade_level = inputdata.get("grade", "Grade Not Provided")
    subtitle = f"{lesson_topic} - {grade_level}"
    c.drawCentredString(width / 2, height - 80, subtitle)

    # Content
    c.setFont("Times-Bold", 12)
    c.drawString(50, height - 120, "Learning Objectives:")
    learning_objective = inputdata.get("learningObjective", "Learning Objective Not Provided")
    c.setFont("Times-Roman", 12)
    c.drawString(70, height - 140, learning_objective)

    c.setFont("Times-Bold", 12)
    c.drawString(50, height - 170, "Lesson Outline:")
    c.setFont("Times-Roman", 12)
    c.drawString(70, height - 190, f"- Opening Activity: {lessout1}")
    c.drawString(70, height - 210, f"- Lesson Sequence: {lessout2}")
    c.drawString(70, height - 230, f"- Lesson Summary: {lessout3}")

    c.setFont("Times-Bold", 12)
    c.drawString(50, height - 260, "Formative Assessment:")
    c.setFont("Times-Roman", 12)
    c.drawString(70, height - 280, "Assessment details here...")

    c.setFont("Times-Bold", 12)
    c.drawString(50, height - 310, "Materials:")
    c.setFont("Times-Roman", 12)
    c.drawString(70, height - 330, "List of materials here...")

    # Disabilities section
    c.setFont("Times-Bold", 12)
    c.drawString(50, height - 360, "Disabilities & Student Difficulties:")
    c.setFont("Times-Roman", 12)
    disabilities = inputdata.get("disabilities", ["No disabilities listed"])
    c.drawString(70, height - 380, ", ".join(disabilities))  # Joining disabilities if more than one

    # Save PDF
    c.showPage()
    c.save()

    return pdf_filename
