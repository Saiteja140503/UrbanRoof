import streamlit as st
import os
import base64
from pdf_processor import extract_text_from_pdf, extract_images_from_pdf
from ai_engine import generate_ddr_report
from dotenv import load_dotenv

load_dotenv()

st.set_page_config(page_title="DDR Report Generator", layout="wide")

st.title("👷‍♂️ Applied AI Builder - DDR Report Generator")
st.markdown("Automated generation of Detailed Diagnostic Reports (DDR) from Inspection & Thermal PDF Reports.")

with st.sidebar:
    st.header("Configuration")
    api_key = st.text_input("Google Gemini API Key", type="password", value=os.environ.get("GEMINI_API_KEY", ""))
    
    st.header("Upload Reports")
    inspection_file = st.file_uploader("Upload Inspection Report (PDF)", type="pdf")
    thermal_file = st.file_uploader("Upload Thermal Report (PDF)", type="pdf")

def render_markdown_with_images(markdown_text: str, all_images: dict):
    """
    Since the LLM outputs `![alt text](image_key)`, we need to replace `image_key` 
    with the actual base64 data URI so Streamlit can render it inline.
    """
    for img_key, img_data in all_images.items():
        base64_str = img_data['base64']
        mime_type = img_data['mime_type']
        data_uri = f"data:{mime_type};base64,{base64_str}"
        
        # Replace the key with the data URI in the markdown
        # The LLM is instructed to strictly use `[[IMAGE: img_key]]`
        img_html = f'<img src="{data_uri}" alt="{img_key}" style="max-width: 100%; height: auto;" />'
        markdown_text = markdown_text.replace(f"[[IMAGE: {img_key}]]", img_html)
        
    st.markdown(markdown_text, unsafe_allow_html=True)

if st.button("Generate Detailed Diagnostic Report", type="primary"):
    if not api_key:
        st.error("Please provide a Google Gemini API Key.")
    elif not inspection_file or not thermal_file:
        st.error("Please upload both the Inspection Report and the Thermal Report.")
    else:
        with st.spinner("Processing documents & extracting data..."):
            
            try:
                # 1. Read files
                insp_bytes = inspection_file.read()
                therm_bytes = thermal_file.read()
                
                # 2. Extract Text
                st.info("Extracting textual observations...")
                insp_text = extract_text_from_pdf(insp_bytes)
                therm_text = extract_text_from_pdf(therm_bytes)
                
                # 3. Extract Images
                st.info("Extracting images...")
                insp_images = extract_images_from_pdf(insp_bytes, prefix="insp")
                therm_images = extract_images_from_pdf(therm_bytes, prefix="therm")
                
                all_extracted_images = {**insp_images, **therm_images}
                st.success(f"Extracted {len(insp_images)} inspection images and {len(therm_images)} thermal images.")
                
                # 4. Generate Report
                st.info("Analyzing data and generating the combined DDR Report...")
                report_markdown = generate_ddr_report(
                    api_key=api_key,
                    inspection_text=insp_text,
                    thermal_text=therm_text,
                    inspection_images=insp_images,
                    thermal_images=therm_images
                )
                
                st.success("Report Generation Complete!")
                st.divider()
                
                # 5. Display the structured output with embedded images
                render_markdown_with_images(report_markdown, all_extracted_images)
                
            except Exception as e:
                st.error(f"An error occurred during processing: {str(e)}")
