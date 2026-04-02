import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import io

# 1. ページ設定
st.set_page_config(page_title="VAF-TC 精密解析ツール", layout="wide")

# 2. タイトル
st.title("🧬 VAF-TC 精密解析ツール")
st.markdown("腫瘍単独シーケンシングにおける生殖細胞系列・体細胞変異の鑑別を支援するインタラクティブ可視化ツール。")
st.caption("⚠️ 本ツールは遺伝カウンセリングの補助ツールです。確認的な生殖細胞系列検査や確立された臨床ガイドラインの代替とはなりません。")
st.caption("⚠️ 本ツールは遺伝子ごとの事前確率を考慮していません。TP53・APC・PTENなどは体細胞変異の頻度が高く、臨床的文脈と家族歴による総合的判断が不可欠です。")

# 3. 遺伝子リファレンスデータ
GENE_INFO = {
    # 生殖細胞系列優位グループ
    "BRCA1":  ("germline", "🟡 BRCA1：生殖細胞系列変異は臨床的に重要です（HBOC）。VAFパターンが生殖細胞系列と一致する場合、確認的な生殖細胞系列検査を推奨します。"),
    "BRCA2":  ("germline", "🟡 BRCA2：生殖細胞系列変異は臨床的に重要です（HBOC）。VAFパターンが生殖細胞系列と一致する場合、確認的な生殖細胞系列検査を推奨します。"),
    "PALB2":  ("germline", "🟡 PALB2：生殖細胞系列変異は遺伝性乳がんと関連します。確認的検査を推奨します。"),
    "ATM":    ("germline", "🟡 ATM：生殖細胞系列変異は遺伝性乳がん・毛細血管拡張性運動失調症と関連します。確認的検査を推奨します。"),
    "CHEK2":  ("germline", "🟡 CHEK2：生殖細胞系列変異は遺伝性乳がん・大腸がんと関連します。確認的検査を推奨します。"),
    "MLH1":   ("germline", "🟡 MLH1：生殖細胞系列変異はLynch症候群と関連します。確認的な生殖細胞系列検査を強く推奨します。"),
    "MSH2":   ("germline", "🟡 MSH2：生殖細胞系列変異はLynch症候群と関連します。確認的な生殖細胞系列検査を強く推奨します。"),
    "MSH6":   ("germline", "🟡 MSH6：生殖細胞系列変異はLynch症候群と関連します。確認的な生殖細胞系列検査を強く推奨します。"),
    "PMS2":   ("germline", "🟡 PMS2：生殖細胞系列変異はLynch症候群と関連します。確認的な生殖細胞系列検査を強く推奨します。"),
    "RAD51C": ("germline", "🟡 RAD51C：生殖細胞系列変異は遺伝性卵巣がんと関連します。確認的検査を推奨します。"),
    "RAD51D": ("germline", "🟡 RAD51D：生殖細胞系列変異は遺伝性卵巣がんと関連します。確認的検査を推奨します。"),
    "CDH1":   ("germline", "🟡 CDH1：生殖細胞系列変異は遺伝性びまん性胃がんと関連します。確認的検査を推奨します。"),
    "VHL":    ("germline", "🟡 VHL：生殖細胞系列変異はフォン・ヒッペル・リンダウ病と関連します。確認的検査を推奨します。"),
    "RB1":    ("germline", "🟡 RB1：生殖細胞系列変異は遺伝性網膜芽細胞腫と関連します。確認的検査を推奨します。"),
    "NF1":    ("germline", "🟡 NF1：生殖細胞系列変異は神経線維腫症1型と関連します。確認的検査を推奨します。"),
    "STK11":  ("germline", "🟡 STK11：生殖細胞系列変異はPeutz-Jeghers症候群と関連します。確認的検査を推奨します。"),
    # 両方重要グループ
    "TP53":   ("dual", "🟠 TP53：**生殖細胞系列・体細胞変異の両方が臨床的に重要です。** 体細胞TP53変異はがんで最も頻度が高いですが、若年発症・多発がん・強い家族歴がある場合はLi-Fraumeni症候群（生殖細胞系列）を考慮してください。"),
    "APC":    ("dual", "🟠 APC：**生殖細胞系列・体細胞変異の両方が臨床的に重要です。** 体細胞APC変異は大腸がんに頻出しますが、大腸ポリポーシスや家族歴がある場合は家族性大腸腺腫症（FAP）の生殖細胞系列変異を考慮してください。"),
    "PTEN":   ("dual", "🟠 PTEN：**生殖細胞系列・体細胞変異の両方が臨床的に重要です。** 多発性過誤腫や関連する家族歴がある場合はCowden症候群（生殖細胞系列）を考慮してください。"),
    "CDKN2A": ("dual", "🟠 CDKN2A：**生殖細胞系列・体細胞変異の両方が臨床的に重要です。** 生殖細胞系列変異は遺伝性黒色腫・膵がんと関連します。"),
    # 体細胞優位グループ
    "KRAS":   ("somatic", "🔵 KRAS：がんにおける生殖細胞系列変異は極めてまれです。この変異はほぼ確実に体細胞変異です。"),
    "PIK3CA": ("somatic", "🔵 PIK3CA：生殖細胞系列変異はがんでは極めてまれです。この変異はほぼ確実に体細胞変異です。"),
    "BRAF":   ("somatic", "🔵 BRAF：生殖細胞系列変異はがんでは極めてまれです。この変異はほぼ確実に体細胞変異です。"),
    "EGFR":   ("somatic", "🔵 EGFR：生殖細胞系列変異はがんでは極めてまれです。この変異はほぼ確実に体細胞変異です。"),
    "NRAS":   ("somatic", "🔵 NRAS：生殖細胞系列変異はがんでは極めてまれです。この変異はほぼ確実に体細胞変異です。"),
    "IDH1":   ("somatic", "🔵 IDH1：生殖細胞系列変異は極めてまれです。この変異はほぼ確実に体細胞変異です。"),
    "IDH2":   ("somatic", "🔵 IDH2：生殖細胞系列変異は極めてまれです。この変異はほぼ確実に体細胞変異です。"),
    "MET":    ("somatic", "🔵 MET：体細胞変異が一般的です。生殖細胞系列METは遺伝性乳頭状腎細胞がんとまれに関連します。"),
    "CDK4":   ("somatic", "🔵 CDK4：生殖細胞系列変異はがんでは極めてまれです。この変異はほぼ確実に体細胞変異です。"),
}

