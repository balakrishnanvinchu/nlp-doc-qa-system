"""
Document upload and management routes
"""
import os
import time
from fastapi import APIRouter, UploadFile, File, HTTPException
from app.models.schemas import DocumentResponse, DocumentListResponse, DocumentMetadata, ErrorResponse
from app.services.document_indexer import DocumentIndexer
from app.utils.document_processor import DocumentProcessor

router = APIRouter(prefix="/api/documents", tags=["documents"])

# Initialize the document indexer
indexer = DocumentIndexer()


@router.post("/upload", response_model=DocumentResponse)
async def upload_document(file: UploadFile = File(...)):
    """
    Upload and process a document
    
    Supported formats: PDF, DOCX, TXT
    """
    try:
        # Validate file extension
        if not DocumentProcessor.is_valid_file(file.filename):
            raise HTTPException(
                status_code=400,
                detail=f"Unsupported file format. Allowed: PDF, DOCX, TXT"
            )
        
        # Save uploaded file temporarily
        upload_dir = "/tmp/qa_uploads"
        os.makedirs(upload_dir, exist_ok=True)
        
        file_path = os.path.join(upload_dir, file.filename)
        contents = await file.read()
        
        with open(file_path, 'wb') as f:
            f.write(contents)
        
        # Process document
        doc_id, text_length, num_passages = indexer.add_document(file_path, file.filename)
        
        # Clean up temporary file
        os.remove(file_path)
        
        return DocumentResponse(
            message="Document uploaded and processed successfully",
            doc_id=doc_id,
            filename=file.filename
        )
    
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/list", response_model=DocumentListResponse)
async def list_documents():
    """Get list of all uploaded documents"""
    try:
        documents = indexer.get_all_documents()
        return DocumentListResponse(
            documents=[DocumentMetadata(**doc) for doc in documents],
            total_count=len(documents)
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.delete("/{doc_id}")
async def delete_document(doc_id: str):
    """Delete a document by ID"""
    try:
        if indexer.delete_document(doc_id):
            return {"message": "Document deleted successfully", "doc_id": doc_id}
        else:
            raise HTTPException(status_code=404, detail="Document not found")
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/stats")
async def get_statistics():
    """Get indexing statistics"""
    try:
        stats = indexer.get_statistics()
        return stats
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/clear")
async def clear_all_documents():
    """Clear all documents (for testing)"""
    try:
        indexer.clear_all()
        return {"message": "All documents cleared"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


def get_indexer():
    """Get the document indexer instance (for use in other routes)"""
    return indexer
