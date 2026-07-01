## Diagnostic Copilot
Diagnostic Copilot is an internal, ruggedized AI-powered diagnostic engine designed for Tesla Gigafactory maintenance teams. The system leverages Retrieval-Augmented Generation (RAG) to instantly convert complex machine error codes, fault symptoms, and electrical failures into actionable, step-by-step physical troubleshooting checklists.
By grounding responses strictly in verified Original Equipment Manufacturer (OEM) manuals, the tool eliminates manual document-search bottlenecks, minimizes Mean Time to Repair (MTTR), and protects high-value assembly line hardware.

------------------------------
## Key Features

* Zero-Hallucination Grounding: System prompts strictly forbid guessing. If an error code or repair procedure is missing from the corpus, the bot explicitly refuses to answer.
* Safety-First Ingestion: Automatically surfaces mandatory Lock-Out/Tag-Out (LOTO) protocols and high-voltage warnings before presenting physical repair steps.
* Precise Source Citations: Every generated checklist includes the exact manual title, section, and page number with direct links to verify schematics.
* Deterministic Table Parsing: Uses layout-aware processing to ensure dense troubleshooting matrices and hardware pin-outs do not get fragmented or misread.

------------------------------
## 📂 Supported Document Corpus
The vector database is partitioned and tagged using strict metadata matrices to support the primary automation systems deployed on the factory floor:

| System Category | Targeted Hardware Elements | Essential Documents Parsed |
|---|---|---|
| Robotics & Kinematics | Fanuc R-2000iC, Kuka KR QUANTEC | Controller Guides (R-30iB/KRC4), Mechanical Maintenance Manuals |
| Automation & PLCs | Siemens SIMATIC S7-1500, Allen-Bradley ControlLogix 5580 | Hardware Installation Guides, System Diagnostic Buffer Manuals |
| Motion & Drive Control | Siemens SINAMICS S120, Allen-Bradley Kinetix | Servo Drive Fault & Alarm Tables, VFD Parameter Guides |
| Plant Safety | Integrated Robotic Cells | Facility Lock-Out/Tag-Out (LOTO) Regs, E-Stop Circuit Schematics |

------------------------------
## 🛠️ Technical Architecture
The platform runs entirely within a secure, private network footprint to protect proprietary facility layouts and network schema.

[User Query] ➔ [API Gateway] ➔ [Guardrails Layer] ➔ [Vector Search via Metadata]
                                                            │
[Actionable Checklist Output] 🖫 [LLM Generation] 🗄️ [Context Retrieval from Vector DB]

## Core Stack

* Document Ingestion: [Unstructured.io](https://unstructured.io/) / LlamaParse (Vision-based PDF extraction to preserve tables and columns).
* Vector Database: ChromaDB / Pinecone (Self-hosted or private cloud instance).
* Embeddings & LLM: text-embedding-3-small + Grounded Context Tuning.
* Frontend UI: Light, high-contrast web app optimized for floor-mounted terminals and ruggedized maintenance tablets.

------------------------------
## 💻 Sample Ingestion Pipeline
To parse technical manuals without splitting critical troubleshooting table rows across separate vector chunks, run the specialized chunking script:

from llamaindex.core import SimpleDirectoryReaderfrom llamaindex.core.node_parser import SemanticSplitterNodeParserfrom llamaindex.embeddings.openai import OpenAIEmbedding
# Initialize layout-aware document parserreader = SimpleDirectoryReader(
    input_dir="./corpus/fanuc_manuals",
    required_exts=[".pdf"]
)documents = reader.load_data()
# Use semantic/structural chunking to keep troubleshooting matrices intactembed_model = OpenAIEmbedding()splitter = SemanticSplitterNodeParser(
    buffer_size=1, 
    breakpoint_percentile_threshold=95, 
    embed_model=embed_model
)nodes = splitter.get_nodes_from_documents(documents)
# Inject mandatory equipment metadata tags for scoped queryingfor node in nodes:
    node.metadata["factory_site"] = "Giga_Texas"
    node.metadata["equipment_class"] = "Robotics_Fanuc"

------------------------------
## 🚦 Verification & Guardrails
To protect both technicians and heavy assembly machinery, the chatbot's system prompt enforces three unbreakable operational rules:

   1. Explicit Refusal over Speculation: If the vector database returns an empty context array for an error query, the system output must match: "Error configuration not found in localized manuals. Escalate immediately to Automation Engineering."
   2. Safety Preamble: Any retrieved passage containing DANGER, WARNING, or HIGH VOLTAGE tags must be fully extracted and pinned to the absolute top of the user output in bold formatting.
   3. Strict Bounds: The model is programmatically isolated from executing active system code modifications, modifying active PLC rungs, or accessing external search engines.

------------------------------
## 📈 Definition of Done
This tool is considered production-ready when the pilot phase matches the following metrics:

* User Group: 5 senior maintenance technicians across rotating shifts.
* Duration: 1 contiguous week of live tracking during breakdown events.
* Target Metric: A reduction of average diagnostic intake time (time spent searching documentation prior to executing a physical repair) by at least 15 minutes per complex fault event.

------------------------------
Would you like me to add a section details on how to configure the specific Docker container for local on-premise hosting, or should we write out the exact System Prompt text that enforces the safety guardrails?


https://www.haascnc.com/content/dam/haascnc/en/service/reference/fanuc-manuals/Fanuc%20Robot%20Series%20R-30iB%20Mate%20+%20Mate%20Plus%20Maintenance%20Manual.pdf

https://robochallenge.pl/wp-content/uploads/2025/02/R-30iBMate_Plus_controller_maintenance_manual_B-83525EN_10.1.pdf

https://www.fanuc.com/fvl/vn/product/catalog/RR-2000iC(E)-06.pdf

https://robochallenge.pl/wp-content/uploads/2025/02/R-30iBMate_Plus_controller_maintenance_manual_B-83525EN_10.1.pdf

