import os
import re
import spacy
import pdfplumber
import pandas as pd
from datetime import datetime
from collections import Counter

# ✅ Output directory setup
OUTPUT_DIR = os.path.join("backend", "outputs")
os.makedirs(OUTPUT_DIR, exist_ok=True)

def extract_text_from_pdf(pdf_path):
    if not os.path.exists(pdf_path):
        print(f"❌ File not found: {pdf_path}")
        return None

    text = ""
    try:
        with pdfplumber.open(pdf_path) as pdf:
            for page in pdf.pages:
                page_text = page.extract_text()
                if page_text:
                    text += page_text + "\n"

        if text.strip():
            # ✅ Save extracted text inside OUTPUT_DIR
            output_path = os.path.join(OUTPUT_DIR, "extracted_text.txt")
            with open(output_path, "w", encoding="utf-8") as f:
                f.write(text)
            return output_path
        else:
            print("⚠️ No text found in the PDF.")
            return None
    except Exception as e:
        print(f"❌ Error: {e}")
        return None

def analyze_esg(pdf_path):
    txt_file = extract_text_from_pdf(pdf_path)
    if not txt_file:
        return

    with open(txt_file, "r", encoding="utf-8") as f:
        text = f.read().lower()

    nlp = spacy.load("en_core_web_sm")
    doc = nlp(text)
    lemmas = [token.lemma_ for token in doc]

    esg_risk_keywords = {
        "Environmental":
 { 
"pollution": 2, "emission": 2, "toxic": 3, "waste": 1, "contamination": 3, "leak": 2, "climate": 2, "greenhouse": 2, "scarcity": 2, "depletion": 2, "deforestation": 3, "carbon": 2, "spill": 2, "violation": 2, "fine": 1, "fined": 1, "penalty": 2, "cleanup": 1, "remediation": 1, "liability": 2, "harm": 2, "destruction": 3, "extinction": 3, "endangered": 2, "habitat loss": 3, "flood": 2, "drought": 2, "storm": 2, "wildfire": 3, "temperature": 1, "warming": 2, "rising": 1, "shortage": 2, "overuse": 1, "unsustainable": 2, "degradation": 3, "non-compliance": 2, "illegal": 3, "unauthorized": 2, "banned": 2, "restricted": 1, "hazardous": 3, "dangerous": 3, "risky": 2, "unsafe": 2, "uncontrolled": 3
 },
 "Social":
 { "harassment": 3, "abuse": 3, "discrimination": 3, "accident": 2, "injury": 2, "fatality": 3, "death": 3, "violence": 3, "assault": 3, "strike": 1, "protest": 1, "boycott": 1, "dispute": 2, "conflict": 2, "unrest": 2, "opposition": 1, "lawsuit": 2, "complaint": 2, "allegation": 2, "claim": 1, "charged": 2, "sued": 2, "prosecuted": 3, "child labor": 3, "forced labor": 3, "slavery": 3, "trafficking": 3, "underpaid": 2, "unpaid": 2, "overtime": 1, "overwork": 1, "exhaustion": 1, "stress": 1, "burnout": 1, "turnover": 1, "quit": 1, "fired": 2, "terminated": 2, "laid off": 2, "downsized": 1, "restructured": 1, "closure": 1, "inequality": 2, "unfair": 2, "bias": 2, "exclusion": 2, "retaliation": 3, "whistleblower": 2, "breach": 2, "hack": 3, "stolen": 3, "exposed": 2, "compromised": 2
 },
 "Governance":
 { 
"corruption": 3, "bribery": 3, "fraud": 3, "embezzlement": 3, "theft": 3, "stealing": 3, "misuse": 2, "criminal": 3, "prosecuted": 3, "charged": 3, "arrested": 3, "convicted": 3, "sentenced": 3, "sanctions": 3, "investigation": 2, "probe": 2, "inquiry": 2, "audit": 1, "review": 1, "examination": 1, "scrutiny": 1, "litigation": 2, "court": 2, "trial": 2, "settlement": 1, "judgment": 2, "misconduct": 3, "malpractice": 3, "negligence": 3, "failure": 2, "default": 2, "manipulation": 3, "insider trading": 3, "conflict": 2, "undisclosed": 3, "hidden": 2, "secret": 2, "falsified": 3, "misrepresented": 2, "overstated": 2, "understated": 2, "concealed": 3, "withheld": 2, "resignation": 1, "dismissed": 2, "removed": 2, "suspended": 2, "replaced": 1, "crisis": 3, "scandal": 3, "controversy": 2, "accusation": 2 
}
    }

    analysis_data = []
    total_score = 0
    total_terms = 0
    category_risks = {}

    for category, keywords in esg_risk_keywords.items():
        score = 0
        term_count = 0
        unique_hits = 0
        for kw, sev in keywords.items():
            count = text.count(kw) if " " in kw else lemmas.count(nlp(kw)[0].lemma_)
            score += count * sev
            term_count += count
            if count > 0:
                unique_hits += 1
        analysis_data.append({
            "Category": category,
            "Total ESG Terms Matched": term_count,
            "Weighted ESG Risk Score": score,
            "Unique Keywords Matched": unique_hits,
            "Total Keywords in Dictionary": len(keywords)
        })
        total_score += score
        total_terms += term_count

    for entry in analysis_data:
        entry["Risk Percentage (%)"] = round((entry["Weighted ESG Risk Score"] / total_score) * 100, 2) if total_score else 0
        entry["Term Percentage (%)"] = round((entry["Total ESG Terms Matched"] / total_terms) * 100, 2) if total_terms else 0
        pct = entry["Risk Percentage (%)"]
        if pct > 60:
            level = "High"
        elif pct > 30:
            level = "Medium"
        else:
            level = "Low"
        category_risks[entry["Category"]] = level

    company_risk = "High Risk" if "High" in category_risks.values() else "Medium Risk" if "Medium" in category_risks.values() else "Low Risk"

    # ✅ Save CSV into OUTPUT_DIR
    summary_csv_path = os.path.join(OUTPUT_DIR, "esg_summary.csv")
    df = pd.DataFrame(analysis_data)
    df = df[[ "Category", "Total ESG Terms Matched", "Weighted ESG Risk Score",
              "Unique Keywords Matched", "Total Keywords in Dictionary",
              "Term Percentage (%)", "Risk Percentage (%)" ]]
    df.to_csv(summary_csv_path, index=False)

    # Risky sentence
    highest = max(((sum(sev * sent.text.lower().count(kw) for cat in esg_risk_keywords.values() for kw, sev in cat.items()), sent.text.strip())
                   for sent in doc.sents), key=lambda x: x[0], default=(0, "Not found"))[1]

    company_match = re.search(r"(?:company\s*name\s*[:\-]?\s*|^)([A-Z][a-zA-Z&,\s]+(?:Inc|Ltd|Corporation|Corp|LLC|Group|Co\.|Limited))", text, re.IGNORECASE)
    company_name = company_match.group(1).strip() if company_match else "Unknown"
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    summary = f"""📄 ESG Risk Summary Report
====================================
🏢 Company Name         : {company_name}
🕒 Date of Analysis     : {timestamp}
📊 ESG Term Count       : {total_terms}
⚖️  Total Risk Score     : {total_score}
📈 Final ESG Risk Level : {company_risk}

📌 Risk Levels by Category:
"""
    for cat, lvl in category_risks.items():
        summary += f"   - {cat}: {lvl} Risk\n"

    summary += f"""

🚨 Highest Risky Sentence:
\"{highest}\""""

    # ✅ Save final text summary to OUTPUT_DIR
    summary_txt_path = os.path.join(OUTPUT_DIR, "company_esg_risk_summary.txt")
    with open(summary_txt_path, "w", encoding="utf-8") as f:
        f.write(summary)

    print("✅ Analysis complete. Reports saved to:", OUTPUT_DIR)

# Example run
if __name__ == "__main__":
    pdf = os.path.join("backend", "data", "nestle-esg.pdf")  # Adjust if needed
    analyze_esg(pdf)
