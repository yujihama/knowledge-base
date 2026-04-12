---
title: "GCP第5世代XeonにおけるLLMパフォーマンスベンチマーク：C4 vs N2インスタンス比較"
url: "https://huggingface.co/blog/intel-gcp-c4"
date: 2026-04-08
tags: [Intel AMX, Xeon Emerald Rapids, GCP, optimum-intel, IPEX, CPU推論, LLM推論, テキスト埋め込み, Llama-3.2, エージェントAI]
category: "infra"
memo: "[HF Blog] Benchmarking Language Model Performance on 5th Gen Xeon at GCP"
processed_at: "2026-04-08T12:29:48.885338"
---

## 要約

本記事は、Google Cloud Compute Engine上のXeonベースCPUインスタンス（C4およびN2）において、エージェントAIワークロードの2つの代表的コンポーネント（テキスト埋め込みとテキスト生成）のパフォーマンスをベンチマーク比較した内容である。

C4インスタンスは第5世代Intel Xeon（Emerald Rapids）を搭載し、Intel AMX（Advanced Matrix Extensions）という新しいAIテンソルアクセラレータを内蔵する。一方N2は第3世代Intel Xeon（Ice Lake）でAVX-512のみを持ち、AMXは非搭載。比較はどちらも96 vCPUのiso-core-count条件で実施。

ベンチマークにはHugging Faceの統合ベンチマークライブラリ「optimum-benchmark」とIntelアーキテクチャ向け高速化ライブラリ「optimum-intel（IPEXバックエンド）」を使用。

【テキスト埋め込み】
モデル：WhereIsAI/UAE-Large-V1、入力シーケンス長128、バッチサイズ1〜128でスイープ。
結果：C4はN2比で10倍〜24倍のスループット向上。

【テキスト生成】
モデル：meta-llama/Llama-3.2-3B、入力256トークン・出力32トークン、バッチサイズ1〜64でスイープ。
結果：C4はN2比で2.3倍〜3.6倍のスループット向上。バッチサイズ1〜16では13倍のスループット改善が得られ、レイテンシを大幅に悪化させずに並列クエリ処理が可能。

【コスト効率（TCO）】
C4の時間単価はN2の約1.3倍であるにもかかわらず、テキスト埋め込みでは7倍〜19倍、テキスト生成では1.7倍〜2.9倍のTCO優位性を持つ。

結論として、軽量エージェントAIソリューション（SLM＋RAG構成）をGPUなしでCPUのみに展開することが現実的な選択肢となりうることを実証している。AMX世代のCPU進化と、Meta Llama 3.2（1B/3B）などの小型高性能モデルの登場が、このCPU完結型アーキテクチャを支えている。

## アイデア

- Intel AMX（Advanced Matrix Extensions）により、GPUなしでCPUのみでエージェントAIシステム全体（埋め込み＋テキスト生成）を完結させる構成が現実的なコスト効率で実現できる
- テキスト埋め込みの世代間スループット向上（最大24倍）はテキスト生成（最大3.6倍）より圧倒的に大きく、RAGのretrieval層がCPUボトルネックになりにくくなることを示唆している
- optimum-benchmarkとoptimum-intelの組み合わせにより、再現性の高いマルチバックエンド・マルチデバイスベンチマーク環境を簡易に構築でき、インフラ選定の定量的根拠として活用可能

## Yujiの取り組みへの示唆

監査エージェントシステムの本番展開において、GPUリソースが確保できない環境（クラウド予算制約、セキュリティ要件でGPUインスタンス不可など）でも、第5世代Xeon搭載インスタンス（GCP C4相当）を使えばLlama-3.2-3B程度のSLMとRAG埋め込みを合理的なコストで動かせることが定量的に示されている。LangGraphベースの監査エージェントのPoC環境や社内デプロイ先としてCPUのみ構成を検討する際の技術的裏付けとして参照価値がある。

## 原文リンク

[GCP第5世代XeonにおけるLLMパフォーマンスベンチマーク：C4 vs N2インスタンス比較](https://huggingface.co/blog/intel-gcp-c4)
