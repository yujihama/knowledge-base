---
title: "LatentAudit: RAGのリアルタイム白箱忠実性モニタリングと検証可能なデプロイメント"
url: "https://tldr.takara.ai/p/2604.05358"
date: 2026-04-10
tags: [RAG, faithfulness, hallucination-detection, residual-stream, Mahalanobis-distance, Groth16, zk-SNARK, white-box, Llama-3, AUROC]
category: "audit-ai"
memo: "[HF Daily Papers] LatentAudit: Real-Time White-Box Faithfulness Monitoring for Retrieval-Augmented Generation with Verifiable Deployment"
processed_at: "2026-04-10T12:07:08.210597"
---

## 要約

RAG（Retrieval-Augmented Generation）システムは幻覚（ハルシネーション）を軽減するが完全には排除できない。推論時に生成された回答が実際に検索証拠に支持されているかを判定する仕組みが必要である。本論文はLatentAuditを提案する。これはオープンウェイト生成モデルの中層〜後層の残差ストリーム（residual-stream）活性化をプールし、証拠表現とのマハラノビス距離（Mahalanobis distance）を計測する白箱監査器である。

技術的仕組みとしては、LLMの内部表現（残差ストリームの幾何学的構造）が忠実性シグナルを保持しているという観察に基づく。このシグナルを二次規則（quadratic rule）として定式化し、補助的な判定モデル（judge model）を一切必要としない。小規模なホールドアウトセットで較正できるため、実運用への導入コストが低い。

性能評価では、PubMedQA（医療QAベンチマーク）にてLlama-3-8Bを使用し、AUROCスコア0.942を達成し、オーバーヘッドはわずか0.77ミリ秒。3つのQAベンチマーク（PubMedQA, HotpotQA等）と5つのモデルファミリー（Llama-2/3, Qwen-2.5/3, Mistral）でモニターの安定性を確認。矛盾する情報・検索ミス・部分的サポートノイズの4方向ストレステストでは、PubMedQAで0.9566〜0.9815 AUROC、HotpotQAで0.9142〜0.9315 AUROCを達成した。

検証可能なデプロイメントの観点では、16ビット固定小数点精度（fixed-point）での監査規則がFP16 AUROCの99.8%を保持し、Groth16ベースのゼロ知識証明（zk-SNARK）による公開検証を可能にする。これによりモデルの重みや活性化を開示することなく、監査規則の正当性を第三者が検証できる。RAGシステムの信頼性を外部から証明可能にするという点で、エンタープライズ・規制対応領域での活用が期待される。

## アイデア

- LLMの内部残差ストリームの幾何学的構造（マハラノビス距離）が、外部判定モデルなしに忠実性を検出できるという発見は、モデルが「何を信じているか」を内部表現から直接読み取る新たなアプローチを示す
- Groth16ベースのゼロ知識証明により、モデルの重みや推論内容を公開せずに監査規則の正当性を第三者検証できる構造は、AIシステムの説明責任と機密保持の両立に向けた実用的な設計パターンである
- 0.77ミリ秒という極低オーバーヘッドで生成時にリアルタイム監査が実行できる点は、プロダクション環境のRAGパイプラインへの統合を現実的にする
## 関連記事

- /deep_49 MARCH: LLMハルシネーション検出のためのマルチエージェント強化自己チェックフレームワーク
- /deep_1116 🤗 Optimum IntelとfastRAGによるCPU最適化エンベディング
- /deep_1334 製造業向けRAGシステムのアクセス制御設計
- /deep_861 蒸留モデルとは何か？ - DeepSeek R1の登場から1年で振り返るLLM知識蒸留の仕組みと実力
- /deep_112 知識ベースを自然淘汰するRAG「Darwin RAG」をつくってみた

## 原文リンク

[LatentAudit: RAGのリアルタイム白箱忠実性モニタリングと検証可能なデプロイメント](https://tldr.takara.ai/p/2604.05358)
