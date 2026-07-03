# Learnova AI Service

Learnova AI Service is a FastAPI backend for turning uploaded PDF learning material into generated multiple-choice tests. It extracts PDF text, chunks the content, embeds it with a Hugging Face sentence-transformer model, stores document chunks in ChromaDB, and uses a LangGraph workflow with Groq-backed LLM calls to extract topics, build a question blueprint, and generate MCQs.

## Features

- PDF upload and text extraction with PyMuPDF
- Text chunking with LangChain text splitters
- Local persistent vector storage with ChromaDB
- Embeddings via `sentence-transformers/all-MiniLM-L6-v2`
- Topic extraction and test generation workflow using LangGraph
- MCQ generation through Groq/LangChain
- FastAPI endpoints with interactive Swagger docs

## Project Structure

```text
.
|-- main.py                         # FastAPI application entry point
|-- requirements.txt                # Python dependencies
|-- app/
|   |-- api/                        # HTTP routes
|   |   |-- document_routes.py      # Document upload endpoint
|   |   `-- test_routes.py          # Test generation endpoint
|   |-- config.py                   # Service constants and model settings
|   |-- graph/                      # LangGraph state, nodes, and graph builder
|   |-- models/                     # Request/response models
|   `-- services/                   # Document, embedding, retrieval, topic, LLM, and question services
|-- storage/
|   `-- chroma_db/                  # Persistent ChromaDB data
`-- uploads/                        # Uploaded PDF files
```

## Architecture

The service is organized as a layered FastAPI application. Routes receive HTTP requests, service modules handle document processing, embeddings, retrieval, topic processing, and question generation, and the LangGraph workflow coordinates the test-generation pipeline.

```mermaid
flowchart TD
    Client[Client / Frontend / Swagger UI]
    API[FastAPI App]
    DocRoutes[Document Routes]
    TestRoutes[Test Routes]
    PdfService[PDF Service]
    ChunkService[Chunk Service]
    EmbeddingService[Embedding Services]
    Chroma[ChromaDB Vector Store]
    Graph[LangGraph Workflow]
    TopicServices[Topic Services]
    BlueprintServices[Blueprint Services]
    QuestionServices[Question Services]
    Groq[Groq LLM]
    Uploads[uploads/]
    Storage[storage/chroma_db/]

    Client --> API
    API --> DocRoutes
    API --> TestRoutes

    DocRoutes --> Uploads
    DocRoutes --> PdfService
    PdfService --> ChunkService
    ChunkService --> EmbeddingService
    EmbeddingService --> Chroma
    Chroma --> Storage

    TestRoutes --> Graph
    Graph --> Chroma
    Graph --> TopicServices
    Graph --> BlueprintServices
    Graph --> QuestionServices
    TopicServices --> Groq
    QuestionServices --> Groq
```

### Generation Workflow

```mermaid
flowchart LR
    A[Document ID + Test Request] --> B[Load Document Chunks]
    B --> C[Extract Topics]
    C --> D[Flatten and Canonicalize Topics]
    D --> E[Aggregate Topics]
    E --> F[Create Blueprint]
    F --> G[Resolve Focus Topics]
    G --> H[Optimize Blueprint]
    H --> I[Generate MCQs]
    I --> J[Test Response]
```

## Data Flow Diagrams

### DFD Level 0

Level 0 shows the whole Learnova AI Service as a single process that receives learning documents and test-generation requests, then returns processed document IDs and generated MCQ tests.

```mermaid
flowchart LR
    User[User / Teacher]
    System((Learnova AI Service))
    VectorStore[(ChromaDB Storage)]
    FileStore[(Uploaded PDF Storage)]
    LLM[Groq LLM API]

    User -->|Upload PDF| System
    System -->|Document ID| User
    User -->|Document ID, title, difficulty, question count, focus topic| System
    System -->|Generated MCQ test| User

    System -->|Save uploaded PDF| FileStore
    System -->|Store chunks and embeddings| VectorStore
    System -->|Prompt for topic and question generation| LLM
    LLM -->|Generated text output| System
```

