import fitz  # PyMuPDF
import json
from pathlib import Path

INPUT_DIR = Path("/app/input")
OUTPUT_DIR = Path("/app/output")
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

def normalize_size(sz, tol=0.5):
    return round(sz / tol) * tol

def extract_text(doc):
    font_freq = {}
    items = []

    for pg_num, page in enumerate(doc, start=1):
        for block in page.get_text("dict")["blocks"]:
            for line in block.get("lines", []):
                spans = line.get("spans", [])
                texts = [s["text"] for s in spans if s["text"].strip()]
                if not texts:
                    continue
                content = " ".join(texts)
                size = max(normalize_size(s["size"]) for s in spans)
                font_freq[size] = font_freq.get(size, 0) + 1
                items.append((content, size, pg_num))
    return items, font_freq

def rank_fonts(font_freq):
    sorted_fonts = sorted(font_freq.items(), key=lambda x: -x[0])
    rank = {}
    if sorted_fonts: rank[sorted_fonts[0][0]] = "Title"
    if len(sorted_fonts) > 1: rank[sorted_fonts[1][0]] = "H1"
    if len(sorted_fonts) > 2: rank[sorted_fonts[2][0]] = "H2"
    if len(sorted_fonts) > 3: rank[sorted_fonts[3][0]] = "H3"
    return rank

def parse_document(pdf_path):
    doc = fitz.open(pdf_path)
    elements, freq = extract_text(doc)
    fonts = rank_fonts(freq)

    result = {"title": "", "outline": []}
    title_lines = []
    headings = []

    for text, size, page in elements:
        role = fonts.get(size)

        if role == "Title" and page == 1:
            title_lines.append(text)
        elif role and role.startswith("H"):
            headings.append((text, size, page))

    # Heuristic: If all pages have >5 headings, assume it's a form; suppress outline
    page_count = {}
    for _, _, pg in headings:
        page_count[pg] = page_count.get(pg, 0) + 1

    suppress_outline = all(count > 5 for count in page_count.values())

    if not suppress_outline:
        for text, size, page in headings:
            result["outline"].append({
                "level": fonts.get(size),
                "text": text,
                "page": page
            })

    result["title"] = " ".join(title_lines)
    return result

def main():
    for file in INPUT_DIR.glob("*.pdf"):
        print(f"\U0001F4C4 {file.name}")
        parsed = parse_document(file)
        out_path = OUTPUT_DIR / f"{file.stem}.json"
        with open(out_path, "w", encoding="utf-8") as f:
            json.dump(parsed, f, indent=2, ensure_ascii=False)
        print(f"✅ Saved: {out_path.name}")

if __name__ == "__main__":
    main()