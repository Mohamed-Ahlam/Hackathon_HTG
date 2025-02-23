from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib import colors
import os
from datetime import datetime

# Ensure the "generated_pdfs" directory exists
if not os.path.exists("generated_pdfs"):
    os.makedirs("generated_pdfs")

def generate_pdf(data):
    """Generates a PDF lesson plan based on form data"""
    pdf_path = "generated_pdfs/Lesson_Plan.pdf"

    c = canvas.Canvas(pdf_path, pagesize=letter)
    width, height = letter

    # Add a border line around the page
    c.setStrokeColor(colors.black)
    c.setLineWidth(1)
    c.rect(30, 30, width - 60, height - 60)  # Border around the page with padding

    # Add current date
    current_date = datetime.now().strftime("%B %d, %Y")  # Format: "March 22, 2025"

    # Header 1: Title (Centered)
    c.setFont("Times-Roman", 16)
    title = f"{current_date} - Lesson Plan"
    title_width = c.stringWidth(title, "Times-Roman", 16)
    c.drawString((width - title_width) / 2, height - 100, title)

    # Header 2: Lesson Topic + Grade Level (Centered)
    c.setFont("Times-Roman", 12)
    lesson_header = f"{data['Lesson Topic']} - {data['Grade Level']}"
    lesson_header_width = c.stringWidth(lesson_header, "Times-Roman", 12)
    c.drawString((width - lesson_header_width) / 2, height - 140, lesson_header)

    # Space between sections
    y_position = height - 180

    # Bolded: Learning Objectives
    c.setFont("Times-Bold", 12)
    c.drawString(100, y_position, "Learning Objectives:")
    y_position -= 20
    c.setFont("Times-Roman", 12)
    c.drawString(100, y_position, data["Learning Objective"])
    y_position -= 40

    # Bolded: Lesson Outline
    c.setFont("Times-Bold", 12)
    c.drawString(100, y_position, "Lesson Outline:")
    y_position -= 20

    # List of lesson outline
    c.setFont("Times-Roman", 12)
    c.drawString(120, y_position, "- Opening Activity")
    y_position -= 20
    c.drawString(120, y_position, "- Lesson Sequence")
    y_position -= 20
    c.drawString(120, y_position, "- Lesson Summary")
    y_position -= 40

    # Formative Assessment Section
    c.setFont("Times-Bold", 12)
    c.drawString(100, y_position, "Formative Assessment:")
    y_position -= 20
    c.setFont("Times-Roman", 12)
    c.drawString(100, y_position, "Assessing student understanding throughout the lesson.")
    y_position -= 40

    # Materials Section
    c.setFont("Times-Bold", 12)
    c.drawString(100, y_position, "Materials:")
    y_position -= 20
    c.setFont("Times-Roman", 12)
    c.drawString(100, y_position, "Textbooks, project materials, whiteboard, etc.")
    y_position -= 40

    # List of Disabilities and Student Difficulties at the bottom
    disabilities_y_position = 60  # Set the Y position for the disabilities list near the bottom

    c.setFont("Times-Bold", 12)
    c.drawString(100, disabilities_y_position, "Disabilities and Student Difficulties:")
    disabilities = data["Disability"]
    student_difficulties = data["Assistance"]

    # List disabilities and difficulties at the bottom
    c.setFont("Times-Roman", 12)
    c.drawString(120, disabilities_y_position - 20, disabilities)
    c.drawString(120, disabilities_y_position - 40, student_difficulties)

    # Save the PDF
    c.save()
    return pdf_path
