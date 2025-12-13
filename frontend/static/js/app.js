// Frontend JavaScript for Doc-QA System

const API_BASE_URL = 'http://localhost:8000/api';

// Initialize event listeners
document.addEventListener('DOMContentLoaded', function() {
    setupUploadArea();
    loadDocuments();
});

// ==================== Upload Area Setup ====================

function setupUploadArea() {
    const uploadArea = document.getElementById('uploadArea');
    const fileInput = document.getElementById('fileInput');

    // Click to upload
    uploadArea.addEventListener('click', () => fileInput.click());

    // Drag and drop
    uploadArea.addEventListener('dragover', (e) => {
        e.preventDefault();
        uploadArea.classList.add('dragover');
    });

    uploadArea.addEventListener('dragleave', () => {
        uploadArea.classList.remove('dragover');
    });

    uploadArea.addEventListener('drop', (e) => {
        e.preventDefault();
        uploadArea.classList.remove('dragover');
        handleFiles(e.dataTransfer.files);
    });

    // File input change
    fileInput.addEventListener('change', (e) => {
        handleFiles(e.target.files);
    });
}

function handleFiles(files) {
    const validFiles = Array.from(files).filter(file => {
        const ext = file.name.split('.').pop().toLowerCase();
        return ['pdf', 'docx', 'txt'].includes(ext);
    });

    if (validFiles.length === 0) {
        showError('Please upload PDF, DOCX, or TXT files only');
        return;
    }

    validFiles.forEach(file => uploadDocument(file));
}

async function uploadDocument(file) {
    const formData = new FormData();
    formData.append('file', file);

    try {
        showLoading(true);
        const response = await fetch(`${API_BASE_URL}/documents/upload`, {
            method: 'POST',
            body: formData
        });

        if (!response.ok) {
            throw new Error('Failed to upload document');
        }

        const data = await response.json();
        loadDocuments();
        showLoading(false);
    } catch (error) {
        showError(`Upload failed: ${error.message}`);
        showLoading(false);
    }
}

// ==================== Document Management ====================

async function loadDocuments() {
    try {
        const response = await fetch(`${API_BASE_URL}/documents/list`);
        if (!response.ok) {
            throw new Error('Failed to load documents');
        }

        const data = await response.json();
        displayDocuments(data.documents);
    } catch (error) {
        console.error('Error loading documents:', error);
    }
}

function displayDocuments(documents) {
    const container = document.getElementById('documentsList');

    if (documents.length === 0) {
        container.innerHTML = '<p class="text-muted small">No documents uploaded yet</p>';
        return;
    }

    container.innerHTML = documents.map(doc => `
        <div class="document-item">
            <div class="flex-grow-1">
                <div class="document-name">📄 ${escapeHtml(doc.filename)}</div>
                <div class="document-meta">
                    ${formatDate(doc.upload_time)} • ${doc.num_sentences} sentences
                </div>
            </div>
            <button class="delete-btn" onclick="deleteDocument('${doc.doc_id}', '${escapeHtml(doc.filename)}')" 
                    title="Delete document">✕</button>
        </div>
    `).join('');
}

async function deleteDocument(docId, filename) {
    if (!confirm(`Are you sure you want to delete "${filename}"?`)) {
        return;
    }

    try {
        const response = await fetch(`${API_BASE_URL}/documents/${docId}`, {
            method: 'DELETE'
        });

        if (!response.ok) {
            throw new Error('Failed to delete document');
        }

        loadDocuments();
    } catch (error) {
        showError(`Delete failed: ${error.message}`);
    }
}

// ==================== Question Answering ====================

async function askQuestion() {
    const question = document.getElementById('questionInput').value.trim();
    const topK = parseInt(document.getElementById('topK').value);

    if (!question) {
        showError('Please enter a question');
        return;
    }

    try {
        showLoading(true);
        const response = await fetch(`${API_BASE_URL}/qa/ask`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ question, top_k: topK })
        });

        if (!response.ok) {
            const error = await response.json();
            throw new Error(error.detail || 'Failed to get answer');
        }

        const data = await response.json();
        displayResults(data);
        showLoading(false);
    } catch (error) {
        showError(error.message);
        showLoading(false);
    }
}

async function askQuestionDirect() {
    const text = document.getElementById('directText').value.trim();
    const question = document.getElementById('directQuestion').value.trim();
    const topK = parseInt(document.getElementById('directTopK').value);

    if (!text || !question) {
        showError('Please enter both text and question');
        return;
    }

    try {
        showLoading(true);
        const response = await fetch(`${API_BASE_URL}/qa/ask-direct`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ text, question, top_k: topK })
        });

        if (!response.ok) {
            const error = await response.json();
            throw new Error(error.detail || 'Failed to get answer');
        }

        const data = await response.json();
        displayResults(data);
        showLoading(false);
    } catch (error) {
        showError(error.message);
        showLoading(false);
    }
}

function displayResults(data) {
    document.getElementById('welcomeMessage').style.display = 'none';
    document.getElementById('resultsSection').style.display = 'block';

    document.getElementById('questionDisplay').textContent = data.question;
    document.getElementById('processingTime').textContent = 
        `Processing time: ${data.processing_time}s`;

    if (data.answers.length === 0) {
        document.getElementById('answersContainer').innerHTML = 
            '<p class="alert alert-warning">No answers found. Try different question or documents.</p>';
        return;
    }

    const answersHTML = data.answers.map((answer, index) => {
        const confidence = answer.confidence_score;
        const confidenceClass = confidence > 0.7 ? 'high' : confidence > 0.4 ? 'medium' : 'low';
        
        return `
            <div class="answer-card ${confidenceClass}-confidence">
                <div class="answer-text">
                    <strong>Answer ${index + 1}:</strong> ${escapeHtml(answer.answer)}
                </div>
                <div>
                    <span class="confidence-score confidence-${confidenceClass}">
                        Confidence: ${(confidence * 100).toFixed(1)}%
                    </span>
                </div>
                <div class="source-info">
                    <div class="source-label">Source Information</div>
                    <div class="source-document">📄 ${escapeHtml(answer.source_document)}</div>
                    <div class="source-text">
                        "${escapeHtml(answer.source_text.substring(0, 200))}${answer.source_text.length > 200 ? '...' : ''}"
                    </div>
                </div>
            </div>
        `;
    }).join('');

    document.getElementById('answersContainer').innerHTML = answersHTML;
}

// ==================== Utility Functions ====================

function showLoading(show) {
    document.getElementById('loadingIndicator').style.display = show ? 'block' : 'none';
}

function showError(message) {
    const errorDiv = document.getElementById('errorMessage');
    document.getElementById('errorText').textContent = message;
    errorDiv.style.display = 'block';
    
    // Auto-hide after 6 seconds
    setTimeout(() => {
        errorDiv.style.display = 'none';
    }, 6000);
}

function escapeHtml(text) {
    const div = document.createElement('div');
    div.textContent = text;
    return div.innerHTML;
}

function formatDate(dateString) {
    const date = new Date(dateString);
    return new Intl.DateTimeFormat('en-US', {
        month: 'short',
        day: 'numeric',
        hour: '2-digit',
        minute: '2-digit'
    }).format(date);
}
