"""
Document indexing and storage service
"""
import uuid
from datetime import datetime
from typing import Dict, List, Tuple, Optional
from app.utils.document_processor import DocumentProcessor
from pathlib import Path


class DocumentIndexer:
    """Manages document storage and indexing"""
    
    def __init__(self):
        """Initialize the document indexer with in-memory storage"""
        self.documents: Dict[str, Dict] = {}  # {doc_id: {metadata, text, passages}}
        self.doc_counter = 0
    
    def add_document(
        self,
        file_path: str,
        filename: str,
        passage_window: int = 3
    ) -> Tuple[str, int, int]:
        """
        Add a document to the index
        
        Args:
            file_path: Path to the uploaded document
            filename: Original filename
            passage_window: Window size for creating passages (in sentences)
            
        Returns:
            Tuple of (doc_id, text_length, num_passages)
        """
        try:
            # Extract text from document
            text = DocumentProcessor.extract_text(file_path)
            
            # Clean text
            text = DocumentProcessor.clean_text(text)
            
            if not text:
                raise ValueError("Document is empty after extraction")
            
            # Create passages
            passages = DocumentProcessor.split_into_passages(text, passage_window)
            
            # Generate unique ID
            doc_id = str(uuid.uuid4())
            
            # Store document metadata and content
            self.documents[doc_id] = {
                "filename": filename,
                "upload_time": datetime.now().isoformat(),
                "text": text,
                "text_length": len(text),
                "passages": passages,
                "num_passages": len(passages),
                "num_sentences": len(DocumentProcessor.split_into_sentences(text))
            }
            
            self.doc_counter += 1
            
            return doc_id, len(text), len(passages)
        
        except Exception as e:
            raise ValueError(f"Error processing document: {str(e)}")
    
    def get_document(self, doc_id: str) -> Optional[Dict]:
        """Get document by ID"""
        return self.documents.get(doc_id)
    
    def get_all_documents(self) -> List[Dict]:
        """Get metadata for all documents"""
        documents_list = []
        for doc_id, doc_data in self.documents.items():
            documents_list.append({
                "doc_id": doc_id,
                "filename": doc_data["filename"],
                "upload_time": doc_data["upload_time"],
                "text_length": doc_data["text_length"],
                "num_sentences": doc_data["num_sentences"],
                "num_passages": doc_data["num_passages"]
            })
        return documents_list
    
    def delete_document(self, doc_id: str) -> bool:
        """Delete a document from the index"""
        if doc_id in self.documents:
            del self.documents[doc_id]
            self.doc_counter -= 1
            return True
        return False
    
    def get_all_passages(self) -> List[Tuple[str, str, int, int]]:
        """
        Get all passages from all documents
        
        Returns:
            List of (passage_text, doc_id, start_pos, end_pos) tuples
        """
        all_passages = []
        for doc_id, doc_data in self.documents.items():
            for passage, start_pos, end_pos in doc_data["passages"]:
                all_passages.append((passage, doc_id, start_pos, end_pos))
        return all_passages
    
    def get_document_passages(self, doc_id: str) -> List[Tuple[str, int, int]]:
        """Get passages for a specific document"""
        doc = self.get_document(doc_id)
        if doc:
            return doc["passages"]
        return []
    
    def search_documents(self, keyword: str) -> List[Dict]:
        """Search documents by keyword"""
        results = []
        keyword_lower = keyword.lower()
        
        for doc_id, doc_data in self.documents.items():
            if keyword_lower in doc_data["text"].lower():
                results.append({
                    "doc_id": doc_id,
                    "filename": doc_data["filename"],
                    "matches": doc_data["text"].lower().count(keyword_lower)
                })
        
        return sorted(results, key=lambda x: x["matches"], reverse=True)
    
    def get_document_text(self, doc_id: str) -> Optional[str]:
        """Get full text of a document"""
        doc = self.get_document(doc_id)
        if doc:
            return doc["text"]
        return None
    
    def clear_all(self) -> None:
        """Clear all documents from the index"""
        self.documents.clear()
        self.doc_counter = 0
    
    def get_statistics(self) -> Dict:
        """Get indexing statistics"""
        total_documents = len(self.documents)
        total_text_length = sum(d["text_length"] for d in self.documents.values())
        total_passages = sum(d["num_passages"] for d in self.documents.values())
        
        return {
            "total_documents": total_documents,
            "total_text_length": total_text_length,
            "total_passages": total_passages,
            "avg_doc_size": total_text_length / total_documents if total_documents > 0 else 0
        }
