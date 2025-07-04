﻿# 🌍 ESG Risk Analyzer

The ESG Risk Analyzer is a web-based tool that allows users to upload ESG (Environmental, Social, and Governance) reports in PDF or TXT format, automatically analyze them using natural language processing, and generate downloadable risk summary reports.

---

## 🚀 Features

- Upload PDF/TXT ESG documents
- Extract and analyze ESG-related keywords
- Calculate weighted ESG risk scores
- Generate downloadable CSV and text summaries
- Responsive web interface with Light/Dark mode
- Sidebar with detailed project information

---

## 🛠️ Tech Stack

- **Backend**: Python, Flask
- **Frontend**: HTML, CSS, JavaScript (Vanilla)
- **Libraries**: pdfplumber, pandas, spaCy (NLP)
- **Deployment**: Render (free cloud hosting)

---

## 🧪 How to Run Locally

### ✅ 1. Clone the Repository

```bash
git clone https://github.com/your-username/esg-analyzer.git
cd esg-analyzer


>>Install dependencies 
pip install -r requirements.txt
python -m spacy download en_core_web_sm


>>Run
python app.py

>>live server
index.html
 or

>>Run locally
http://127.0.0.1:5000
