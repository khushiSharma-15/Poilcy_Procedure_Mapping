import streamlit as st
import PyPDF2
import re
import io
import numpy as np
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# Page Configuration
st.set_page_config(
    page_title="Secure Policy & Procedure Compliance Auditor",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom Styling - Modern Glassmorphism & Dark Theme
st.markdown("""
<style>
    /* Dark Theme Base */
    .stApp {
        background-color: #0d1117;
        color: #c9d1d9;
    }
    
    /* Header Container */
    .main-header {
        background: linear-gradient(135deg, rgba(30, 41, 59, 0.7), rgba(15, 23, 42, 0.9));
        backdrop-filter: blur(10px);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 16px;
        padding: 24px;
        margin-bottom: 24px;
        box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.37);
    }
    .main-header h1 {
        color: #58a6ff;
        font-size: 2.2rem;
        margin-bottom: 8px;
    }
    .main-header p {
        color: #8b949e;
        font-size: 1.05rem;
    }

    /* Privacy Banner */
    .privacy-banner {
        background: rgba(46, 160, 67, 0.15);
        border: 1px solid rgba(46, 160, 67, 0.4);
        border-radius: 10px;
        padding: 12px 16px;
        color: #3fb950;
        font-size: 0.95rem;
        display: flex;
        align-items: center;
        margin-bottom: 20px;
    }

    /* Metric Cards */
    .metric-card {
        background: rgba(22, 27, 34, 0.8);
        border: 1px solid rgba(48, 54, 61, 0.8);
        border-radius: 12px;
        padding: 18px;
        text-align: center;
    }
    .metric-value {
        font-size: 2.2rem;
        font-weight: 700;
        margin-top: 4px;
    }
    .metric-label {
        font-size: 0.9rem;
        color: #8b949e;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }

    /* Status Badges */
    .badge-compliant {
        background-color: rgba(46, 160, 67, 0.2);
        color: #3fb950;
        border: 1px solid rgba(46, 160, 67, 0.4);
        padding: 4px 12px;
        border-radius: 20px;
        font-weight: 600;
        font-size: 0.85rem;
    }
    .badge-non-compliant {
        background-color: rgba(248, 81, 73, 0.2);
        color: #f85149;
        border: 1px solid rgba(248, 81, 73, 0.4);
        padding: 4px 12px;
        border-radius: 20px;
        font-weight: 600;
        font-size: 0.85rem;
    }

    /* Policy Match Container */
    .match-box {
        background: rgba(30, 41, 59, 0.4);
        border-left: 4px solid #58a6ff;
        padding: 12px 16px;
        margin-top: 10px;
        border-radius: 0 8px 8px 0;
    }
</style>
""", unsafe_allow_html=True)

# Main Header
st.markdown("""
<div class="main-header">
    <h1>🛡️ Secure Compliance & Policy Auditor</h1>
    <p>Upload requirement standards and organizational policies to perform automated local vector matching & gap analysis.</p>
</div>
""", unsafe_allow_html=True)

# Privacy Banner
st.markdown("""
<div class="privacy-banner">
    🔒 <strong>Zero-Knowledge Local Execution:</strong> All uploaded PDFs are processed purely in-memory (RAM) on your local machine. Documents are never saved to disk or transmitted over external networks.
</div>
""", unsafe_allow_html=True)

# Helper Functions
def read_pdf_bytes(file_bytes, filename):
    data = []
    try:
        pdf_file = io.BytesIO(file_bytes)
        reader = PyPDF2.PdfReader(pdf_file)
        for i, page in enumerate(reader.pages):
            text = page.extract_text() or ""
            data.append({
                "doc": filename,
                "page": i + 1,
                "text": text
            })
    except Exception as e:
        st.error(f"Error reading PDF '{filename}': {e}")
    return data

def chunk_data(all_data):
    chunks = []
    for item in all_data:
        doc = item["doc"]
        page = item["page"]
        text = item["text"]
        lines = text.split("\n")
        for line in lines:
            line = line.strip()
            if len(line.split()) >= 4:
                chunks.append({"doc": doc, "page": page, "text": line})
            else:
                sentences = re.split(r'(?<=[.!?])\s+', line)
                for sentence in sentences:
                    if len(sentence.split()) >= 4:
                        chunks.append({"doc": doc, "page": page, "text": sentence})
    return chunks

def run_tfidf_audit(pci_requirements, chunks, threshold):
    if not chunks:
        return []
    
    texts = [c["text"] for c in chunks]
    vectorizer = TfidfVectorizer(stop_words='english')
    tfidf_matrix = vectorizer.fit_transform(texts)
    
    results = []
    for req in pci_requirements:
        req_text = req.strip()
        if not req_text:
            continue
            
        query_vec = vectorizer.transform([req_text])
        scores = cosine_similarity(tfidf_matrix, query_vec).flatten()
        best_indices = scores.argsort()[::-1][:5]
        
        matches = []
        for idx in best_indices:
            score = float(scores[idx])
            if score >= threshold:
                matches.append({
                    "doc": chunks[idx]["doc"],
                    "page": chunks[idx]["page"],
                    "text": chunks[idx]["text"],
                    "score": score
                })
        
        status = "Compliant" if matches else "Not Compliant"
        reason = "Relevant policy found with high similarity" if matches else "No matching policy text found above similarity threshold"
        
        results.append({
            "requirement": req_text,
            "status": status,
            "reason": reason,
            "matches": matches
        })
    return results

# Sidebar Controls
st.sidebar.title("⚙️ Audit Configuration")
similarity_threshold = st.sidebar.slider(
    "Similarity Score Threshold",
    min_value=0.10,
    max_value=0.80,
    value=0.20,
    step=0.05,
    help="Minimum score required to tag a requirement as Compliant."
)

st.sidebar.markdown("---")
st.sidebar.subheader("📄 Local Workspace Policies")
use_sample_policies = st.sidebar.checkbox("Load 10 Local Policy PDFs (Default Dataset)", value=True)

# Main Inputs Column Layout
col1, col2 = st.columns([1, 1])

with col1:
    st.subheader("1. Requirements Input")
    req_option = st.radio("Choose Requirement Source:", ["Upload Requirements PDF", "Paste Custom Requirements Text"])
    
    requirements_list = []
    if req_option == "Upload Requirements PDF":
        req_file = st.file_uploader("Upload Requirements Standard (PDF)", type=["pdf"], key="req_pdf")
        if req_file:
            req_data = read_pdf_bytes(req_file.read(), req_file.name)
            req_chunks = chunk_data(req_data)
            requirements_list = [c["text"] for c in req_chunks if len(c["text"].split()) >= 5]
            st.success(f"Extracted {len(requirements_list)} requirements from '{req_file.name}'")
    else:
        custom_req_text = st.text_area(
            "Paste Requirements (one per line):",
            value="PCI DSS Req 3.3.1: SAD is not stored after authorization, even if encrypted\nPCI DSS Req 3.4.1: PAN is masked when displayed, showing at most BIN and last four digits\nPCI DSS Req 8.3.1: Passwords meet minimum length of 12 characters",
            height=150
        )
        requirements_list = [line.strip() for line in custom_req_text.split("\n") if line.strip()]

with col2:
    st.subheader("2. Policy Documents Input")
    uploaded_policy_files = st.file_uploader(
        "Upload Organizational Policy PDFs (Multiple allowed)",
        type=["pdf"],
        accept_multiple_files=True,
        key="policy_pdfs"
    )

# Process Uploaded & Default Policies
all_policy_data = []

# Load local PDFs if checked
default_files = [
    "01_Information_Security_Policy.pdf",
    "02_Acceptable_Use_Policy.pdf",
    "03_Access_Control_Policy.pdf",
    "04_Change_Control_Policy.pdf",
    "05_Configuration_Management_Policy.pdf",
    "06_Data_Handling_and_Encryption_Policy.pdf",
    "07_Hardening_Procedures.pdf",
    "08_Password_Policy.pdf",
    "09_Incident_Response_Policy.pdf",
    "10_Secure_Development_Policy.pdf"
]

if use_sample_policies:
    for fname in default_files:
        try:
            with open(fname, "rb") as f:
                all_policy_data.extend(read_pdf_bytes(f.read(), fname))
        except Exception:
            pass

if uploaded_policy_files:
    for pfile in uploaded_policy_files:
        all_policy_data.extend(read_pdf_bytes(pfile.read(), pfile.name))

policy_chunks = chunk_data(all_policy_data)

st.markdown("---")

# Run Audit Section
if st.button("🚀 Run Compliance Audit", type="primary", use_container_width=True):
    if not requirements_list:
        st.warning("Please provide requirement statements or upload a requirements PDF.")
    elif not policy_chunks:
        st.warning("Please upload policy documents or enable local default policy files.")
    else:
        with st.spinner("Analyzing compliance requirements against policy documents..."):
            audit_results = run_tfidf_audit(requirements_list, policy_chunks, similarity_threshold)
            st.session_state["audit_results"] = audit_results
            st.session_state["policy_chunks_count"] = len(policy_chunks)

# Display Results if Audit Has Run
if "audit_results" in st.session_state:
    results = st.session_state["audit_results"]
    total_reqs = len(results)
    compliant_count = sum(1 for r in results if r["status"] == "Compliant")
    non_compliant_count = total_reqs - compliant_count
    compliance_rate = (compliant_count / total_reqs * 100) if total_reqs > 0 else 0

    st.subheader("📊 Compliance Audit Dashboard")
    
    # KPI Metrics Cards
    m1, m2, m3, m4 = st.columns(4)
    with m1:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-label">Total Evaluated</div>
            <div class="metric-value" style="color:#58a6ff;">{total_reqs}</div>
        </div>
        """, unsafe_allow_html=True)
    with m2:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-label">Compliant</div>
            <div class="metric-value" style="color:#3fb950;">{compliant_count}</div>
        </div>
        """, unsafe_allow_html=True)
    with m3:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-label">Non-Compliant Gaps</div>
            <div class="metric-value" style="color:#f85149;">{non_compliant_count}</div>
        </div>
        """, unsafe_allow_html=True)
    with m4:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-label">Compliance Rate</div>
            <div class="metric-value" style="color:#d29922;">{compliance_rate:.1f}%</div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    
    # Export Options
    excel_rows = []
    for r in results:
        if r["matches"]:
            for m in r["matches"]:
                excel_rows.append({
                    "Requirement": r["requirement"],
                    "Status": r["status"],
                    "Reason": r["reason"],
                    "Document": m["doc"],
                    "Page": m["page"],
                    "Similarity Score": round(m["score"], 2),
                    "Matching Policy Text": m["text"]
                })
        else:
            excel_rows.append({
                "Requirement": r["requirement"],
                "Status": r["status"],
                "Reason": r["reason"],
                "Document": "N/A",
                "Page": "N/A",
                "Similarity Score": 0.0,
                "Matching Policy Text": "No strong match found"
            })
            
    df_export = pd.DataFrame(excel_rows)
    excel_buffer = io.BytesIO()
    df_export.to_excel(excel_buffer, index=False, engine='openpyxl')
    excel_data = excel_buffer.getvalue()

    st.download_button(
        label="📥 Download Full Compliance Excel Report (.xlsx)",
        data=excel_data,
        file_name="PCI_Compliance_Audit_Report.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        use_container_width=True
    )

    st.markdown("<br>", unsafe_allow_html=True)
    st.subheader("📋 Requirement Match Breakdown")
    
    # Filter Tabs
    status_filter = st.radio("Filter Status:", ["All", "Compliant Only", "Non-Compliant Only"], horizontal=True)

    for i, res in enumerate(results):
        if status_filter == "Compliant Only" and res["status"] != "Compliant":
            continue
        if status_filter == "Non-Compliant Only" and res["status"] != "Not Compliant":
            continue
            
        badge_html = f'<span class="badge-compliant">Compliant</span>' if res["status"] == "Compliant" else f'<span class="badge-non-compliant">Not Compliant</span>'
        
        with st.expander(f"Req #{i+1}: {res['requirement'][:90]}... - Status: {res['status']}", expanded=(res["status"] == "Not Compliant")):
            st.markdown(f"**Requirement Statement**: {res['requirement']}")
            st.markdown(f"**Audit Status**: {badge_html}", unsafe_allow_html=True)
            st.markdown(f"**Reason**: {res['reason']}")
            
            if res["matches"]:
                st.markdown("#### Matched Policy Citations:")
                for m in res["matches"]:
                    st.markdown(f"""
                    <div class="match-box">
                        <strong>📄 File:</strong> <code>{m['doc']}</code> | <strong>Page:</strong> {m['page']} | <strong>Similarity:</strong> {m['score']*100:.1f}%<br>
                        <em>"{m['text']}"</em>
                    </div>
                    """, unsafe_allow_html=True)
            else:
                st.warning("⚠️ Action Required: No matching clause found in policy documents above the configured threshold.")
