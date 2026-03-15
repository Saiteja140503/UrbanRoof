from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch

def create_pdf(text_data, filename="Final_DDR_Report.pdf"):
    doc = SimpleDocTemplate(filename, pagesize=letter)
    styles = getSampleStyleSheet()
    
    # Custom styles
    title_style = styles['Title']
    heading_style = styles['Heading2']
    normal_style = styles['Normal']
    
    normal_style.spaceAfter = 10
    normal_style.leading = 14
    
    story = []
    
    # Simple parsing to roughly format the PDF based on the text structure provided
    lines = text_data.split('\n')
    
    for line in lines:
        line = line.strip()
        if not line:
            continue
            
        if line.startswith("Detailed Diagnosis Report"):
            story.append(Paragraph(line, title_style))
            story.append(Spacer(1, 0.2*inch))
        elif line.startswith("1.") or line.startswith("2.") or line.startswith("3.") or line.startswith("4.") or line.startswith("5.") or line.startswith("6.") or line.startswith("7."):
            story.append(Spacer(1, 0.2*inch))
            story.append(Paragraph("<b>" + line + "</b>", heading_style))
        elif "Visual Observations:" in line or "Thermal Observations:" in line:
            story.append(Spacer(1, 0.1*inch))
            story.append(Paragraph("<b>" + line + "</b>", normal_style))
        elif line.endswith(".jpeg"):
            # Mock image placement
            story.append(Paragraph(f"<i>[Image Reference: {line}]</i>", normal_style))
            story.append(Spacer(1, 0.1*inch))
        else:
            story.append(Paragraph(line, normal_style))
            
    doc.build(story)

