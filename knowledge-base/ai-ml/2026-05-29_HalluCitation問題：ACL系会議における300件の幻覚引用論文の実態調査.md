---
title: "HalluCitation問題：ACL系会議における300件の幻覚引用論文の実態調査"
url: "https://arxiv.org/abs/2601.18724"
date: 2026-05-29
tags: [HalluCitation, citation-hallucination, LLM, 科学的信頼性, ACL, EMNLP, ファジーマッチング, Levenshtein距離, MinerU, GROBID, 査読プロセス]
category: "ai-ml"
related: [1266, 1449, 2449, 1969, 564]
memo: "[2601.18724] HalluCitation Matters: Revealing the Impact of Hallucinated References with 300 Hallucinated Papers in ACL Conferences"
processed_at: "2026-05-29T09:01:23.015998"
---

## 要約

NAISTの研究チームが、ACL・NAACL・EMNLP 2024〜2025に掲載された17,842件の論文を対象に、実在しない文献を引用する「HalluCitation」の蔓延状況を体系的に調査した研究。分析パイプラインは、MinerUによるPDF参照リストのOCR抽出→GROBIDによる構造化→ACL Anthology・arXiv・DBLP・OpenAlexのメタデータとのファジーマッチング（正規化Levenshtein距離0.9閾値）→手動確認という4段階で構成される。74万1656件の引用から候補を絞り込み、最終的に295件の論文にHalluCitationが確認された。年次推移では2024年の20件から2025年の275件へと約14倍に急増。EMNLP 2025単独で154件（全体の52%）を占め、そのうち100件以上がMain・Findingsトラックの採択論文であることが判明した。HalluCitated論文の割合も2024年の0.28%から2025年の2.59%（EMNLP 2025単独では3.7%）へと拡大。HalluCitation候補が4件以上含まれる論文のヒット率は60.7%を超えており、単純なタイトルマッチングでも有効な検出が可能であることを示す。研究分野別では、Low-Resource NLP・LLM Efficiency・AI/LLM Agentsで発生率が高く、これらはEMNLP 2025で新設されたトラックであることから、新興分野では適切な査読者の確保が困難なことが一因と推察される。タイトルTF-IDF分析では、HalluCited論文は「Multimodal」「Decoding」「Quantization」などの効率化・略語系キーワードを多用する傾向がある。原因については、LLMによる文献生成だけでなく、Google ScholarやZoteroなどの二次ソースに既存するハルシネーションを著者が無検証で転記するケースも考慮すべきとしており、自動検出ツールを投稿前チェックに組み込む仕組みの整備を推奨している。監査AIの観点では、LLMを活用した文書生成・引用推薦の信頼性検証に同様のファジーマッチング手法が応用可能であり、証跡の実在確認プロセス設計への示唆がある。

## アイデア

- OCR→ファジーマッチング→手動確認の3段階パイプラインで74万件の引用から295件の幻覚引用を検出するスケーラブルな手法設計が実用的
- 候補件数4件以上で命中率60%超という実用的な閾値ガイドラインを提示しており、投稿前自動チェックツールへの組み込みが可能
- 幻覚引用の原因がLLM直接生成だけでなく、学術文献管理ツールや検索エンジンの二次ソース汚染にも起因する可能性を示唆し、サプライチェーン的な信頼性問題として捉える視点が新しい

## 前提知識

- **LLM hallucination** (TODO: 読むべき)
- **Levenshtein距離** (TODO: 読むべき)
- **TF-IDF** → /deep_208 差分プライバシーを用いたAIチャットボット利用状況分析フレームワーク「Urania」
- **ACL Anthology** (TODO: 読むべき)
- **GROBID** (TODO: 読むべき)

## 関連記事

- /deep_1266 🤗 Transformersでネイティブサポートされる量子化スキームの概要
- /deep_1449 🤗 PEFT：低リソースハードウェアで数十億パラメータモデルをパラメータ効率的にファインチューニング
- /deep_2449 静的ペルソナを超えて：LLMのための状況依存パーソナリティ制御
- /deep_1969 階層的SVGトークン化：スケーラブルなベクターグラフィックスモデリングのためのコンパクトな視覚プログラム学習
- /deep_564 階層とロールを捨てよ：自己組織化LLMエージェントが設計された構造を上回る理由

## 原文リンク

[HalluCitation問題：ACL系会議における300件の幻覚引用論文の実態調査](https://arxiv.org/abs/2601.18724)
