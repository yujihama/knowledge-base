---
title: "FedProxy: プロキシSLMと異質性対応融合によるLLMの連合ファインチューニング"
url: "https://tldr.takara.ai/p/2604.19015"
date: 2026-04-29
tags: [Federated Learning, LLM Fine-Tuning, Knowledge Distillation, Privacy-Preserving ML, SLM, Heterogeneous Data, Model Compression, Offsite-Tuning]
category: "ai-ml"
related: [738, 495, 2178, 2209, 2632]
memo: "[HF Daily Papers] FedProxy: Federated Fine-Tuning of LLMs via Proxy SLMs and Heterogeneity-Aware Fusion"
processed_at: "2026-04-29T12:08:25.798658"
---

## 要約

FedProxyは、大規模言語モデル（LLM）の連合ファインチューニングにおける三つの課題（LLMの知的財産保護・クライアントのプライバシー保護・異質データによる性能低下）を同時解決する新フレームワークである。

従来のOffsite-Tuning（OT）は、クライアント側に軽量アダプター（例: 上位・下位レイヤーのみ）だけを送り、中間層を非公開にすることでLLMのIPを守る手法だが、アダプターの表現力が弱いため中央集権型学習に対して大きな性能差が生じるという根本的ボトルネックがあった。

FedProxyはこの問題を「弱いアダプターをProxyとなる小型言語モデル（Proxy SLM）で置き換える」というアイデアで解決する。Proxy SLMはサーバー保有のプロプライエタリLLMから蒸留・圧縮されたもので、LLMの本体を公開せずに高い表現力を持つ代理モデルとしてクライアントに配布される。

フレームワークは三段階のアーキテクチャで構成される。①**効率的表現（Efficient Representation）**: サーバーが構造的圧縮技術でLLMからProxy SLMを生成し、クライアントのリソース制約に対応する。②**堅牢な最適化（Robust Optimization）**: クライアントはProxy SLMをローカルデータでファインチューニングし、集約時は干渉を抑制するHeterogeneity-Aware Fusionによりデータ分布の偏りによる性能劣化を緩和する。③**省力的融合（Effortless Fusion）**: 学習済みProxy SLMの知識を元のLLMに「プラグイン」として訓練不要で統合する。

実験ではFedProxyがOT手法を大幅に上回り、中央集権型学習の性能に近い精度を達成。LLMのIPとクライアントプライバシーを守りながら実用的な精度を実現する新たなベンチマークを確立した。

監査エージェント開発への示唆として、機密データを外部LLMに送れない金融・監査分野での活用可能性が高い。各監査法人や企業が自社データでLLMをファインチューニングしたい場合、FedProxyのようなフレームワークは知財・プライバシー双方の制約を満たしながら高精度なドメイン適応を可能にする技術的基盤となりうる。

## アイデア

- LLMを公開せずに圧縮した代理SLMをクライアントに配布するという発想は、モデルIPとプライバシーのトレードオフを新軸（モデル品質の代理化）で解決しており、従来のアダプター手法と本質的に異なるアプローチ
- 訓練不要の「プラグイン」融合機構により、Proxy SLMで学んだ知識を元のLLMに後付けで統合できる点は、推論コストを抑えながら連合学習の成果を本番LLMに反映できるという実用性が高い
- Heterogeneity-Aware Fusionによる集約時の干渉抑制は、Non-IIDデータを持つ複数クライアント（例: 異なる業種の監査データ）が協調学習する際の標準的な問題を直接ターゲットしており、実環境での適用可能性が高い

## 前提知識

- **Federated Learning** → /deep_360 マルチモーダル大規模言語モデルの連合事前学習に向けた一歩
- **LoRA / PEFT** (TODO: 読むべき)
- **Knowledge Distillation** → /deep_144 LLMにベイズ推論を学習させる：確率的推論の教示フレームワーク
- **Offsite-Tuning** (TODO: 読むべき)
- **Non-IID データ** (TODO: 読むべき)

## 関連記事

- /deep_738 言語モデルのタスク中心型パーソナライズ連合ファインチューニング
- /deep_495 マルチモーダル大規模言語モデルの連合事前学習に向けた一歩
- /deep_2178 連合学習のための表現整合型マルチスケール個別化（FRAMP）
- /deep_2209 書類からのテキスト抽出精度をオープンソースのAIモデルで比較してみた
- /deep_2632 推測不要：連合学習における検証可能な勾配反転攻撃（VGIA）

## 原文リンク

[FedProxy: プロキシSLMと異質性対応融合によるLLMの連合ファインチューニング](https://tldr.takara.ai/p/2604.19015)
