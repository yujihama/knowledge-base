---
title: "TGI Multi-LoRA：1回のデプロイで30モデルを同時配信"
url: "https://huggingface.co/blog/multi-lora-serving"
date: 2026-04-09
tags: [LoRA, Multi-LoRA, TGI, fine-tuning, LLM serving, Mistral, HuggingFace, モデルデプロイ, VRAM効率化]
category: "infra"
memo: "[HF Blog] TGI Multi-LoRA: Deploy Once, Serve 30 Models"
processed_at: "2026-04-09T09:08:49.882164"
---

## 要約

HuggingFaceのText Generation Inference（TGI）v2.1.1以降で提供されるMulti-LoRA Servingは、1つのベースモデルを1回デプロイするだけで、複数のLoRAアダプターを動的に切り替えながら複数の特化モデルとして機能させる仕組みである。

LoRA（Low-Rank Adaptation）はベースモデルの重みを固定したまま、行列AとBの2つの小さなパラメータ群を学習する手法で、フルファインチューニングと同等の品質を保ちつつ、ストレージ・メモリのオーバーヘッドをモデルサイズの約1%に抑える。例として、mistralai/Mistral-7B-v0.1（14.48GB）に対しpredibase/magicoder LoRAアダプターはわずか13.6MB（約1/1000）であり、30アダプターを同時ロードしてもVRAM増加は約3%に留まる。

Multi-LoRA Servingでは、ユーザーリクエストにLoRA IDを付与した「異種バッチ（heterogeneous batch）」として処理する。TGIはリクエスト内のタスク情報を元に適切なLoRAを動的に選択し推論を実行する。これにより、従来はモデルごとに個別のデプロイが必要だった構成を、単一デプロイに集約できる。

デプロイ方法はシンプルで、TGI v2.1.1以降のDockerイメージを使用し、`LORA_ADAPTERS`環境変数にカンマ区切りでアダプター名（例：`predibase/customer_support,predibase/magicoder`）を指定するだけである。推論時はOpenAI互換APIの`model`パラメーターにLoRA名を指定してリクエストする。

Predibaseの研究では、Mistral-7B-v0.1ベースのタスク特化LoRAがGPT-4を上回る性能を示したケースが報告されており、小型特化モデルの有効性が裏付けられている。

LoRA訓練にはAutoTrainのノーコードUIを活用でき、Hugging Face Space・DGX Cloud（最大8×H100）・Google Colab（T4 GPU）など多様な環境に対応する。訓練後はフルマージモデルではなくアダプター重みのみをHubにプッシュすれば、TGIがベースモデルを自動推定してロードする設計になっている。

コスト・運用面では、n個のモデルをn台のサーバーで運用する従来構成と比較して、GPU台数・管理工数を大幅に削減できる。組織内の複数チームがそれぞれ独立したLoRAを訓練・更新しながら、共通の推論インフラを共有できる点も実用上の強みである。

## アイデア

- LoRAアダプターはベースモデルの1/1000程度のサイズ（13.6MB vs 14.48GB）であり、30アダプターのVRAM増加が約3%という具体的な数値は、マルチテナント型LLMサービス設計の実現可能性を裏付ける重要な根拠になる
- リクエストごとにLoRA IDを付与する『異種バッチ処理』の設計思想は、エージェントシステムで複数の専門エージェントを単一推論エンドポイントに集約する際のアーキテクチャパターンとして応用できる
- 組織内の複数チームが独立してLoRAを訓練・更新しながら共通インフラを共有するモデルは、マイクロサービス的な分業体制とLLM運用コスト最適化を両立するガバナンス設計として参考になる

## Yujiの取り組みへの示唆

監査エージェントシステムを開発する上で、タスク別（リスク評価・証拠収集・レポート生成など）にLoRAをファインチューニングし、単一のTGIデプロイで複数の専門エージェントを動かす構成は、推論コストを抑えながらエージェントの専門性を高める有効なアプローチになる。LangGraphでのマルチエージェント設計においても、各ノード（エージェント）がLoRA IDを指定してAPIを呼び出すだけで役割を切り替えられるため、アーキテクチャをシンプルに保てる。ローカルLLMインフラ（RTX 3090）上でOllamaではなくTGIを採用する場合、このMulti-LoRA機能は単一GPUで複数の監査特化モデルを運用する際の現実的な選択肢となる。

## 原文リンク

[TGI Multi-LoRA：1回のデプロイで30モデルを同時配信](https://huggingface.co/blog/multi-lora-serving)
