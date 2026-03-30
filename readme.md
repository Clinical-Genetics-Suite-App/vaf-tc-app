# VAF-TC Relationship Visualizer 🧬

[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_svg)](https://vaf-tc-graph.streamlit.app) 
*(Please replace the link above with your actual deployed URL)*

## Overview
The **VAF-TC Relationship Visualizer** is an interactive clinical tool designed to assist in the interpretation of genetic variants by modeling the mathematical relationship between **Pathological Tumor Content (TC)** and **Variant Allele Fraction (VAF)**. 

Based on Knudson's Two-Hit Theory and established copy number alteration models, this tool helps clinicians and researchers distinguish between germline and somatic events, particularly in complex clinical scenarios.

## Key Features
- **Interactive Modeling**: Real-time visualization of theoretical trajectories for Germline (Heterozygous, cnLOH, LOH-Deletion) and Somatic (Heterozygous, cnLOH, LOH-Deletion) variants.
- **Low Confidence Zone**: Automatic highlighting for samples with TC < 30%, where diagnostic reliability may be reduced due to low tumor purity.
- **Convergence Zone (Gray Zone) Alert**: An automated warning system for high-purity samples (TC ≥ 70%). In this range, germline and somatic LOH curves mathematically converge, necessitating careful clinical correlation.
- **Fixed Scaling**: A standardized 0–100% scale for both axes to ensure consistent visual interpretation across different samples.

## Clinical Significance
Distinguishing between germline and somatic LOH is critical for therapeutic decision-making. 

As demonstrated in our study, high-TC samples (TC ≥ 90%) with elevated VAFs are often at risk of being misidentified as somatic events. However, such cases may represent **Germline LOH**, which is a vital finding for identifying Hereditary Breast and Ovarian Cancer (HBOC) and Lynch Syndrome. Accurate identification in this "Convergence Zone" is therapeutically significant, as these patients may show favorable responses to targeted therapies such as **PARP inhibitors**.

## How to Use
1. **Access the Web App**: [Click here to launch the interactive tool](https://vaf-tc-graph.streamlit.app).
2. **Input Parameters**: Use the sidebar to input the pathological TC (%) and observed VAF (%) from your NGS report.
3. **Analyze**: Compare your data point (black circle) against the theoretical curves to assess the likelihood of germline vs. somatic origin.

## Installation (Local Execution)
If you wish to run this tool locally, ensure you have Python installed, then:

```bash
git clone [https://github.com/Clinical-Genetics-Suite/vaf-tc-graph.git](https://github.com/Clinical-Genetics-Suite/vaf-tc-graph.git)
cd vaf-tc-graph
pip install -r requirements.txt
streamlit run app.py
