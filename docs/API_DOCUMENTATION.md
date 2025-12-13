# API Documentation

## Base URL
```
http://localhost:8000/api
```

## Authentication
None (open API for this version)

## Response Format
All endpoints return JSON responses with the following structure:

### Success Response
```json
{
  "data": {},
  "message": "Success message",
  "status": "success"
}
```

### Error Response
```json
{
  "error": "Error message",
  "details": "Detailed error information",
  "status": "error"
}
```

---

## Document Management Endpoints

### 1. Upload Document

**Endpoint**: `POST /documents/upload`

**Description**: Upload and process a document (PDF, DOCX, or TXT)

**Request**:
- Method: POST
- Content-Type: multipart/form-data
- Parameters:
  - `file` (File, required): Document file to upload

**Response** (200 OK):
```json
{
  "message": "Document uploaded and processed successfully",
  "doc_id": "550e8400-e29b-41d4-a716-446655440000",
  "filename": "document.pdf"
}
```

**Error Responses**:
- 400 Bad Request: Invalid file format
- 500 Internal Server Error: File processing error

**Examples**:

Using curl:
```bash
curl -X POST "http://localhost:8000/api/documents/upload" \
  -F "file=@/path/to/document.pdf"
```

Using JavaScript:
```javascript
const formData = new FormData();
formData.append('file', fileInput.files[0]);

fetch('http://localhost:8000/api/documents/upload', {
  method: 'POST',
  body: formData
})
.then(response => response.json())
.then(data => console.log(data));
```

---

### 2. List Documents

**Endpoint**: `GET /documents/list`

**Description**: Retrieve list of all uploaded documents with metadata

**Request**:
- Method: GET
- Parameters: None

**Response** (200 OK):
```json
{
  "documents": [
    {
      "doc_id": "550e8400-e29b-41d4-a716-446655440000",
      "filename": "document.pdf",
      "upload_time": "2024-12-12T10:30:45.123456",
      "text_length": 5000,
      "num_sentences": 150
    }
  ],
  "total_count": 1
}
```

**Examples**:

Using curl:
```bash
curl "http://localhost:8000/api/documents/list"
```

Using JavaScript:
```javascript
fetch('http://localhost:8000/api/documents/list')
  .then(response => response.json())
  .then(data => console.log(data.documents));
```

---

### 3. Delete Document

**Endpoint**: `DELETE /documents/{doc_id}`

**Description**: Remove a document from the system

**Request**:
- Method: DELETE
- URL Parameters:
  - `doc_id` (string, required): Unique identifier of the document

**Response** (200 OK):
```json
{
  "message": "Document deleted successfully",
  "doc_id": "550e8400-e29b-41d4-a716-446655440000"
}
```

**Error Responses**:
- 404 Not Found: Document ID not found

**Examples**:

Using curl:
```bash
curl -X DELETE "http://localhost:8000/api/documents/550e8400-e29b-41d4-a716-446655440000"
```

---

### 4. Get Statistics

**Endpoint**: `GET /documents/stats`

**Description**: Get indexing and storage statistics

**Request**:
- Method: GET
- Parameters: None

**Response** (200 OK):
```json
{
  "total_documents": 5,
  "total_text_length": 50000,
  "total_passages": 450,
  "avg_doc_size": 10000
}
```

---

### 5. Clear All Documents

**Endpoint**: `POST /documents/clear`

**Description**: Remove all documents from the system (for testing)

**Request**:
- Method: POST
- Parameters: None

**Response** (200 OK):
```json
{
  "message": "All documents cleared"
}
```

---

## Question Answering Endpoints

### 1. Ask Question on Uploaded Documents

**Endpoint**: `POST /qa/ask`

**Description**: Submit a question to be answered based on uploaded documents

**Request**:
- Method: POST
- Content-Type: application/json
- Body:
```json
{
  "question": "What is the main topic?",
  "top_k": 3
}
```

**Parameters**:
- `question` (string, required): User's question
- `top_k` (integer, optional): Number of top answers to return (default: 3, max: 5)

**Response** (200 OK):
```json
{
  "question": "What is the main topic?",
  "answers": [
    {
      "answer": "The main topic is artificial intelligence.",
      "confidence_score": 0.8542,
      "source_document": "document.pdf",
      "source_text": "The main topic is artificial intelligence and its applications in modern society.",
      "start_position": 50,
      "end_position": 51
    },
    {
      "answer": "AI and machine learning are discussed extensively.",
      "confidence_score": 0.7213,
      "source_document": "document.pdf",
      "source_text": "AI and machine learning are discussed extensively throughout the document.",
      "start_position": 120,
      "end_position": 121
    }
  ],
  "processing_time": 1.235
}
```

