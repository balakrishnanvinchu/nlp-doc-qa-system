"""
Question answering routes
"""
import time
from fastapi import APIRouter, HTTPException
from app.models.schemas import QuestionRequest, DirectTextRequest, QAResponse, AnswerResult
from app.services.qa_engine import QAEngine
from app.services.document_indexer import DocumentIndexer
from app.utils.document_processor import DocumentProcessor
from app.routes.documents import get_indexer

router = APIRouter(prefix="/api/qa", tags=["qa"])

# Initialize QA engine
qa_engine = QAEngine()


@router.post("/ask", response_model=QAResponse)
async def ask_question(request: QuestionRequest):
    """
    Ask a question based on uploaded documents
    
    Returns answers with source references and confidence scores
    """
    try:
        indexer = get_indexer()
        
        # Get all passages from uploaded documents
        all_passages = indexer.get_all_passages()
        
        if not all_passages:
            raise HTTPException(
                status_code=400,
                detail="No documents uploaded. Please upload documents first."
            )
        
        start_time = time.time()
        
        # Process question
        passages_only = [p[0] for p in all_passages]
        answers = qa_engine.process_question(
            request.question,
            [(p[0], p[2], p[3]) for p in all_passages],
            top_k=request.top_k
        )
        
        # Format results
        answer_results = []
        for answer in answers:
            # Find source document for this passage
            passage_text = answer["source_text"]
            source_doc_id = None
            
            for passage, doc_id, start_pos, end_pos in all_passages:
                if passage == passage_text:
                    source_doc_id = doc_id
                    break
            
            source_doc = indexer.get_document(source_doc_id) if source_doc_id else None
            source_filename = source_doc["filename"] if source_doc else "Unknown"
            
            answer_results.append(
                AnswerResult(
                    answer=answer["answer"],
                    confidence_score=round(answer["confidence_score"], 4),
                    source_document=source_filename,
                    source_text=answer["source_text"],
                    start_position=answer["source_position"],
                    end_position=answer["source_position"] + 1
                )
            )
        
        processing_time = time.time() - start_time
        
        return QAResponse(
            question=request.question,
            answers=answer_results,
            processing_time=round(processing_time, 3)
        )
    
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/ask-direct", response_model=QAResponse)
async def ask_question_direct(request: DirectTextRequest):
    """
    Ask a question on directly provided text without uploading documents
    
    Useful for ad-hoc queries
    """
    try:
        if not request.text or not request.question:
            raise HTTPException(
                status_code=400,
                detail="Both text and question fields are required"
            )
        
        start_time = time.time()
        
        # Clean and process text
        text = DocumentProcessor.clean_text(request.text)
        passages = DocumentProcessor.split_into_passages(text, window_size=3)
        
        # Process question
        answers = qa_engine.process_question(
            request.question,
            passages,
            top_k=request.top_k
        )
        
        # Format results
        answer_results = []
        for answer in answers:
            answer_results.append(
                AnswerResult(
                    answer=answer["answer"],
                    confidence_score=round(answer["confidence_score"], 4),
                    source_document="Direct Input",
                    source_text=answer["source_text"],
                    start_position=answer["source_position"],
                    end_position=answer["source_position"] + 1
                )
            )
        
        processing_time = time.time() - start_time
        
        return QAResponse(
            question=request.question,
            answers=answer_results,
            processing_time=round(processing_time, 3)
        )
    
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "qa_engine": "ready",
        "model": qa_engine.model_name
    }
