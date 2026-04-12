---
title: "Google Cloud C4がIntelとHugging Faceの協力でGPT OSSのTCOを70%改善"
url: "https://huggingface.co/blog/gpt-oss-on-intel-xeon"
date: 2026-04-05
tags: [Intel Xeon 6, Google Cloud C4, MoE, CPU推論, GPT OSS, TCO最適化, Hugging Face transformers, bfloat16]
category: "infra"
memo: "[HF Blog] Google Cloud C4 Brings a 70% TCO improvement on GPT OSS with Intel and Hugging Face"
processed_at: "2026-04-05T12:08:19.273840"
---

## 要約

IntelとHugging Faceは、Google Cloud C4 VM（Intel Xeon 6プロセッサ、コードネームGranite Rapids）上でOpenAIのオープンソースMoE（Mixture of Experts）モデル「GPT OSS（120Bパラメータ）」を動作させ、前世代のC3 VM（4th Gen Intel Xeon、Sapphire Rapids）と比較したベンチマーク結果を公開した。

主要な成果として、C4インスタンスはC3と比較してvCPU当たりのスループットで1.4〜1.7倍の改善を達成し、TCO（総所有コスト）で約70%（1.7倍）の改善を実現した。ハードウェア構成はC3が172 vCPU、C4が144 vCPUであり、vCPU数が少ないにもかかわらずC4が上回る点が特筆される。

技術的な最適化として、Intel・Hugging Faceが共同でtransformersライブラリにMoE実行最適化（PR #40304）をマージした。従来の実装ではすべてのエキスパートが全トークンを処理していたが、本最適化によりルーティングされたトークンのみを各エキスパートが処理するよう変更し、不要なFLOPS計算を排除した。これによりCPU推論における計算効率が大幅に向上している。

ベンチマーク条件は、モデル「unsloth/gpt-oss-120b-BF16」をbfloat16精度で使用し、入力・出力ともに1024トークン固定、バッチサイズ1〜64の範囲で評価した。静的KVキャッシュとSDPAアテンションバックエンドを有効化し、再現性を確保している。実行環境はDockerコンテナ上でPyTorch 2.8.0（CPU版）を使用し、numactl経由でNUMAバインディングを活用している。

MoEアーキテクチャはトークンごとに一部のエキスパートのみをアクティブ化するため、総パラメータ数が大きくてもCPU推論が現実的なオプションとなる点が本検証の前提にある。GPUを使用しないCPUオンリー推論でも大規模LLMの実用的なスループットを達成できることを示した事例として意義がある。

## アイデア

- MoEモデルはアクティブパラメータが全体の一部のみであるため、GPUなしのCPU推論でも実用的なスループットを達成できる点は、GPU調達が困難な環境での大規模LLM活用の選択肢を広げる
- 「全エキスパートが全トークンを処理」という実装上の冗長性をOSSへのPRで修正することで1.4〜1.7倍の性能改善を達成した事例は、推論コードの実装品質がTCOに直結することを示す
- vCPU数が少ない（144 vs 172）にもかかわらずC4がC4を上回った結果は、アーキテクチャ世代の改善が単純なコア数比較を超えることを示し、インフラ選定時のベンチマーク重要性を裏付ける

## Yujiの取り組みへの示唆

Yujiが構築中のローカルLLMインフラ（GALLERIA XA7C-R37T、RTX 3090予定）において、GPU環境整備の前段階やコスト制約がある場面でCPU推論の現実的な性能水準の参考になる。また監査エージェントシステムでMoEベースのLLMを推論バックエンドとして採用する際、エキスパートルーティング最適化（PR #40304の手法）がレイテンシ・コスト設計の参考として活用できる。クラウドVM選定においてもTCO視点でのベンチマーク手法（numactl、静的KVキャッシュ、SDPA）は再現性ある評価基盤として応用可能。

## 原文リンク

[Google Cloud C4がIntelとHugging Faceの協力でGPT OSSのTCOを70%改善](https://huggingface.co/blog/gpt-oss-on-intel-xeon)
