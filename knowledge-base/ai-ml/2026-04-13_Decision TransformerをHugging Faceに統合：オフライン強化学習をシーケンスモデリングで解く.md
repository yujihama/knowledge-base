---
title: "Decision TransformerをHugging Faceに統合：オフライン強化学習をシーケンスモデリングで解く"
url: "https://huggingface.co/blog/decision-transformers"
date: 2026-04-13
tags: [Decision Transformer, オフライン強化学習, GPT-2, シーケンスモデリング, return-to-go, 自己回帰モデル, HuggingFace, Gym環境]
category: "ai-ml"
related: [238, 1572, 1529, 1494, 1449]
memo: "[HF Blog] Introducing Decision Transformers on Hugging Face 🤗"
processed_at: "2026-04-13T12:10:00.292553"
---

## 要約

Hugging Faceは、Chen L. et al.（2021）が提案したDecision Transformer（DT）を🤗 transformersライブラリおよびHugging Face Hubに統合したことを発表した。

DTの核心的なアイデアは、強化学習（RL）を「条件付きシーケンスモデリング問題」として再定式化する点にある。従来のRL手法では価値関数を学習し、累積報酬（リターン）を最大化する方策を導出するが、DTでは「望ましいリターン（return-to-go）・過去の状態・過去の行動」を入力として、GPT-2アーキテクチャが未来の行動を自己回帰的に生成する。つまり、リターンを最大化するのではなく、目標リターンを条件として行動列を生成するという発想の転換が行われている。

モデルへの入力は直近K=20タイムステップ分の3種トークン（return-to-go、state、action）であり、状態がベクトルの場合は線形層、フレームの場合はCNNエンコーダで埋め込まれる。位置エンコーディングにはエピソード内タイムステップ番号が用いられ、causal self-attentionマスクで因果関係を保ちながら行動を予測する。

オフラインRL（Offline Reinforcement Learning）の文脈では、エージェントは環境と直接インタラクションせず、既存のデータセット（他エージェントや人間のデモンストレーション）のみから方策を学習する。これにより、実環境やシミュレータが不要になる一方、エージェントがデータセットに存在しない状態空間に入った場合の「反事実的クエリ問題」が課題となる。

Hugging Face Hub上にはGym環境のHopper、Walker2D、HalfcheetahタスクにおけるExpert・Medium・Medium-Replayの9種類の事前学習済みチェックポイントが公開された。利用方法はDecisionTransformerModel.from_pretrained()で読み込み、get_action()関数内でパディング処理と注意マスクを設定しつつ自己回帰的に行動を生成するという流れになる。

監査エージェント開発への示唆としては、DTのアーキテクチャは「意思決定の軌跡（状態・行動・結果）をシーケンスとして記録し、目標状態を条件としてトレースを生成・再現する」という枠組みを提供する点が注目される。監査プロセスにおいてもオフラインデータ（過去の監査ログ）から望ましい監査手順を条件付き生成するアプローチに応用可能であり、LangGraphベースのエージェント設計においてもリターン条件付きプランニングの参考になる。

## アイデア

- RLを報酬最大化問題としてではなく条件付きシーケンス生成問題として定式化することで、Transformerの汎用シーケンスモデリング能力をそのまま意思決定に転用できる点は、LLMベースのプランニングエージェント設計に直接応用できる発想の転換
- return-to-goという『目標リターンを入力として与える』設計により、同一モデルが異なる性能目標（expert/medium等）に対して推論時に柔軟に対応できる——これはエージェントの品質・コスト制約を動的に切り替えるガバナンス設計に類似する
- オフラインデータのみから方策を学習する枠組みは、実環境インタラクションが困難なリスク評価・監査シナリオ（過去ログからの手順学習）に適しており、LLM-as-judgeによる報酬設計と組み合わせることでRLAIFへの拡張可能性がある

## 前提知識

- **Transformer / GPT-2** (TODO: 読むべき)
- **強化学習（Policy, Return）** (TODO: 読むべき)
- **オフラインRL** → /deep_754 複数の選好オラクルを用いたオフライン制約付きRLHF
- **自己回帰モデル** → /deep_19 LLMのコード生成はなぜ同じミスを繰り返すのか — 失敗を「演算子」にして生成過程を書き換える
- **Gym環境** (TODO: 読むべき)

## 関連記事

- /deep_238 オフライン決定トランスフォーマーによる神経組合せ最適化：巡回セールスマン問題でヒューリスティックを超える
- /deep_1572 🧨 DiffusersによるStable Diffusion：仕組みと実装ガイド
- /deep_1529 🤗 TransformersによるWhisperの多言語ASRファインチューニング
- /deep_1494 🤗 TransformersによるProbabilistic時系列予測
- /deep_1449 🤗 PEFT：低リソースハードウェアで数十億パラメータモデルをパラメータ効率的にファインチューニング

## 原文リンク

[Decision TransformerをHugging Faceに統合：オフライン強化学習をシーケンスモデリングで解く](https://huggingface.co/blog/decision-transformers)
