---
title: "Modular Diffusers 入門：拡散パイプラインのためのコンポーザブルなビルディングブロック"
url: "https://huggingface.co/blog/modular-diffusers"
date: 2026-03-31
tags: [diffusers, Modular Diffusers, HuggingFace, FLUX, ControlNet, ComponentsManager, pipeline-composition, Depth-Anything-V2]
category: "infra"
memo: "[HF Blog] Introducing Modular Diffusers - Composable Building Blocks for Diffusion Pipelines"
related: [1572, 1302, 1389, 1265, 1268]
processed_at: "2026-03-31T21:04:50.139517"
---

## 要約

Hugging Face が 2026年3月5日に公開した Modular Diffusers は、diffusers ライブラリに対して新しいパイプライン構築パラダイムを導入する。従来の DiffusionPipeline が一枚岩のクラスとして実装されているのに対し、Modular Diffusers はテキストエンコーダー・VAEエンコーダー・デノイズ・デコードなどの処理を独立したブロック（ModularPipelineBlocks）として分割し、それらを自由に組み合わせることでワークフローを構築できる。

API 設計として、ModularPipeline.from_pretrained() でパイプラインを定義し、load_components() でモデルウェイトを後から読み込む遅延ロード方式を採用している。FLUX.2 Klein 4B を例に取ると、pipe.blocks で内部ブロック構成を確認でき、sub_blocks.pop() で特定ブロックを切り出して単体パイプラインとして動作させることも可能。テキストエンコード結果（prompt_embeds）だけを先行して取得し、残りのブロックに渡すといった分割実行が自然に書ける。

カスタムブロックは Python クラスとして定義する。expected_components でモデル依存関係を宣言し、inputs・intermediate_outputs で入出力を明示し、__call__ で計算ロジックを実装する。例として Depth Anything V2 を使った深度マップ抽出ブロック（DepthProcessorBlock）が紹介されており、このブロックを Qwen の ControlNet ワークフローの先頭に挿入するだけで、control_image の出力が下流ブロックへ自動的に伝播するデータフロー設計が示されている。

ComponentsManager はメモリ管理のための仕組みで、複数パイプラインをまたいでモデルを共有し、使用中でないモデルを CPU にオフロードする。カスタムブロックは Hub に公開でき（trust_remote_code=True で読み込み）、コミュニティがブロック単位で再利用・共有できるエコシステムを想定している。また、ノードベースのビジュアルワークフロー UI である Mellon との統合も提供されており、ブロックをGUI上で配線してパイプラインを組み立てることも可能。

## アイデア

- ブロック単位の入出力宣言（InputParam / OutputParam）によってデータフローが自動解決される設計は、LangGraph のノード・エッジグラフに近い抽象であり、エージェントパイプライン設計への転用が概念的に興味深い
- ComponentsManager によるクロスパイプラインのモデル共有とCPUオフロードは、複数エージェントが異なるモデルを呼び出すマルチエージェントシステムのリソース管理パターンとして参照できる
- expected_components にデフォルトの pretrained_model_name_or_path を持たせることで依存モデルを宣言的に管理する手法は、Pydantic のフィールドデフォルト設計に近く、コンポーネント仕様の自己記述性を高める設計思想として汎用性が高い
## 関連記事

- /deep_1572 🧨 DiffusersによるStable Diffusion：仕組みと実装ガイド
- /deep_1302 🤗 Diffusers 1周年記念：1年間の主要機能まとめ
- /deep_1389 無料Google ColabでDeepFloyd IFをDiffusersで動かす方法
- /deep_1265 Würstchen：42倍圧縮による高速・低コスト画像生成拡散モデルの紹介
- /deep_1268 T2I-AdapterによるSDXLの効率的な制御可能生成

## 原文リンク

[Modular Diffusers 入門：拡散パイプラインのためのコンポーザブルなビルディングブロック](https://huggingface.co/blog/modular-diffusers)
