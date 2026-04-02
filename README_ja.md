# VAF-TC 精密解析ツール

[![Python 3.9+](https://img.shields.io/badge/python-3.9+-blue.svg)](https://www.python.org/downloads/)
[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://vaf-tc-app.streamlit.app/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

腫瘍単独シーケンシングにおける生殖細胞系列・体細胞変異の鑑別を支援するインタラクティブ可視化ツール。病理学的**腫瘍含有率（TC）**と**変異アレル頻度（VAF）**の数学的関係に基づいています。

> **免責事項：** 本ツールは遺伝カウンセリングの補助ツールです。確認的な生殖細胞系列検査や確立された臨床ガイドライン（ACMG、AMEDコスガイグループ）の代替とはなりません。さらなる前向き検証が必要です。
> 本ツールは遺伝子ごとの事前確率を考慮していません。臨床的文脈と家族歴による総合的判断が不可欠です。

## ライブアプリケーション

**https://vaf-tc-app.streamlit.app/**

## 背景

腫瘍単独の包括的ゲノムプロファイリング（CGP）では、生殖細胞系列変異と体細胞変異の鑑別が根本的な課題です。VAF 約50%は生殖細胞系列ヘテロ接合変異を示すと考えられがちですが、**LOHを伴う体細胞変異も腫瘍含有率によっては同じVAFを示す**ことがあります（診断上の落とし穴）。

本ツールは**Knudsonの二段階発癌説**（二倍体モデル）に基づく5つの理論的VAF-TCモデルを可視化し、既知の判別困難ゾーンに対して自動アラートを提供します。

## 数理モデル

腫瘍含有率 *f*（0〜1）に対して：

| モデル | 数式 | 説明 |
|-------|------|------|
| Germline + cnLOH | VAF = (1 + f) / 2 | コピー数中立LOH（UPD）を伴う生殖細胞系列変異 |
| Germline + LOH (Del) | VAF = 1 / (2 - f) | 欠失によるLOHを伴う生殖細胞系列変異 |
| Germline Heterozygous | VAF = 0.5 | LOHを伴わない生殖細胞系列変異 |
| Somatic + cnLOH | VAF = f | コピー数中立LOH（UPD）を伴う体細胞変異 |
| Somatic + LOH (Del) | VAF = f / (2 - f) | 欠失によるLOHを伴う体細胞変異 |

病理学的TC推定の変動性を考慮し、モデルマッチングには **±10%の誤差マージン**を適用しています。

## 臨床アラートシステム

本アプリはTCとVAFに基づいて6つの状況依存アラートを生成します。

### アラート1 - Somatic cnLOH トラップ（TC 40〜60%）

TC 約50%では、Somatic + cnLOHがVAF = TCを示し、Germline Heterozygous（50%）の±10%以内に収まります。UPDを伴う体細胞変異が生殖細胞系列所見に偽装する可能性があります。ペア正常検査が必須です。

### アラート2 - グレーゾーン（TC 61〜66%）

TCが66.7%に近づくにつれ、Somatic + LOH (Del) = f/(2-f)が50%に下から近づきます。この範囲では体細胞LOH欠失ラインがGermline Heterozygous変異との判別困難を生じさせます。

### アラート3 - LOH収束ゾーン（TC ≥ 67%）

TC = 2/3（約66.7%）でSomatic + LOH (Del)がGermline Heterozygousと50%で一致します。このTCを超えると体細胞・生殖細胞系列のLOH線が収束します。以下の条件を両方満たす場合に発動します：

- **TC ≥ 67%**、かつ
- **VAF ≥ 現在のTCにおけるSomatic LOH (Del)ライン**

### アラート4 - 極高腫瘍純度（TC ≥ 90%）

純度が非常に高い場合、5つの理論モデルすべてが狭いVAF範囲に圧縮されます。高VAFでも体細胞起源の可能性があります。すべての症例で生殖細胞系列検査が必須です。

### アラート5 - 低VAF（VAF ≤ 20%）

低VAFでは理論線の信頼性が低下します。サブクローン変異・正常組織の混入・技術的ノイズを反映している可能性があります。

### アラート6 - 高VAF（VAF ≥ 60%）

高いVAFは体細胞起源を否定しません。体細胞LOHやコピー数変化によりVAFがこの範囲まで上昇することがあります。

## 遺伝子リファレンスシステム

本アプリは3カテゴリの遺伝子別メッセージを自動表示します。

| カテゴリ | 遺伝子 | メッセージ |
|---|---|---|
| 🟡 生殖細胞系列優位 | BRCA1, BRCA2, PALB2, ATM, CHEK2, MLH1, MSH2, MSH6, PMS2, RAD51C, RAD51D, CDH1, VHL, RB1, NF1, STK11 | 生殖細胞系列変異は臨床的に重要。確認的検査を推奨。 |
| 🟠 両方重要 | TP53, APC, PTEN, CDKN2A | 生殖細胞系列・体細胞変異の両方が重要。臨床的文脈が必須。 |
| 🔵 体細胞優位 | KRAS, PIK3CA, BRAF, EGFR, NRAS, IDH1, IDH2, MET, CDK4 | 生殖細胞系列変異は極めてまれ。ほぼ体細胞変異。 |
| ⬜ リスト外 | その他の遺伝子 | 臨床ガイドラインと家族歴を参照。 |

## 主な機能

- **インタラクティブグラフ**：5本の理論的VAF-TC曲線（Plotly）
- **モデルマッチング**：±10%誤差マージンによる適合モデルと理論VAFの表示
- **自動解釈**：適合モデルの組み合わせに基づく臨床的解釈文の自動生成
- **遺伝子別メッセージ**：臨床的に重要な25遺伝子への対応
- **6つのアラート**：TCとVAFの値に基づく状況依存アラート
- **低信頼ゾーン**：TC < 30%のグレーゾーン表示
- **複数変異CSVアップロード**：同一グラフへの複数変異の一括プロット
- **CSVテンプレートダウンロード**：複数変異ワークフロー用テンプレート
- **理論モデルデータダウンロード**：CSV・Excel形式での理論モデルデータ取得

## 複数変異アップロード

1患者の複数変異をCSVファイルとしてアップロードし、同一グラフ上に一括プロットできます。Lynch症候群・POLE変異腫瘍など高変異量を示す症例に特に有用です。

**CSV形式：**

```
Gene,TC,VAF
BRCA2,70,57
TP53,70,35
MSH2,70,68
```

各変異は異なる色と遺伝子名ラベルでプロットされます。各変異の解釈文と遺伝子別メッセージも個別に表示されます。テンプレートCSVはアプリ内からダウンロードできます。

## セットアップ

### 必要環境

- Python 3.9以上
- 依存パッケージ：streamlit, plotly, numpy, pandas

### インストール

```bash
pip install -r requirements.txt
streamlit run app.py        # 英語版
streamlit run app_ja.py     # 日本語版
```

## リポジトリ内容

| ファイル | 説明 |
|------|-------------|
| app.py | メインStreamlitアプリ・英語版（ver 3.2） |
| app_ja.py | メインStreamlitアプリ・日本語版（ver 3.2） |
| requirements.txt | Pythonの依存パッケージ |
| VAF-TC theoretical_model.xlsx | VAF-TC理論曲線生成用Excelファイル |
| VAF_TC_theoretical_model.csv | 理論モデルデータのCSV版 |
| data_dictionary.txt | 理論モデルの変数定義 |

## 引用

本ツールを研究に使用される場合は以下を引用してください：

> Kashima M, Tsubamoto H, et al. "VAF-Tumor Content Graph: A Simple Visual Tool for Discriminating Germline and Somatic Variants in Tumor-Only Sequencing." *Journal of Human Genetics*（投稿中）.

## 著者

**Clinical Genetics Suite** - 兵庫医科大学

## ライセンス

MIT License
