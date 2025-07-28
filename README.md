# Adobe Hackathon - Round 1A Submission

## 🧠 Challenge Overview

Build a system that extracts structured outlines from PDF documents including:

- Document title
- Headings with levels (H1, H2, H3)
- Page numbers for each heading
- Output format: structured JSON

The solution must work fully offline, complete within 60 seconds for 3–5 documents, and consume ≤1GB RAM using only CPU.

---

## 💡 Approach

We developed a layout-aware and font-sensitive PDF processor using `PyMuPDF` and optionally `pdfplumber`. The method relies on visual and structural cues (font size, boldness, positioning) to classify text elements into heading levels.

### Key Steps:

1. **Load PDF**: Open using `PyMuPDF` (`fitz`) for lightweight access to text and layout.
2. **Text Extraction**: Extract text blocks and metadata like font size, flags (bold), and coordinates.
3. **Heading Detection**:
   - Classify headings based on relative font size and boldness.
   - Use positional heuristics (e.g. left-aligned, top of page).
   - Dynamically infer H1, H2, H3 using most frequent size groups.
4. **Structuring Output**:
   - Each heading includes: text, heading level (H1–H3), and page number.
   - JSON output format for integration into downstream systems.

---

## 📦 Models & Libraries Used

| Library       | Purpose                                |
|---------------|----------------------------------------|
| `PyMuPDF`     | Primary PDF text + layout extraction   |
| `pdfplumber`  | (Optional) Additional structural parsing |
| `json`        | For output formatting                  |
| `re`, `os`    | Utility + regex pattern detection      |

> ❌ No ML models used — fully rule-based to stay within memory and offline constraints.

---

## 🐳 How to Build & Run (Offline Mode)

### Build Docker Image
```bash
docker build -t adobe-outline-extractor .
