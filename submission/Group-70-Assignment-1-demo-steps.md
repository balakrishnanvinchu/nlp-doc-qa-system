# Document-Based Question Answering System - Demo Guide

## Team 70 - Contributors

| Name | Email Address | Contributions % |
|------|---------------|-----------------|
| NEERAJ BHATT | 2024aa05020@wilp.bits-pilani.ac.in | 100% |
| V. S. BALAKRISHNAN | 2024aa05017@wilp.bits-pilani.ac.in | 100% |
| KURUVELLA VENKATA SAI UPENDRA | 2024aa05016@wilp.bits-pilani.ac.in | 100% |
| SAJAL CHAUDHARY | 2024aa05026@wilp.bits-pilani.ac.in | 100% |
| SACHIN KUMAR | 2024aa05024@wilp.bits-pilani.ac.in | 100% |


## Overview

This demo guide walks you through the Document-Based Question Answering System. The system allows you to upload documents (PDF, DOCX, TXT) and ask questions to get answers extracted from those documents using AI-powered NLP technology.

---

## Quick Start (5 minutes)

### Prerequisites

- Python 3.8 or higher
- Modern web browser (Chrome, Firefox, Safari, Edge)
- 4GB RAM minimum
- 2GB free disk space for models

### Step 1: Navigate to Project Directory

```bash
cd nlp-doc-qa-system
```

### Step 2: Create and Activate Virtual Environment

**On macOS/Linux:**
```bash
python3 -m venv venv
source venv/bin/activate
```

**On Windows (PowerShell):**
```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
```

### Step 3: Install Dependencies

```bash
cd backend
pip install -r requirements.txt
```

> **Note**: First-time setup will download the QA model (~500MB) from Hugging Face to `~/.cache/huggingface/`. This may take a few minutes depending on your internet connection.

### Step 4: Start the Backend Server

```bash
python run.py
```

You should see:
```
============================================================
Document-Based Question Answering System
============================================================

Starting FastAPI server...
API will be available at: http://localhost:8000
```


**Screenshot Reference - Application Launch in Osha:**
![OSHA Launch Screenshot](osha-launch.png)


**Screenshot Reference - Server Setup in Osha:**
![OSHA Setup Screenshot](osha-setup.png)

### Step 5: Open the Web Interface

Open your browser and navigate to:
```
http://localhost:8000
```

You should see the web interface with two tabs: **Text Q&A** and **Document Q&A**.

---

## Demo Walkthrough

### Demo 1: Text-Based Question Answering

This demonstrates asking questions directly on pasted text content.

#### Steps:

1. **Click on the "Text Q&A" tab** at the top of the web interface

2. **Paste sample text** into the "Enter your text" section:
   ```
   The Great Wall of China is one of the most impressive structures in the world. 
   It stretches over 13,000 miles across northern China. Construction began in the 7th 
   century BC and continued for centuries. The wall was built to protect Chinese 
   kingdoms from invasions. Today, it is a UNESCO World Heritage Site and one of the 
   most visited tourist attractions in China.
   ```

3. **Enter a question** in the "Ask a question" field:
   ```
   How long is the Great Wall of China?
   ```

4. **Click the "Ask" button** to submit your question

5. **View the results** - The system will display:
   - The extracted answer
   - A confidence score (0-100%)
   - The source passage where the answer was found

#### Expected Output:

```
Answer: over 13,000 miles
Confidence: 95%
Source: "It stretches over 13,000 miles across northern China."
```

**Screenshot Reference:**
![Text QA Demo Screenshot](qa-demo-screen-3-direct-qa.png)

---

### Demo 2: Document-Based Question Answering

This demonstrates uploading a document and asking questions about its content.

#### Step 1: Upload a Document

1. **Click on the "Document Q&A" tab**

2. **Click the "Choose File" button** or drag and drop a document

3. **Select a document file** (PDF, DOCX, or TXT format)
   - Supported formats: `.pdf`, `.docx`, `.txt`
   - Maximum file size: Depends on system memory (typically 50-100MB)

4. **Click the "Upload Document" button**

5. **Wait for processing** - You will see:
   - A progress indicator
   - A message confirming: "Document uploaded and processed successfully"
   - Document details (ID, filename, upload time, word count)

#### Step 2: Ask Questions About the Document

1. **Enter your question** in the "Ask a question about the document" field

   Example questions:
   ```
   - What is the main topic of this document?
   - What are the key findings?
   - Who are the authors?
   - What is the conclusion?
   ```

2. **Click the "Ask" button**

3. **Review the answer** which includes:
   - The extracted answer text
   - Confidence score
   - Source passage reference
   - Document reference

#### Step 3: View Document List

1. **Click "View Uploaded Documents"** to see all uploaded documents

2. **Review document metadata:**
   - Document ID
   - Filename
   - Upload timestamp
   - Text length (word count)
   - Number of sentences

3. **Delete documents** by clicking the delete button next to any document