### DFD Level 1

Level 1 breaks the service into its main internal processes: document ingestion, embedding storage, test request handling, topic and blueprint creation, and MCQ generation.

```mermaid
flowchart TD
    User[User / Teacher]
    P1((1. Upload Document))
    P2((2. Extract and Chunk Text))
    P3((3. Generate Embeddings))
    P4((4. Store Document Vectors))
    P5((5. Receive Test Request))
    P6((6. Build Topics and Blueprint))
    P7((7. Generate MCQs))
    FileStore[(uploads/)]
    VectorStore[(storage/chroma_db/)]
    LLM[Groq LLM API]

    User -->|PDF file| P1
    P1 -->|Saved PDF| FileStore
    P1 -->|File path| P2
    P2 -->|Text chunks| P3
    P3 -->|Chunk embeddings| P4
    P4 -->|Document chunks and vectors| VectorStore
    P4 -->|Document ID| User

    User -->|Document ID and test options| P5
    P5 -->|Document ID| P6
    P6 -->|Read chunks| VectorStore
    P6 -->|Topic extraction prompts| LLM
    LLM -->|Topic output| P6
    P6 -->|Optimized blueprint| P7
    P7 -->|Question generation prompts| LLM
    LLM -->|Generated MCQs| P7
    P7 -->|Final test| User
```

## Requirements

- Python 3.11+
- A Groq API key

## Setup

Create and activate a virtual environment:

```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
```

Install dependencies:

```powershell
pip install -r requirements.txt
```

Create a `.env` file in the project root:

```env
GROQ_API_KEY=your_groq_api_key_here
```

## Run the API

Start the development server:

```powershell
uvicorn main:app --reload
```

The API will be available at:

```text
http://127.0.0.1:8000
```

Interactive API documentation:

```text
http://127.0.0.1:8000/docs
```

## API Endpoints

### Health Check

```http
GET /
```

Example response:

```json
{
  "status": "running",
  "service": "learnova-ai-service"
}
```

### Upload a Document

```http
POST /documents/upload
```

Upload a PDF file using multipart form data with the field name `file`.

Example with `curl`:

```bash
curl -X POST "http://127.0.0.1:8000/documents/upload" \
  -F "file=@cloud_dummy.pdf"
```

Example response:

```json
{
  "document_id": "generated-document-id",
  "message": "Document processed successfully."
}
```

Keep the returned `document_id`; it is required to generate a test from the uploaded document.

### Generate a Test

```http
POST /tests/generate
```

Example request body:

```json
{
  "document_id": "generated-document-id",
  "question_count": 10,
  "difficulty": "Medium",
  "focus_topic": null,
  "title": "Cloud Computing Basics"
}
```

Example response:

```json
{
  "title": "Cloud Computing Basics",
  "mcqs": []
}
```

The `mcqs` array is populated by the LangGraph generation workflow.

## Configuration

Core settings live in `app/config.py`.

```python
LLM_MODEL = "llama-3.3-70b-versatile"
LLM_TEMPERATURE = 0
EMBEDDING_MODEL = "sentence-transformers/all-MiniLM-L6-v2"
TOP_K_CHUNKS = 2
DEFAULT_DIFFICULTY = "Medium"
```

Adjust these values to change the LLM model, embedding model, retrieval behavior, retry behavior, or generation defaults.

## Data and Storage

- Uploaded files are saved to `uploads/`.
- ChromaDB persists vectors and document chunks in `storage/chroma_db/`.
- Local environment variables should stay in `.env`, which is ignored by Git.

## Development Notes

- The first embedding run may download model files from Hugging Face.
- The LLM workflow requires `GROQ_API_KEY` to be set.
- Use `/docs` while developing to test upload and generation requests from the browser.
