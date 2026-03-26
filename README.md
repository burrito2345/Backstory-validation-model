# NovelRAG — Character Backstory Consistency Checker

> *Does your backstory hold up against the canon? NovelRAG will tell you.*

---

## The Problem

LLMs forget. Feed them an entire novel and ask them to verify a character's backstory — they'll hallucinate timelines, invent relationships, and confidently get it wrong. For authors, editors, and game developers working with rich, established lore, that's a dealbreaker.

---

## The Solution

**NovelRAG** is a Retrieval-Augmented Generation pipeline built specifically for long-form fiction. It ingests an entire novel, extracts verifiable character facts, and cross-references them against any proposed backstory — returning a grounded, evidence-backed consistency verdict.

No hallucinations. No plot holes. Just the lore.

---

## What It Does

| | |
|---|---|
| **Bypasses Context Limits** | Processes full-length novels without overflowing any LLM's context window |
| **Atomic Fact Extraction** | Decomposes complex character histories into isolated, single-fact statements |
| **Automated Verdicts** | Returns `support`, `contradict`, or `neutral` for every claim in the hypothesis |
| **Detailed Scoring** | Quantifies consistency as a ratio of supporting vs. contradicting evidence |
| **Full Observability** | Powered by LangChain & LangSmith with end-to-end tracing and debugging |

---

## How It Works

```
Novel → Chunks → Embeddings → Vector Store
                                    ↓
         Backstory (Hypothesis) → Retrieval → Atomic Facts
                                                    ↓
                                            Consistency Check
                                                    ↓
                                    support / contradict / neutral
```

**① Ingestion & Chunking** — The novel is split into semantically meaningful chunks and embedded into a vector database.

**② Retrieval** — Given a character and a proposed backstory, the pipeline fetches the most relevant lore passages.

**③ Fact Decomposition** — Retrieved chunks are broken into atomic statements — one fact, one sentence, fully verifiable.

**④ Consistency Verdict** — An LLM evaluates the hypothesis against every atomic fact, mapping support and contradiction into a final scored report.

---

*Built for writers who take their lore seriously.*
