import fitz  # PyMuPDF
import io
import base64
from PIL import Image

def extract_text_from_pdf(pdf_bytes: bytes) -> str:
    """Extracts text from a PDF."""
    text_content = []
    doc = fitz.open(stream=pdf_bytes, filetype="pdf")
    for page_num in range(len(doc)):
        page = doc[page_num]
        text = page.get_text()
        text_content.append(f"--- Page {page_num + 1} ---\n{text}")
    return "\n".join(text_content)

def extract_images_from_pdf(pdf_bytes: bytes, prefix="img") -> dict:
    """
    Extracts images from a PDF and returns a dictionary 
    mapping an image identifier to its base64 encoded string.
    """
    extracted_images = {}
    doc = fitz.open(stream=pdf_bytes, filetype="pdf")
    
    img_index = 1
    for page_num in range(len(doc)):
        page = doc[page_num]
        image_list = page.get_images(full=True)
        
        for img in image_list:
            xref = img[0]
            base_image = doc.extract_image(xref)
            image_bytes = base_image["image"]
            image_ext = base_image["ext"]
            
            # Convert to standard format (e.g., JPEG or PNG) if needed, or just use base64
            try:
                # We convert it to base64 so we can pass it directly to Gemini
                encoded_image = base64.b64encode(image_bytes).decode("utf-8")
                
                # Image label for the LLM to reference
                image_label = f"{prefix}_page{page_num+1}_{img_index}.{image_ext}"
                extracted_images[image_label] = {
                    "base64": encoded_image,
                    "mime_type": f"image/{image_ext}"
                }
                img_index += 1
            except Exception as e:
                print(f"Failed to extract image on page {page_num+1}: {e}")
                
    return extracted_images
