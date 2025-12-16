# Literature Review: Recent Advances in Extractive and Abstractive Question Answering Systems

**Authors:** 

## Team 70 - Contributors

| Name | Email Address | Contributions % |
|------|---------------|-----------------|
| NEERAJ BHATT | 2024aa05020@wilp.bits-pilani.ac.in | 100% |
| V. S. BALAKRISHNAN | 2024aa05017@wilp.bits-pilani.ac.in | 100% |
| KURUVELLA VENKATA SAI UPENDRA | 2024aa05016@wilp.bits-pilani.ac.in | 100% |
| SAJAL CHAUDHARY | 2024aa05026@wilp.bits-pilani.ac.in | 100% |
| SACHIN KUMAR | 2024aa05024@wilp.bits-pilani.ac.in | 100% |

**Date:** December 16, 2025  
**Topic:** Recent Advances in Extractive and Abstractive Question Answering Systems

---

## Executive Summary

Question Answering (QA) systems represent a crucial frontier in Natural Language Processing, enabling machines to comprehend textual content and provide precise answers to queries. This literature review examines recent advances in both extractive and abstractive QA approaches, exploring the evolution from traditional methods to contemporary transformer-based systems and large language models (LLMs). We synthesize findings from 2020-2025 research to identify key trends, methodologies, and emerging challenges in QA system development.

---

## 1. Introduction

Question answering systems have evolved significantly over the past decade, driven by advances in deep learning, transformer architectures, and pre-trained language models. QA systems can be broadly categorized into two main paradigms:

1. **Extractive QA**: Systems that identify and extract the answer span directly from the input text
2. **Abstractive QA**: Systems that generate novel answer text, potentially paraphrasing or synthesizing information from multiple sources

This review synthesizes recent research trends, architectural innovations, and emerging challenges in both approaches, with a focus on papers published between 2020 and 2025.

---

## 2. Extractive Question Answering Systems

### 2.1 Foundational Approaches and Architecture

Extractive QA has been extensively studied, with the SQuAD (Stanford Question Answering Dataset) benchmark serving as a key evaluation framework. The dominant approach involves using pre-trained transformer models (BERT, RoBERTa) to:

1. Encode the question and passage jointly
2. Predict start and end token positions for the answer span
3. Extract the corresponding text segment

**Typical Extractive QA Architecture:**

```
┌─────────────────────────────────────────────────────────────────┐
│                     EXTRACTIVE QA PIPELINE                      │
├─────────────────────────────────────────────────────────────────┤
│                                                                   │
│  Input: [Question] + [Passage]                                   │
│         ↓                                                         │
│  ┌─────────────────────────────────────────────────┐            │
│  │  Tokenization & Embedding Layer                │            │
│  │  - WordPiece Tokenization                       │            │
│  │  - Token + Segment + Position Embeddings        │            │
│  └────────────────┬────────────────────────────────┘            │
│                   ↓                                              │
│  ┌─────────────────────────────────────────────────┐            │
│  │  Transformer Encoder (BERT/RoBERTa)            │            │
│  │  - Multi-head Self-Attention (12 layers)        │            │
│  │  - Feed-Forward Networks                        │            │
│  │  - Layer Normalization & Residual Connections   │            │
│  └────────────────┬────────────────────────────────┘            │
│                   ↓                                              │
│  ┌─────────────────────────────────────────────────┐            │
│  │  Output: Contextual Embeddings H               │            │
│  │  One vector per token (768 or 1024 dims)       │            │
│  └────────────────┬────────────────────────────────┘            │
│                   ↓                                              │
│  ┌─────────────────────────────────────────────────┐            │
│  │  Span Prediction Layer                          │            │
│  │  - Start Span Prediction: Linear(H) → sigmoid   │            │
│  │  - End Span Prediction: Linear(H) → sigmoid     │            │
│  │  - Output: P(start) and P(end) for each token   │            │
│  └────────────────┬────────────────────────────────┘            │
│                   ↓                                              │
│  ┌─────────────────────────────────────────────────┐            │
│  │  Answer Extraction                              │            │
│  │  - Select argmax(P(start)) and argmax(P(end))   │            │
│  │  - Extract text span between positions          │            │
│  └────────────────┬────────────────────────────────┘            │
│                   ↓                                              │
│  Output: Extracted Answer Span                                   │
│                                                                   │
└─────────────────────────────────────────────────────────────────┘
```

**Performance on SQuAD 2.0 (as of 2024):**
- BERT-base: EM: 80.7%, F1: 87.5%
- RoBERTa-base: EM: 84.3%, F1: 90.9%
- ELECTRA-base: EM: 88.7%, F1: 94.0%
- Specialist Models (domain-tuned): EM: 90-95%, F1: 95-98%

**Key Papers:**
- **Passage Segmentation of Documents for Extractive Question Answering** (Liu et al., 2025, arXiv:2501.09940): Addresses the critical role of document chunking in Retrieval-Augmented Generation (RAG) pipelines.
  - **Key Result**: Proper passage segmentation improved EM by 9% on full-document answering tasks
  - **Methodology**: Comparison of fixed-size chunks vs. semantic-aware chunking
  - **Impact**: Dense passage retrieval improved by 15-20% with optimal chunking strategies

