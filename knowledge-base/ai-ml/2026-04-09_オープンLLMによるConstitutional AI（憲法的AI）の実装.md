---
title: "オープンLLMによるConstitutional AI（憲法的AI）の実装"
url: "https://huggingface.co/blog/constitutional_ai"
date: 2026-04-09
tags: [Constitutional AI, CAI, DPO, RLAIF, Mistral-7B, 合成データ生成, アライメント, llm-swarm, SFT, Slurm]
category: "ai-ml"
memo: "[HF Blog] Constitutional AI with Open LLMs"
processed_at: "2026-04-09T21:04:11.147504"
---

## 要約

AnthropicのConstitutional AI（CAI）手法をオープンモデルで再現するエンドツーエンドのレシピをHugging Faceチームが公開した。CAIの基本的な仕組みは、まずモデルに有害な質問への回答を生成させ、次に「憲法（constitution）」と呼ばれる原則集に基づいて自己批判させ、最後に修正した回答を出力させるという3ステップのプロセスである。この自己改善ループによって生成されたデータを用いてSFT（Supervised Fine-Tuning）および選好データセットを構築し、DPOやPPOによるアライメントを実施する。

使用ベースモデルはmistralai/Mistral-7B-Instruct-v0.1。このモデルはLlama-70Bを上回るベンチマーク性能を持つが、ガードレールが少ないため詐欺メール生成などに悪用される可能性があり、アライメント追加の動機となっている。プロンプト収集にはAnthropic HH preference dataset（Anthropic/hh-rlhf）を使用し、レッドチーミング用プロンプトを抽出した。

大規模合成データ生成のためにllm-swarmというツールを新規開発・公開。SlurmクラスタのGPU群をTGIまたはvLLMで駆動し、非同期APIにより大量テキストを並列生成できる。同ツールは複数インスタンスをnginxロードバランサで束ね、AsyncInferenceClientで呼び出す構成をとる。

成果物として2種類のデータセット・モデルを公開：(1) Anthropicの憲法に基づくDPOモデル（HuggingFaceH4/mistral-7b-anthropic）と対応データセット、(2) xAI Grokを模した憲法に基づくSFTモデル（HuggingFaceH4/mistral-7b-grok）と対応データセット。憲法の内容を変えるだけで異なる価値観を持つモデルを生成できる点がCAIの最大の利点であり、高コストな人手フィードバック収集が不要となる。

一方、自己批判ステップは完全ではなく、特に小規模モデルでは憲法違反を見逃すケースがある。実用には適切なシステムプロンプト設計、後処理、few-shotプロンプティングの組み合わせが必要とされる。ソースコードはalignment-handbookリポジトリのconstitutional-aiレシピとして公開されている。

## アイデア

- 「憲法（原則集）」をドメイン固有にカスタマイズするだけで、特定用途向けのアライメントが人手フィードバックなしに実現できる点。監査・コンプライアンス領域専用の原則集を定義すれば、専門特化モデルを低コストで作れる。
- 自己批判→修正のループで生成した（プロンプト、拒否回答、修正回答）のトリプレットが選好データセットになる構造。DPOの学習データを人手ではなくモデル自身に生成させるRLAIFの代表的実装例として参照価値が高い。
- llm-swarmによるSlurm + TGI/vLLM構成の非同期大量生成アーキテクチャ。ローカルGPU環境でも同様のパイプラインを構築でき、合成データ生成のインフラパターンとして再利用可能。
## 関連記事

- /deep_520 TRL v1.0: フィールドの変化に追従するポストトレーニングライブラリ
- /deep_265 RapidFire AIによるTRLファインチューニングの最大20倍高速化
- /deep_570 PoseDreamer: 拡散モデルを活用したスケーラブルでフォトリアリスティックな人体データ生成パイプライン
- /deep_222 Falcon-H1-Arabic: ハイブリッドMamba-Transformerアーキテクチャによるアラビア語AI最前線
- /deep_335 DPO学習におけるバッチサイズと勾配累積がlossに与える影響を検証

## 原文リンク

[オープンLLMによるConstitutional AI（憲法的AI）の実装](https://huggingface.co/blog/constitutional_ai)