def get_gene_message(gene):
    key = gene.upper().strip()
    if key in GENE_INFO:
        return GENE_INFO[key]
    return ("unknown", f"⬜ {gene}：リファレンスリストにない遺伝子です。臨床ガイドラインと家族歴を参考に総合的に判断してください。")

# 4. サイドバー入力
st.sidebar.header("📋 患者データ入力")
st.sidebar.markdown("👉 **遺伝子名・TC・VAFを入力してください。**")

gene_name = st.sidebar.text_input("遺伝子名", value="BRCA2")
tc_input = st.sidebar.slider("病理学的腫瘍含有率（TC %）", 0, 100, 50)
vaf_input = st.sidebar.slider("変異アレル頻度（VAF %）", 0, 100, 50)

st.sidebar.markdown("---")
st.sidebar.caption("⚠️ 下記でCSVをアップロードすると、上記の入力（遺伝子名・TC・VAF）は無効になります。")

# 複数変異CSVアップロード
st.sidebar.subheader("📂 複数変異アップロード")
st.sidebar.caption("CSV形式：Gene, TC, VAF")
uploaded_file = st.sidebar.file_uploader("CSVをアップロード", type=["csv"])

multi_df = None
if uploaded_file is not None:
    try:
        multi_df = pd.read_csv(uploaded_file)
        required_cols = {"Gene", "TC", "VAF"}
        if not required_cols.issubset(multi_df.columns):
            st.sidebar.error("CSVにはGene・TC・VAF列が必要です。")
            multi_df = None
        else:
            st.sidebar.success(f"{len(multi_df)} 件の変異を読み込みました。")
    except Exception as e:
        st.sidebar.error(f"CSV読み込みエラー：{e}")
        multi_df = None

st.sidebar.markdown("---")
st.sidebar.info(f"💡 **解析モード：** {gene_name}")

