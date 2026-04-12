---
title: "Intel Gaudi向けAssisted Generation（投機的サンプリング）の高速化サポート"
url: "https://huggingface.co/blog/assisted-generation-support-gaudi"
date: 2026-04-09
tags: [Speculative Sampling, Assisted Generation, Intel Gaudi, Optimum Habana, KV Cache, 推論最適化, 量子化]
category: "infra"
memo: "[HF Blog] Faster assisted generation support for Intel Gaudi"
processed_at: "2026-04-09T09:23:32.135061"
---

## 要約

本記事は、HuggingFaceのOptimum HabanaライブラリにIntel Gaudi向けのAssisted Generation（アシスト生成）サポートが追加されたことを解説するブログ記事である。

Assisted Generation（別名：Speculative Sampling / 投機的サンプリング）は、テキスト生成の推論レイテンシを削減する手法で、大きなターゲットモデルと小さなドラフトモデルの2段階構成で動作する。まずドラフトモデルがKトークンを高速に生成し、ターゲットモデルがそれらを並列評価・検証する。ドラフトモデルのトークンが採択されればそのまま使用し、棄却された場合はターゲットモデルが正しいトークンを生成してリセットするという繰り返しプロセスである。

理論的にはターゲットモデルの出力分布が完全に再現されること（Chen et al., arXiv:2302.01318）が証明されており、サンプリング品質を損なわずに速度向上を実現できる。実測では大型Transformerモデルで約2倍のスループット向上が報告されている。

Intel Gaudi向けの実装では、量子化モデルとKVキャッシュを組み合わせた最適化を適用している。ドラフトモデルとターゲットモデルはそれぞれ異なるサイズのKVキャッシュを持つため、両方の最適化戦略を同時に活用する実装上の課題があったが、それを解決した形となっている。

Intel GaudiはNvidia H100と同等の推論性能を持ちながら、価格帯はNvidia A100 80GBと同程度とされており、コスト効率の観点で注目されるハードウェアである。

Hugging Face TransformersのAPIレベルでは、`.generate()`メソッドに`assistant_model`パラメータを渡すだけで利用できるため、実装コストは低い。Optimum Habanaを通じてGaudiプロセッサ上で既存のTransformersワークフローをそのまま最適化できる点が実用上の強みである。

ドラフトモデルの採択率は入力テキストに依存するため、効果が出るかはユースケースによる。採択率が低い場合やドラフトモデルとターゲットモデルのサイズ差が小さい場合は速度向上が見込めないという制約もある。

## アイデア

- ドラフトモデルの採択率がサンプリング品質に影響を与えないことが数学的に証明されている点は、精度保証が必要な業務用途（監査AI等）での採用を正当化する根拠になりうる
- 小さなドラフトモデルで候補を生成し大きなモデルで検証するというパターンは、LLM-as-judgeアーキテクチャや提案→検証型のマルチエージェント設計と概念的に類似している
- Intel GaudiがH100同等性能・A100同等価格帯という位置付けは、ローカルLLMインフラ構築時のGPU選定において比較対象となりうるハードウェアオプションである

## Yujiの取り組みへの示唆

監査エージェントシステムでLangGraphを用いた推論パイプラインを構築する際、LLMの推論レイテンシはReActループのターンアラウンドに直結するため、Speculative Samplingによる2倍の高速化は実用的な改善手段となる。また、RTX 3090でのローカルLLMインフラ構築を検討中の文脈では、Intel Gaudi（H100同等性能・A100同等価格）のコスト効率比較情報として参照価値がある。ドラフトモデル＋ターゲットモデルの提案・検証構成は、監査エージェントにおける「仮説生成→根拠検証」フローと構造的に対応しており、アーキテクチャ設計の参考になりうる。

## 原文リンク

[Intel Gaudi向けAssisted Generation（投機的サンプリング）の高速化サポート](https://huggingface.co/blog/assisted-generation-support-gaudi)
