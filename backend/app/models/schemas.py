"""
Data models and schemas for the QA application
"""
from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime


class AnswerResult(BaseModel):
    """Model for answer results"""
    answer: str
    confidence_score: float
    source_document: str
    source_text: str
    start_position: int
    end_position: int


class QuestionRequest(BaseModel):
    """Model for question requests"""
    question: str
    top_k: int = 3


class DocumentMetadata(BaseModel):
    """Model for document metadata"""
    doc_id: str
    filename: str
    upload_time: datetime
    text_length: int
    num_sentences: int


class DocumentResponse(BaseModel):
    """Response model for document operations"""
    message: str
    doc_id: str
    filename: str


class DocumentListResponse(BaseModel):
    """Response model for listing documents"""
    documents: List[DocumentMetadata]
    total_count: int


class QAResponse(BaseModel):
    """Response model for QA queries"""
    question: str
    answers: List[AnswerResult]
    processing_time: float


class DirectTextRequest(BaseModel):
    """Model for direct text input"""
    text: str
    question: str
    top_k: int = 3


class ErrorResponse(BaseModel):
    """Model for error responses"""
    error: str
    details: Optional[str] = None