# 遺伝子リファレンス表（折りたたみ）
with st.sidebar.expander("📖 遺伝子リファレンス"):
    st.markdown("**🟡 生殖細胞系列優位：**")
    st.caption("BRCA1, BRCA2, PALB2, ATM, CHEK2, MLH1, MSH2, MSH6, PMS2, RAD51C, RAD51D, CDH1, VHL, RB1, NF1, STK11")
    st.markdown("**🟠 生殖細胞系列・体細胞両方重要：**")
    st.caption("TP53（Li-Fraumeni）, APC（FAP）, PTEN（Cowden）, CDKN2A（遺伝性黒色腫）")
    st.markdown("**🔵 体細胞優位：**")
    st.caption("KRAS, PIK3CA, BRAF, EGFR, NRAS, IDH1, IDH2, MET, CDK4")
    st.caption("⬜ リスト外の遺伝子：臨床ガイドラインと家族歴を参照してください。")

tc = tc_input / 100.0
vaf = vaf_input / 100.0

# 5. 数理モデル（二倍体モデル）
x_range = np.linspace(0.01, 1.0, 100)
y_germ_cnloh = (1 + x_range) / 2
y_germ_del = 1 / (2 - x_range)
y_germ_hetero = np.full_like(x_range, 0.5)
y_som_cnloh = x_range
y_som_del = x_range / (2 - x_range)

# 6. メインレイアウト（左1：右2）
col_alerts, col_graph = st.columns([1, 2])

