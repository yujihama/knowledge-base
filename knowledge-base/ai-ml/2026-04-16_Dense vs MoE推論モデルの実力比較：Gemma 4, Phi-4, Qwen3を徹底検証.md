---
title: "Dense vs MoE推論モデルの実力比較：Gemma 4, Phi-4, Qwen3を徹底検証"
url: "https://zenn.dev/lixian/articles/gemma-phi-qwen3-reasoning-benchmark"
date: 2026-04-16
tags: [LLM, MoE, Dense, Gemma4, Phi-4, Qwen3, ベンチマーク, 推論モデル, VRAM, プロンプト戦略, トレードオフ評価]
category: "ai-ml"
related: [641, 886, 125, 1565, 196]
memo: "[Zenn LLM] Dense vs MoE推論モデルの実力比較"
processed_at: "2026-04-16T12:43:27.920104"
---

## 要約

Rensselaer Polytechnic InstituteのManikらが2026年4月に発表した論文（arXiv:2604.07035）は、オープンソース推論LLM7種を対象に、精度・レイテンシ・VRAM・FLOPsを同時評価した8,400回の統制実験を報告する。対象モデルはGemma-4-E2B/E4B/26B-A4B（MoE）、Qwen3-8B/30B-A3B（MoE）、Phi-4-mini-reasoning/Phi-4-reasoningで、評価ベンチマークはARC-Challenge（重み0.20）・GSM8K（0.40）・Math L1-3（0.30）・TruthfulQA MC1（0.10）の4種。プロンプト戦略はZero-shot・CoT・Few-shot CoTの3種を全組み合わせで実施した。

最大の発見は、DenseモデルのGemma-4-E4Bが加重精度0.675・VRAM 14.9GBで全体最優秀のトレードオフを達成したことだ。MoE構成のGemma-4-26B-A4Bは活性パラメータこそ4BでE4Bと同等だが、VRAMは48.1GBと3.2倍に膨らみ、精度もわずかに低い（0.663）。Qwen3-30B-A3Bは活性パラメータ3Bで最少にもかかわらずVRAM 57.6GBと全モデル中最大で、「活性パラメータ数＝メモリ消費量」という単純な等式が成立しないことを実証した。

タスク依存性も顕著で、ARC-ChallengeはGemma-4-26B-A4Bが0.960でトップ、TruthfulQAはPhi-4-reasoningが完璧な1.000を記録する一方、同モデルはMathで0.000という極端な二極化を示した。Qwen3-30B-A3BはGSM8Kで0.030-0.070と算術推論に根本的弱点がある。

プロンプト戦略の影響では、Phi-4-reasoningがGSM8KでCoT時0.670→Few-shot CoT時0.110と精度が約6分の1に急落する「プロンプト崩壊」が観測された。Few-shot例のフォーマットが事前学習データ分布と不整合を起こし内部推論パターンを乱したと考えられる。Gemmaシリーズはどのプロンプト戦略でも安定した性能を示し、プロンプト堅牢性で優れる。

MoEの優位性は訓練時スケーリングにあり、26Bの知識を4B活性パラメータで習得できる利点があるが、推論時は全エキスパートのパラメータをVRAMに展開する必要があり、デプロイメントコストが高騰する。監査エージェント開発への示唆として、汎用マルチタスク推論エージェントには小〜中規模Denseモデルから検証を始めるDense first戦略が有効で、モデル切り替え時は全プロンプト戦略での再テストが必須。精度単独ではなくVRAM制約も性能指標の一部として評価する設計が実務上不可欠となる。

## アイデア

- 活性パラメータ数が同じ（4B）でもDense vs MoEでVRAMが3.2倍差（14.9GB vs 48.1GB）になる：MoEの「効率神話」が推論デプロイメントでは逆転する
- Phi-4がCoT→Few-shot CoTの切り替えだけでGSM8K精度が0.670→0.110と急落：プロンプト戦略の非線形効果がモデル選定基準を根本的に変える
- Phi-4がMath 0.000／TruthfulQA 1.000という極端な二極化を示す：推論特化ファインチューニングが特定能力へ過集中し汎化を損なうメカニズムの証拠

## 前提知識

- **MoE（Mixture of Experts）** (TODO: 読むべき)
- **Dense LLM** (TODO: 読むべき)
- **Chain-of-Thought prompting** (TODO: 読むべき)
- **Few-shot learning** → /deep_189 EmoTaG: 感情認識型トーキングヘッド合成 — 3D Gaussian Splattingとフューショット個人化の統合
- **推論ベンチマーク（GSM8K, ARC）** (TODO: 読むべき)

## 関連記事

- /deep_641 トレーニング不要なエキスパート言語モデルの動的アップサイクリング
- /deep_886 クラッシュウェーブ vs. ライジングタイド：労働市場タスクに関する数千件の労働者評価から得られたAI自動化の予備的知見
- /deep_125 SliderQuant: LLM向け高精度ポストトレーニング量子化フレームワーク
- /deep_1565 QaRL: 学習・推論ミスマッチ下での高速・安定訓練のためのロールアウト整合量子化対応強化学習
- /deep_196 MoEアーキテクチャ最適化のための包括的スケーリング則

## 原文リンク

[Dense vs MoE推論モデルの実力比較：Gemma 4, Phi-4, Qwen3を徹底検証](https://zenn.dev/lixian/articles/gemma-phi-qwen3-reasoning-benchmark)
