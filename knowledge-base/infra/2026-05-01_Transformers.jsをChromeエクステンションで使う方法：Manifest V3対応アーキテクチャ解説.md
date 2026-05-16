---
title: "Transformers.jsをChromeエクステンションで使う方法：Manifest V3対応アーキテクチャ解説"
url: "https://huggingface.co/blog/transformersjs-chrome-extension"
date: 2026-05-01
tags: [Transformers.js, Chrome拡張機能, Manifest V3, Gemma 4, WebGPU, ONNX, サービスワーカー, ローカル推論, ツール呼び出し]
category: "infra"
related: [1307, 410, 1709, 2696, 2924]
memo: "[HF Blog] How to Use Transformers.js in a Chrome Extension"
processed_at: "2026-05-01T12:07:42.519839"
---

## 要約

HuggingFaceが公開したブログ記事で、Transformers.jsをChrome拡張機能（Manifest V3）上で動作させるための実装アーキテクチャを解説している。具体的にはGemma 4 E2B（onnx-community/gemma-4-E2B-it-ONNX、q4f16量子化）とMiniLM-L6-v2（feature-extraction、fp32）の2モデルをローカル推論で使用するブラウザアシスタント拡張機能の構築例を示す。

アーキテクチャの核心はMV3の3つのランタイム分離にある。①バックグラウンドサービスワーカー（background.ts）：エージェントライフサイクル、モデル初期化、ツール実行、KVキャッシュ（DynamicCache）管理を担うコントロールプレーン。②サイドパネル（sidebar）：チャットUI、ストリーミング表示。③コンテンツスクリプト（content.ts）：DOM抽出とハイライト操作のページブリッジ。推論はすべてバックグラウンドで実行されるため、モデルの重複ロードが発生せず、キャッシュもchrome-extension://のオリジン下に一元管理される。

メッセージングはsrc/shared/types.tsで型定義された列挙型（BackgroundTasks、BackgroundMessages、ContentTasks）で厳密に管理される。例えばサイドパネルがAGENT_GENERATE_TEXTを送ると、バックグラウンドがchatMessagesに追記して推論を実行し、MESSAGES_UPDATEをサイドパネルに返す一方向フローを採る。

ツール呼び出しはTransformers.jsのpipeline('text-generation')にtoolsスキーマを渡すことで実現し、モデルのチャットテンプレートが実際のプロンプトフォーマットを処理する。エージェントループはAGENT_INITIALIZE→AGENT_GENERATE_TEXT→ツール結果注入→再生成というReActライクなサイクルで動作する。

MV3特有の制約として、サービスワーカーはサスペンド・再起動が発生するため、モデルの実行時状態は再初期化可能な設計にする必要がある。またモデルのダウンロード管理はCHECK_MODELS（キャッシュ確認）→INITIALIZE_MODELS（ダウンロード・初期化）の2フェーズで明示的に行い、DOWNLOAD_PROGRESSでUIに進捗を通知する。

権限設計もアーキテクチャの一部として扱われており、sidePanel、storage、tabs、scripting、host_permissions（http(s)://*/*）の5種のみをrequestしている。推論はすべてローカルで実行されユーザーデータが外部送信されない点が明示されている。監査エージェント開発への示唆として、バックグラウンドをコントロールプレーンとしてエージェントロジックを集約し、UIは薄いクライアントに徹するパターンは、LangGraphベースのエージェントシステムでもWorkerとOrchestratorを分離する設計原則と直接対応する。

## アイデア

- バックグラウンドサービスワーカーをエージェントのコントロールプレーンとして使い、UIとページスクリプトを薄いワーカーに徹させる分離パターンは、LangGraphのOrchestrator-Worker構成と同型であり、ブラウザ環境でのエージェント実装の参照アーキテクチャになり得る
- モデルキャッシュをchrome-extension://オリジン下に一元管理することで、タブやセッションをまたいでモデルを再利用できる点は、サーバーレスエッジ環境でのLLMホスティングにおけるコールドスタート問題の回避策として応用可能
- Gemma 4（推論・ツール判断）とMiniLM-L6-v2（ベクトル埋め込み）を明示的に役割分担させる設計は、軽量RAGシステムをブラウザ内で完結させる構成として、オフライン監査ツールや機密文書処理アプリへの応用が考えられる

## 前提知識

- **Manifest V3** (TODO: 読むべき)
- **Transformers.js** → /deep_940 Llama 3.2 リリース：視覚理解とオンデバイス推論を兼ね備えたオープンモデル群
- **WebGPU推論** (TODO: 読むべき)
- **ONNX量子化** (TODO: 読むべき)
- **ReActエージェントループ** (TODO: 読むべき)

## 関連記事

- /deep_1307 Transformers.jsでMLパワードWebゲームを作る方法
- /deep_410 Transformers.js v4：NPMで正式リリース — WebGPUランタイム完全刷新とブラウザ・サーバ横断対応
- /deep_1709 機械学習エキスパート・インタビュー：Lewis Tunstall（Hugging Face MLエンジニア）
- /deep_2696 日本語入力システムSumibiの開発 part18: ローカルLLMが閾値を超えたかも
- /deep_2924 小規模モデルへの行動的傾向の蒸留：3段階にわたる否定的結果

## 原文リンク

[Transformers.jsをChromeエクステンションで使う方法：Manifest V3対応アーキテクチャ解説](https://huggingface.co/blog/transformersjs-chrome-extension)
