# 👷‍♂️ Applied AI Builder - DDR Report Generator

An automated AI workflow designed to ingest raw technical site inspection documents (Inspection Reports and Thermal Anomalies) and systematically convert them into a structured, client-ready Detailed Diagnostic Report (DDR).

This project was built to test applied reasoning, multimodal data integration, formatting reliability, and handling of imperfect, conflicting, or missing real-world data without hallucinations.

---

## 🏗️ Architecture & Workflow

The system is built on a Python backend and presented through a **Streamlit** user interface. It utilizes **PyMuPDF** for data extraction and **Google Gemini (2.5-Flash)** for multimodal reasoning.

1. **Document Ingestion (`app.py`)**: Users upload the Visual Inspection PDF and the Thermal Scan PDF via the Streamlit UI. 
2. **Multimodal Extraction (`pdf_processor.py`)**: 
   - `PyMuPDF` parses the raw textual data and page context.
   - It also performs granular extraction of the embedded images themselves. 
   - *Optimization safeguard*: The extraction logic utilizes `Pillow (PIL)` to ignore micro-icons and compress massively high-resolution images down to < 800px. It implements a hard-cap limit to prevent API payload explosion (e.g. 5,400+ hidden thermal points natively embedded in PDF layers).
3. **AI Reasoning Engine (`ai_engine.py`)**: 
   - The system passes the text and the Base64-encoded image bytes directly into the `gemini-2.5-flash` multimodal context window.
   - Using strict System Prompting, Gemini analyzes the visual observations and correlates them physically with the thermal anomalies.
   - Output constraints force the model to render a strict 7-section markdown structure matching the exact presentation of a professional DDR, including replacing the image references with explicit structural tags (e.g. `[[IMAGE: <key>]]`).
4. **Dynamic Output Rendering (`app.py`)**: Streamlit parses the AI's structural tags and dynamically executes inline HTML / CSS to cleanly render the extracted Base64 images directly inside the final generated report, right beneath the observations they prove.
5. **PDF Export (`create_final_pdf.py`)**: A standalone script using `ReportLab` that can convert the generated markdown/text output into a stylized `Final_DDR_Report.pdf` document.

---

## 🛠️ Installation & Setup

1. **Clone the repository:**
   ```bash
   git clone https://github.com/Saiteja140503/UrbanRoof.git
   cd UrbanRoof
   ```

2. **Create and activate a virtual environment:**
   ```bash
   python -m venv venv
   # Windows
   .\venv\Scripts\activate
   # Mac/Linux
   source venv/bin/activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Environment Variables:**
   Create a `.env` file in the root directory and add your Google Gemini API Key:
   ```env
   GEMINI_API_KEY=your_api_key_here
   ```

5. **Run the Application:**
   ```bash
   streamlit run app.py
   ```
   The application will launch locally at `http://localhost:8501`.

---

## 📋 Evaluation Criteria Addressed

* **Accuracy of Extracted Information:** Gemini temperature is set to `0.2`. It is strictly prompted not to invent facts and to explicitly label missing data as "Not Available."
* **Logical Merging:** The prompt system links specific thermal anomalies (e.g. Sub-surface moisture) to the specific visual symptoms (e.g. Water pooling near HVAC) and places them under the exact same "Area-wise Observation" sub-header.
* **Handling Conflict:** The system prompt instructs the AI to directly call out inconsistencies.
* **System Thinking:** Image bytes are extracted gracefully via `Pillow`, sized for bandwidth limits, safely analyzed by an LLM visually, and systematically injected back into a Streamlit GUI bypassing Markdown injection limitations.

## 📹 Demonstration
A full video walkthrough of the logic, the file execution, and the final output is available in the repository as `Demo_Recording.zip`.
