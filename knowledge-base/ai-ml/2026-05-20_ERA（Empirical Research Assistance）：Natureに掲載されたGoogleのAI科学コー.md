---
title: "ERA（Empirical Research Assistance）：Natureに掲載されたGoogleのAI科学コーディング支援ツールとComputational Discoveryの公開"
url: "https://research.google/blog/empirical-research-assistance-era-from-nature-publication-to-catalyzing-computational-discovery/"
date: 2026-05-20
tags: [ERA, Gemini, 科学コーディング, ツリーサーチ, AlphaEvolve, Computational Discovery, 疫学予測, CO2モニタリング, Google Research]
category: "ai-ml"
related: [4244, 3898, 1965, 5034, 248]
memo: "[Google AI Blog] Empirical Research Assistance (ERA): From Nature publication to catalyzing Computational Discovery"
processed_at: "2026-05-20T09:18:09.617306"
---

## 要約

GoogleはGeminiを活用した科学コーディング支援AIツール「Empirical Research Assistance（ERA）」をNature誌に発表し、同日「Computational Discovery」としてGemini for Science経由のトラステッドテスタープログラムを開始した。

ERAの中核的な仕組みは、科学的問題と成功指標を与えると、文献検索・コード生成・解探索・技術統合・評価を反復するツリーサーチ（木探索）アプローチを用いて、数千の候補オプションを探索しながら出力コードを最適化するものである。AlphaEvolveとも統合されており、Computational Discoveryはこの2システムを組み合わせて構築されている。

ベンチマーク評価はゲノミクス・公衆衛生・衛星画像解析・神経科学予測・時系列予測・数学の6分野に及び、すべてにおいてエキスパートレベルの性能を達成した。

実応用として8本の論文が公開されており、主な成果は以下の通り：
（1）疫学的予測：米国のインフルエンザ・COVID-19・RSVによる州別入院患者数を最大4週間先まで予測し、CDCの公開リーダーボードで3ウイルス全てにおいて首位または上位にランクイン。
（2）カリフォルニア州の積雪融水予測：春季流量の早期予測精度において、州公式予測（Bulletin 120）を有意に上回った。
（3）大気CO2濃度マッピング：静止気象衛星GOES-Eastのデータを活用し、10分間隔・高空間分解能でCO2濃度を推定。ロサンゼルス盆地の都市排出パターンも明瞭に捉えた（Orbiting Carbon Observatory-2は16日に1回しか同一地点を観測できないのに対し）。
（4）3D太陽光パネル最適化：Google Antigravityと組み合わせ、500三角形の体積ファン形状が後方遮蔽ゼロで散乱放射を最大捕捉できることを発見。
（5）小売販売予測：米国経済指標・Google Trendsデータ・消費者センチメントを入力とし、商用コンセンサス予測およびシカゴ連銀のCART月次予測を上回る精度を達成。

監査エージェント開発への示唆として、ERAのツリーサーチによる反復的コード最適化は、監査手続きの自動生成・改善ループに直接応用可能なアーキテクチャパターンである。また、疫学・経済・環境など複数ドメインにわたる定量予測タスクでの実績は、内部統制リスクの定量評価モデル構築においても同様のアプローチが有効であることを示唆する。

## アイデア

- ツリーサーチで数千の候補コードを探索し自動最適化する手法は、監査手続き生成エージェントにおいて複数の分析アプローチを並列探索するアーキテクチャとして転用可能
- 静止衛星データ（16日に1回→10分間隔）という時間解像度の大幅向上は、スパースな監査証拠から高頻度の内部統制モニタリングシグナルを補完するアプローチに対応する概念
- 単一AIシステム（ERA）を疫学・流体力学・CO2化学・小売経済など全く異なるドメインに適用できた汎用性は、ドメイン特化ファインチューニングなしに専門性を発揮できる科学的根拠として重要

## 前提知識

- **ツリーサーチ（MCTS）** (TODO: 読むべき)
- **Gemini** → /deep_2 AIエージェント自作のための基礎知識 - Google ADK (Go) を使ったエージェント構築
- **AlphaEvolve** → /deep_1965 自己進化するAIが「正しいものを書き換える」理由 ── AlphaEvolveとLLM wikiの分岐点
- **時系列予測** → /deep_113 金融時系列予測でLightGBM / LSTM / Transformerを比較してみた
- **科学的コード生成** (TODO: 読むべき)

## 関連記事

- /deep_4244 Google研究者がEmpirical Research Assistance（ERA）を活用した4つの事例：疫学・宇宙論・気候・神経科学
- /deep_3898 階層型記憶3層設計 — LLMの「忘れる」問題を設計で解く
- /deep_1965 自己進化するAIが「正しいものを書き換える」理由 ── AlphaEvolveとLLM wikiの分岐点
- /deep_5034 自己同一性を前提としない体系「顕現論（Aletheics）」をLLMに与えて哲学談義すると面白い
- /deep_248 研究ブレークスルーと実世界応用の「マジックサイクル」加速：Google Research最新成果

## 原文リンク

[ERA（Empirical Research Assistance）：Natureに掲載されたGoogleのAI科学コーディング支援ツールとComputational Discoveryの公開](https://research.google/blog/empirical-research-assistance-era-from-nature-publication-to-catalyzing-computational-discovery/)
