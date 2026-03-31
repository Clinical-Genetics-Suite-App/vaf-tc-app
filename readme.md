# VAF-TC Precision Analyzer: Clinical Genetics Support Tool

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.9+](https://img.shields.io/badge/python-3.9+-blue.svg)](https://www.python.org/downloads/)
[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://vaf-tc-app.streamlit.app/)

## 🧬 Overview
**VAF-TC Precision Analyzer** is a clinical decision-support tool designed to differentiate between somatic and germline variants by modeling the mathematical relationship between **Pathological Tumor Content (TC)** and **Variant Allele Frequency (VAF)**. 

In precision oncology, distinguishing true germline variants (e.g., *BRCA1/2* in HBOC) from somatic drivers with Loss of Heterozygosity (LOH) is a major diagnostic challenge. This tool provides a robust framework to identify the "50% VAF Trap" and addresses the mathematical convergence in high-purity samples.

---

## 🚀 Key Clinical Features

### 1. The "50% VAF Trap" Alert (Dynamic Logic)
One of the most critical pitfalls in NGS interpretation is the reflexive assumption that a **VAF ≈ 50%** indicates a germline variant. Our model flags a specific "Grey Zone":
- **The Intersection:** At a Pathological TC of **~66.7%**, a **Somatic LOH (deletion)** event yields a theoretical VAF of exactly **50%**.
- **Alert Mechanism:** When TC is between 60-75%, the app triggers a high-priority warning, preventing the misidentification of somatic drivers as hereditary findings.

### 2. High TC Convergence Analysis (≥90%)
At very high tumor purity, the theoretical VAFs for both **Somatic LOH** and **Germline LOH** converge toward 100%. 
- The tool explicitly alerts users that mathematical differentiation based on VAF alone becomes unreliable in this range.
- This prevents over-interpretation of VAFs in high-purity samples (e.g., *TP53* somatic LOH vs. germline variants).

### 3. Multi-Model Compatibility (±10% Variance)
To account for NGS "noise" (sequencing depth, library bias) and biological complexity (aneuploidy), the tool lists all theoretical models within a **±10% VAF margin**, ensuring a conservative diagnostic approach.

---

## 🩺 Clinical Context & Regulatory Scope

### PARP Inhibitor (PARPi) Indications
While the identification of **Biallelic Inactivation (LOH)** is a key biomarker for PARPi sensitivity, the app provides guidance on current regulatory landscapes:

| Organ System | Sensitivity Rationale | Clinical Indication (Typical) |
| :--- | :--- | :--- |
| **Ovarian & Prostate** | Biallelic inactivation (LOH) | **gBRCA and sBRCA** |
| **Breast & Pancreatic** | Biallelic inactivation (LOH) | **gBRCA Only** |

*Note: Clinical decisions must always align with regional drug labels (e.g., FDA, PMDA) and professional guidelines (NCCN, ESMO).*

---

## 🌐 Live Application
Access the tool here: 👉 **[https://vaf-tc-app.streamlit.app/](https://vaf-tc-app.streamlit.app/)**

---

## 📊 Mathematical Foundation
The app utilizes the following frameworks ($f$ = Tumor Fraction):
- **Somatic Heterozygous:** $VAF = f / 2$
- **Somatic LOH (Deletion):** $VAF = f / (2 - f)$
- **Germline Heterozygous:** $VAF = 0.5$
- **Germline LOH (Deletion):** $VAF = 1 / (2 - f)$

---

## 🛠 Installation & Usage (Local)

1. Clone the repository:
   ```bash
   git clone [https://github.com/Clinical-Genetics-Suite-App/vaf-tc-app.git](https://github.com/Clinical-Genetics-Suite-App/vaf-tc-app.git)
