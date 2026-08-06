# VAF–TC Visualizer

[![Python 3.9+](https://img.shields.io/badge/python-3.9+-blue.svg)](https://www.python.org/downloads/)
[![Streamlit App (EN)](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://vaf-tc-app.streamlit.app/)
[![Streamlit App (JA)](https://img.shields.io/badge/Streamlit-日本語版-FF4B4B?logo=streamlit&logoColor=white)](https://vaf-tc-app-ja.streamlit.app/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

腫瘍単独シーケンシングにおける生殖細胞系列・体細胞変異の鑑別を支援するインタラクティブ可視化ツール。病理学的**腫瘍含有率(TC)**と**変異アレル頻度(VAF)**の数学的関係に基づいています。

> **免責事項：** 本ツールは遺伝カウンセリングの補助ツールです。確認的な生殖細胞系列検査や確立された臨床ガイドラインの代替とはなりません。さらなる前向き検証が必要です。
> 遺伝子リファレンスシステムは **厚生労働科学研究費補助金 がん遺伝子パネル検査におけるGPV/PGPV対応手順に関する指針(2025版)** のT-only検査PGPV開示推奨遺伝子リストに準拠しています。

## ライブアプリケーション

- **English (英語版):** https://vaf-tc-app.streamlit.app/
- **日本語版:** https://vaf-tc-app-ja.streamlit.app/

## 背景

腫瘍単独の包括的ゲノムプロファイリング(CGP)では、生殖細胞系列変異と体細胞変異の鑑別が根本的な課題です。VAF 約50%は生殖細胞系列ヘテロ接合変異を示すと考えられがちですが、**LOHを伴う体細胞変異も腫瘍含有率によっては同じVAFを示す**ことがあります（診断上の落とし穴）。

本ツールは**Knudsonの二段階発癌説**（二倍体モデル）に基づく5つの理論的VAF-TCモデルを可視化し、既知の判別困難ゾーンに対して自動アラートを提供します。

## 重要な注意事項 ― 数理モデルの前提

1. **二倍体仮定(Knudsonの二段階発癌説)：** 各理論線は二倍体(2コピー)をベースラインとした特定のバイアレリック不活化シナリオを表しています。5つのモデルは理想化された数学的リファレンスであり、すべての可能な機構を網羅するものではありません。
2. **異数性は考慮されない：** 実腫瘍ではしばしば異数性、染色体全体のゲイン/ロス、サブクローン異質性を示します。観測されるVAFは理論線から大きく乖離する可能性があります。
3. **TC推定には ±10〜20% の誤差がある：** 病理学的TC推定は、組織学的異質性・サンプリング部位・観察者間一致度により、通常 ±10〜20% の変動を伴います。本ツールのモデルマッチングには ±10% マージンを適用していますが、臨床解釈では全体の不確実性を考慮する必要があります。
4. **診断ツールではありません：** 本ツールは遺伝カウンセリングの視覚的補助ツールです。臨床判断には確認的な生殖細胞系列検査が標準です。

## 数理モデル

腫瘍含有率 *f*(0〜1)に対して：

| モデル | 数式 | 説明 |
|-------|------|------|
| germline (cnLOH) | VAF = (1 + f) / 2 | コピー数中立LOH(UPD)を伴う生殖細胞系列変異 |
| germline (LOH with Del) | VAF = 1 / (2 - f) | 欠失によるLOHを伴う生殖細胞系列変異 |
| germline (Hetero) | VAF = 0.5 | LOHを伴わないヘテロ接合性生殖細胞系列変異 |
| somatic (LOH with Del) | VAF = f / (2 - f) | 欠失によるLOHを伴う体細胞変異 |
| somatic (Hetero) | VAF = f / 2 | LOHを伴わないヘテロ接合性体細胞変異 |

病理学的TC推定の変動性を考慮し、モデルマッチングには **±10%の誤差マージン**を適用しています。

## 臨床アラートシステム

本アプリはTCに基づいて4つの状況依存アラートを生成します。TCの閾値（≤ 20%・≥ 60%・≥ 70%）は *Journal of Human Genetics* 掲載論文における本ソフトウェアの記述に準拠しています。

### アラート1 ― 低TC(TC ≤ 20%)

低TCでは理論線が狭いVAF範囲に圧縮され、モデルマッチングの信頼性が低下します。サブクローン変異・正常組織の混入・技術的ノイズが支配的になる可能性があります。グラフ上では該当領域をグレーで網掛け表示します。

### アラート2 ― 高TC(TC ≥ 60%)

**高VAFであっても体細胞起源は否定できません。** 高TCでは生殖細胞系列と体細胞のLOH線が収束するため、体細胞変異でもLOHを伴えば生殖細胞系列変異に典型的なVAF値に達しうるためです。グラフ上では該当領域を黄色で網掛け表示します。

### アラート3 ― LOH収束(TC ≥ 70%)

TC = 2/3（約66.7%）を超えると somatic (LOH with Del) が germline (Hetero) の50%を上回り、生殖細胞系列のLOH線に接近します。以下の条件を両方満たす場合に発動します：

- **TC ≥ 70%**、かつ
- **VAF ≥ 現在のTCにおける somatic (LOH with Del) ライン**

### アラート4 ― 極高腫瘍純度(TC ≥ 90%)

純度が非常に高い場合、5つの理論モデルすべてが狭いVAF範囲に圧縮されます。高VAFでも体細胞起源の可能性があります。すべての症例で生殖細胞系列検査が必須です。

### 低VAF解釈に関する注記

体細胞モデルのみが該当する場合、本アプリは生殖細胞系列の可能性が「低い」と表示しますが、**除外はできません**。reverse LOH（腫瘍細胞内で変異アレルが失われる現象）により、生殖細胞系列変異が低VAFとして現れることがあるためです。

## 遺伝子リファレンスシステム(GPV/PGPV対応手順指針 2025版 準拠)

本アプリは **厚生労働科学研究費補助金 がん遺伝子パネル検査におけるGPV/PGPV対応手順に関する指針(2025版)** のT-only検査PGPV開示推奨遺伝子リスト(31遺伝子)に基づく遺伝子別メッセージを自動表示します。

| カテゴリ | VAF閾値 | 遺伝子 | 備考 |
|---|---|---|---|
| 🔴 低閾値 | VAF ≥ 10% | BRCA1, BRCA2 | 低VAFでもGPVの可能性。エキスパートパネル検討推奨。 |
| 🟠 年齢条件付き | SNV ≥ 30%, Indel ≥ 20% かつ発症 < 30歳 | APC, CDKN2A, PTEN, RB1, TP53 | Box_E：APC, PTEN, RB1, TP53は表現型評価が必要 |
| 🟡 標準 | SNV ≥ 30%, Indel ≥ 20% | ATM, BAP1, BARD1, BRIP1, CHEK2, DICER1, FH, FLCN, MLH1, MSH2, MSH6, MUTYH(bi), NF1, PALB2, PMS2, POLD1, POLE, RAD51C, RAD51D, RET, SDHA, SDHB, TSC2, VHL | MUTYH：両アレルのみ。NF1：Box_E表現型評価。 |
| ⬜ リスト外 | ― | その他の遺伝子 | 2025年版T-only PGPVリストに含まれない。臨床ガイドラインと家族歴を参照。 |

## 主な機能

- **インタラクティブグラフ**：5本の理論的VAF-TC曲線(Plotly)
- **モデルマッチング**：±10%誤差マージンによる適合モデルと理論VAFの表示
- **自動解釈**：適合モデルの組み合わせに基づく臨床的解釈文の自動生成
- **遺伝子別メッセージ**：GPV/PGPV対応手順指針(2025版)準拠の31遺伝子対応
- **4つのアラート**：TCの値に基づく状況依存アラート（≤ 20% / ≥ 60% / ≥ 70% / ≥ 90%）
- **網掛け表示**：Fig. 1 を再現し、TC ≤ 20%(低信頼)とTC ≥ 60%(高VAFでも体細胞起源を否定できない)を色分け
- **重要な注意事項**：起動時にモデルの前提と限界を表示
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
| app.py | メインStreamlitアプリ・英語版(ver 3.5) |
| app_ja.py | メインStreamlitアプリ・日本語版(ver 3.5) |
| requirements.txt | Pythonの依存パッケージ |
| VAF-TC theoretical_model.xlsx | VAF-TC理論曲線生成用Excelファイル |
| VAF_TC_theoretical_model.csv | 理論モデルデータのCSV版 |
| data_dictionary.txt | 理論モデルの変数定義 |

## 変更履歴(ver 3.5)

掲載論文（*J Hum Genet* 2026, doi:10.1038/s10038-026-01494-7）との整合と、長期公開に向けた堅牢化。

- **改称** アプリ名を論文で用いられている **VAF–TC Visualizer** に変更
- **変更** アラート閾値を論文の記述に合わせ **TC ≤ 20% / ≥ 60% / ≥ 70%** に統一。従来のグレーゾーン(TC 61〜66%)はTC ≥ 60%アラートと論点が重複するため廃止
- **追加** TC ≥ 60%アラートに論文の文言「高VAFであっても体細胞起源は否定できない」を明示
- **追加** TC ≥ 60%の黄色網掛けと「Germline (LOH with gain)」「Subclone」の領域ラベル（Fig. 1 の再現）
- **変更** 低VAF時の解釈を、**reverse LOH** により生殖細胞系列を除外できない旨を明記する表現に修正
- **修正** CSVに非数値・範囲外のTC/VAFがあるとゼロ除算でアプリが停止する不具合。該当行は報告のうえスキップするように変更
- **修正** TC帯域アラートがCSVの各行ではなくサイドバーのスライダー値を参照していた不具合
- **追加** requirements.txt に pandas を追加（従来は未宣言の直接インポート）し、メジャーバージョンの上限を設定
- **更新** 引用情報を全著者名・DOI付きに更新

## 変更履歴(ver 3.4)

- **再設計** サイドバー：複数変異ワークフローを統合(テンプレートDL → CSVアップロード → 注意書き)し、直感的な操作フローに変更
- **移動** 理論モデルデータのダウンロードをサイドバーに移動
- **移動** 遺伝子リファレンスをサイドバーからグラフ下の右カラムに移動(広い表示・折りたたみなし)
- **移動** 解析モードインジケーターをサイドバーから左カラム最上部に移動(目立つバナー表示)
- **移動** 重要な注意事項をページ最上部(折りたたみ式)から左カラム最下段に移動(常時表示・グラフを圧迫しない)

## 変更履歴(ver 3.3)

- **削除** Somatic + cnLOHモデル → **追加** somatic (Hetero) = f/2
- **変更** 全モデルラベルを小文字形式に統一：germline (cnLOH), germline (LOH with Del), germline (Hetero), somatic (LOH with Del), somatic (Hetero)
- **削除** アラート1(Somatic cnLOH トラップ) → アラート再番号付け(全5個)
- **変更** 低VAF/高VAFアラート → **低TC/高TC** アラートに変更
- **変更** 低信頼ゾーンを TC < 30% → **TC < 20%** に変更
- **追加** 起動時の重要な注意事項(Knudson仮説・異数性・TC推定誤差)
- **再構築** 遺伝子リファレンスシステムを **厚生労働科学研究費補助金 GPV/PGPV対応手順指針(2025版)** 準拠に更新(31遺伝子・3カテゴリ)

## 引用

本ツールを研究に使用される場合は以下を引用してください：

> Kashima M, Tsubamoto H, Ueda T, Kinjo C, Okada C, Muroi Y, Ueda M, Otsuki T, Kataoka K, Nagahashi M, Matsuda I, Sawai H, Kijima T, Miyazaki A. VAF–tumor content graph: a simple visual framework for interpreting hereditary cancer variants and supporting genetic counseling in tumor-only sequencing. *Journal of Human Genetics*. 2026. https://doi.org/10.1038/s10038-026-01494-7

本論文は [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/) のオープンアクセスです。本アプリは論文中で **VAF–TC Visualizer** として参照されています。

## 著者

**Clinical Genetics Suite** - 兵庫医科大学

## ライセンス

MIT License
