from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from datetime import datetime
import os

def generate_pdf(form_data, lessout1, lessout2, lessout3):
    """ Creates a PDF lesson plan based on form data """
    
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
    subtitle = f"{form_data['Lesson Topic']} - {form_data['Grade Level']}"
    c.drawCentredString(width / 2, height - 80, subtitle)

    

    # Content
    c.setFont("Times-Bold", 12)
    c.drawString(50, height - 120, "Learning Objectives:")
    c.setFont("Times-Roman", 12)
    c.drawString(70, height - 140, form_data["Learning Objective"])

    c.setFont("Times-Bold", 12)
    c.drawString(50, height - 170, "Lesson Outline:")
    c.setFont("Times-Roman", 12)
    c.drawString(70, height - 190, "- Opening Activity")
    c.drawString(70, height - 210, "- Lesson Sequence")
    c.drawString(70, height - 230, "- Lesson Summary")

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
    c.drawString(70, height - 380, form_data["Disabilities"])

    # Save PDF
    c.showPage()
    c.save()

    return pdf_filename
