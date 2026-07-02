# GigaPilot Architecture

## Purpose
GigaPilot is a localized, ruggedized diagnostic AI engine designed to eliminate unplanned downtime across Tesla’s Gigafactory assembly lines.

By functioning as a digital maintenance assistant for on-the-ground crew members, GigaPilot instantly translates complex machine error codes and physical breakdown symptoms into step-by-step, safety-first repair checklists.


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
        db[("Postgres<br>chats, documents, chunks<br>pgvector + full-text")]
  end
    user["Technician"] --> browser["Browser<br>React chat app"]
    frontend -- serves app --> browser
    browser -- sign in --> auth
    auth -- JWT session --> browser
    browser -- chat request + JWT --> backend
    backend -- verify user --> auth
    backend -- retrieve passages<br>persist chats + citations --> db
    backend -- generate grounded answer --> gemini["Gemini<br>LLM + embeddings"]
    backend -- stream answer + citations --> browser
    corpus["OEM technical manuals, wiring schematics"] --> ingestion["Ingestion pipeline<br>download, parse, chunk, embed"]
    ingestion -- create embeddings --> gemini
    ingestion -- store documents + chunks --> db
  

```