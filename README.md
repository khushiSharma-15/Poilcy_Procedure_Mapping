# 🛡️ PCI DSS Policy & Procedure Compliance Auditor

An AI-powered compliance auditing tool that automatically maps **PCI DSS requirements** to your organization's **policy and procedure documents**. It reads, chunks, and semantically searches across multiple PDF documents to find the most relevant policy matches — helping you verify compliance at scale.

![Python](https://img.shields.io/badge/Python-3.8%2B-blue?logo=python&logoColor=white)
![Streamlit](https://img.shields.io/badge/Streamlit-1.x-FF4B4B?logo=streamlit&logoColor=white)
![PCI DSS](https://img.shields.io/badge/PCI%20DSS-v4.0-green)
![License](https://img.shields.io/badge/License-MIT-yellow)

---

## 📌 Overview

Compliance teams spend **hundreds of hours** manually cross-referencing regulatory requirements against internal policy documents. This tool automates that process using **NLP-based vector similarity matching**.

### How It Works

```
📄 Policy PDFs → 📖 Read & Extract → 🧩 Chunk Text → 🔢 Vectorize → 🔍 Semantic Search → ✅ Compliance Report
```

1. **Document Ingestion** — Reads multiple organizational policy & procedure PDFs
2. **Text Chunking** — Splits documents into meaningful text segments (line-level + sentence-level)
3. **Vectorization** — Converts text chunks into numerical vectors using TF-IDF / AI embeddings
4. **Semantic Search** — Compares each PCI DSS requirement against all policy chunks
5. **Compliance Mapping** — Identifies best matches with similarity scores and generates a compliance report

---

## 🚀 Features

| Feature | Description |
|---|---|
| **Multi-Document Support** | Upload and process 10+ policy PDFs simultaneously |
| **Dual Engine** | TF-IDF (web app) + Sentence Transformers (notebook) for flexible matching |
| **Interactive Dashboard** | Streamlit-based UI with compliance KPIs, filters, and visual badges |
| **Excel Export** | One-click download of the full compliance audit report (.xlsx) |
| **Adjustable Threshold** | Fine-tune the similarity score cutoff via sidebar slider |
| **Zero-Knowledge** | All processing happens locally — no data leaves your machine |
| **Gap Analysis** | Instantly identify non-compliant requirements with no matching policies |

---

## 🗂️ Project Structure

```
Policy_procedure_mapping/
│
├── app.py                                  # 🌐 Streamlit Web Application (TF-IDF engine)
├── POLICY MATCH.ipynb                      # 📓 Jupyter Notebook (Sentence Transformers engine)
├── README.md                               # 📖 This file
│
├── 01_Information_Security_Policy.pdf      # 📄 Sample policy documents
├── 02_Acceptable_Use_Policy.pdf
├── 03_Access_Control_Policy.pdf
├── 04_Change_Control_Policy.pdf
├── 05_Configuration_Management_Policy.pdf
├── 06_Data_Handling_and_Encryption_Policy.pdf
├── 07_Hardening_Procedures.pdf
├── 08_Password_Policy.pdf
├── 09_Incident_Response_Policy.pdf
├── 10_Secure_Development_Policy.pdf
│
└── PCI_Compliance_Report.xlsx              # 📊 Generated compliance report
```

---

## ⚙️ Installation

### Prerequisites

- Python 3.8 or higher
- pip (Python package manager)

### Setup

```bash
# Clone the repository
git clone https://github.com/your-username/Policy_procedure_mapping.git
cd Policy_procedure_mapping

# Install dependencies
pip install streamlit PyPDF2 pandas openpyxl scikit-learn numpy

# (Optional) For the Jupyter Notebook engine with AI embeddings
pip install sentence-transformers torch
```

---

## 🖥️ Usage

### Web Application (Recommended)

Run the Streamlit dashboard:

```bash
streamlit run app.py
```

This opens a browser at `http://localhost:8501` with:
- 📄 **Upload** your PCI DSS requirements (PDF or paste text)
- 📂 **Load** organizational policy documents (10 pre-loaded defaults available)
- 🎚️ **Adjust** the similarity threshold via the sidebar
- 🚀 **Run** the compliance audit
- 📥 **Download** the Excel report

### Jupyter Notebook

For the AI-powered version using Sentence Transformers:

```bash
jupyter notebook "POLICY MATCH.ipynb"
```

Run all cells sequentially. The notebook uses the `all-MiniLM-L6-v2` model for deeper semantic understanding.

---

## 📊 Sample Output

| Requirement | Status | Document | Page | Score | Matching Policy Text |
|---|---|---|---|---|---|
| PCI DSS Req 3.3.1: SAD not stored after authorization | ✅ Compliant | Information_Security_Policy.pdf | 7 | 0.67 | SAD shall never be stored after authorization, even if encrypted |
| PCI DSS Req 3.4.1: PAN masked when displayed | ✅ Compliant | Information_Security_Policy.pdf | 7 | 0.60 | Full PAN shall be masked when displayed, showing at most the first six... |
| PCI DSS Req 8.3.1: Password minimum 12 characters | ✅ Compliant | Password_Policy.pdf | 2 | 0.65 | Minimum Length: 8 characters (Standard) / 12 characters (CDE Systems) |

---

## 🔧 Configuration

| Parameter | Default | Description |
|---|---|---|
| Similarity Threshold | 0.20 (TF-IDF) / 0.60 (Embeddings) | Minimum score to mark as "Compliant" |
| Top-K Results | 5 | Number of best matches returned per requirement |
| Min Chunk Length | 4 words | Minimum words for a text chunk to be indexed |

---

## 🧠 Technical Details

### Matching Engines

| Engine | Used In | Method | Pros |
|---|---|---|---|
| **TF-IDF** | `app.py` (Web App) | Term Frequency–Inverse Document Frequency | Fast, no GPU needed, lightweight |
| **Sentence Transformers** | `POLICY MATCH.ipynb` | `all-MiniLM-L6-v2` neural embeddings | Deeper semantic understanding, context-aware |

### Chunking Strategy

The system uses a **two-level chunking** approach:
1. **Line-level split** — Preserves the natural structure of policy documents
2. **Sentence-level fallback** — For short lines, splits on sentence boundaries (`.`, `!`, `?`)
3. **Minimum length filter** — Only chunks with ≥ 4 words are indexed

---

## 🤝 Contributing

Contributions are welcome! Here are some ideas:
- Add support for more compliance frameworks (ISO 27001, SOC 2, HIPAA)
- Implement a hybrid TF-IDF + embedding scoring approach
- Add PDF highlighting to show exact match locations
- Build a comparison mode for before/after policy updates

---

## 📜 License

This project is licensed under the MIT License. See [LICENSE](LICENSE) for details.

---

## 👨‍💻 Author

**Shubham Kumar**

---

> ⚠️ **Disclaimer**: This tool provides automated compliance suggestions based on text similarity. It is intended to **assist** compliance teams, not replace professional audit judgment. Always verify results with qualified compliance professionals.