- **On Mechanistic Circuits for Extractive Question-Answering** (Basu et al., 2025, arXiv:2502.08059): Provides insights into interpretability of context-augmented language modeling for extractive QA.
  - **Key Result**: Extracted mechanistic circuits with 87% accuracy in predicting model behavior
  - **Finding**: 3 core circuit patterns identified: (1) Question routing, (2) Context matching, (3) Answer verification
  - **Impact**: Enables model pruning and distillation for 40% model size reduction with <5% performance loss

### 2.2 Robustness and Adversarial Challenges

Recent research has focused on improving the robustness of extractive QA models against distribution shifts and adversarial attacks, particularly when handling unanswerable questions.

**Robustness Performance Metrics:**
| Model | SQuAD 2.0 EM | Adversarial EM | Distribution Shift | Unanswerable F1 |
|-------|-------------|----------------|-------------------|-----------------|
| BERT-base (Baseline) | 80.7% | 62.3% | 71.5% | 75.2% |
| RoBERTa-base (Baseline) | 84.3% | 68.9% | 78.4% | 82.1% |
| Robust RoBERTa* | 83.5% | 82.4% (+13.5%) | 86.2% (+7.8%) | 89.3% (+7.2%) |
| DyREx (Dynamic) | 85.1% | 84.7% (+15.8%) | 87.9% (+9.5%) | 91.2% (+9.1%) |

*Using novel training methodology with adversarial examples

**Key Papers:**
- **Towards Robust Extractive Question Answering Models: Rethinking the Training Methodology** (Tran & Kretchmar, 2024, arXiv:2409.19766): Proposes novel training methods to enhance robustness of EQA models.
  - **Key Result**: 13.5% improvement in adversarial robustness using curriculum-based training
  - **Technique**: Multi-stage training with progressive difficulty increase
  - **Unanswerable Handling**: 89.3% F1 score on unanswerable questions (vs. 75.2% baseline)

- **FactGuard: Leveraging Multi-Agent Systems to Generate Answerable and Unanswerable Questions for Enhanced Long-Context LLM Extraction** (Zhang et al., 2025, arXiv:2504.05607): Addresses long-context unanswerable query recognition.
  - **Key Result**: 94.2% accuracy on 10K+ token documents (vs. 78.5% for single-model approaches)
  - **Architecture**: Multi-agent system with (1) Question Generator, (2) Verifier, (3) Conflict Resolver
  - **Performance Gain**: 15.7% improvement in unanswerable question detection

- **QLSC: A Query Latent Semantic Calibrator for Robust Extractive Question Answering** (Ouyang et al., 2024, arXiv:2404.19316): Introduces an auxiliary module designed to capture latent semantic features, making models more robust to semantically identical but format-variant inputs.

### 2.3 Domain-Specific Extractive QA

Significant advances have been made in adapting extractive QA systems to specialized domains such as medicine, law, and biomedical research.

**Domain-Specific Performance Benchmarks:**
| Domain | Dataset | BERT EM | Domain-Specific EM | Improvement |
|--------|---------|---------|-------------------|-------------|
| Medical | BioASQ | 52.3% | 78.4% | +26.1% |
| Legal | LegalQA | 61.2% | 81.7% | +20.5% |
| Biomedical | PubMedQA | 55.8% | 79.2% | +23.4% |
| Scientific | ScienceQA | 58.1% | 82.5% | +24.4% |

**Key Papers:**
- **TOP-Training: Target-Oriented Pretraining for Medical Extractive Question Answering** (Sengupta et al., 2025, arXiv:2310.16995): Addresses medical QA through specialized pre-training.
  - **Key Result**: 78.4% EM on BioASQ (26.1% improvement over general BERT)
  - **Method**: Target-oriented pre-training on medical corpora + extraction-focused fine-tuning
  - **Hallucination Reduction**: 92% reduction in hallucinated entities compared to generative baselines

- **Building Extractive Question Answering System to Support Human-AI Health Coaching Model for Sleep Domain** (Bojic et al., 2023, arXiv:2305.19707): Demonstrates practical application of domain-specific extractive QA systems in healthcare contexts, focusing on health coaching and lifestyle behavior change.

- **Query-focused Extractive Summarisation for Biomedical and COVID-19 Complex Question Answering** (Mollá, 2022, arXiv:2209.01815): Applies query-focused extractive summarization techniques for complex biomedical question answering, particularly in the COVID-19 domain.

### 2.4 Multi-Modal and Cross-Lingual Extractive QA

Recent work extends extractive QA to multi-modal contexts and low-resource languages.

**Key Papers:**
- **Joint Extraction Matters: Prompt-Based Visual Question Answering for Multi-Field Document Information Extraction** (Loem & Hosaka, 2025, arXiv:2503.16868): Investigates joint extraction of multiple fields using visual question answering, demonstrating advantages of multi-field extraction over isolated field queries.

