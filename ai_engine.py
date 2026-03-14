import os
from google import genai
from google.genai import types

def generate_ddr_report(api_key: str, inspection_text: str, thermal_text: str, inspection_images: dict, thermal_images: dict) -> str:
    """
    Generates the Detailed Diagnostic Report using Gemini based on 
    the provided text and image dictionaries.
    """
    client = genai.Client(api_key=api_key)
    
    # We will use gemini-2.5-flash which is multimodal and fast
    model = "gemini-2.5-flash"
    
    system_instruction = """
You are an expert technical AI assistant responsible for converting raw site inspection documents into a client-ready 
Detailed Diagnostic Report (DDR).

You have been provided with data from two reports:
1. Inspection Report (visual observations)
2. Thermal Report (temperature and thermal anomalies)

You are also provided with a list of extracted images from these reports.

INSTRUCTIONS:
- Extract relevant observations from both reports.
- Combine information logically.
- Avoid duplicate points.
- If information conflicts, explicitly mention the conflict.
- If information is missing, write "Not Available".
- Use simple, client-friendly language, avoiding unnecessary technical jargon.
- Do NOT invent facts or hallucinate details.
- Insert relevant images directly into the appropriate sections (especially under Area-wise Observations).
  - You MUST use the exact syntax: `[[IMAGE: KEY]]` where KEY is the provided Image Key. Do NOT use markdown. Do NOT use HTML. Just use `[[IMAGE: KEY]]`.
  - ONLY use image dictionary keys provided in the context.
  - If no relevant image is found for an observation where one is expected, mention "Image Not Available".

OUTPUT STRUCTURE REQUIRED:
The final markdown output MUST strictly follow this structure exactly, including the bolded headers and the table-like styling for severity:

# Detailed Diagnosis Report

## 1. Property Issue Summary
[Brief summary of the main cumulative issues found, describing the condition and the area of concern]

## 2. Area-wise Observations
[List observations area by area, combining both visual and thermal findings. Embed relevant images here directly under each point to serve as photographic proof.]

Example: 
### [Location Name - e.g. Roof Area]
**Visual Observations:**
- Water pooling observed.
- Membrane appears cracked.
[[IMAGE: inspection_page2_1.png]]

**Thermal Observations:**
- Sub-surface moisture detected (-2.4 Celsius anomaly).
[[IMAGE: thermal_page1_2.png]]

## 3. Probable Root Cause
[Synthesis of what is likely causing the observed issues]

## 4. Severity Assessment
**Status / Severity Level**: [High / Medium / Low]  
**Reasoning**: [Reasoning based on the findings]

## 5. Recommended Actions
[Client-friendly list of next steps to remediate the issues, bulleted]

## 6. Additional Notes
[Any other relevant facts, disclaimers, or limitations of the report]

## 7. Missing or Unclear Information
[Explicitly list what was not covered or unclear. If there is nothing missing, write "None Noted"]
"""

    # Prepare multimodal content
    contents = [
        types.Part.from_text(text=f"INSPECTION REPORT TEXT:\n{inspection_text}\n\n"),
        types.Part.from_text(text=f"THERMAL REPORT TEXT:\n{thermal_text}\n\n"),
        types.Part.from_text(text="AVAILABLE INSPECTION IMAGES (Use these exact keys as markdown image paths if relevant):\n" + ", ".join(inspection_images.keys()) + "\n\n"),
        types.Part.from_text(text="AVAILABLE THERMAL IMAGES (Use these exact keys as markdown image paths if relevant):\n" + ", ".join(thermal_images.keys()) + "\n\n"),
        types.Part.from_text(text="Please generate the final DDR report based on the provided instructions and structure.")
    ]
    
    # To actually send the images to Gemini so it understands their content and can map them 
    # to observations logically:
    for img_key, img_data in inspection_images.items():
        contents.insert(0, types.Part.from_bytes(
            data=img_data["base64"],
            mime_type=img_data["mime_type"],
        ))
        contents.insert(1, types.Part.from_text(text=f"IMAGE REFERENCE KEY: {img_key}\n"))

    for img_key, img_data in thermal_images.items():
        contents.insert(0, types.Part.from_bytes(
            data=img_data["base64"],
            mime_type=img_data["mime_type"],
        ))
        # Ensure we tell Gemini which image corresponds to which key
        contents.insert(1, types.Part.from_text(text=f"IMAGE REFERENCE KEY: {img_key}\n"))

    response = client.models.generate_content(
        model=model,
        contents=contents,
        config=types.GenerateContentConfig(
            system_instruction=system_instruction,
            temperature=0.2, # Keep hallucination low
        )
    )
    
    return response.text
