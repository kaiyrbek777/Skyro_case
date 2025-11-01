# How to Add PDF and Word Documents

## ✅ Good News - PDF Support Already Added!

The system now supports PDF files automatically! Just drop PDF files into the `data/documents/` folder and they will be indexed on startup.

---

## 📄 How to Add PDF Files

### Step 1: Get Your PDF Files
Any PDF document you want to add (product specs, contracts, reports, etc.)

### Step 2: Copy to Documents Folder
```bash
# Place PDFs in appropriate subfolders:
cp my-report.pdf data/documents/confluence/
cp contract.pdf data/documents/product_specs/
cp meeting-notes.pdf data/documents/meetings/
```

### Step 3: Restart Backend (if already running)
```bash
docker-compose restart backend
```

**That's it!** The backend will automatically:
1. Detect the PDF files
2. Extract text from all pages
3. Generate embeddings
4. Store in pgvector
5. Make searchable in the UI

---

## 📝 How to Add Word Documents (.docx)

Word files are NOT yet supported, but you can easily convert them:

### Option 1: Convert to PDF (Recommended)
1. Open Word document
2. File → Save As → PDF
3. Follow PDF instructions above

### Option 2: Convert to Markdown
1. Open Word document
2. File → Save As → Plain Text (.txt)
3. Place in `data/documents/` folder

### Option 3: Add Word Support (Advanced)
If you want native .docx support, update `backend/requirements.txt`:

```bash
# Add this line:
python-docx==1.1.0
```

Then update `backend/ingestion/document_loader.py`:

```python
# Add at top:
try:
    from docx import Document
    DOCX_AVAILABLE = True
except ImportError:
    DOCX_AVAILABLE = False

# In _is_supported_format method, add:
if DOCX_AVAILABLE:
    supported_extensions.add(".docx")

# In _load_file method, add:
elif file_path.suffix == ".docx":
    content = self._load_docx(file_path)

# Add new method:
def _load_docx(self, file_path: Path) -> str:
    """Load Word document and extract text"""
    if not DOCX_AVAILABLE:
        return ""

    try:
        doc = Document(file_path)
        paragraphs = [p.text for p in doc.paragraphs if p.text.strip()]
        return "\n\n".join(paragraphs)
    except Exception as e:
        logger.error(f"Failed to load Word doc {file_path}: {e}")
        return ""
```

---

## 🧪 Testing PDF Files

### Create a Test PDF
You can use any PDF, or create one for testing:

**Using Python:**
```python
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

def create_test_pdf():
    c = canvas.Canvas("test-document.pdf", pagesize=letter)
    c.drawString(100, 750, "Skyro Test Document")
    c.drawString(100, 720, "This is a sample PDF for testing.")
    c.drawString(100, 690, "It contains information about Skyro's products.")
    c.save()

create_test_pdf()
```

**Using Online Tools:**
- https://www.pdf24.org/en/create-pdf.html
- https://smallpdf.com/word-to-pdf

### Verify PDF is Indexed
```bash
# Check backend logs
docker-compose logs backend | grep "Extracted"

# Should see:
# "Extracted 3 pages from test-document.pdf"
```

### Search for PDF Content
In the UI, ask questions about content that's in your PDF:
- "What does the test document say?"
- "Show me information from the PDF"

---

## 📊 Supported File Formats

| Format | Extension | Support | How to Add |
|--------|-----------|---------|------------|
| Markdown | .md | ✅ Built-in | Drop in folder |
| Plain Text | .txt | ✅ Built-in | Drop in folder |
| JSON | .json | ✅ Built-in | Drop in folder |
| **PDF** | .pdf | ✅ **Added** | Drop in folder |
| Word | .docx | ⚠️ Manual | Convert or add code |
| Excel | .xlsx | ❌ Not supported | Convert to CSV/JSON |
| PowerPoint | .pptx | ❌ Not supported | Convert to PDF |

---

## 🔧 Troubleshooting

### PDF not being indexed
1. Check file is in correct location:
   ```bash
   ls -la data/documents/**/*.pdf
   ```

2. Check backend logs for errors:
   ```bash
   docker-compose logs backend | grep -i pdf
   ```

3. Verify PDF is readable (not password-protected or corrupted):
   ```bash
   # Try opening in PDF reader
   ```

### PDF text extraction is empty
- PDF might be scanned images (needs OCR)
- Solution: Use OCR tool first
  - Adobe Acrobat: Tools → Recognize Text
  - Online: https://www.onlineocr.net/

### Backend not restarting
```bash
# Force rebuild
docker-compose up -d --build backend
```

---

## 📁 Example File Structure

```
data/documents/
├── confluence/
│   ├── payment-gateway.md
│   ├── fraud-detection.md
│   └── security-policy.pdf        # ✅ PDF file
│
├── meetings/
│   ├── 2024-01-15-review.md
│   └── 2024-02-board-meeting.pdf  # ✅ PDF file
│
└── product_specs/
    ├── mobile-app.md
    ├── api-endpoints.json
    ├── compliance-guide.pdf       # ✅ PDF file
    └── financial-report-q4.pdf    # ✅ PDF file
```

---

## ✨ Best Practices

1. **Organize by type:** Use subfolders (confluence, meetings, product_specs)
2. **Use descriptive names:** `q4-2023-financial-report.pdf` not `doc1.pdf`
3. **Keep PDFs text-based:** Avoid scanned images without OCR
4. **Test after adding:** Ask a question about the new content
5. **Monitor ingestion:** Check logs to ensure successful indexing

---

## 🚀 Quick Start Example

```bash
# 1. Download or create a PDF
curl -o data/documents/product_specs/sample.pdf https://example.com/doc.pdf

# 2. Restart backend
docker-compose restart backend

# 3. Wait for ingestion (check logs)
docker-compose logs -f backend

# 4. Test in UI
# Open http://localhost:8501
# Ask: "What does the sample PDF contain?"
```

---

## 💡 Need Help?

- Check logs: `docker-compose logs backend`
- Test API: `curl http://localhost:8000/health`
- File an issue: https://github.com/kaiyrbek777/Skyro_case/issues

---

**Happy document indexing! 🎉**