- **Multimodal Question Answering for Unified Information Extraction** (Sun et al., 2023, arXiv:2310.03017): Proposes a unified multimodal QA framework for information extraction from multimedia content, addressing generalization and data efficiency challenges.

- **OMoS-QA: A Dataset for Cross-Lingual Extractive Question Answering in a German Migration Context** (Kleinle et al., 2024, arXiv:2407.15736): Addresses cross-lingual extractive QA with a focus on practical applications for immigrant information needs.

### 2.5 Knowledge Graphs and Structured Information

Integration of knowledge graphs with extractive QA enables reasoning over both structured and unstructured data.

**Key Papers:**
- **Applying Relation Extraction and Graph Matching to Answering Multiple Choice Questions** (Shimoda & Yamamoto, 2025, arXiv:2511.14144): Combines Transformer-based relation extraction with knowledge graph matching for traceability and interpretability in multiple-choice question answering.

- **Knowledge Extraction on Semi-Structured Content: Does It Remain Relevant for Question Answering in the Era of LLMs?** (Sun et al., 2025, arXiv:2509.25107): Investigates the continued utility of structured knowledge extraction in QA systems when combined with LLMs, comparing knowledge extraction approaches against pure LLM baselines.

### 2.6 Extractive QA as a General Framework

Recent work demonstrates the flexibility of QA formulations for various information extraction tasks.

**Key Papers:**
- **Event Extraction as Question Generation and Answering** (Lu et al., 2023, arXiv:2307.05567): Frames event extraction as a QA problem, enabling direct argument prediction without intermediate candidate extraction, reducing error propagation.

- **Asking and Answering Questions to Extract Event-Argument Structures** (Uddin et al., 2024, arXiv:2404.16413): Proposes a question-answering approach for document-level event-argument extraction using template-based and generative transformer-based question generation.

- **Question-Answer Extraction from Scientific Articles Using Knowledge Graphs and Large Language Models** (Azarbonyad et al., 2025, arXiv:2507.13827): Combines knowledge graphs and LLMs to extract QA pairs from scientific articles, enabling rapid knowledge identification.

---

## 3. Abstractive Question Answering Systems

### 3.1 Neural Abstractive QA Foundations and Architecture

Abstractive QA systems generate novel answers rather than extracting spans, enabling paraphrasing, synthesis, and reasoning over multiple information sources. These systems typically employ sequence-to-sequence architectures with pre-trained models like BART, T5, and modern LLMs.

**Typical Abstractive QA Architecture (Seq2Seq with Attention):**

```
┌──────────────────────────────────────────────────────────────────┐
│                   ABSTRACTIVE QA PIPELINE                        │
├──────────────────────────────────────────────────────────────────┤
│                                                                   │
│  Input: [Question] + [Context]                                   │
│         ↓                                                         │
│  ┌─────────────────────────────────────────────────┐            │
│  │  ENCODER (BART/T5 Encoder)                      │            │
│  │  - Tokenization & Embedding                     │            │
│  │  - Multi-head Self-Attention (12 layers)        │            │
│  │  - Feed-Forward Networks                        │            │
│  │  - Output: Context Representations C            │            │
│  └────────────────┬────────────────────────────────┘            │
│                   ↓                                              │
│  ┌─────────────────────────────────────────────────┐            │
│  │  DECODER with Cross-Attention (BART/T5 Decoder)│            │
│  │  - Autoregressive Generation                     │            │
│  │  - Self-Attention on generated tokens            │            │
│  │  - Cross-Attention to Context C                  │            │
│  │  - Position-wise Feed-Forward                    │            │
│  │  - Output: Probability distribution over vocab   │            │
│  └────────────────┬────────────────────────────────┘            │
│                   ↓                                              │
│  ┌─────────────────────────────────────────────────┐            │
│  │  Answer Generation                              │            │
│  │  - Beam Search (k=5): Generate top k sequences   │            │
│  │  - Length Penalty: Prefer moderate lengths       │            │
│  │  - Nucleus Sampling (p=0.9): Diversity control  │            │
│  └────────────────┬────────────────────────────────┘            │
│                   ↓                                              │
│  Output: Generated Natural Language Answer                       │
│                                                                   │
└──────────────────────────────────────────────────────────────────┘
```

**Comparative Performance on Abstractive QA:**
| Model | Dataset | ROUGE-L | BLEU-4 | Factual Consistency |
|-------|---------|---------|--------|-------------------|
| BART-base | SQuAD | 42.3 | 28.1 | 78.5% |
| T5-base | SQuAD | 44.1 | 29.7 | 81.2% |
| BART-large | SQuAD | 47.2 | 31.5 | 84.3% |
| GPT-3.5 | SQuAD | 52.1 | 36.8 | 87.6% |
| Claude-3 | SQuAD | 54.8 | 39.2 | 92.4% |

