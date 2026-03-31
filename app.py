import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go

# --- Page Configuration ---
st.set_page_config(page_title="VAF-TC Precision Analyzer", layout="wide")

st.title("🧬 VAF-TC Clinical Genetics Analyzer")
st.markdown("""
This tool analyzes the relationship between **Pathological Tumor Content (TC)** and **Variant Allele Frequency (VAF)** to differentiate between Somatic and Germline variants, specifically focusing on LOH (Loss of Heterozygosity).
""")

# --- Sidebar Inputs ---
st.sidebar.header("📋 Patient Data Input")
tc_input = st.sidebar.slider("Pathological Tumor Content (%)", 10, 100, 50, help="Assessment by a pathologist is the gold standard for this model.")
vaf_input = st.sidebar.slider("Observed VAF (%)", 1, 100, 25)
st.sidebar.info("Note: 'Pathological TC' is used to ensure independent analysis, avoiding circular reasoning from NGS estimates.")

# --- Mathematical Models (f = Tumor Fraction) ---
f = tc_input / 100

models = {
    "Somatic Heterozygous": (f / 2) * 100,
    "Somatic LOH (with Del)": (f / (2 - f)) * 100,
    "Germline Heterozygous": 50.0,
    "Germline LOH (with Del)": (1 / (2 - f)) * 100
}

# --- 1. Dynamic Alert Logic ---
st.subheader("🚨 Real-time Clinical Alerts")

# Logic for Point 1: The 50% VAF Trap (TC 60-75%)
if 60 <= tc_input <= 75:
    vaf_loh = models["Somatic LOH (with Del)"]
    st.warning(f"""
    **Alert: The 50% VAF Trap (Grey Zone)**
    At your input TC of {tc_input}%, the theoretical VAF for **Somatic LOH (with Del)** is {vaf_loh:.1f}%.
    Crucially, at TC ≈ 66.7%, this somatic model crosses the **50% threshold**.
    In this range, a somatic mutation can perfectly mimic a germline variant. 
    **Recommendation:** Do not assume VAF ≈ 50% is always Germline.
    """)

# Logic for Point 5: High TC Convergence (TC >= 90%)
elif tc_input >= 90:
    st.info(f"""
    **⚠️ High TC Analysis Limit (≥90%):**
    At very high tumor purity, the theoretical VAFs for **Somatic LOH** and **Germline LOH** mathematically converge toward 100% (currently {models['Somatic LOH (with Del)']:.1f}% vs {models['Germline LOH (with Del)']:.1f}%). 
    In this 'Convergence Zone', VAF alone cannot distinguish between a somatic event (e.g., *TP53* Somatic LOH) and a germline event. 
    **Clinical correlation with family history is essential.**
    """)
else:
    st.success("Current TC range: No critical mathematical intersections detected.")

# --- 2. Compatible Models (±10% Range) ---
st.subheader("🔍 Compatible Theoretical Models")
st.write(f"Standard models within a ±10% margin of the observed VAF ({vaf_input}%):")

compatible_data = []
for name, theory_vaf in models.items():
    diff = abs(vaf_input - theory_vaf)
    if diff <= 10.0:
        compatible_data.append({
            "Model Name": name,
            "Theoretical VAF (%)": f"{theory_vaf:.2f}%",
            "Difference (%)": f"{diff:.2f}%"
        })

if compatible_data:
    st.table(pd.DataFrame(compatible_data))
else:
    st.error("No standard models match within ±10%. Consider clonal heterogeneity or aneuploidy.")

# --- 3. Clinical Interpretation & PARPi Guidance ---
with st.expander("📝 Clinical Interpretation & PARP Inhibitor (PARPi) Notes"):
    st.markdown(f"""
    ### Interpretation Factors
    - **NGS Variance:** Sequencing depth and library prep may cause fluctuations (±5-10%).
    - **Aneuploidy / Copy Number Changes:** Significant deviations often suggest large-scale genomic shifts.
    
    ### PARP Inhibitor (PARPi) Indications
    Biallelic inactivation (LOH) is a biological marker for PARPi sensitivity, but clinical indications follow specific regulatory labels:
    
    | Organ | Sensitivity Marker | Regulatory Indication (Typical) |
    | :--- | :--- | :--- |
    | **Ovarian / Prostate** | LOH (Biallelic) | **gBRCA and sBRCA** |
    | **Breast / Pancreatic** | LOH (Biallelic) | **gBRCA Only** (includes Talazoparib for Breast) |

    *Note: Always verify with current NCCN/ESMO guidelines and regional drug labels.*
    """)

# --- 4. Visualization ---
st.subheader("📈 VAF-TC Theoretical Projection")
tc_range = np.linspace(10, 100, 100)
fr = tc_range / 100

fig = go.Figure()
fig.add_trace(go.Scatter(x=tc_range, y=(fr/2)*100, name="Somatic Het", line=dict(color='blue', width=1)))
fig.add_trace(go.Scatter(x=tc_range, y=(fr/(2-fr))*100, name="Somatic LOH (Del)", line=dict(color='blue', dash='dash')))
fig.add_trace(go.Scatter(x=tc_range, y=[50]*100, name="Germline Het", line=dict(color='green', width=1)))
fig.add_trace(go.Scatter(x=tc_range, y=(1/(2-fr))*100, name="Germline LOH (Del)", line=dict(color='red', width=2)))

# Current Case
fig.add_trace(go.Scatter(x=[tc_input], y=[vaf_input], mode='markers+text', 
                         name="User Case", text=["CASE"], textposition="top center",
                         marker=dict(color='black', size=15, symbol='x')))

fig.update_layout(xaxis_title="Pathological Tumor Content (%)", yaxis_title="VAF (%)",
                  legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1))
st.plotly_chart(fig, use_container_width=True)

st.divider()
st.caption("Developed by Clinical Genetics Suite (Maintainer: Sawai1960). Version 2.2 (Final Strategy Update).")
