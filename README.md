# Applied AI Builder - DDR Report Generator

This project is an AI-powered workflow designed to construct a Detailed Diagnostic Report (DDR) by automatically extracting, analyzing, and structuring text and image data from PDF technical inspection reports.

## Architecture

* **Streamlit (`app.py`)**: The frontend interface allowing users to upload their `Inspection Report` and `Thermal Report` PDFs.
* **Extraction (`pdf_processor.py`)**: Utilizes `PyMuPDF` to extract raw text with page context, as well as converting embedded PDF images into Base64 format for multimodal analysis.
* **LLM Engine (`ai_engine.py`)**: Configured with Google's `gemini-2.5-flash` multimodal AI. The model receives strict systemic prompts to intelligently synthesize visual and thermal findings while mapping the exact extracted images back into the markdown output via structure tagging.

## How to Run

1. Clone the repository natively.
2. Initialize and activate a Python virtual environment: `python -m venv venv` and `.\venv\Scripts\activate`.
3. Install dependencies: `pip install -r requirements.txt`.
4. Create a `.env` file in the root directory and add your key: `GEMINI_API_KEY=your_key_here`
5. Run the app: `streamlit run app.py`

## Features

- Evaluates missing/conflicting data logically according to prompt constraints.
- Native injection of proxy Base64 image byte structures mapped via `<img src="base64_data">` dynamically through Streamlit UI rendering.
