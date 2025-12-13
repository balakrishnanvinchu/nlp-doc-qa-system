# Installation and Setup Guide

## System Requirements

- Python 3.8 or higher
- 4GB RAM minimum (8GB recommended)
- 2GB free disk space for models
- macOS, Linux, or Windows

## Quick Start (5 minutes)

### 1. Navigate to project directory

```bash
cd /Users/bvs/Documents/assignments/NLP/doc-qa-system
```

### 2. Create and activate virtual environment

```bash
# Create virtual environment
python3 -m venv venv

# Activate it
source venv/bin/activate
```

### 3. Install dependencies

```bash
cd backend
pip install -r requirements.txt
```

First time setup will download the QA model (~500MB) to `~/.cache/huggingface/`

### 4. Start the backend server

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
API Documentation: http://localhost:8000/docs
```

### 5. Access the frontend

Open in your browser:
```
file:///Users/bvs/Documents/assignments/NLP/doc-qa-system/frontend/index.html
```

## Complete Installation (Detailed Steps)

### Step 1: Prerequisites Check

```bash
# Check Python version
python3 --version  # Should be 3.8+

# Check pip is available
pip3 --version

# Check available disk space
df -h
```

### Step 2: Clone/Navigate to Project

```bash
cd /Users/bvs/Documents/assignments/NLP/doc-qa-system
```

### Step 3: Set Up Python Virtual Environment

**Why Virtual Environment?**
- Isolates project dependencies
- Prevents version conflicts
- Keeps system Python clean

```bash
# Create virtual environment
python3 -m venv venv

# Activate virtual environment
# On macOS/Linux:
source venv/bin/activate

# You should see (venv) in your terminal prompt
```

### Step 4: Upgrade pip

```bash
pip install --upgrade pip
```

### Step 5: Install Backend Dependencies

```bash
cd backend
pip install -r requirements.txt
```

**What's being installed:**
- fastapi: Web framework
- uvicorn: ASGI server
- transformers: NLP models
- torch: Deep learning library
- scikit-learn: Machine learning
- PyPDF2, python-docx: File parsing

**Installation time**: 5-10 minutes (first time with model download: 10-20 minutes)

### Step 6: Run Backend Server

```bash
python run.py
```

**Expected output:**
```
============================================================
Document-Based Question Answering System
============================================================

Starting FastAPI server...
API will be available at: http://localhost:8000
API Documentation: http://localhost:8000/docs

Press Ctrl+C to stop the server
------------------------------------------------------------
INFO:     Uvicorn running on http://0.0.0.0:8000 (Press CTRL+C to quit)
INFO:     Application startup complete
```

### Step 7: Open Frontend

**Option A: Direct File Open (Simplest)**
```bash
open /Users/bvs/Documents/assignments/NLP/doc-qa-system/frontend/index.html
```

**Option B: Local HTTP Server (Better)**
```bash
# In a new terminal
cd /Users/bvs/Documents/assignments/NLP/doc-qa-system/frontend
python3 -m http.server 8001
```

Then open: `http://localhost:8001`

### Step 8: Test the Application

1. **Upload a document**
   - Click upload area
   - Choose a PDF, DOCX, or TXT file
   - Wait for confirmation

2. **Ask a question**
   - Type your question
   - Click "Ask Question"
   - View results with confidence scores

3. **Check API Documentation**
   - Open: `http://localhost:8000/docs`
   - Try endpoints directly in Swagger UI

## Troubleshooting

### Issue: `ModuleNotFoundError: No module named 'fastapi'`

**Solution**: Ensure virtual environment is activated
```bash
source venv/bin/activate
pip install -r requirements.txt
```

### Issue: Port 8000 already in use

**Solution**: Use different port
```bash
# Modify run.py to use port 8001
# OR kill existing process
lsof -i :8000  # Find process
kill -9 <PID>  # Kill it
```

### Issue: Model download timeout

**Solution**: Download manually
```bash
# Pre-download model
python -c "from transformers import pipeline; pipeline('question-answering')"
```

### Issue: Out of memory error

