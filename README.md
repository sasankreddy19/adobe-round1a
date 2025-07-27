# Adobe Hackathon - Round 1A Submission

## 🧠 Challenge
Build a system that extracts structured outlines from PDFs, including:

- Title
- Headings: H1, H2, H3
- With level and page number
- Output format: JSON

## 🛠️ Approach

We used a combination of layout-based PDF parsing (`pdfplumber` / `PyMuPDF`) and heuristics such as font size, font weight, and text position to identify heading levels. The script processes each page and classifies headings based on relative features.

### Steps:
1. Load and parse the PDF
2. Identify potential headings using text attributes
3. Assign levels: H1, H2, H3 using custom logic
4. Output a clean JSON file per input

## 🧰 Libraries Used

- `PyMuPDF` (fitz) – PDF text and layout extraction
- `pdfplumber` – for additional page-level parsing
- `re`, `json`, `os` – for processing

> ⚠️ No external API or internet calls used. The solution is fully offline and meets size/runtime constraints.

## 🐳 How to Build & Run (Offline)

### Build the Docker image:
```bash
docker build --platform linux/amd64 -t adobe-solution:latest .
