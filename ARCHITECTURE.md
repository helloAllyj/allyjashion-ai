# System Architecture

## Overview

AllyJashion uses a hybrid AI architecture combining computer vision (CLIP + metric learning) with LLM capabilities (Claude) for intelligent fashion recommendations.

## Component Breakdown

### 1. Data Layer
**Supabase**: PostgreSQL + Object Storage
- Tables: `closet_items`, `pinterest_inspiration`, `embeddings`
- Storage: Image files with public URLs
- Real-time subscriptions for updates

### 2. ML Pipeline

#### Feature Extraction
```python
CLIP (frozen) → Projection Head (trainable)
ViT-B/32: 512 dims → 256 dims (embedding)
```

#### Training Strategy
- **Loss**: Triplet loss with margin=0.5
- **Mining**: Hard negative mining (top 10% hardest)
- **Optimizer**: Adam (lr=1e-4, weight_decay=1e-5)
- **Batch Size**: 32 triplets
- **Epochs**: 50

#### Triplet Formation
```
Anchor: Pinterest outfit
Positive: Same style category
Negative: Different style (mined)
```

### 3. Inference Pipeline
```
User Input → Claude NLP → Query Embedding → FAISS Search → Top-K Items → Outfit Generation → Claude Explanation
```

**Latency Breakdown:**
- Claude parsing: 300ms
- Embedding: 50ms
- Search: 10ms
- Recommendation logic: 100ms
- Claude explanation: 500ms
**Total: ~960ms**

### 4. API Layer

**FastAPI Endpoints:**
- `POST /api/v1/recommend` - Main recommendation
- `POST /api/v1/search` - Text search
- `POST /api/v1/upload` - Add items
- `POST /api/v1/train` - Trigger training
- `GET /api/v1/embeddings` - Export embeddings

### 5. Deployment

**Docker Compose Stack:**
- API container (FastAPI)
- Training container (PyTorch)
- Redis (caching)

## Design Decisions

### Why CLIP?
- Pre-trained on 400M image-text pairs
- Understands visual semantics
- Enables text-to-image search
- Strong zero-shot capabilities

### Why Triplet Loss?
- Learns relative distances (better than classification)
- Handles new items without retraining entire model
- Interpretable embedding space
- Standard in production systems (face recognition, visual search)

### Why Claude?
- Strong reasoning for styling advice
- Good at parsing nuanced queries
- Explains decisions naturally
