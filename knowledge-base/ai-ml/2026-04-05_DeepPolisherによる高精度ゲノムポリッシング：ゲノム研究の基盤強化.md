---
title: "DeepPolisherによる高精度ゲノムポリッシング：ゲノム研究の基盤強化"
url: "https://research.google/blog/highly-accurate-genome-polishing-with-deeppolisher-enhancing-the-foundation-of-genomic-research/"
date: 2026-04-05
tags: [Transformer, deep-learning, genome-assembly, DeepPolisher, DeepConsensus, PacBio, bioinformatics, HPRC, sequence-model]
category: "ai-ml"
memo: "[Google AI Blog] Highly accurate genome polishing with DeepPolisher: Enhancing the foundation of genomic research"
processed_at: "2026-04-05T21:01:01.788674"
---

## 要約

DeepPolisherは、GoogleとUC Santa Cruz Genomics Instituteが共同開発したオープンソースのゲノムアセンブリ精度向上ツールで、論文はGenome Researchに掲載された。ゲノムアセンブリにおける塩基レベルの誤りを深層学習で修正し、全体誤りを約50%、挿入・欠失（indel）誤りを70%以上削減する。indelエラーは遺伝子の読み枠をずらし、臨床解析や創薬における遺伝子アノテーションを妨げるため、この削減は特に重要。アーキテクチャはDeepConsensusを改良したTransformer（エンコーダのみ）を採用。入力チャネルは塩基情報・シーケンサー報告クオリティ・マッピングクオリティ・ミスマッチ塩基アノテーションの4種。学習データはPersonal Genomes Projectに提供されたヒト細胞株のゲノム（NISTおよびNHGRIが検証済み、正確度99.99999%、60億塩基中誤りは300〜1000箇所程度）。染色体1〜19で学習し、21・22でモデル選択、20で精度報告というホールドアウト構成。ゲノム品質はQ-scoreで評価され、Q60は99.9999%の正確度に相当。DeepPolisherはQ-scoreを平均で数Q値分（例：Q47→Q50超）改善することを示した。Human Pangenome Reference Consortium（HPRC）の新規ゲノムアセンブリにも採用され、ヒトパンゲノム参照配列の品質向上に貢献。処理フローはPacBioロングリードシーケンシング→アセンブリ→DeepPolisher適用で、シーケンス読み取りは親由来（フェージング）ごとに分類されて入力される。前段のDeepConsensusがPacBioシーケンサー上でエラー率を0.1%未満に下げた後、さらにDeepPolisherがアセンブリ段階での残存誤りを修正するという二段階構成。コードはオープンソースとして公開済み。

## アイデア

- エンコーダのみのTransformerを用いて塩基配列の誤り分類と修正提案を同一モデルで行う設計は、トークン列の分類＋生成を軽量に実現する手法として参考になる
- 学習・検証・テスト用に染色体を分割するホールドアウト戦略は、ゲノムデータの空間的相関を考慮した評価設計であり、ドメイン固有の評価分割の好例
- 99.99999%精度のゴールドスタンダードデータを教師ラベルとして用いることで、極めて低いエラー率の修正モデルを学習できる点は、高品質アノテーションがモデル性能に直結することを示す実証例

## 関連記事

- /deep_195 Mamba解説：TransformerへのState Space Modelによる挑戦
- /deep_1494 🤗 TransformersによるProbabilistic時系列予測
- /deep_113 金融時系列予測でLightGBM / LSTM / Transformerを比較してみた
- /deep_216 金融市場へのLLM応用：価格予測・合成データ・マルチモーダル学習の可能性と限界
- /deep_370 設計段階でのスパース化によるクロスモダリティ予測：信頼性と効率的学習のためのL0ゲート表現

## 原文リンク

[DeepPolisherによる高精度ゲノムポリッシング：ゲノム研究の基盤強化](https://research.google/blog/highly-accurate-genome-polishing-with-deeppolisher-enhancing-the-foundation-of-genomic-research/)