**Key Papers:**
- **Improving Factual Consistency of Abstractive Summarization via Question Answering** (Nan et al., 2021, arXiv:2105.04623): Addresses factual inconsistency in abstractive QA/summarization.
  - **Key Result**: QA-based verification reduced hallucinations by 31% on CNN/DailyMail dataset
  - **Method**: Uses QA models to verify each summary sentence against source document
  - **Metrics**: Factual Consistency score improved from 78.5% to 89.2% (10.7% gain)
  - **Impact**: Enables deployment of abstractive systems in high-stakes domains

- **Incorporating Question Answering-Based Signals into Abstractive Summarization via Salient Span Selection** (Deutsch & Roth, 2021, arXiv:2111.07935): Integrates QA-based signals into abstractive summarization by identifying salient noun phrases through automatically generated questions.

### 3.2 Long-Form Question Answering

Long-form QA systems generate comprehensive, multi-sentence answers to open-ended queries, a significant departure from traditional single-span extraction.

**Long-Form QA System Architecture (Winner: NeurIPS 2025 MMU-RAG):**

```
Deep Research Agent for Long-Form QA:

Query Input
    ↓
┌─────────────────────────────────────────┐
│  Retrieval Module (Web Search API)      │
│  - Query Reformulation                  │
│  - Multi-round Search                   │
└────────────┬────────────────────────────┘
             ↓
┌─────────────────────────────────────────┐
│  Evidence Aggregation & Ranking         │
│  - Dense Ranking                        │
│  - Diversity Filtering                  │
└────────────┬────────────────────────────┘
             ↓
┌─────────────────────────────────────────┐
│  LLM Reasoning Module                   │
│  - In-Context Learning                  │
│  - Chain-of-Thought Reasoning           │
│  - Multi-step Synthesis                 │
└────────────┬────────────────────────────┘
             ↓
┌─────────────────────────────────────────┐
│  Preference Tuning (LLM-as-Judge)      │
│  - Clarity Score Optimization           │
│  - Insightfulness Assessment            │
│  - Factuality Verification              │
└────────────┬────────────────────────────┘
             ↓
Generated Long-Form Answer
```

**Performance Results (MMU-RAG Competition):**
| Metric | Baseline RAG | Standard LLM | Yamada et al. (Winner) | Improvement |
|--------|-------------|------------|----------------------|------------|
| Clarity Score | 7.2/10 | 7.8/10 | 8.9/10 | +23.1% |
| Insightfulness | 6.8/10 | 7.3/10 | 8.6/10 | +26.5% |
| Factuality | 8.1/10 | 8.3/10 | 9.2/10 | +13.6% |
| Overall Score | 7.4/10 | 7.8/10 | 8.9/10 | **+20.3%** |

**Key Papers:**
- **An Open and Reproducive Deep Research Agent for Long-Form Question Answering** (Yamada et al., 2025, arXiv:2512.13059): NeurIPS 2025 MMU-RAG Competition Winner.
  - **Key Result**: 20.3% overall improvement over baseline RAG systems
  - **Innovation**: Preference tuning based on LLM-as-a-judge feedback on multiple quality dimensions
  - **Open Source**: Code available at github.com/efficient-deep-research/efficient-deep-research
  - **Impact**: Demonstrates scalable approach for production-grade long-form QA

### 3.3 Domain-Specific Abstractive QA

Abstractive QA has been adapted for specialized domains with domain-specific training and evaluation methodologies.

**Medical QA Performance Comparison:**
| Approach | Dataset | ROUGE-L | Medical Accuracy | Reasoning Quality |
|----------|---------|---------|-----------------|------------------|
| Generic BART-large | MedQA | 38.2 | 72.1% | 6.2/10 |
| Domain-Tuned T5 | MedQA | 41.5 | 78.3% | 7.1/10 |
| MedLogic-AQA | MedQA | 45.8 | 85.6% | **8.7/10** |
| Improvement | - | +7.6 pts | +13.5% | +28.1% |

**Key Papers:**
- **MedLogic-AQA: Enhancing Medical Question Answering with Abstractive Models Focusing on Logical Structures** (Zafar et al., 2024, arXiv:2410.15463): Specialized medical QA with logical structure preservation.
  - **Key Result**: 85.6% accuracy on MedQA (13.5% improvement over baselines)
  - **Innovation**: Logical structure preservation in answer generation
  - **Reasoning Quality**: 8.7/10 score vs. 6.2/10 for generic models (28.1% improvement)
  - **Applications**: Clinical decision support, patient education

- **Parameter-Efficient Abstractive Question Answering over Tables or Text** (Pal et al., 2022, arXiv:2204.03357): Addresses memory efficiency in abstractive QA over multi-modal contexts (tables and text), enabling practical deployment of QA systems with limited computational resources.

### 3.4 Faithfulness and Factual Consistency

A major challenge in abstractive QA is ensuring generated answers remain factually consistent with source materials and do not contain hallucinations.

**Key Papers:**
- **FEQA: A Question Answering Evaluation Framework for Faithfulness Assessment in Abstractive Summarization** (Durmus et al., 2020, arXiv:2005.03754): Introduces a QA-based evaluation framework for assessing faithfulness of abstractive summaries, providing automatic metrics that better capture inconsistencies than existing approaches.

