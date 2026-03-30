# VAF-TC Relationship Visualizer 🧬

[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_svg)](https://vaf-tc-graph.streamlit.app) 

## Overview
The **VAF-TC Relationship Visualizer** is an interactive clinical tool designed to assist in the interpretation of genetic variants by modeling the mathematical relationship between **Pathological Tumor Content (TC)** and **Variant Allele Fraction (VAF)**. 

This tool helps clinicians and researchers distinguish between germline and somatic events, providing a theoretical framework based on Knudson's Two-Hit Theory and copy number alteration models.

## Key Features
- **Interactive Modeling**: Real-time visualization of theoretical trajectories for Germline (Heterozygous, cnLOH, LOH-Deletion) and Somatic (Heterozygous, cnLOH, LOH-Deletion) variants.
- **Low Confidence Zone**: Automatic highlighting for samples with TC < 30%, where diagnostic reliability may be reduced due to low tumor purity.
- **Convergence Zone (Gray Zone) Alert**: A targeted warning system for high-purity samples (**TC ≥ 70%**) with **elevated VAF levels**. In this range, theoretical curves for germline LOH and somatic LOH converge, making them mathematically difficult to distinguish by VAF alone.
- **Fixed Scaling**: A standardized 0–100% scale for both axes to ensure consistent visual perspective and reliable comparison across different clinical samples.

## Clinical Significance
Distinguishing between germline and somatic LOH is critical for therapeutic decision-making in oncology.

As demonstrated in our study, high-TC samples (TC ≥ 90%) with elevated VAFs are at significant risk of being misidentified as somatic events. However, such cases may represent **Germline LOH**, a vital finding for identifying Hereditary Breast and Ovarian Cancer (HBOC) and Lynch Syndrome. Accurate identification in this "Convergence Zone" is therapeutically significant, as these patients may show favorable responses to targeted therapies such as **PARP inhibitors**.

## How to Use
1. **Access the Web App**: [Click here to launch the interactive tool](https://vaf-tc-graph.streamlit.app).
2. **Input Parameters**: Use the sidebar to input the **Gene Name**, **Pathological TC (%)**, and observed **VAF (%)**.
3. **Analyze**: 
    - The black circle represents your sample. 
    - The "Automated Interpretation" section will identify which theoretical models most closely align with your data.
    - If the sample falls into the Convergence Zone with high VAF, a warning will appear to prompt further clinical correlation.

## Installation (Local Execution)
To run this tool locally:

```bash
git clone [https://github.com/Clinical-Genetics-Suite/vaf-tc-graph.git](https://github.com/Clinical-Genetics-Suite/vaf-tc-graph.git)
cd vaf-tc-graph
pip install -r requirements.txt
streamlit run app.py