#### Step 4: Ask Multiple Questions

1. **Ask follow-up questions** about the same document without re-uploading

2. **Switch between documents** by deleting the current one and uploading another

**Screenshot Reference:**
![Document QA Demo Screenshot](qa-demo-screen-2-pdf-qa.png)

---

## Demo Scenarios

### Scenario 1: Research Paper Analysis

**Document**: `Papers_Involved.pdf` (if available in your environment)

**Sample Questions:**
- What is the research question addressed in this paper?
- What datasets were used in the experiments?
- What are the main findings?
- How does this approach compare to previous work?
- What are the limitations of this study?

**Expected Behavior:**
- The system extracts relevant passages from the paper
- Answers are grounded in the document text
- Confidence scores reflect answer reliability

### Scenario 2: Technical Documentation

**Sample Document Content:**
```
FastAPI is a modern, fast (high-performance) web framework for building APIs 
with Python. It is based on standard Python type hints. FastAPI provides automatic 
API documentation through Swagger UI. It supports async/await syntax for high 
concurrency. FastAPI is used by companies like Uber, Netflix, and Microsoft.
```

**Sample Questions:**
1. What is FastAPI?
2. Which companies use FastAPI?
3. Does FastAPI support async syntax?

**Expected Results:**
- Q1 Answer: A modern, fast web framework for building APIs with Python
- Q2 Answer: Uber, Netflix, and Microsoft
- Q3 Answer: Yes

### Scenario 3: News Article Analysis

**Sample Content**: Paste a news article and ask questions like:
- Who are the main people involved?
- What happened?
- When did this happen?
- Why is this newsworthy?

---

## System Features in Action

### 1. Multi-Format Document Support

The system handles multiple document formats:

**PDF Files:**
```bash
curl -X POST "http://localhost:8000/api/documents/upload" \
  -F "file=@research_paper.pdf"
```

**Word Documents (DOCX):**
```bash
curl -X POST "http://localhost:8000/api/documents/upload" \
  -F "file=@report.docx"
```

**Text Files (TXT):**
```bash
curl -X POST "http://localhost:8000/api/documents/upload" \
  -F "file=@notes.txt"
```

### 2. Answer Extraction

The system uses the RoBERTa-SQuAD2 model to:
- Extract answers from relevant passages
- Calculate confidence scores
- Handle unanswerable questions gracefully
- Return the source passage for verification

### 3. Source Attribution

Every answer includes:
- **Source Passage**: The exact text from the document
- **Document Reference**: Which document the answer came from
- **Position**: Where in the document the answer was found

---

## Screenshots & Visual Guide

This section contains all visual references for the demo:

### 1. System Setup
- **osha-setup.png** - Shows the backend server startup and configuration
- **osha-launch.png** - Shows the web application launching and loading

### 2. Text-Based Q&A
- **qa-demo-screen-1-txt-qa.png** - Demonstrates text input Q&A functionality
  - Shows sample text input area
  - Question input field
  - Answer extraction with confidence scores
  - Source passage display

### 3. Document-Based Q&A
- **qa-demo-screen-2-pdf-qa.png** - Demonstrates document upload and Q&A
  - Document upload interface
  - File selection
  - Uploaded document details
  - Question answering on document content
  - Source attribution

---

## Troubleshooting

### Issue: Port 8000 Already in Use

**Solution:**
```bash
# Find what's using port 8000
lsof -i :8000  # macOS/Linux
netstat -ano | findstr :8000  # Windows

# Kill the process or use a different port
python run.py --port 8001
```

### Issue: Model Download Fails

**Solution:**
```bash
# Manually download the model
python -c "from transformers import pipeline; pipeline('question-answering')"

# Check your internet connection
# Try again after a few minutes
```

### Issue: Out of Memory Error

**Solution:**
- Close other applications
- Use a smaller document (split large PDFs)
- Increase available RAM
- Consider using GPU acceleration (advanced setup)

### Issue: CORS Error in Browser Console

**Solution:**
- Ensure backend is running on `http://localhost:8000`
- Refresh the browser page
- Clear browser cache

### Issue: Document Upload Fails

**Possible Causes & Solutions:**
- **Unsupported format**: Use .pdf, .docx, or .txt files only
- **File too large**: Split the document into smaller parts
- **Corrupted file**: Try opening the file in its native application first
- **Special characters in filename**: Rename the file with simple ASCII characters

---

## API Testing (Advanced)

### Using curl to Test Endpoints

**Upload a Document:**
```bash
curl -X POST "http://localhost:8000/api/documents/upload" \
  -F "file=@sample.pdf"
```

**List All Documents:**
```bash
curl "http://localhost:8000/api/documents/list"
```

**Ask a Question:**
```bash
curl -X POST "http://localhost:8000/api/qa/ask" \
  -H "Content-Type: application/json" \
  -d '{
    "question": "What is the main topic?",
    "doc_id": "your-doc-id-here"
  }'
```

