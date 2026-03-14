from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
import os
from PIL import Image, ImageDraw

def create_sample_image(filename, text, color):
    img = Image.new('RGB', (400, 300), color=(200, 200, 200))
    d = ImageDraw.Draw(img)
    d.text((10, 10), text, fill=color)
    d.rectangle([50, 50, 350, 250], outline=color, width=5)
    img.save(filename)

def create_inspection_report(filename):
    c = canvas.Canvas(filename, pagesize=letter)
    c.setFont("Helvetica-Bold", 24)
    c.drawString(50, 750, "Visual Inspection Report - 101 Factory Lane")
    
    c.setFont("Helvetica", 14)
    c.drawString(50, 700, "Date: March 14, 2026")
    c.drawString(50, 680, "Inspector: Jane Doe")
    
    c.setFont("Helvetica-Bold", 16)
    c.drawString(50, 640, "1. Roof Area Observations")
    c.setFont("Helvetica", 12)
    c.drawString(50, 620, "- Significant water pooling observed near the HVAC unit on the East Wing.")
    c.drawString(50, 605, "- Minimal debris, but membrane looks slightly cracked under the pooling water.")
    
    c.setFont("Helvetica-Bold", 16)
    c.drawString(50, 550, "2. Interior Ceiling (Below East Wing)")
    c.setFont("Helvetica", 12)
    c.drawString(50, 530, "- Faint brown watermark visible on the drop ceiling tiles.")
    c.drawString(50, 515, "- No active dripping at the time of inspection.")

    # Create dummy images and embed them
    create_sample_image("roof_pooling.jpg", "Roof Water Pooling", (0, 0, 255))
    create_sample_image("ceiling_stain.jpg", "Ceiling Stain", (139, 69, 19))
    
    c.drawImage("roof_pooling.jpg", 50, 300, width=250, height=200)
    c.drawString(50, 280, "Figure 1: Water pooling on East Wing Roof")
    
    c.showPage()
    
    c.drawImage("ceiling_stain.jpg", 50, 500, width=250, height=200)
    c.drawString(50, 480, "Figure 2: Interior ceiling stain directly below pooling")

    c.save()
    os.remove("roof_pooling.jpg")
    os.remove("ceiling_stain.jpg")

def create_thermal_report(filename):
    c = canvas.Canvas(filename, pagesize=letter)
    c.setFont("Helvetica-Bold", 24)
    c.drawString(50, 750, "Thermal Analysis Report - 101 Factory Lane")
    
    c.setFont("Helvetica", 14)
    c.drawString(50, 700, "Date: March 14, 2026")
    c.drawString(50, 680, "Technician: John Smith")
    
    c.setFont("Helvetica-Bold", 16)
    c.drawString(50, 640, "1. East Wing Roof Scan")
    c.setFont("Helvetica", 12)
    c.drawString(50, 620, "- Large thermal anomaly detected around the HVAC unit.")
    c.drawString(50, 605, "- Delta T (Temperature difference) of -3.2°C compared to dry areas.")
    c.drawString(50, 590, "- Indicates severe sub-surface moisture accumulation within the insulation layer.")
    
    c.setFont("Helvetica-Bold", 16)
    c.drawString(50, 550, "2. Interior Wall Scan (Server Room)")
    c.setFont("Helvetica", 12)
    c.drawString(50, 530, "- Slight thermal bridging spotted at the corner junctions.")
    c.drawString(50, 515, "- Not related to the roof leak, just missing insulation batting.")

    create_sample_image("thermal_roof.jpg", "Thermal Anomaly Roof", (255, 0, 0))
    c.drawImage("thermal_roof.jpg", 50, 300, width=250, height=200)
    c.drawString(50, 280, "Figure 1: FLIR imagery showing -3.2°C anomaly zone")
    
    c.save()
    os.remove("thermal_roof.jpg")

if __name__ == "__main__":
    create_inspection_report("Sample_Inspection_Report.pdf")
    create_thermal_report("Sample_Thermal_Report.pdf")
    print("Sample reports created successfully.")
