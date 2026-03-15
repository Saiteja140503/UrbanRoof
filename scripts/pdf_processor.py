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
    Added constraints to avoid 5400+ icon extraction loops by ignoring very small images 
    and shrinking large ones using PIL.
    """
    extracted_images = {}
    doc = fitz.open(stream=pdf_bytes, filetype="pdf")
    
    img_index = 1
    for page_num in range(len(doc)):
        page = doc[page_num]
        image_list = page.get_images(full=True)
        
        for img in image_list:
            # Hard stop if PDF contains thousands of useless images
            if img_index > 50:
                print("Hit max image limit (50). Stopping extraction.")
                return extracted_images

            xref = img[0]
            base_image = doc.extract_image(xref)
            image_bytes = base_image["image"]
            image_ext = base_image["ext"]
            
            try:
                # Open with Pillow to check dimensions and resize
                image = Image.open(io.BytesIO(image_bytes))
                
                # Filter out tiny icon-like images (e.g. 10x10 colored dots)
                if image.width < 100 or image.height < 100:
                    continue

                # Check if it needs resizing to save bandwidth and LLM tokens
                max_size = (800, 800)
                image.thumbnail(max_size, Image.Resampling.LANCZOS)
                
                # Make sure to convert RGBA to RGB before saving to JPEG
                if image.mode in ("RGBA", "P"):
                    image = image.convert("RGB")
                    
                output_buffer = io.BytesIO()
                image.save(output_buffer, format="JPEG")
                processed_bytes = output_buffer.getvalue()

                # Convert to Base64
                encoded_image = base64.b64encode(processed_bytes).decode("utf-8")
                
                # Image label for the LLM to reference
                image_label = f"{prefix}_page{page_num+1}_{img_index}.jpeg"
                extracted_images[image_label] = {
                    "base64": encoded_image,
                    "mime_type": "image/jpeg"
                }
                img_index += 1
            except Exception as e:
                print(f"Failed to process image on page {page_num+1}: {e}")
                
    return extracted_images
