# VAF–TC Visualizer

[![Python 3.9+](https://img.shields.io/badge/python-3.9+-blue.svg)](https://www.python.org/downloads/)
[![Streamlit App (EN)](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://vaf-tc-app.streamlit.app/)
[![Streamlit App (JA)](https://img.shields.io/badge/Streamlit-日本語版-FF4B4B?logo=streamlit&logoColor=white)](https://vaf-tc-app-ja.streamlit.app/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

An interactive visual tool for differentiating germline and somatic variants in **tumor-only sequencing**, based on the mathematical relationship between pathological **Tumor Content (TC)** and **Variant Allele Fraction (VAF)**.

> **Disclaimer:** This tool is intended as a supportive aid for genetic counseling. It does not replace confirmatory germline testing or established clinical guidelines. Further prospective validation is required.
> Gene Reference System is based on the **Guidelines for GPV/PGPV Handling Procedures in Cancer Gene Panel Testing (2025 Edition)** (MHLW Research Grant) — T-only PGPV disclosure recommended gene list.

## Live Application

- **English:** https://vaf-tc-app.streamlit.app/
- **Japanese (日本語版):** https://vaf-tc-app-ja.streamlit.app/

## Background

In tumor-only comprehensive genomic profiling (CGP), distinguishing germline from somatic variants is a fundamental challenge. While VAF of approximately 50% is often assumed to indicate a germline heterozygous variant, **somatic variants with LOH can produce the same VAF** depending on tumor content — a diagnostic trap.

This tool visualizes five theoretical VAF-TC models derived from **Knudson's two-hit hypothesis** (diploid model) and provides automated clinical alerts for known ambiguity zones.

## Important Note — Mathematical Model Assumptions

1. **Diploid assumption (Knudson's two-hit model):** Each theoretical line represents a specific biallelic inactivation scenario assuming a diploid (2-copy) baseline. The five models are idealized mathematical references, not an exhaustive catalog of all possible mechanisms.
2. **Aneuploidy is not accounted for:** Real tumors frequently exhibit aneuploidy, whole-chromosome gains/losses, and subclonal heterogeneity. Observed VAF may deviate substantially from the theoretical lines.
3. **TC estimation carries +/-10-20% error:** Pathological TC estimation is subject to +/-10-20% variability due to histological heterogeneity, sampling region, and inter-observer agreement. A +/-10% matching margin is applied, but clinical interpretation should consider the full uncertainty range.
4. **Not a diagnostic tool:** This is a visual aid for genetic counseling. Confirmatory germline testing remains the standard for any clinical decision.

## Mathematical Models

Given tumor content *f* (0-1):

| Model | Formula | Description |
|-------|---------|-------------|
| germline (cnLOH) | VAF = (1 + f) / 2 | Germline variant with copy-neutral LOH (UPD) |
| germline (LOH with Del) | VAF = 1 / (2 - f) | Germline variant with LOH by deletion |
| germline (Hetero) | VAF = 0.5 | Germline heterozygous variant without LOH |
| somatic (LOH with Del) | VAF = f / (2 - f) | Somatic variant with LOH by deletion |
| somatic (Hetero) | VAF = f / 2 | Somatic heterozygous variant without LOH |

A **+/-10% error margin** is applied for model matching to account for variability in pathological TC estimation.

## Clinical Alert System

The app generates four context-dependent alerts based on TC and VAF. The TC thresholds (<= 20%, >= 60%) follow the description of this software published in *Journal of Human Genetics*. The TC >= 90% alert is an addition not described in the paper.

### Alert 1 — Low TC (TC <= 20%)

At low tumor content, theoretical lines are compressed into a narrow VAF range and model matching is less reliable. Subclonal variants, admixture with normal tissue, or technical noise may dominate. The corresponding region is shaded gray on the graph.

### Alert 2 — High TC (TC >= 60%)

**High VAF does not exclude a somatic origin.** At high tumor content, germline and somatic LOH lines converge, and variants with somatic LOH can reach VAF values typical of germline variants. The corresponding region is shaded yellow on the graph.

### Alert 3 — LOH Convergence (TC >= 60%)

As TC rises, somatic (LOH with Del) climbs past germline (Hetero) at 50% (at TC = 2/3, approximately 66.7%) and approaches the germline LOH lines. This alert fires when:

- **TC >= 60%**, AND
- **VAF >= somatic (LOH with Del) line** at current TC

Both conditions must be met. The alert displays the actual theoretical values for clinical reference.

### Alert 4 — Extreme Tumor Purity (TC >= 90%)

At very high purity, all five theoretical models compress into a narrow VAF range. Variants may still be of somatic origin even at high VAF. This alert fires regardless of VAF, as germline testing becomes essential in all cases.

### Note on low-VAF interpretation

When only somatic models are compatible, the app states that germline origin is *less likely* but **cannot be excluded**: reverse LOH, in which the variant allele is lost within tumor cells, can make a germline variant appear at low VAF.

## Gene Reference System (GPV/PGPV Guidelines 2025 Edition)

The app provides gene-specific contextual messages based on the **Guidelines for GPV/PGPV Handling Procedures in Cancer Gene Panel Testing (2025 Edition)** (MHLW Research Grant), T-only PGPV disclosure recommended gene list (31 genes).

| Category | VAF Threshold | Genes | Notes |
|---|---|---|---|
| 🔴 Low threshold | VAF >= 10% | BRCA1, BRCA2 | Even low-VAF variants may be GPV. Expert panel review recommended. |
| 🟠 Age-conditional | SNV >= 30%, indel >= 20% AND onset < 30 y | APC, CDKN2A, PTEN, RB1, TP53 | Box_E: phenotype evaluation required for APC, PTEN, RB1, TP53 |
| 🟡 Standard | SNV >= 30%, indel >= 20% | ATM, BAP1, BARD1, BRIP1, CHEK2, DICER1, FH, FLCN, MLH1, MSH2, MSH6, MUTYH(bi), NF1, PALB2, PMS2, POLD1, POLE, RAD51C, RAD51D, RET, SDHA, SDHB, TSC2, VHL | MUTYH: bi-allelic only. NF1: Box_E phenotype evaluation. |
| ⬜ Not listed | — | All other genes | Not on 2025 T-only PGPV list. Consult clinical guidelines and family history. |

## Features

- **Interactive graph** with five theoretical VAF-TC curves (Plotly)
- **Model matching** with +/-10% error margin and theoretical VAF display
- **Automated interpretation** based on compatible model combinations
- **Gene-specific messages** for 31 genes per GPV/PGPV Guidelines (2025 Edition)
- **Four clinical alerts** based on TC values (<= 20% / >= 60% / >= 90%)
- **Shaded bands** reproducing Fig. 1: TC <= 20% (low confidence) and TC >= 60% (high VAF does not exclude somatic origin)
- **Important Note** on startup with model assumptions and limitations
- **Multi-variant CSV upload** to plot multiple variants simultaneously on the graph
- **CSV template download** for multi-variant workflows
- **Theoretical model data download** (CSV and Excel) directly from the app

## Multi-variant Upload

Multiple variants from a single patient can be uploaded as a CSV file and plotted simultaneously on the graph. This is particularly useful for cases with high mutational burden (e.g., Lynch syndrome, POLE-mutant tumors).

**CSV format:**

```
Gene,TC,VAF
BRCA2,70,57
TP53,70,35
MSH2,70,68
```

Each variant is plotted with a distinct color and gene label. Interpretation and gene-specific messages are shown for each variant. A template CSV can be downloaded from within the app.

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
| app.py | Main Streamlit application (ver 3.6) |
| requirements.txt | Python dependencies |
| VAF-TC theoretical_model.xlsx | Excel file for generating theoretical VAF-TC curves |
| VAF_TC_theoretical_model.csv | CSV version of the theoretical model data |
| data_dictionary.txt | Variable definitions for the theoretical model |

## Changelog (ver 3.6)

- **Fixed** the LOH Convergence alert threshold: **TC >= 70% -> >= 60%**. Ver 3.5 was built against a pre-publication proof that read ">=70%"; the published article reads ">=60%". The app now matches the published text, and the threshold coincides with the TC >= 60% shaded band in Fig. 1.
- **Clarified** that the TC >= 90% alert is an addition not described in the paper.

## Changelog (ver 3.5)

Aligned with the published paper (*J Hum Genet* 2026, doi:10.1038/s10038-026-01494-7) and hardened for long-term public use.

- **Renamed** the application to **VAF–TC Visualizer**, the name used in the paper
- **Changed** alert thresholds to **TC <= 20% / >= 60%**, matching the published description; the former Gray Zone alert (TC 61-66%) was removed as redundant with the TC >= 60% alert
- **Added** the paper's wording "High VAF does not exclude a somatic origin" to the TC >= 60% alert
- **Added** TC >= 60% yellow shading, plus "Germline (LOH with gain)" and "Subclone" area labels, reproducing Fig. 1
- **Changed** low-VAF interpretation to state that germline origin cannot be excluded, citing **reverse LOH**
- **Fixed** crash on CSV rows with non-numeric or out-of-range TC/VAF (division by zero); such rows are now reported and skipped
- **Fixed** TC-band alerts reading the sidebar sliders instead of each uploaded CSV row
- **Added** pandas to requirements.txt (previously an undeclared direct import) and pinned major versions
- **Updated** citation with the full author list and DOI

## Changelog (ver 3.4)

- **Redesigned** sidebar: unified Multi-variant Workflow section (Download template → Upload CSV → warning note) for intuitive user flow
- **Moved** Theoretical Model Data download to sidebar
- **Moved** Gene Reference from sidebar to right column below graph (wider display, no longer collapsible)
- **Moved** Analysis Mode indicator from sidebar to top of left column (prominent banner)
- **Moved** Important Note from page top (collapsible expander) to bottom of left column (always visible, no longer blocks graph)

## Changelog (ver 3.3)

- **Removed** Somatic + cnLOH model; **added** somatic (Hetero) = f/2
- **Renamed** all model labels to lowercase format: germline (cnLOH), germline (LOH with Del), germline (Hetero), somatic (LOH with Del), somatic (Hetero)
- **Deleted** Alert 1 (Somatic cnLOH Trap); alerts renumbered (5 total)
- **Changed** Low VAF / High VAF alerts to **Low TC / High TC** alerts
- **Changed** Low Confidence Zone from TC < 30% to **TC < 20%**
- **Added** Important Note on startup (Knudson assumptions, aneuploidy, TC estimation error)
- **Rebuilt** Gene Reference System per **MHLW GPV/PGPV Guidelines (2025 Edition)** (31 genes, 3 tiers)

## Citation

If you use this tool in your research, please cite:

> Kashima M, Tsubamoto H, Ueda T, Kinjo C, Okada C, Muroi Y, Ueda M, Otsuki T, Kataoka K, Nagahashi M, Matsuda I, Sawai H, Kijima T, Miyazaki A. VAF–tumor content graph: a simple visual framework for interpreting hereditary cancer variants and supporting genetic counseling in tumor-only sequencing. *Journal of Human Genetics*. 2026. https://doi.org/10.1038/s10038-026-01494-7

The article is Open Access under [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/). This application is referred to as the **VAF–TC Visualizer** in the paper.

## Authors

**Clinical Genetics Suite** - Hyogo Medical University

## License

MIT License
