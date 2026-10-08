# PCI DSS Policy Match

An AI-powered compliance checker that reads an organization's policy and procedure documents, then automatically matches each PCI DSS requirement to the exact place in those documents where it is (or isn't) addressed — down to the document name, page number, and matching text.

## Overview

Compliance teams typically have to manually cross-reference dozens of PCI DSS requirements against a stack of internal policy PDFs — a slow, error-prone process. This project automates that lookup using semantic search: instead of relying on exact keyword matches, it uses sentence embeddings to understand the *meaning* of each requirement and find the policy text that actually addresses it, even if the wording is completely different.

**Pipeline:** `Documents → Read → Chunk → Embeddings → Search → Compliance → Output`

## How It Works

1. **Read** — All policy/procedure PDFs are parsed page-by-page using `PyPDF2`.
2. **Chunk** — Each page's text is split into smaller units (lines, falling back to sentence-level splitting for short lines) so that search results point to a specific, readable snippet rather than a whole page.
3. **Embed** — Every chunk is converted into a 384-dimensional vector using the `all-MiniLM-L6-v2` sentence-transformer model, which captures semantic meaning rather than just keywords.
4. **Search** — Each PCI DSS requirement is embedded the same way, and cosine/dot-product similarity against every chunk is computed in a single vectorized NumPy operation (no loops) to rank the most relevant matches.
5. **Compliance Check** — The top matches are filtered by a similarity threshold (`> 0.6`). If a strong match exists, the requirement is marked **Compliant**; otherwise, **Not Compliant**.
6. **Output** — Results are displayed inline, exportable to a pandas DataFrame, or written out to an Excel report (`PCI_Compliance_Report.xlsx`).

## Tech Stack

| Purpose | Library |
|---|---|
| PDF text extraction | `PyPDF2` |
| Sentence embeddings | `sentence-transformers` (`all-MiniLM-L6-v2`) |
| Similarity scoring | `NumPy` (vectorized dot product) |
| Results table / export | `pandas`, `openpyxl` |

## Example Input

A sample of PCI DSS requirements checked against the policy set:

- **Req 3.3.1** — SAD (Sensitive Authentication Data) must not be stored after authorization, even if encrypted.
- **Req 3.4.1** — PAN must be masked when displayed (showing at most the BIN and last four digits).
- **Req 8.3.1** — Passwords must meet a minimum complexity/length standard.

## Example Output

```
==================================================
Requirement: PCI DSS Req 3.3.1: SAD is not stored after authorization, even if encrypted
Status: Compliant
Reason: Relevant policy found with high similarity

Document: 01_Information_Security_Policy.pdf
Page: 7
Score: 0.67
Text: SAD shall never be stored after authorization, even if encrypted
```

Each result tells you exactly **which document**, **which page**, and **which sentence** satisfies (or fails to satisfy) the requirement — along with a similarity score for confidence.

## Sample Policy Documents Expected

The notebook expects the following PDFs in its working directory (any organization's equivalents can be substituted):

```
01_Information_Security_Policy.pdf
02_Acceptable_Use_Policy.pdf
03_Access_Control_Policy.pdf
04_Change_Control_Policy.pdf
05_Configuration_Management_Policy.pdf
06_Data_Handling_and_Encryption_Policy.pdf
07_Hardening_Procedures.pdf
08_Password_Policy.pdf
09_Incident_Response_Policy.pdf
10_Secure_Development_Policy.pdf
```

## Output Formats

- **Inline console output** — human-readable per-requirement breakdown.
- **Pandas DataFrame** — tabular view for further analysis.
- **Excel report** (`PCI_Compliance_Report.xlsx`) — shareable spreadsheet with Requirement, Status, Reason, Document, Page, Score, and matched Text columns.

## Getting Started

```bash
pip install PyPDF2 sentence-transformers numpy pandas openpyxl
```

Place your policy PDFs in the project directory, update the `files` list and `pci_requirements` list in the notebook, then run all cells in order.

## Possible Extensions

- Expand the PCI DSS requirement list to cover the full standard (v4.0) rather than a sample subset.
- Tune or replace the similarity threshold with a more robust classifier.
- Swap `all-MiniLM-L6-v2` for a larger/domain-tuned embedding model for higher accuracy.
- Add a simple UI (Streamlit/Gradio) for non-technical compliance reviewers.
- Support additional document formats beyond PDF (DOCX, HTML).

## Disclaimer

This tool assists with locating candidate policy language for PCI DSS requirements based on semantic similarity; it does not constitute a certified compliance assessment. Results should be reviewed by a qualified compliance professional (e.g., a QSA) before being relied upon for an actual PCI DSS audit.