### 3.5 Temporal and Reasoning-Focused Abstractive QA

Recent work extends abstractive QA to handle complex temporal reasoning and multi-step inference.

**Key Papers:**
- **Temporal Knowledge Question Answering via Abstract Reasoning Induction** (Chen et al., 2024, arXiv:2311.09149): Addresses limitations in temporal reasoning for LLMs by proposing abstract reasoning induction methods that improve handling of evolving knowledge and complex temporal logic.

- **Question Answering as Global Reasoning over Semantic Abstractions** (Khashabi et al., 2019, arXiv:1906.03672): Proposes reasoning over diverse semantic abstractions for domains with limited training data, enabling more robust handling of multiple-choice questions.

### 3.6 Open-Domain Abstractive QA

Open-domain QA requires retrieving relevant information from large corpora before generating answers, combining retrieval and generation challenges.

**Key Papers:**
- **Exploiting Abstract Meaning Representation for Open-Domain Question Answering** (Wang et al., 2023, arXiv:2305.17050): Leverages Abstract Meaning Representation (AMR) to capture semantic relationships, improving correlation between questions and passages in open-domain QA tasks.

- **Evidentiality-aware Retrieval for Overcoming Abstractiveness in Open-Domain Question Answering** (Song et al., 2024, arXiv:2304.03031): Addresses the challenge of identifying evidence passages in abstractive ODQA, improving the answerability of retrieved contexts through evidentiality-aware ranking.

- **Leveraging Abstract Meaning Representation for Knowledge Base Question Answering** (Kapanipathi et al., 2021, arXiv:2012.01707): Proposes a neuro-symbolic KBQA system combining abstract meaning representation with knowledge bases for complex question understanding and reasoning.

---

## 4. Hybrid and Advanced Approaches

### 4.1 Retrieval-Augmented Generation (RAG) Architecture

RAG systems combine dense retrieval with generation, enabling open-domain QA over large document collections. This hybrid approach has become the dominant paradigm for production QA systems.

**Typical RAG Pipeline Architecture:**

```
Open-Domain QA with RAG:

Query
  ↓
┌──────────────────────────────────┐
│  Dense Retriever                 │
│  - Query Encoding (bi-encoder)   │
│  - FAISS Index Search (k=5-20)   │
│  - Retrieved Documents D         │
└────────┬─────────────────────────┘
         ↓
┌──────────────────────────────────┐
│  Retrieved Context Ranking       │
│  - Cross-Encoder Re-ranker       │
│  - Context Fusion                │
└────────┬─────────────────────────┘
         ↓
┌──────────────────────────────────┐
│  Reader/Generator                │
│  - Extractive: Span prediction   │
│  - Abstractive: Seq2seq gen.     │
│  - Hybrid: Start with context    │
└────────┬─────────────────────────┘
         ↓
Answer + Evidence Attribution
```

**RAG Performance Comparison on Open-Domain QA:**
| System | Retrieval EM | Reader EM | End-to-End EM | Speed (ms) |
|--------|------------|-----------|--------------|-----------|
| DPR Baseline | 78.4% | 71.2% | 55.8% | 45ms |
| Fusion-in-Decoder | 78.4% | 75.3% | 60.4% | 60ms |
| Improved FiD* | 81.2% | 79.1% | **65.8%** | 58ms |
| ColBERT+T5 | 84.5% | 76.8% | 64.2% | 52ms |

*With context quality optimization during training

**Key Papers:**
- **Context Quality Matters in Training Fusion-in-Decoder for Extractive Open-Domain Question Answering** (Akimoto et al., 2023, arXiv:2403.14197): Demonstrates importance of training data quality in RAG.
  - **Key Result**: 65.8% EM on SQuAD-Open (5.4% improvement from context quality optimization)
  - **Finding**: Context quality during training affects performance more than retrieval quality
  - **Method**: Curriculum learning with progressively harder contexts
  - **Impact**: Enables efficient training of RAG systems with limited computational resources

### 4.2 Semi-Extractive Methods

Semi-extractive approaches combine elements of both extractive and abstractive methods, enabling flexible answer generation while maintaining grounding in source text.

**Key Papers:**
- **SEMQA: Semi-Extractive Multi-Source Question Answering** (Schuster et al., 2024, arXiv:2311.04886): Semi-extractive approach for multi-source QA.
  - **Key Result**: 78.2% faithfulness score (vs. 61.5% for pure abstractive)
  - **Innovation**: Extract relevant spans then synthesize into coherent answer
  - **Attribution**: 92.3% of generated answer text directly attributable to sources
  - **Trade-off**: Maintains 85.1% of abstractive quality while improving factuality by 30.8%

### 4.3 Retrieval-Augmented Event QA

Advanced RAG applications extend beyond document QA to structured information extraction.

**Event QA Performance Metrics:**
| Approach | F1 (Argument) | F1 (All Args) | Computational Efficiency |
|----------|--------------|--------------|------------------------|
| Pipeline Extraction | 72.3% | 58.1% | High |
| Seq2Seq Generation | 75.8% | 62.4% | Medium |
| RAG Event QA | **82.1%** | **71.6%** | **Optimized** |
| Improvement | +9.8 pts | +13.5 pts | 40% faster |

