---
title: "SyGra Studio 紹介：合成データ生成のビジュアル・インタラクティブ環境"
url: "https://huggingface.co/blog/ServiceNow-AI/sygra-studio"
date: 2026-04-02
tags: [synthetic-data, SyGra, visual-workflow, LLM-pipeline, Pydantic, Ollama, vLLM, HuggingFace, self-critique, ServiceNow]
category: "agent-arch"
memo: "[HF Blog] Introducing SyGra Studio"
processed_at: "2026-04-02T09:07:43.364633"
---

## 要約

SyGra 2.0.0で導入されたStudioは、合成データ生成ワークフローをYAMLファイルやターミナル操作なしにビジュアルキャンバス上で構築・実行できるインタラクティブ環境。ServiceNow AIチームが開発し、2026年2月5日に公開された。

主な機能は以下の通り。モデル設定はOpenAI、Azure OpenAI、Ollama、Vertex AI、AWS Bedrock、vLLM、カスタムエンドポイントをGUIフォームで設定・検証できる。データソースはHugging Face、ローカルファイルシステム、ServiceNowに対応し、実行前にサンプル行をプレビュー可能。データソースのカラム名は自動的に状態変数（例：{prompt}、{genre}）として登録され、後続ノードのプロンプト内で即座に参照できる。

フロー構築はドラッグ＆ドロップ方式。LLMノードを配置してモデルを選択し、プロンプトを記述して出力変数名を定義する。プロンプト入力中に「{」を打つと利用可能な状態変数が自動補完される。構造化出力、ツール連携、Lambda/Subgraphノードによる再利用可能ロジックやブランチ処理も設定可能。複数LLMによる並列生成設定にも対応する。

コードパネルではStudioが生成するYAML/JSONをリアルタイムで確認でき、tasks/examples/に書き出されるアーティファクトと完全一致する。実行時はノード単位でステータス、トークン使用量、レイテンシ、コストをストリーミング表示し、実行履歴は.executions/runs/*.jsonに保存される。Monacoエディタによるインラインコード編集、ブレークポイント、自動保存ドラフト機能でデバッグも容易。

既存ワークフローの実行例として、glaive_code_assistantワークフローが示されている。glaiveai/glaive-code-assistant-v2データセットを取り込み、回答生成ノード（generate_answer）と批評ノード（critique_answer）を条件付きエッジで接続し、「NO MORE FEEDBACK」が返るまでループする自己改善型パイプラインをキャンバス上で可視化・実行できる。

インストールはgit clone後にmake studioで起動。合成データはモデルトレーニング、評価パイプライン、アノテーションツール向けの出力として利用できる。

## アイデア

- データソースのカラム名を自動的に状態変数として登録し、後続ノードで即座に参照できる仕組みは、マルチステップエージェントにおける状態管理の明示的な可視化パターンとして参考になる
- generate_answer→critique_answer→条件分岐ループという構造は、LLM-as-judgeによる自己改善型合成データ生成パイプラインの具体的な実装例であり、RLAIFのデータ収集フローに直接応用できる
- ビジュアルキャンバスで設計したフローが対応するYAML/JSONを自動生成する双方向同期の仕組みは、ノーコード・ローコードとコードベース管理を両立させるアーキテクチャ設計として注目に値する
## 関連記事

- /deep_647 Transformersライブラリ：モデル定義の標準化とエコシステムの統合
- /deep_835 Synthetic Data Generator：自然言語でデータセットを構築するノーコードツール
- /deep_301 Nemotron-Personas-India: 主権AIのための合成インドペルソナデータセット
- /deep_649 Inference Endpoints で実現する超高速 Whisper 音声認識（最大8倍高速化）
- /deep_859 Google Gemma 4 実践ガイド — Ollama・HuggingFace で動かすマルチモーダル対応オープンモデル

## 原文リンク

[SyGra Studio 紹介：合成データ生成のビジュアル・インタラクティブ環境](https://huggingface.co/blog/ServiceNow-AI/sygra-studio)
