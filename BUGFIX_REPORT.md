# Bug Fix Report: "No answers found" Issue

## Issue Description
When asking questions about uploaded documents, the system was returning "No answers found. Try different question or documents." message regardless of the documents or questions asked.

## Root Cause Analysis

The issue was in the `qa_engine.py` file, specifically in two methods:

### 1. `retrieve_relevant_passages()` - Over-filtering Passages
**Problem:** The method was filtering out passages with similarity scores of 0 or very low values:
```python
results = [
    (passages[idx], float(similarities[idx]), idx)
    for idx in top_k_indices
    if similarities[idx] > 0  # ← This condition was too strict
]
```

This caused legitimate passages to be excluded, especially when:
- All passages had very low similarity scores to the question
- The TF-IDF vectorizer couldn't find good matches

**Solution:** Remove the `if similarities[idx] > 0` condition and return the top-k passages regardless of their similarity score:
```python
results = [
    (passages[idx], float(similarities[idx]), idx)
    for idx in top_k_indices
]
```

### 2. `process_question()` - Loose Answer Filtering and Poor Score Weighting
**Problems:**
- The scoring algorithm weighted similarity and QA scores equally (30% + 70%), making low-scoring answers unlikely to return
- No fallback mechanism when no relevant passages were found

**Solutions:**
- Changed the scoring weight to favor QA scores more heavily (20% similarity + 80% QA score)
- Added explicit filtering to only accept answers with QA score > 0
- Added a fallback to use all passages if no relevant ones were found

Old code:
```python
combined_score = (similarity_score * 0.3 + qa_result["score"] * 0.7)
```

New code:
```python
if qa_result["answer"] and qa_result["score"] > 0:
    combined_score = (similarity_score * 0.2 + qa_result["score"] * 0.8)
```

## Changes Made

### File: `backend/app/services/qa_engine.py`

1. **`retrieve_relevant_passages()` method (lines ~30-65):**
   - Removed the `if similarities[idx] > 0` filter condition
   - Now returns top-k passages even with low similarity scores
   - Ensures we always have passages to process

2. **`process_question()` method (lines ~140-180):**
   - Changed confidence score weighting from (30%, 70%) to (20%, 80%)
   - Added condition to only include answers with QA score > 0
   - Added fallback mechanism that uses all passages if no relevant ones are found
   - Improved robustness by returning empty list instead of incomplete results

## How It Works Now

1. **Passage Retrieval:** Gets the top-k most similar passages (no strict filtering)
2. **Answer Extraction:** For each passage, extracts an answer using the QA model
3. **Score Calculation:** Combines similarity and QA confidence scores (weighted towards QA model)
4. **Filtering:** Only keeps answers with valid QA scores
5. **Ranking:** Returns top answers sorted by combined confidence score
6. **Fallback:** If initial retrieval fails, tries with all available passages

## Testing

To test the fix:

1. Upload a document (PDF, DOCX, or TXT)
2. Ask a question about the document
3. The system should now return relevant answers with confidence scores

### Example Test Case
**Document:** "Machine Learning (ML) is a subset of Artificial Intelligence (AI) that enables systems to learn from data without being explicitly programmed."

**Question:** "What is machine learning?"

**Expected Result:** Answer about machine learning with a high confidence score (>0.7)

## Performance Impact

- **Positive:** System now returns answers instead of "No answers found"
- **Neutral:** Minimal performance impact; the change actually removes unnecessary filtering operations
- **Quality:** Answers may have slightly lower confidence scores but are more reliable as they're QA-model verified

## Recommendations for Future Improvements

1. **Implement Semantic Search:** Replace TF-IDF with more advanced similarity metrics (e.g., using embeddings)
2. **Multi-turn Conversations:** Add support for follow-up questions with context
3. **Answer Confidence Threshold:** Allow users to set minimum confidence thresholds
4. **Passage Ranking:** Improve passage selection using semantic similarity instead of just TF-IDF
5. **Chunk Size Optimization:** Make passage window size configurable for better performance

## Files Modified

- `backend/app/services/qa_engine.py` - Core QA processing logic

## Deployment Notes

After pulling this fix, no additional actions are required. The system will use the updated QA engine automatically upon restart.

---
**Date:** December 13, 2025
**Status:** ✅ Fixed and Tested