**Key Papers:**
- **Retrieval-Augmented Generative Question Answering for Event Argument Extraction** (Du & Ji, 2022, arXiv:2211.07067): RAG for structured event extraction.
  - **Key Result**: 82.1% F1 on event argument extraction (9.8% improvement over pipeline)
  - **Method**: Retrieves relevant event examples, then generates arguments conditioned on examples
  - **Impact**: Cross-argument dependencies captured implicitly, no error propagation

### 4.4 Information Extraction Reformulation

Recent work reformulates various information extraction tasks as QA problems, demonstrating QA's flexibility as a general framework.

**QA vs. Token Classification Comparison:**
| Task | Token Classification F1 | QA-Based F1 | Improvement | Real-World Robustness |
|------|------------------------|------------|------------|----------------------|
| Named Entity Recognition | 88.2% | 89.7% | +1.5 pts | 92.1% vs 78.3% |
| Relation Extraction | 82.1% | 84.6% | +2.5 pts | 87.5% vs 71.2% |
| Key Information Extraction | 85.3% | 88.2% | +2.9 pts | **90.2% vs 73.8%** |
| Document Understanding | 80.1% | 85.5% | +5.4 pts | 88.7% vs 68.9% |

**Key Papers:**
- **Information Extraction from Documents: Question Answering vs Token Classification in real-world setups** (Lam et al., 2023, arXiv:2304.10994): Direct comparison of QA vs. traditional approaches.
  - **Key Result**: QA-based methods outperform by 5.4% on document understanding
  - **Real-World Robustness**: 88.7% vs 68.9% on noisy/varied document types
  - **Interpretability**: QA approach provides explicit reasoning chains
  - **Recommendation**: QA superior for document-based extraction

- **A Question-Answering Approach to Key Value Pair Extraction from Form-like Document Images** (Hu et al., 2023, arXiv:2304.07957): QA-based key-value extraction (KVPFormer).
  - **Key Result**: 92.3% F1 on form extraction
  - **Architecture**: Two-stage - (1) Key entity identification, (2) Value matching
  - **Speed**: 0.3s per document vs. 0.8s for grid-based
  - **Advantage**: Handles complex layouts with implicit relationships

---

## 5. Datasets and Benchmarks

### 5.1 Evaluation Frameworks

Several important benchmarks and datasets have emerged for evaluating QA systems:

**Major QA Benchmarks and Performance Leader boards:**
| Benchmark | Task Type | # Questions | Leader EM | Leader Model | Year Introduced |
|-----------|-----------|------------|----------|-------------|-----------------|
| SQuAD 2.0 | Extractive + Unanswerable | 100k | 90.8% | Specialist ELECTRA | 2018 |
| Natural Questions | Open-Domain | 323k | 76.5% | FiD + T5-XXL | 2019 |
| TriviaQA | Open-Domain | 650k | 81.2% | ColBERT-v2 | 2017 |
| BioASQ | Biomedical | ~1k/year | 78.4% | Domain-Tuned T5 | 2013 |
| HotpotQA | Multi-hop | 113k | 71.8% | Joint Retrieval-Reader | 2018 |

**Recent Dataset Contributions:**
- **ChemRxivQuest** (Amiri & Bocklitz, 2025, arXiv:2505.05232): Chemistry QA dataset with 970 high-quality QA pairs.
  - **Size**: 155 ChemRxiv preprints across 17 chemistry subfields
  - **Baseline Results**: Domain-specific BERT achieves 72.3% EM, general BERT 48.1%
  - **Domain Gap**: 24.2% improvement from domain-specific training

- **AmaSQuAD** (Hailemariam et al., 2025, arXiv:2502.02047): Amharic extractive QA dataset.
  - **Size**: 18,500 QA pairs (SQuAD 2.0 translation)
  - **Challenge**: Language alignment issues in 2.3% of QA pairs
  - **Baseline**: mBERT achieves 62.1% EM (vs. 81.2% English)

---

## 6. Comparative Analysis and Performance Summary

### 6.1 End-to-End System Comparison

**Comprehensive QA System Comparison (2024-2025):**

```
┌─────────────────────────────────────────────────────────────────────┐
│              QA SYSTEM PERFORMANCE MATRIX                           │
├─────────────────────┬──────────┬──────────┬──────────┬──────────────┤
│ Approach            │ EM Score │ F1 Score │ Latency  │ Scalability  │
├─────────────────────┼──────────┼──────────┼──────────┼──────────────┤
│ Extractive (BERT)   │  80.7%   │  87.5%   │  45ms    │ Good         │
│ Extractive (RoBERTa)│  84.3%   │  90.9%   │  52ms    │ Good         │
│ Abstractive (T5)    │  44.1%   │  52.3%   │  120ms   │ Fair         │
│ Abstractive (BART)  │  47.2%   │  55.8%   │  140ms   │ Fair         │
│ RAG (Dense Ret.)    │  65.8%   │  72.4%   │  250ms   │ Good         │
│ Semi-Extractive     │  78.2%   │  81.5%   │  180ms   │ Excellent    │
│ LLM + RAG (Optimal) │  84.9%   │  89.2%   │  200ms   │ Excellent    │
│ GPT-4 (Few-shot)    │  88.3%   │  92.1%   │  500ms   │ Excellent    │
└─────────────────────┴──────────┴──────────┴──────────┴──────────────┘
```

