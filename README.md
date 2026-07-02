## Giga Pilot
GigaPilot is a diagnostic AI engine designed to eliminate unplanned downtime across Tesla’s Gigafactory assembly lines.

* Full Brief: [docs/client-brief.md](docs/client-brief.md)
* Full Architecture: [docs/Architecture.md](docs/Architecture.md)

------------------------------


## High-Level Architecture

Service Level Arcitecuture for GigaPilot 

```mermaid
flowchart LR
 subgraph railway["Railway"]
        frontend["Frontend service<br>Vite build"]
        backend["Backend service<br>FastAPI + PydanticAI"]
  end
 subgraph supabase["Supabase"]
        auth["Auth<br>email session"]
        database[("Postgres<br>chats, documents, chunks<br>pgvector + full-text")]
  end
    user["Technician"] --> browser["Browser<br>React chat app"]
    frontend -- serves app --> browser
    browser -- sign in --> auth
    auth -- JWT session --> browser
    browser -- chat request + JWT --> backend
    backend -- verify user --> auth
    backend -- retrieve passages<br>persist chats + citations --> database
    backend -- generate grounded answer --> gemini["Gemini<br>LLM + embeddings"]
    backend -- stream answer + citations --> browser
    corpus["OEM technical manuals, wiring schematics"] --> ingestion["Ingestion pipeline<br>download, parse, chunk, embed"]
    ingestion -- create embeddings --> gemini
    ingestion -- store documents + chunks --> database
  

```

## Core Stack

* Document Ingestion: Docling
* Vector Database: pgvector
* Embeddings & LLM: Gemini + Gemini 1.0 embedding 
* Retrival: Supabase `pgvector` + Postgres full-text search 
* Frontend UI: Vite + React SPA + TypeScript 
* Backend: Python + FastAPI  




