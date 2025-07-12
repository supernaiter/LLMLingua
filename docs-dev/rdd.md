# LLMLingua‑JP — Detailed Roadmap & Requirements/Design Document (RDD)

*Last updated: 2025‑07‑13*

---

## 0. Overview

LLMLingua‑JP is a fork of Microsoft Research’s **LLM‑Lingua** that adds first‑class support for Japanese text compression so that long Japanese prompts can be reduced in token length before being sent to local or cloud LLMs. The project is released under MIT License and targets Python ≥ 3.9.

---

## 1. Roadmap (4‑Week MVP Cycle)

| Week                             | Milestone                     | Key Activities                                                                                                                                                                                                                                | Owner(s)        | Deliverables           |
| -------------------------------- | ----------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | --------------- | ---------------------- |
| **W0 – Kick‑off**                | Fork & Project Setup          | • Fork upstream repo<br>• Verify MIT license compatibility<br>• Enable GitHub Discussions/Projects<br>• Add CODEOWNERS & Contributing guide                                                                                                   | Lead Maintainer | *Repo skeleton live*   |
| **W1 – Tokenizer Integration**   | Japanese tokenisation         | • Select **fugashi + unidic‑lite** as default deps<br>• Implement `tokenize_jp()` util<br>• Create `PromptCompressorJP` subclass (Strategy pattern)<br>• Add basic JP unit tests (pytest)<br>• CI matrix (English + Japanese)                 | Core Dev        | PR #1 merged           |
| **W2 – Core Compression Wiring** | Wire tokenizer into core flow | • Override `compress_prompt()` to accept `lang="ja"` or auto‑detect Unicode blocks<br>• Preserve sentence order & punctuation<br>• Bench accuracy vs upstream (±1 %)<br>• Update docs & type hints<br>• Maintain 100 % backward compatibility | Core Dev        | PR #2 merged           |
| **W3 – CLI & Packaging**         | PyPI release & CLI            | • Create `llmlingua‑jp` namespace pkg<br>• Implement `llmlingua‑jp` CLI (`-i/-o/-b` flags)<br>• Write README (EN/JA)<br>• Add example notebooks & Dockerfile<br>• Publish **v0.1.0** to PyPI                                                  | Release Eng     | v0.1.0 tag + PyPI      |
| **W4 – QA & Demo**               | Alpha release & showcase      | • End‑to‑end benches (fugashi+ELYZA 8B)<br>• Collect precision/recall metrics on JA summarisation dataset<br>• Create HF Space demo & blog post<br>• File upstream PR or RFC for integration                                                  | QA Lead         | v0.2.0 “alpha” release |

> **Fast‑track option:** Combine W1+W2 in a single sprint and release v0.1.0 at end of Week 2 if resources are limited.

---

## 2. Requirements & Design Document (RDD)

### 2.1 Purpose

Provide a Japanese‑capable prompt compressor that trims input length by 30–50 % without semantic drift, enabling faster and cheaper inference with local (e.g., Llama‑3‑ELYZA‑JP‑8B) and remote LLMs.

### 2.2 Scope

* **In‑scope:** Japanese tokenisation, scoring, and reconstruction; CLI; PyPI package; CI/CD; docs.
* **Out‑of‑scope (MVP):** Custom ML retraining, multilingual generalisation beyond JA/EN, GUI, fine‑tuning models.

### 2.3 Stakeholders

| Role          | Name                   | Interest               |
| ------------- | ---------------------- | ---------------------- |
| Product Owner | You (Repo Owner)       | Direction, accept PRs  |
| Core Dev(s)   | Volunteer contributors | Feature implementation |
| Users         | JP LLM community       | Usable compressor      |

### 2.4 Functional Requirements

| ID       | Description                       | Acceptance Criteria                                     |
| -------- | --------------------------------- | ------------------------------------------------------- |
| **FR‑1** | Handle UTF‑8 Japanese input       | No Unicode errors on 10k‑char articles                  |
| **FR‑2** | Compression ratio control         | `context_budget` 0.1–0.9; output <= ratio±1 %           |
| **FR‑3** | Preserve original order & meaning | ROUGE‑L drop <5 % vs reference summary                  |
| **FR‑4** | CLI tool                          | `llmlingua‑jp -i foo.txt -b 0.4` prints compressed text |
| **FR‑5** | Backward compatibility            | Upstream English tests all green                        |

### 2.5 Non‑Functional Requirements

| ID        | Metric       | Target                                       |
| --------- | ------------ | -------------------------------------------- |
| **NFR‑1** | Throughput   | ≥20k JP chars / ≤1 s (M1 Pro)                |
| **NFR‑2** | Dependencies | Only `fugashi`, `unidic‑lite`, existing libs |
| **NFR‑3** | Coverage     | pytest ≥80 % lines                           |
| **NFR‑4** | CI           | GitHub Actions <5 min run                    |

### 2.6 System Design

* **Tokenizer Layer** – `tokenize_jp(text)` uses fugashi; returns whitespace‑delimited string.
* **Compressor Core** – Reuses Lingua‑2 scoring; accepts tokenised input.
* **Facade Class** – `PromptCompressorJP` selects tokenizer by `lang`.
* **CLI** – Thin wrapper over compressor; supports file/stdin pipe.
* **Packaging** – `llmlingua_jp` namespace; entry‑point console\_script.

### 2.7 Interfaces

```python
compress_prompt(prompt:str, *, context_budget:float=0.3, lang:str="auto") -> dict
```

Returns `{compressed_prompt:str, original_len:int, compressed_len:int}`.

### 2.8 Data & Models

* No new weights; relies on heuristic scoring.
* Unit test fixtures: JP Wikipedia abstracts, Japanese novel snippets.

### 2.9 Testing Strategy

1. **Unit** – Tokeniser correctness, ratio maths.
2. **Integration** – CLI round‑trip, backward compatibility suite.
3. **Benchmark** – Speed benchmark via `pytest-benchmark`.
4. **Regression** – Snapshot compressed outputs in Git LFS.

### 2.10 Deployment & Release

* **Branching:** `main` (stable) / `dev` (active).
* **Versioning:** SemVer; start at `0.1.0`.
* **Distribution:** PyPI (`twine upload`).
* **Docker:** `docker build -t llmlingua-jp .` for demo.

### 2.11 Risks & Mitigations

| Risk                      | Impact         | Likelihood | Mitigation                              |
| ------------------------- | -------------- | ---------- | --------------------------------------- |
| Tokenisation edge cases   | Semantic loss  | Medium     | Add rule‑based post‑checks, unit tests  |
| Upstream breaking changes | Build fail     | Medium     | Pin upstream commit; CI alerts          |
| Dependency size (UniDic)  | Install weight | Low        | default to `unidic‑lite`, full as extra |

### 2.12 Future Work

* SentencePiece/Sudachi optional back‑ends
* Training Lingua‑2 on Japanese corpus
* Web UI & VS Code extension

---

## 3. Immediate Next Steps (Action Items)

1. **Fork the repo** and push CODEOWNERS. *(today)*
2. Add `requirements-dev.txt` with fugashi & unidic‑lite. *(today)*
3. Scaffold `tokenize_jp()` util and basic pytest. *(Week 1)*
4. Prepare PR #1 titled **“Add Japanese tokenizer (fugashi)”**. *(Week 1)*

---