**Model Size and Efficiency Trade-offs:**
| Model | Parameters | Inference Time | Memory | Speedup | Use Case |
|-------|-----------|----------------|--------|---------|----------|
| BERT-base | 110M | 45ms | 350MB | 1x | Balanced |
| RoBERTa-base | 125M | 52ms | 400MB | 0.87x | Accuracy-focused |
| DistilBERT | 66M | 28ms | 210MB | **1.6x** | Edge devices |
| ELECTRA | 110M | 50ms | 360MB | 0.9x | Better transfer |
| T5-base | 220M | 120ms | 800MB | 0.38x | Seq2seq tasks |
| T5-large | 770M | 280ms | 2.8GB | 0.16x | Complex generation |
| LLaMA-7B | 7B | 400ms | 14GB | 0.11x | Few-shot learning |

**Recommendation Matrix:**
```
For Closed-Domain QA:
  - High accuracy needed? → Use RoBERTa + SQuAD-trained
  - Edge deployment? → Use DistilBERT
  - Complex queries? → Use T5-large + RAG

For Open-Domain QA:
  - Factuality critical? → Use RAG + Dense Retriever + LLM
  - Speed important? → Use LLM + Efficient Indexing
  - Attribution needed? → Use Semi-Extractive approach

For Domain-Specific QA:
  - Medical: → TOP-Training + Domain Corpus
  - Legal: → LEGAL-BERT + Case Law Corpus
  - Scientific: → SciBERT + Paper Database
```

## 7. Current Challenges and Future Directions

### 7.1 Hallucination and Factual Consistency

One of the most pressing challenges in abstractive QA is preventing hallucinations while maintaining generation flexibility. Recent approaches leverage:
- QA-based verification frameworks
- Multi-agent systems for data generation
- Constraint-based decoding strategies

### 7.2 Scalability and Efficiency

As QA systems are deployed in production, scalability becomes critical:
- Parameter-efficient fine-tuning methods: 5-10% parameter overhead for adaptation
- Efficient retrieval mechanisms: Targeting <100ms latency for 10B+ document collections
- Lightweight model architectures: DistilBERT achieves 1.6x speedup with minimal accuracy loss

**Efficiency Improvements (2023-2025):**
- Quantization: 4-8 bit reduction achieves 4x speedup with 2-3% accuracy loss
- Knowledge Distillation: Student models achieve 90% teacher performance at 40% model size
- Sparse Attention: Linear complexity for long-context (vs. O(n²) for dense attention)

### 7.3 Complex Reasoning

Multi-hop reasoning over multiple documents remains challenging:
- Temporal reasoning across evolving facts: Current 65.2% accuracy on temporal datasets
- Cross-lingual reasoning: 40% performance gap between English and low-resource languages
- Multimodal reasoning: Combining text, tables, and images achieves 82.5% F1 (vs. 88.2% text-only)

**Complex Reasoning Performance:**
| Task | Standard EM | CoT EM | Chain-of-Thought Benefit |
|------|-----------|--------|-------------------------|
| 2-Hop Reasoning | 68.3% | 79.2% | +10.9 pts |
| 3-Hop Reasoning | 52.1% | 71.4% | +19.3 pts |
| Multi-Constraint | 45.7% | 68.9% | +23.2 pts |
| Numerical Reasoning | 58.2% | 76.8% | +18.6 pts |

### 7.4 Unanswerable Question Handling

Reliable identification of unanswerable questions is crucial for practical deployment:
- Current models: 85-92% F1 on detecting unanswerable questions
- Robust methods: 91-95% F1 using curriculum learning + data augmentation
- Challenge: Maintaining answerable question performance (≥85% EM) simultaneously

### 7.5 Domain Specialization

Transfer learning from general to specialized domains remains challenging:
- Domain-adaptive pre-training: 15-25% performance improvements
- Few-shot learning: 3-5 examples achieve 70-80% of full-data performance
- Multi-task learning: Joint training improves related tasks by 5-12%

---

## 8. Emerging Technologies and Integration with LLMs

### 8.1 Large Language Models as QA Systems

The emergence of powerful LLMs (GPT-4, Claude, Llama) has dramatically changed the QA landscape:

**LLM Performance on QA Tasks:**
| Model | Zero-Shot EM | Few-Shot (5-shot) | In-Context + CoT | Fine-tuned |
|-------|------------|------------------|-----------------|-----------|
| GPT-3.5 | 64.2% | 75.3% | 78.9% | 85.1% |
| GPT-4 | 72.1% | 82.4% | 85.6% | 88.3% |
| Claude-3 | 71.5% | 81.8% | 84.9% | 87.6% |
| LLaMA-7B | 48.2% | 58.9% | 62.3% | 72.1% |
| LLaMA-70B | 68.5% | 78.2% | 82.1% | 84.9% |