**Response Fields**:
- `question`: The question that was asked
- `answers`: Array of answer objects
  - `answer`: Extracted answer text
  - `confidence_score`: Score between 0-1 (higher = more confident)
  - `source_document`: Filename of source document
  - `source_text`: The passage from which answer was extracted
  - `start_position`: Starting position in document (index)
  - `end_position`: Ending position in document (index)
- `processing_time`: Time taken to process in seconds

**Error Responses**:
- 400 Bad Request: No documents uploaded or invalid question
- 500 Internal Server Error: Processing error

**Examples**:

Using curl:
```bash
curl -X POST "http://localhost:8000/api/qa/ask" \
  -H "Content-Type: application/json" \
  -d '{
    "question": "What is the main topic?",
    "top_k": 3
  }'
```

Using JavaScript:
```javascript
const question = "What is the main topic?";

fetch('http://localhost:8000/api/qa/ask', {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json'
  },
  body: JSON.stringify({
    question: question,
    top_k: 3
  })
})
.then(response => response.json())
.then(data => {
  data.answers.forEach(answer => {
    console.log(`Answer: ${answer.answer}`);
    console.log(`Confidence: ${(answer.confidence_score * 100).toFixed(1)}%`);
  });
});
```

---

### 2. Ask Question on Direct Text

**Endpoint**: `POST /qa/ask-direct`

**Description**: Submit a question to be answered based on directly provided text

**Request**:
- Method: POST
- Content-Type: application/json
- Body:
```json
{
  "text": "Artificial Intelligence (AI) is transforming industries. Machine learning is a subset of AI that enables systems to learn from data.",
  "question": "What is machine learning?",
  "top_k": 2
}
```

**Parameters**:
- `text` (string, required): Document text to process
- `question` (string, required): User's question
- `top_k` (integer, optional): Number of top answers (default: 3, max: 5)

**Response** (200 OK):
```json
{
  "question": "What is machine learning?",
  "answers": [
    {
      "answer": "Machine learning is a subset of AI that enables systems to learn from data.",
      "confidence_score": 0.9234,
      "source_document": "Direct Input",
      "source_text": "Machine learning is a subset of AI that enables systems to learn from data.",
      "start_position": 0,
      "end_position": 1
    }
  ],
  "processing_time": 0.845
}
```

**Error Responses**:
- 400 Bad Request: Missing text or question field
- 500 Internal Server Error: Processing error

**Examples**:

Using curl:
```bash
curl -X POST "http://localhost:8000/api/qa/ask-direct" \
  -H "Content-Type: application/json" \
  -d '{
    "text": "Your document text here...",
    "question": "What is the main topic?",
    "top_k": 3
  }'
```

---

### 3. Health Check

**Endpoint**: `GET /qa/health`

**Description**: Check if QA engine is ready and loaded

**Request**:
- Method: GET
- Parameters: None

**Response** (200 OK):
```json
{
  "status": "healthy",
  "qa_engine": "ready",
  "model": "deepset/roberta-base-squad2"
}
```

---

## Status Codes

| Code | Meaning |
|------|---------|
| 200 | Success |
| 400 | Bad Request (invalid parameters) |
| 404 | Not Found (document/resource doesn't exist) |
| 500 | Internal Server Error |

## Rate Limiting

No rate limiting implemented (can be added for production)

## Pagination

No pagination implemented for document listing (can be added for large collections)

## CORS

CORS is enabled for all origins. Safe for development/testing.

## Error Handling

All errors include a detailed error message:

```json
{
  "error": "Document not found",
  "details": "The specified document ID does not exist"
}
```

## Best Practices

1. **Always check response status**: Verify the API returns 200 OK before processing response
2. **Handle long documents**: Documents >512 tokens are truncated for QA processing
3. **Use meaningful questions**: More specific questions generally yield better answers
4. **Monitor confidence scores**: Scores <0.4 may be less reliable
5. **Implement error handling**: Always catch network and parsing errors

## Limits

- Maximum file size: 50 MB
- Maximum text length: 1 million characters
- Maximum question length: 512 characters
- QA context window: 512 tokens

## Future Enhancements

- Batch question processing
- Document search/filtering
- Custom model loading
- Answer highlighting in source documents
- Session-based document management
- Export answers as PDF