report_text = """Detailed Diagnosis Report
1. Property Issue Summary
The property exhibits widespread moisture-related issues, including dampness and efflorescence on interior walls across multiple rooms (Hall, Common Bedroom, Master Bedroom, Kitchen) of Flat No. 103. Significant tile hollowness, gaps in tile joints, and loose plumbing connections are prevalent in both the Common and Master Bedroom bathrooms of Flat No. 103, and similar issues are noted in Flat No. 203's bathrooms. External factors such as moderate cracks on the building's exterior walls and leaking external plumbing pipes, along with duct issues, are contributing to the internal water ingress. Seepage is also observed in the parking area ceiling below Flat No. 103. Thermal imaging confirms the presence of cold spots, indicative of active moisture in these affected areas.

2. Area-wise Observations
Hall (Flat No. 103)
Visual Observations:
Dampness is observed at the skirting level. 
insp_page3_4.jpeg
insp_page3_7.jpeg 
Thermal Observations: 
- Cold spots were detected, indicating moisture presence (e.g., 20.8°C compared to an ambient ~23.3°C). 
therm_page1_2.jpeg

Common Bedroom (Flat No. 103)
Visual Observations:
Dampness is observed at the skirting level. 
insp_page3_15.jpeg
insp_page3_17.jpeg 
Thermal Observations:
- Cold spots were detected, indicating moisture presence (e.g., 21.3°C compared to an ambient ~24.4°C). 
therm_page1_13.jpeg

Master Bedroom (Flat No. 103)
Visual Observations:
Dampness and efflorescence are observed on the wall surfaces, particularly at the skirting level. 
insp_page4_26.jpeg
insp_page5_45.jpeg 
Thermal Observations:
- Cold spots were detected, indicating moisture presence (e.g., 21.5°C compared to an ambient ~24.9°C). 
therm_page1_23.jpeg

Kitchen (Flat No. 103)
Visual Observations:
Dampness is observed at the skirting level. 
insp_page4_36.jpeg
Thermal Observations:
Cold spots were detected, indicating moisture presence (e.g., 22.1°C compared to an ambient ~23.2°C). 
therm_page1_31.jpeg

Common Bathroom (Flat No. 103)
Visual Observations:
Tile hollowness is present.
Gaps are observed in tile joints and around the Nahani trap joints.
Loose plumbing joints and rust are noted around fixtures (flush tank, shower, angle cock, bibcock, washbasin).
Mild dampness is observed at the ceiling. 
insp_page3_11.jpeg
insp_page4_34.jpeg 
Thermal Observations:
- Cold spots were detected, indicating moisture presence (e.g., 20.2°C compared to an ambient ~25.2°C). 
therm_page1_27.jpeg

Master Bedroom Bathroom (Flat No. 103)
Visual Observations:
Tile hollowness is present.
Gaps are observed in tile joints.
Plumbing issues are noted. 
insp_page5_38.jpeg
insp_page5_41.jpeg 
Thermal Observations:
- Cold spots were detected, indicating moisture presence (e.g., 21.7°C compared to an ambient ~24.5°C). 
therm_page1_39.jpeg

External Wall (near Master Bedroom of Flat No. 103)
Visual Observations:
Moderate cracks are observed on the external wall surface. 
insp_page5_50.jpeg
External plumbing pipes are moderately cracked and leaking.
Duct issues are present, including rusted pipes and a ladder. 
insp_page5_49.jpeg
Moderate algae, fungus, and moss growth are observed on the external wall. 
Thermal Observations:
Cold spots were detected, indicating moisture presence (e.g., 22.3°C compared to an ambient ~25°C). 
therm_page1_47.jpeg

Parking Area (below Flat No. 103)
Visual Observations:
Seepage is observed at the ceiling. 
insp_page5_49.jpeg
Thermal Observations:
Image Not Available

3. Probable Root Cause
The probable root causes for the observed issues are a combination of external and internal factors:
External Water Ingress: Cracks in the external walls and damaged/leaking external plumbing pipes allow rainwater and other moisture to penetrate the building structure.
Internal Plumbing Leaks: Concealed plumbing leaks, loose plumbing joints, and issues with bathroom waterproofing elements such as the Nahani trap, brickbat coba under tile flooring, and gaps in tile joints are contributing to internal dampness.
Lack of Maintenance: The presence of rust on pipes and algae/fungus on external walls suggests a lack of regular maintenance, exacerbating the issues.

4. Severity Assessment
Status / Severity Level: High 
Reasoning: The property exhibits widespread and persistent dampness, efflorescence, and active leaks across multiple critical areas, including living spaces, bathrooms, and the building exterior. The presence of both external and internal sources of water ingress, confirmed by visual and thermal inspections, indicates a significant and ongoing problem. If left unaddressed, these issues can lead to structural deterioration, mold growth, compromised indoor air quality, and further damage to finishes and electrical systems.

5. Recommended Actions
Conduct a detailed investigation to precisely locate all concealed plumbing leaks within the bathrooms.
Repair or replace all identified loose, rusted, or leaking plumbing joints and fixtures in the bathrooms.
Address tile hollowness and re-grout/seal all tile joints in bathrooms, paying special attention to areas around Nahani traps and floor drains.
Repair all cracks on the external walls and apply appropriate waterproofing and protective coatings.
Inspect, repair, or replace damaged external plumbing pipes and resolve any issues within the duct areas.
Remove existing damp and efflorescence-affected plaster and paint from interior walls and ceilings. Allow affected areas to dry completely before re-plastering and repainting with moisture-resistant materials.
Implement a comprehensive waterproofing solution for all wet areas (bathrooms) and external walls to prevent future water ingress.
Address the seepage in the parking area ceiling, tracing the source back to Flat No. 103 and rectifying it.

6. Additional Notes
The inspection was conducted on September 27, 2022.
The property is a flat located in an 11-story building.
No previous structural audit or repair work was reported for the property.
Thermal imaging effectively identified temperature anomalies consistent with moisture presence, corroborating visual observations of dampness.

7. Missing or Unclear Information
Specific locations within the Hall, Common Bedroom, and Kitchen for each dampness observation are not precisely mapped to individual thermal images.
The exact nature and full extent of the "Duct Issue" are not fully detailed beyond rusted pipes and a ladder.
Images for "Common Bathroom tile hollowness and plumbing issue" (Impacted Area 6 positive side), "Common Bathroom Ceiling Dampness" (Impacted Area 7 negative side), and "Flat no 203 tile joint open and outlet Leakage" (Impacted Area 7 positive side) were mentioned in the report but were not provided in the image list.
Details on the specific type of tile used in the bathrooms are not specified.
Several checklist items related to external wall condition (e.g., sealants on window frames, openings around pipes, vegetation growth, patchwork plaster, structural cracks at beam-column junctions, overhead water tank leakage, loose plaster/hollow sound) were marked as "N/A," indicating they were either not applicable or not assessed during the inspection.
"""

if __name__ == "__main__":
    create_pdf(report_text)
    print("PDF created as Final_DDR_Report.pdf")