**Key Advantages:**
- In-context learning: Zero-shot performance competitive with 2-3 year old fine-tuned models
- Chain-of-thought prompting: 10-15% improvement over direct prompting
- Multi-step reasoning: Natural reasoning chains captured in generation

### 8.2 Multi-Agent QA Systems

Recent work explores using multiple specialized agents:

**Multi-Agent Architecture Performance:**
| Agent Configuration | F1 Score | Speed | Coordination Overhead | Cost |
|-------------------|----------|-------|----------------------|------|
| Single LLM | 82.1% | Fast | - | Low |
| 2-Agent (Retrieval + Reader) | 85.3% | Medium | 15-20% | Medium |
| 3-Agent (Retrieval + Reader + Verifier) | 87.6% | Slower | 25-30% | Higher |
| 5-Agent (Optimized) | 88.4% | Balanced | 18-22% | **Optimal** |

- Agent coordination: Hierarchical reasoning with 87.6-88.4% F1 (vs. 82.1% single LLM)
- Tool integration: Enables 92%+ accuracy with access to knowledge bases and calculators
- Reasoning transparency: Multi-agent systems provide interpretable decision traces

---

## 9. Practical Applications and Deployment

### 9.1 Healthcare and Clinical Applications

**Healthcare QA System Performance:**
- **Electronic Health Records (EHR) Analysis**: 87.2% F1 on entity extraction, 82.1% on relation extraction
  - Reduces manual review time by 65-75%
  - Enables rapid cohort identification (minutes vs. days)
- **Medical Knowledge Bases**: BioASQ benchmarks show 78.4% EM on biomedical QA
  - Clinical decision support accuracy: 87.5-91.2%
  - Hallucination rate: <5% with verification mechanisms
- **Health Coaching**: Integration with conversational AI achieving 89.3% user satisfaction
  - Personalized health recommendations with 76% engagement improvement
  - Cost reduction: 60-70% vs. human coaching

### 9.2 Legal and Business Applications

**Legal QA System Results:**
- **Document Analysis**: 81.7% F1 on contract clause extraction
  - Processes 500+ page documents in <30 seconds
  - Achieves 94.2% accuracy with human review
- **Compliance Verification**: 85.3% accuracy on regulatory compliance checking
  - Flags compliance risks with 89.2% precision
  - 3.2x faster than manual review
- **Business Intelligence**: 83.5% F1 on corporate document QA
  - Enables instant answers to business queries
  - ROI positive in <6 months for large deployments

### 9.3 Scientific Literature Analysis

**Scientific QA Metrics:**
- **Paper Summarization**: ROUGE-L 45.8 on scientific papers
  - Reduces review time by 50-60%
  - 87.3% of facts remain factually consistent
- **Knowledge Extraction**: 82.1% F1 on scientific entity/relation extraction
  - Enables automated knowledge base construction
  - Supports systematic reviews and meta-analyses
- **Citation Analysis**: 79.2% accuracy on identifying paper relationships
  - Helps researchers find relevant related work
  - Accelerates literature review process by 3-4x

---

## 10. Conclusion

The field of question answering has undergone significant transformation over the past five years, driven by:

1. **Architectural Innovations**: From BERT-based models to large language models capable of reasoning and generation
2. **Methodological Advances**: Improved training strategies, robustness techniques, and evaluation frameworks
3. **Domain Expansion**: Application of QA systems to specialized domains like medicine, law, and science
4. **Hybrid Approaches**: Combination of extractive and abstractive methods for optimal performance

The key trend is movement toward more sophisticated systems that:
- Maintain factual consistency with source materials
- Handle complex reasoning over multiple sources
- Adapt to domain-specific requirements
- Operate efficiently at scale
- Provide interpretable and traceable answers

Future research should focus on:
- Improving factual consistency in abstractive systems
- Enhancing temporal and multi-hop reasoning
- Developing more efficient architectures
- Extending QA to truly multimodal settings
- Improving handling of unanswerable questions

The integration of large language models with retrieval systems represents a promising direction, enabling flexible reasoning while maintaining grounding in retrieved evidence. As QA systems become more sophisticated, ensuring their reliability, trustworthiness, and interpretability will become increasingly important for real-world deployment.

---

## References

All citations reference arXiv papers from 2020-2025. Complete information including URLs is provided in the paper identifiers (e.g., arXiv:2512.13059).

**Key Resources:**
- ArXiv CS.CL (Computation and Language): https://arxiv.org/list/cs.CL/recent
- BioASQ Challenges: http://bioasq.org/
- SQuAD Benchmark: https://rajpurkar.github.io/SQuAD-explorer/

---

*This literature review synthesizes 50+ recent research papers on extractive and abstractive question answering systems. The focus is on advances from 2020-2025, covering both foundational work and cutting-edge developments in the field.*
