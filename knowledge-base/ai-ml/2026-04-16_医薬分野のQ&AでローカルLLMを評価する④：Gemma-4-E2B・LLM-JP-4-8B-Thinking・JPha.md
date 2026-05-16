---
title: "医薬分野のQ&AでローカルLLMを評価する④：Gemma-4-E2B・LLM-JP-4-8B-Thinking・JPharmatron-7Bの比較"
url: "https://zenn.dev/eques/articles/298a45808fa06c"
date: 2026-04-16
tags: [LLM評価, KokushiMD-10, 医療QA, Gemma-4, LLM-JP-4, JPharmatron, ドメイン特化モデル, ベンチマーク, vLLM, 日本語LLM]
category: "ai-ml"
related: [1068, 899, 1251, 1065, 774]
memo: "[Zenn LLM] 医薬分野のQ&AでローカルLLMを評価する④"
processed_at: "2026-04-16T12:45:58.849652"
---

## 要約

本記事は「医薬分野のQ&AでローカルLLMを評価するシリーズ」の第4回。日本語医療国家試験10種を収録したベンチマークデータセット「KokushiMD-10」（2025年6月preprint公開）を用いて、3つのローカルLLMを定量比較した実験報告である。

評価対象モデルは以下の3つ：
1. **Gemma-4-E2B**（google/gemma-4-E2B-it）：Googleが公開した小型マルチモーダルモデル。apply_chat_template未適用では出力が全て空になる不具合があったため、`[{"role": "user", "content": prompt}]`形式でchat templateを適用することで解決した。
2. **LLM-JP-4-8B-Thinking**（llm-jp/llm-jp-4-8b-thinking）：国立情報学研究所が公開した日本語特化8Bモデル。chat templateを付与すると正常動作しないため、templateなしで評価。
3. **EQUES JPharmatron-7B**：薬学・製薬業務特化のドメイン特化モデル。ベースはQwen2.5-7B（一世代前）。再評価として前回スコアとの整合性確認も実施。

推論環境は24GB VRAM×2 GPU構成、推論エンジンはvLLMを使用。各モデルN=5回試行の平均・標準偏差を記録。

主な結果（総スコア比較）：
- 「医師」：JPharmatron-7B（270.40）＞ Gemma-4-E2B（211.80）＞ LLM-JP-4（111.80）
- 「薬剤」：JPharmatron-7B（244.80）＞ LLM-JP-4（211.20）≈ Gemma-4-E2B（209.60）
- 「歯科」：JPharmatron-7B（171.60）＞ Gemma-4-E2B（140.60）＞ LLM-JP-4（79.80）
- 「看護」：LLM-JP-4（175.00）＞ Gemma-4-E2B（149.80）＞ JPharmatron-7B（129.80）
- 「理学」：LLM-JP-4（120.40）＞ Gemma-4-E2B（106.40）＞ JPharmatron-7B（92.00）

総括として、JPharmatron-7Bは学習データに含まれる「医師・歯科・薬剤」の3分野で優位。一方、「助産・診療」ではGemma-4-E2Bが、「作業・保健・理学・看護・視能」ではLLM-JP-4-8B-Thinkingが上回った。汎用モデルとしての日本語能力の差がドメイン外分野の性能に反映された可能性が示唆される。監査AIへの示唆として、専門ドメイン特化ファインチューニングは対象分野には有効だが、周辺分野への汎化性能は汎用モデルに劣ることを定量的に示した事例として参考になる。

## アイデア

- chat templateの適用有無がモデルによって正解率に決定的な影響を与える点（Gemma-4は必須、LLM-JP-4は逆効果）は、ローカルLLM運用時のプロンプトエンジニアリング上の重要な落とし穴
- ドメイン特化ファインチューニング（JPharmatron-7BはQwen2.5-7Bベース）が学習対象分野では汎用モデルを上回る一方、非学習分野では逆転される傾向は、特化モデルの適用範囲設計に直結する知見
- KokushiMD-10のような多職種国家試験横断ベンチマークにより、モデルの「医療知識の広さvs深さ」を分野別に分解評価できる設計は、監査AIにおけるドメイン評価設計の参考になる

## 前提知識

- **ファインチューニング** → /deep_530 AIモデルカスタマイズへの移行はアーキテクチャ上の必須事項
- **chat template** (TODO: 読むべき)
- **vLLM** → /deep_27 Holotron-12B - 高スループット・コンピュータ使用エージェント向けマルチモーダルモデル
- **KokushiMD-10** (TODO: 読むべき)
- **Qwen2.5** → /deep_1060 簡潔な方が良い：関数呼び出しエージェントにおけるChain-of-Thoughtの非単調な予算効果

## 関連記事

- /deep_1068 構造化生成によるプロンプト一貫性の改善
- /deep_899 大規模言語モデルのディベート評価：初の多言語LLMディベートコンペティション（FlagEval Debate）
- /deep_1251 マルチターン医療診断のベンチマーク：保留・誘惑・自己修正（MINT）
- /deep_1065 ヘブライ語LLM評価のためのオープンリーダーボード公開
- /deep_774 オープン・アラビック LLMリーダーボード v2 — アラビア語特化評価基盤の刷新

## 原文リンク

[医薬分野のQ&AでローカルLLMを評価する④：Gemma-4-E2B・LLM-JP-4-8B-Thinking・JPharmatron-7Bの比較](https://zenn.dev/eques/articles/298a45808fa06c)