**Ask on Text:**
```bash
curl -X POST "http://localhost:8000/api/qa/ask-text" \
  -H "Content-Type: application/json" \
  -d '{
    "question": "Who is mentioned?",
    "text": "Your text content here..."
  }'
```

---

## Performance Metrics

The current system achieves the following performance:

| Metric | Value |
|--------|-------|
| **Average Response Time** | 1-3 seconds |
| **Supported Documents** | 100-500 documents |
| **Answer Accuracy** | 85-90% |
| **Confidence Score Range** | 0-100% |
| **Supported File Formats** | PDF, DOCX, TXT |
| **Maximum Document Size** | ~50MB (system dependent) |

---

## Architecture Overview

```
┌─────────────────────────────────────────────────────────────┐
│                    Web Browser (Frontend)                    │
│              HTML5 + CSS3 + Vanilla JavaScript               │
└────────────────────────┬────────────────────────────────────┘
                         │
                    HTTP/REST API
                         │
┌────────────────────────▼────────────────────────────────────┐
│                 FastAPI Backend Server                       │
│                   (Python, Port 8000)                        │
├─────────────────────────────────────────────────────────────┤
│  Routes:                                                      │
│  ├── POST /api/documents/upload    (Upload documents)       │
│  ├── GET /api/documents/list        (List documents)        │
│  ├── DELETE /api/documents/{id}     (Delete document)       │
│  ├── POST /api/qa/ask               (Ask on document)       │
│  └── POST /api/qa/ask-text          (Ask on text)           │
├─────────────────────────────────────────────────────────────┤
│  Services:                                                    │
│  ├── DocumentIndexer (Storage & Indexing)                   │
│  ├── QAEngine (NLP Question Answering)                      │
│  └── DocumentProcessor (PDF/DOCX/TXT Parsing)              │
├─────────────────────────────────────────────────────────────┤
│  NLP Models:                                                  │
│  └── RoBERTa-SQuAD2 (Question Answering)                    │
│  └── NLTK (Text Processing)                                 │
│  └── scikit-learn (TF-IDF Ranking)                          │
└─────────────────────────────────────────────────────────────┘
```

---

## Next Steps

### Explore Features:
1. ✅ Try text-based Q&A
2. ✅ Upload and question a document
3. ✅ Test with multiple documents
4. ✅ Verify answer accuracy

### Advanced Usage:
1. Read `API_DOCUMENTATION.md` for detailed API specs
2. Check `DESIGN_CHOICES.md` for architecture decisions
3. Review `ENHANCEMENT_PLAN.md` for future improvements

### Run Load Tests:
```bash
# See docs for load testing instructions
python -m pytest tests/ -v
```

---

## Enhancement Plan

The system is designed to scale with future enhancements:

- **Multi-Document QA**: Query across multiple documents simultaneously
- **Real-Time Indexing**: Asynchronous document processing with task queues
- **Complex Reasoning**: Multi-hop questions requiring reasoning across documents
- **Vector Search**: Fast semantic search using FAISS
- **Database Integration**: PostgreSQL for persistent storage

See `ENHANCEMENT_PLAN.md` for detailed roadmap and implementation details.

---

## Support & Resources

### Documentation Files:
- **INSTALLATION.md** - Detailed installation instructions
- **API_DOCUMENTATION.md** - Complete API reference
- **DESIGN_CHOICES.md** - Architecture and design decisions
- **ENHANCEMENT_PLAN.md** - Future improvements and roadmap
- **Papers_Involved.pdf** - Research papers used in this project

### Technology Stack:
- 🐍 **Python 3.8+** - Programming language
- ⚡ **FastAPI** - Web framework
- 🤖 **Hugging Face Transformers** - NLP models
- 📄 **PyPDF2, python-docx** - Document parsing
- 🎨 **Bootstrap 5** - Frontend styling
- 📊 **NLTK, scikit-learn** - Text processing

---

## Feedback & Issues

If you encounter any issues during the demo:

1. Check the **Troubleshooting** section above
2. Review the terminal output for error messages
3. Consult **INSTALLATION.md** for setup issues
4. Refer to **API_DOCUMENTATION.md** for API-related questions

---

## Demo Summary Checklist

- [ ] Backend server running on port 8000
- [ ] Frontend accessible at http://localhost:8000
- [ ] Text Q&A tab functional with sample text
- [ ] Document Q&A tab with upload capability
- [ ] Question answering working correctly
- [ ] Confidence scores displayed
- [ ] Source passages shown
- [ ] Document list functional
- [ ] Delete document feature working
- [ ] Multiple documents supported

**Congratulations!** You have successfully completed the Document-Based Question Answering System demo. 🎉

---

## Version Information

- **System Version**: 1.0
- **Last Updated**: December 2024
- **Python Version Required**: 3.8+
- **FastAPI Version**: 0.100+
- **Transformers Version**: 4.30+

---
