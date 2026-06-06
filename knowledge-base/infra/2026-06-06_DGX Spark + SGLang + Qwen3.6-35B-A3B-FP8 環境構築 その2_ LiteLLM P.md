---
title: "DGX Spark + SGLang + Qwen3.6-35B-A3B-FP8 環境構築 その2: LiteLLM Proxy 活用"
url: "https://zenn.dev/supertaro/articles/4744c929c8981c"
date: 2026-06-06
tags: [LiteLLM, SGLang, Qwen3, DGX Spark, Docker, OpenAI-compatible API, LLM Gateway, FP8]
category: "infra"
related: [2590, 5969, 6411, 6478, 4331]
memo: "[Zenn LLM] DGX Spark + SGLang + Qwen3.6-35B-A3B-FP8 環境構築 その2: LiteLLM Proxy 活用"
processed_at: "2026-06-06T09:00:57.401601"
---

## 要約

DGX Spark上のDocker環境でSGLangとQwen3.6-35B-A3B-FP8を動かす構成の続編。前編では自作PythonゲートウェイをSGLangの前段に置いていたが、今回はそれをLiteLLM Proxyに置き換える構成変更を解説している。

自作ゲートウェイはPython標準ライブラリのみで実装されており、APIキー認証・SGLang APIへの中継・enable_thinking補完・ストリーミング転送を担っていた。しかし長期運用を想定した場合、自作コードのHTTP中継・JSON変換・認証ロジックを維持し続けるコストが問題となるため、LiteLLM Proxyへの移行を決断した。

新構成ではSGLangをDocker network内部（port 29999、externally unexposed）の純粋な推論サーバーとして閉じ、LiteLLM Proxyが外部向けのOpenAI互換ゲートウェイ（port 30000）として全クライアントリクエストを受け付ける。OpenCode、Hermes Agent、Open WebUIなどのクライアントはすべてLiteLLMに接続し、SGLangへの直接アクセスは行わない。

LiteLLM側では3つのモデルエイリアスを定義する：(1) qwen3.6-35b-a3b-fp8（enable_thinkingをクライアント依存）、(2) qwen3.6-35b-a3b-fp8-fast（未指定時にenable_thinking=falseをプリセット）、(3) qwen3.6-35b-a3b-fp8-think（未指定時にenable_thinking=trueをプリセット）。これらはextra_bodyによるプリセット方式で実装されており、クライアントがchat_template_kwargs.enable_thinkingを明示した場合はクライアント指定が優先される。厳密な強制が必要な場合はカスタムコールバックや別のrewriteプロキシが必要となる点も明記されている。

設定ファイル群は.env・docker-compose.yml・litellm_config.yamlの3ファイル構成。コンテキスト長はSGLang側で262144トークン（256K）に設定し、fast/passthroughモデルは最大入力262144トークン、thinkモデルは32768トークンをmodel_infoに設定する。最大出力は8192トークン。APIキー管理はLiteLLMのmaster keyで行い、virtual keyのためのPostgres連携は省略している。

監査エージェント開発への示唆として、LangGraphベースの監査エージェントでも同様の構成が有効で、推論モード（fast/think）をモデルエイリアスで切り替えることで、ツール呼び出しには高速モード、複雑な判断には思考モードを使い分けられる。

## アイデア

- モデルエイリアスでenable_thinkingのプリセットを分離することで、クライアント側の実装変更なしに推論モードを切り替えられる設計が実用的
- 推論サーバー（SGLang）をDocker network内部に閉じてAPIゲートウェイ（LiteLLM）だけを外部公開する責務分離パターンは、セキュリティと設定シンプルさを両立する
- extra_bodyによるプリセット方式は「デフォルト値の注入」であり「強制」ではない点が重要で、クライアント側の柔軟性を残しつつ運用を簡略化できる

## 前提知識

- **LiteLLM Proxy** (TODO: 読むべき)
- **SGLang** → /deep_5406 Irminsul: エージェント型LLMサービングのためのMLA-ネイティブ位置非依存キャッシュ
- **OpenAI-compatible API** → /deep_5261 『三国志』を使って最小構成のRAGを実装してみた
- **enable_thinking（Qwen3思考モード）** (TODO: 読むべき)
- **Docker Compose** (TODO: 読むべき)

## 関連記事

- /deep_2590 ローカルLLMを簡単にデモする：vLLM + LiteLLM + ngrokの構成
- /deep_5969 初めて作るオレオレAIデータセンター③：DGX SparkとRTX PRO 6000 Blackwell MAX-Qを比較する
- /deep_6411 【Irodori-TTS】DGX Spark (GB10) でOpenAI互換TTSサーバーを構築する
- /deep_6478 Windows11 RTX 5090でAIエージェント用Qwen3.6-27B LLM環境構築
- /deep_4331 RTX 4060 8GB でどこまで動く？ Qwen3 サイズ別 VRAM 境界線を探る

## 原文リンク

[DGX Spark + SGLang + Qwen3.6-35B-A3B-FP8 環境構築 その2: LiteLLM Proxy 活用](https://zenn.dev/supertaro/articles/4744c929c8981c)
