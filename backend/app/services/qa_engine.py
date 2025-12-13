"""
Question Answering engine using Hugging Face transformers
"""
from typing import List, Tuple, Dict
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from transformers import pipeline
import warnings

warnings.filterwarnings('ignore')


class QAEngine:
    """Handles question answering using pre-trained models"""
    
    def __init__(self, model_name: str = "deepset/roberta-base-squad2"):
        """
        Initialize QA engine with a pre-trained model
        
        Args:
            model_name: HuggingFace model identifier
        """
        self.model_name = model_name
        try:
            self.qa_pipeline = pipeline("question-answering", model=model_name)
            print(f"Loaded QA model: {model_name}")
        except Exception as e:
            print(f"Error loading model {model_name}: {str(e)}")
            # Fallback to a lighter model
            self.qa_pipeline = pipeline("question-answering")
    
    def retrieve_relevant_passages(
        self,
        question: str,
        passages: List[str],
        top_k: int = 3
    ) -> List[Tuple[str, float, int]]:
        """
        Retrieve most relevant passages for a question using TF-IDF similarity
        
        Args:
            question: User's question
            passages: List of document passages
            top_k: Number of top passages to return
            
        Returns:
            List of (passage, similarity_score, index) tuples
        """
        if not passages:
            return []
        
        try:
            # Create TF-IDF vectors
            vectorizer = TfidfVectorizer(
                max_features=500,
                stop_words='english',
                lowercase=True
            )
            
            # Combine question and passages for vectorization
            all_texts = [question] + passages
            tfidf_matrix = vectorizer.fit_transform(all_texts)
            
            # Calculate similarity between question and each passage
            question_vector = tfidf_matrix[0]
            passage_vectors = tfidf_matrix[1:]
            
            similarities = cosine_similarity(question_vector, passage_vectors)[0]
            
            # Get top k passages (even if similarity is low, we need at least some passages to work with)
            top_k_indices = np.argsort(similarities)[::-1][:top_k]
            
            results = [
                (passages[idx], float(similarities[idx]), idx)
                for idx in top_k_indices
            ]
            
            return results
        
        except Exception as e:
            print(f"Error in passage retrieval: {str(e)}")
            return []
    
    def answer_question(
        self,
        question: str,
        context: str,
        max_answer_length: int = 512
    ) -> Dict:
        """
        Extract answer from context for a given question
        
        Args:
            question: User's question
            context: Document context/passage
            max_answer_length: Maximum length of answer
            
        Returns:
            Dictionary with answer, score, and positions
        """
        if not context or not question:
            return {
                "answer": "",
                "score": 0.0,
                "start": 0,
                "end": 0
            }
        
        try:
            # Ensure context is not too long
            if len(context) > 512:
                context = context[:512]
            
            result = self.qa_pipeline(
                question=question,
                context=context,
                max_answer_len=min(max_answer_length, len(context))
            )
            
            return {
                "answer": result.get("answer", ""),
                "score": float(result.get("score", 0.0)),
                "start": result.get("start", 0),
                "end": result.get("end", 0)
            }
        
        except Exception as e:
            print(f"Error in QA processing: {str(e)}")
            return {
                "answer": "",
                "score": 0.0,
                "start": 0,
                "end": 0
            }
    
    def process_question(
        self,
        question: str,
        passages: List[Tuple[str, int, int]],
        top_k: int = 3
    ) -> List[Dict]:
        """
        Process a question against multiple passages and return answers
        
        Args:
            question: User's question
            passages: List of (passage_text, start_pos, end_pos) tuples
            top_k: Number of top answers to return
            
        Returns:
            List of answer dictionaries sorted by confidence score
        """
        if not passages:
            return []
        
        passage_texts = [p[0] for p in passages]
        
        # Retrieve relevant passages (now returns top_k without strict filtering)
        relevant = self.retrieve_relevant_passages(question, passage_texts, top_k)
        
        if not relevant:
            # Fallback: if no relevant passages found, try all passages
            relevant = [(p, 0.0, i) for i, p in enumerate(passage_texts[:top_k])]
        
        answers = []
        for passage, similarity_score, idx in relevant:
            # Get QA result
            qa_result = self.answer_question(question, passage)
            
            if qa_result["answer"] and qa_result["score"] > 0:
                # Combine similarity and QA scores
                # Weight QA score more heavily since it's more reliable
                combined_score = (similarity_score * 0.2 + qa_result["score"] * 0.8)
                
                answers.append({
                    "answer": qa_result["answer"],
                    "confidence_score": combined_score,
                    "source_text": passage,
                    "source_position": idx,
                    "qa_score": qa_result["score"],
                    "similarity_score": similarity_score
                })
        
        # Sort by confidence score
        answers.sort(key=lambda x: x["confidence_score"], reverse=True)
        
        # Return top_k answers, or at least try to return something if we have any answer
        return answers[:top_k] if answers else []