# --- 左カラム：解釈とアラート ---
with col_alerts:
    st.subheader("📋 解釈とアラート")

    error_margin = 0.10

    def get_compatible_models(tc_val, vaf_val):
        f = tc_val / 100.0
        v = vaf_val / 100.0
        checks = {
            "Germline + cnLOH": (1 + f) / 2,
            "Germline + LOH (Del)": 1 / (2 - f),
            "Germline (Hetero)": 0.5,
            "Somatic + cnLOH": f,
            "Somatic + LOH (Del)": f / (2 - f)
        }
        return [(name, val) for name, val in checks.items() if abs(val - v) <= error_margin]

    def get_interpretation(compatible):
        names = [name for name, _ in compatible]
        if not names:
            return "warning", "VAFはいずれの標準モデルとも一致しません。クローン異質性・異数性・複雑なコピー数変化を考慮してください。"
        germ_hetero = "Germline (Hetero)"    in names
        germ_cnloh  = "Germline + cnLOH"     in names
        germ_del    = "Germline + LOH (Del)"  in names
        som_cnloh   = "Somatic + cnLOH"       in names
        som_del     = "Somatic + LOH (Del)"   in names

        if germ_hetero and som_cnloh and not germ_del and not som_del:
            return "error", "VAFのみでは **Germline (Hetero)** と **Somatic + cnLOH（UPD）** を区別できません。このTCでは両モデルが同一のVAFを示します。**ペア正常検体による生殖細胞系列検査が必須です。**"
        elif germ_del and som_del:
            return "error", "VAFのみでは **Germline LOH (Del)** と **Somatic LOH (Del)** を区別できません。このTCでは両理論線が収束しています。**生殖細胞系列確認検査が必須です。**"
        elif germ_cnloh and not som_cnloh and not som_del:
            return "success", "**コピー数中立LOH（UPD）を伴う生殖細胞系列変異**のパターンと一致します。生殖細胞系列 + cnLOHによるバイアレリック不活化。"
        elif germ_del and not som_del:
            return "success", "**欠失によるLOHを伴う生殖細胞系列変異**のパターンと一致します。生殖細胞系列 + 欠失によるバイアレリック不活化。"
        elif germ_hetero and not som_cnloh:
            return "success", "**LOHを伴わないヘテロ接合性生殖細胞系列変異**のパターンと一致します。1つのアレルのみが影響を受けています。"
        elif som_cnloh and not germ_hetero:
            return "info", "**コピー数中立LOH（UPD）を伴う体細胞変異**のパターンと一致します。生殖細胞系列の可能性は低いですが、ペア正常検査を推奨します。"
        elif som_del and not germ_del:
            return "info", "**欠失によるLOHを伴う体細胞変異**のパターンと一致します。このTCでは生殖細胞系列の可能性は低いです。"
        else:
            return "info", "複数のモデルが該当します。臨床的文脈との照合とペア正常検査を推奨します。"

    def show_variant_interpretation(g, t, v):
        compatible = get_compatible_models(t, v)
        st.markdown(f"**{g}**（TC {t:.0f}%、VAF {v:.0f}%）")
        if compatible:
            for name, val in compatible:
                st.markdown(f"- **{name}** — 理論VAF {val*100:.1f}%")
        level, msg = get_interpretation(compatible)
        if level == "success":
            st.success(f"➡️ {msg}")
        elif level == "error":
            st.error(f"➡️ {msg}")
        elif level == "warning":
            st.warning(f"➡️ {msg}")
        else:
            st.info(f"➡️ {msg}")
        # VAFベースアラート
        if v <= 20:
            st.warning("⚠️ **低VAF（≤ 20%）：** この理論線の信頼性は低下します。低VAFはサブクローン変異・正常組織の混入・技術的ノイズを反映している可能性があります。")
        if v >= 60:
            st.warning("⚠️ **高VAF（≥ 60%）：** 高いVAFは体細胞起源を否定しません。体細胞LOHやコピー数変化によりVAFがこの範囲まで上昇することがあります。")
        # 遺伝子別メッセージ
        _, gene_msg = get_gene_message(g)
        st.info(gene_msg)
        st.caption("💡 注：この解釈はVAF–TCの数理モデルのみに基づいており、遺伝子ごとの生殖細胞系列確率を反映していません。")

    if multi_df is not None:
        for _, row in multi_df.iterrows():
            show_variant_interpretation(str(row["Gene"]), float(row["TC"]), float(row["VAF"]))
            st.divider()
    else:
        show_variant_interpretation(gene_name, tc_input, vaf_input)

    # --- TCベースのアラート ---
    som_cnloh_vaf = tc * 100
    som_del_vaf = tc / (2 - tc) * 100
    germ_del_vaf = 1 / (2 - tc) * 100

    if 40 <= tc_input <= 60:
        st.warning(
            f"⚠️ **Somatic cnLOH トラップ：** TC {tc_input}%では、Somatic cnLOH（UPD）が "
            f"VAF = {som_cnloh_vaf:.0f}%を示し、Germline Heterozygous（50%）の±10%以内に収まります。"
            f"cnLOHを伴う体細胞変異が生殖細胞系列ヘテロ接合変異に偽装する可能性があります。"
            f"ペア正常検査が必須です。"
        )
    elif 61 <= tc_input <= 66:
        st.warning(
            f"⚠️ **グレーゾーン（Somatic LOH Del）：** TC {tc_input}%では、"
            f"Somatic LOH（欠失）のVAF = {som_del_vaf:.1f}%となり、"
            f"Germline Heterozygous（50%）に接近します。確認検査を推奨します。"
        )
    elif tc_input >= 67:
        if vaf_input >= tc / (2 - tc) * 100:
            st.error(
                f"🔴 **LOH 収束アラート：** TC {tc_input}%、VAF {vaf_input}%では、"
                f"変異がSomatic LOH（欠失）ライン（{som_del_vaf:.1f}%）以上に位置します。"
                f"この領域ではGermline LOH (Del) = {germ_del_vaf:.1f}%と"
                f"Somatic LOH (Del) = {som_del_vaf:.1f}%が収束し、"
                f"VAFのみでは起源を判別できません。生殖細胞系列確認検査が必須です。"
            )
        if tc_input >= 90:
            st.warning(
                f"⚠️ **極高腫瘍純度：** TC {tc_input}%では、すべての理論モデルが"
                f"狭いVAF範囲に圧縮されます。高VAFでも体細胞起源の可能性があります。"
                f"家族歴の確認と生殖細胞系列検査が必須です。"
            )

    st.divider()

    # 複数変異一覧表示
    if multi_df is not None:
        st.subheader("📋 アップロードされた変異")
        st.dataframe(multi_df, use_container_width=True)
        st.divider()

    # CSVテンプレートダウンロード
    st.subheader("📊 複数変異ワークフロー")
    st.caption("💡 下記のテンプレートをダウンロードし、サンプル遺伝子を自分のデータに書き換えてから、左サイドバーの「複数変異アップロード」でアップロードしてください。")
    template_df = pd.DataFrame({
        "Gene": [gene_name, "TP53", "MSH2"],
        "TC":   [tc_input,  tc_input, tc_input],
        "VAF":  [vaf_input, 0.0,      0.0]
    })
    csv_string = template_df.to_csv(index=False)
    st.download_button("📥 CSVテンプレートをダウンロード", csv_string.encode("utf-8"), "VAF_TC_Template.csv", "text/csv")

    # 理論モデルデータダウンロード
    st.subheader("📂 理論モデルデータ")
    try:
        with open("VAF_TC_theoretical_model.csv", "rb") as f:
            st.download_button("📥 理論モデルをダウンロード（CSV）", f.read(), "VAF_TC_theoretical_model.csv", "text/csv")
    except FileNotFoundError:
        st.caption("VAF_TC_theoretical_model.csv が見つかりません。")
    try:
        with open("VAF-TC theoretical_model.xlsx", "rb") as f:
            st.download_button("📥 理論モデルをダウンロード（Excel）", f.read(), "VAF-TC_theoretical_model.xlsx", "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
    except FileNotFoundError:
        st.caption("VAF-TC theoretical_model.xlsx が見つかりません。")


# --- 右カラム：グラフ ---
with col_graph:
    st.subheader("📈 VAF-TC 投影グラフ")
    fig = go.Figure()

    fig.add_trace(go.Scatter(x=x_range*100, y=y_germ_cnloh*100, name="Germline + cnLOH", line=dict(color='#d4af37', width=2)))
    fig.add_trace(go.Scatter(x=x_range*100, y=y_germ_del*100, name="Germline + LOH (Del)", line=dict(color='#e41a1c', width=2)))
    fig.add_trace(go.Scatter(x=x_range*100, y=y_germ_hetero*100, name="Germline (Hetero)", line=dict(color='#a65628', width=2)))
    fig.add_trace(go.Scatter(x=x_range*100, y=y_som_cnloh*100, name="Somatic + cnLOH", line=dict(color='#4daf4a', dash='dash')))
    fig.add_trace(go.Scatter(x=x_range*100, y=y_som_del*100, name="Somatic + LOH (Del)", line=dict(color='#377eb8', dash='dot')))

    if multi_df is not None:
        colors = ['#e41a1c','#377eb8','#4daf4a','#984ea3','#ff7f00',
                  '#a65628','#f781bf','#999999','#66c2a5','#fc8d62']
        for i, row in multi_df.iterrows():
            fig.add_trace(go.Scatter(
                x=[row["TC"]], y=[row["VAF"]],
                mode='markers+text',
                name=str(row["Gene"]),
                text=[f"{row['Gene']}<br>TC:{row['TC']}%<br>VAF:{row['VAF']}%"],
                textposition="top right",
                marker=dict(color=colors[i % len(colors)], size=14, symbol='circle'),
                showlegend=True
            ))
    else:
        fig.add_trace(go.Scatter(
            x=[tc_input], y=[vaf_input],
            mode='markers+text',
            name=f"現在：{gene_name}",
            text=[f"{gene_name}<br>TC:{tc_input}%<br>VAF:{vaf_input}%"],
            textposition="top right",
            marker=dict(color='black', size=14, symbol='circle')
        ))

    fig.add_vrect(x0=0, x1=30, fillcolor="gray", opacity=0.1, layer="below", line_width=0,
                  annotation_text="低信頼ゾーン", annotation_position="top left")

    fig.update_layout(
        xaxis_title="病理学的腫瘍含有率（%）", yaxis_title="変異アレル頻度（%）",
        yaxis=dict(range=[0, 105]), xaxis=dict(range=[0, 105]),
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
        template="simple_white", height=600
    )
    st.plotly_chart(fig, use_container_width=True)

# 7. フッター
st.divider()
st.caption("VAF-TC 精密解析ツール | Clinical Genetics Suite | ver 3.2 ✅")
