# VAF-TC Precision Analyzer

[![Python 3.9+](https://img.shields.io/badge/python-3.9+-blue.svg)](https://www.python.org/downloads/)
[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://vaf-tc-app.streamlit.app/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

An interactive visual tool for differentiating germline and somatic variants in **tumor-only sequencing**, based on the mathematical relationship between pathological **Tumor Content (TC)** and **Variant Allele Fraction (VAF)**.

> **Disclaimer:** This tool is intended as a supportive aid for genetic counseling. It does not replace confirmatory germline testing or established clinical guidelines (ACMG, AMED Kosugi group). Further prospective validation is required.

## Live Application

**https://vaf-tc-app.streamlit.app/**

## Background

In tumor-only comprehensive genomic profiling (CGP), distinguishing germline from somatic variants is a fundamental challenge. While VAF of approximately 50% is often assumed to indicate a germline heterozygous variant, **somatic variants with LOH can produce the same VAF** depending on tumor content — a diagnostic trap.

This tool visualizes five theoretical VAF-TC models derived from **Knudson's two-hit hypothesis** (diploid model) and provides automated clinical alerts for known ambiguity zones.

## Mathematical Models

Given tumor content *f* (0-1):

| Model | Formula | Description |
|-------|---------|-------------|
| Germline + cnLOH | VAF = (1 + f) / 2 | Germline variant with copy-neutral LOH (UPD) |
| Germline + LOH (Del) | VAF = 1 / (2 - f) | Germline variant with LOH by deletion |
| Germline Heterozygous | VAF = 0.5 | Germline variant without LOH |
| Somatic + cnLOH | VAF = f | Somatic variant with copy-neutral LOH (UPD) |
| Somatic + LOH (Del) | VAF = f / (2 - f) | Somatic variant with LOH by deletion |

A **+/-10% error margin** is applied for model matching to account for variability in pathological TC estimation.

## Clinical Alert System

The app generates four context-dependent alerts based on TC and VAF:

### Alert 1 - Somatic cnLOH Trap (TC 40-60%)

At TC near 50%, Somatic + cnLOH produces VAF = TC, which falls within +/-10% of Germline Heterozygous (50%). A somatic variant with acquired uniparental disomy (UPD) can masquerade as a germline finding. Pair-normal testing is essential.

### Alert 2 - Gray Zone (TC 61-66%)

As TC increases toward 66.7%, Somatic + LOH (Del) = f/(2-f) approaches 50% from below. In this range, the somatic LOH deletion line is close enough to 50% to create ambiguity with Germline Heterozygous variants.

### Alert 3 - LOH Convergence Zone (TC >= 67%)

At TC = 2/3 (approximately 66.7%), Somatic + LOH (Del) **exactly equals** Germline Heterozygous at 50%. Above this TC, the somatic and germline LOH lines converge. This alert fires when:

- **TC >= 67%**, AND
- **VAF >= Somatic LOH (Del) line** at current TC

Both conditions must be met. The alert displays the actual theoretical values for clinical reference.

### Alert 4 - Extreme Tumor Purity (TC >= 90%)

At very high purity, all five theoretical models compress into a narrow VAF range. Variants may still be of somatic origin even at high VAF. This alert fires regardless of VAF, as germline testing becomes essential in all cases.

## Features

- **Interactive graph** with five theoretical VAF-TC curves (Plotly)
- **Model matching** with +/-10% error margin and theoretical VAF display
- **Low Confidence Zone** shading for TC < 30%
- **CSV template download** for multi-variant workflows
- **Clinical notes** on PARPi indications and Lynch Syndrome / ICI responsiveness

## Getting Started

### Requirements

- Python 3.9+
- Dependencies: streamlit, plotly, numpy, pandas

### Installation

```bash
pip install -r requirements.txt
streamlit run app.py
```

## Repository Contents

| File | Description |
|------|-------------|
| app.py | Main Streamlit application (ver 3.0) |
| requirements.txt | Python dependencies |
| VAF-TC theoretical_model.xlsx | Excel file for generating theoretical VAF-TC curves |
| VAF_TC_theoretical_model.csv | CSV version of the theoretical model data |
| data_dictionary.txt | Variable definitions for the theoretical model |

## Citation

If you use this tool in your research, please cite:

> Kashima M, Tsubamoto H, et al. "VAF-Tumor Content Graph: A Simple Visual Tool for Discriminating Germline and Somatic Variants in Tumor-Only Sequencing." *Journal of Human Genetics* (submitted).

## Authors

**Clinical Genetics Suite** - Hyogo Medical University

## License

MIT License
