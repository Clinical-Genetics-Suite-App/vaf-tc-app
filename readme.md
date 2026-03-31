# VAF-TC Precision Analyzer: Clinical Genetics Support Tool

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.9+](https://img.shields.io/badge/python-3.9+-blue.svg)](https://www.python.org/downloads/)
[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://vaf-tc-app.streamlit.app/)

## 🧬 Overview
**VAF-TC Precision Analyzer** is a clinical decision-support tool designed to differentiate between somatic and germline variants by modeling the mathematical relationship between **Pathological Tumor Content (TC)** and **Variant Allele Frequency (VAF)**. 

In precision oncology, distinguishing true germline variants (e.g., *BRCA1/2* in HBOC) from somatic drivers with Loss of Heterozygosity (LOH) is a major diagnostic challenge. This tool provides a robust framework to identify the "50% VAF Trap" and other common pitfalls in NGS data interpretation.

---

## 🚀 Key Clinical Features

### 1. The "50% VAF Trap" Alert (Dynamic Logic)
The most critical diagnostic error in NGS analysis is the reflexive interpretation of a **VAF ≈ 50%** as a heterozygous germline variant. Our model identifies a specific "Grey Zone":
- **The Intersection:** At a Pathological TC of **~66.7%**, a **Somatic LOH (deletion)** event yields a theoretical VAF of exactly **50%**.
- **Dynamic Alert:** When a user inputs TC between 60-75%, the app triggers a high-priority warning. This alerts the clinician that a somatic driver could perfectly mimic a germline finding in this purity range.

### 2. Multi-Model Compatibility (±10% Variance)
NGS data contains inherent "noise" (sequencing depth, library preparation bias) and biological complexity (aneuploidy/mosaicism). Instead of a single deterministic result, this tool:
- Lists all theoretical models (Somatic Het, Somatic LOH, Germline Het, Germline LOH) within a **±10% VAF margin** of the observed data.
- Encourages a conservative, multi-faceted diagnostic approach.

### 3. Pathological TC as the Gold Standard
Unlike tools that rely on NGS-derived purity estimates (which can lead to circular reasoning), this analyzer emphasizes **Pathological Tumor Content** (assessed by a pathologist) as the primary independent variable, enhancing the external validity of the results.

---

## 🩺 Clinical Context & Scope

### PARP Inhibitor (PARPi) Indications
The app calculates **Biallelic Inactivation (LOH)**—a primary biomarker for PARPi sensitivity. However, users are alerted to the following regulatory nuances:
- **Ovarian & Prostate Cancer:** Sensitivity is often observed in both **Germline (gBRCA)** and **Somatic (sBRCA)** variants with LOH.
- **Breast & Pancreatic Cancer:** Regulatory approval is primarily restricted to **Germline (gBRCA)** carriers.
*Note: This tool provides biological insights; clinical decisions should follow regional guidelines (NCCN, ESMO, etc.).*

---

## 🌐 Live Application
The analyzer is deployed and accessible at:
👉 **[https://vaf-tc-app.streamlit.app/](https://vaf-tc-app.streamlit.app/)**

---

## 🛠 Installation & Usage (Local)

1. Clone the repository:
   ```bash
   git clone [https://github.com/Clinical-Genetics-Suite-App/vaf-tc-app.git](https://github.com/Clinical-Genetics-Suite-App/vaf-tc-app.git)