**Solution**: Use smaller model
```python
# In backend/app/services/qa_engine.py
# Change to: model_name="distilbert-base-uncased-distilled-squad"
```

### Issue: CORS error in browser console

**Solution**: Already enabled in FastAPI. Check:
1. Backend is running on localhost:8000
2. Frontend can access http://localhost:8000/api
3. Try different browser

### Issue: Frontend shows "No documents uploaded yet" after upload

**Debugging steps**:
1. Check browser console (F12)
2. Check API response in Network tab
3. Verify backend logs in terminal
4. Try direct API call:
```bash
curl "http://localhost:8000/api/documents/list"
```

## File Structure Reference

```
doc-qa-system/
├── backend/
│   ├── app/
│   │   ├── main.py              ← FastAPI app
│   │   ├── models/
│   │   │   └── schemas.py       ← Data models
│   │   ├── routes/
│   │   │   ├── documents.py     ← Upload endpoints
│   │   │   └── qa.py            ← QA endpoints
│   │   ├── services/
│   │   │   ├── qa_engine.py     ← QA processing
│   │   │   └── document_indexer.py
│   │   └── utils/
│   │       └── document_processor.py
│   ├── requirements.txt         ← Dependencies
│   └── run.py                   ← Start server
│
├── frontend/
│   ├── index.html               ← Main page
│   └── static/
│       ├── css/style.css
│       └── js/app.js
│
└── docs/
    ├── API_DOCUMENTATION.md
    ├── DESIGN_CHOICES.md
    └── ENHANCEMENT_PLAN.md
```

## Development Commands

```bash
# Start backend (with auto-reload)
python run.py

# View API documentation
# Open: http://localhost:8000/docs

# Run tests (if tests directory exists)
pytest

# Format code
black app/

# Check code style
flake8 app/

# Deactivate virtual environment
deactivate
```

## Performance Tips

1. **First Query**: Models are lazy-loaded, first query will be slow (5-10 sec)
2. **GPU Support**: If you have NVIDIA GPU, install:
   ```bash
   pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118
   ```
3. **Larger Models**: For better accuracy, modify `qa_engine.py`:
   ```python
   model_name="deepset/xlm-roberta-large-finetuned-squad2"
   ```

## Sample Test Files

For testing, use these sample documents:

**test1.txt**:
```
Artificial Intelligence (AI) is the simulation of human intelligence processes 
by computer systems. These processes include learning, reasoning, and self-correction.
Machine Learning is a subset of AI that enables systems to learn from data 
without being explicitly programmed.
```

**Sample Questions**:
- "What is artificial intelligence?"
- "What is machine learning?"
- "How does AI relate to machine learning?"

## Next Steps

1. **Read the documentation**:
   - `docs/DESIGN_CHOICES.md` - Understand design decisions
   - `docs/API_DOCUMENTATION.md` - Learn all API endpoints
   - `docs/ENHANCEMENT_PLAN.md` - Future improvements

2. **Test thoroughly**:
   - Try with different document types
   - Test various question formats
   - Check confidence scores

3. **Customize**:
   - Modify colors in `frontend/static/css/style.css`
   - Change QA model in `backend/app/services/qa_engine.py`
   - Add new API endpoints in `backend/app/routes/`

4. **Deploy**:
   - See README.md for production deployment options
   - Docker containerization possible
   - Cloud deployment (AWS, Azure, GCP) ready

## Getting Help

1. **API Issues**: Check `http://localhost:8000/docs` (Swagger UI)
2. **Backend Logs**: Check terminal running `python run.py`
3. **Browser Errors**: Open DevTools (F12) → Console tab
4. **Model Issues**: Ensure `~/.cache/huggingface/` has ~500MB space

## Uninstall/Cleanup

```bash
# Deactivate virtual environment
deactivate

# Remove virtual environment
rm -rf venv

# Remove cached models (optional, saves 500MB)
rm -rf ~/.cache/huggingface/

# Remove temporary uploads (if any)
rm -rf /tmp/qa_uploads
```

---

**Congratulations! Your Document-Based QA System is ready to use!** 🎉
