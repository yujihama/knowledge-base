---
title: "Kaggle自然言語処理コンペ向けローカルLLM活用入門"
url: "https://speakerdeck.com/k951286/kagglezi-ran-yan-yu-chu-li-konpexiang-kerokarullmhuo-yong-ru-men"
date: 2026-04-12
tags: [LoRA, vLLM, 量子化, Qwen2.5, Gemma, Kaggle, 因果言語モデル, AWQ, GPTQ, FineTuning]
category: "ai-ml"
related: [1350, 524, 1049, 125, 1357]
memo: "Kaggle自然言語処理コンペ向けローカルLLM活用入門 - Speaker Deck"
processed_at: "2026-04-12T12:00:52.545437"
---

## 要約

GO株式会社の立松郁也氏が2025年2月に発表した、Kaggle NLPコンペでのローカルLLM活用に関する入門資料。Kaggle Eediコンペ（2024年12月締切）への参加経験をもとに、ゼロから得た知見をまとめたもの。

【背景・動向】近年のKaggle NLPコンペでは上位解法にLLMの採用が増加しており、Eediコンペ（Qwen2.5）、LMSYSコンペ（gemma-2、Llama3）、LLM Prompt Recovery（Mistral、Gemma）などが例として挙げられる。一方、AES 2.0やPII Data DetectionではDeBERTa-v3が依然主流であり、タスク依存の選択が必要。

【学習編】トレーニングタスクとして、因果言語モデル（AutoModelForCausalLM）を第一候補とすることを推奨。シーケンス分類タスクでも「はい/いいえ」形式に変換して因果言語モデルとして扱える。参照コードとしてatmaCup#17 1st place solutionが有用。主要モデルとしてはGemma（2B/7B）とQwen2.5（7B/32B/72B）が挙げられ、後者には数学・コーディング特化weightも存在。

ファインチューニングにはLoRA（Low Rank Adaptation）を活用。元モデルの重みは固定し、低ランク行列Adapterのみを学習することでパラメータ数を大幅削減。HuggingFace PEFTで簡単に実装可能。ハイパーパラメータのTipsとしてChris Deotte氏の知見を紹介：全モジュールにLoRAを適用、学習率2e-4または2e-5、フルバッチサイズ8、r=16固定でalphaを[2,4,8,16,32,64]で探索、その後alphaを固定してrを調整。

【推論編】vLLMを推論ライブラリとして活用することでHuggingFace比14〜24倍の高速化が可能。tensor_parallel_sizeで複数GPU並列、enable_prefix_cachingで共通prefixをキャッシュ、cpu_offload_gbでGPUメモリ超過分をCPU処理（Kaggle T4×2環境でも72Bモデルの推論が可能）。独自LogitsProcessorで出力トークンを「Yes/No」等に制限することで、分類タスク向けの確率値算出も実現。

量子化ではGPTQ（グループ単位の重み量子化）とAWQ（アクティベーション影響によるチャネル単位最適化）が主要手法。Eediコンペ1位・2位チームはタスク固有のキャリブレーションデータを使った自前量子化を採用。手順はLoRA Adapterとベースモデルのマージ→キャリブレーションデータ準備→AutoAWQ/AutoGPTQで量子化実行。

## アイデア

- シーケンス分類タスクを因果言語モデルに変換するアプローチ：「はい/いいえ」等の単一トークン出力に誘導し、LogitsProcessorで出力トークンを固定することで確率値も取得できる設計は、監査エージェントの判定出力（異常/正常）にそのまま応用可能
- 自前量子化によるタスク特化キャリブレーション：汎用量子化モデルではなく、解きたいタスクに近いデータでキャリブレーションすることで量子化による精度劣化を最小化する手法は、ドメイン特化LLM（例：監査文書処理）の本番デプロイ時に有効
- vLLMのcpu_offload_gbオプションにより、Kaggle T4×2（計32GB VRAM）のような制約環境でも72Bモデルの推論が可能という点は、ローカルLLMインフラ構築（RTX 3090 24GB）での大規模モデル活用戦略に直接的な示唆を与える

## 前提知識

- **LoRA / PEFT** (TODO: 読むべき)
- **Transformer** → /deep_99 LLM Architecture Gallery徹底解説：30+モデルの内部構造を4軸で横断比較する
- **HuggingFace Transformers** → /deep_1394 TransformersライブラリによるグラフClassification：Graphormerを用いた実装ガイド
- **量子化 (GPTQ/AWQ)** (TODO: 読むべき)
- **vLLM** → /deep_27 Holotron-12B - 高スループット・コンピュータ使用エージェント向けマルチモーダルモデル

## 関連記事

- /deep_1350 SafetensorsがPyTorch Foundationに参加——Linux Foundation傘下でコミュニティガバナンスへ移行
- /deep_524 NVIDIA NIMでHugging Face上の10万以上のLLMを高速デプロイ
- /deep_1049 Kaggle MedGemma Impact Challenge 全解剖：受賞9件＋落選30件から学ぶ医療AI開発
- /deep_125 SliderQuant: LLM向け高精度ポストトレーニング量子化フレームワーク
- /deep_1357 FalconモデルがHugging Faceエコシステムに登場

## 原文リンク

[Kaggle自然言語処理コンペ向けローカルLLM活用入門](https://speakerdeck.com/k951286/kagglezi-ran-yan-yu-chu-li-konpexiang-kerokarullmhuo-yong-ru-men)
