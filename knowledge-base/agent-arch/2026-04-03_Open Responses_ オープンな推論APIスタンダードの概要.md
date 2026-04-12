---
title: "Open Responses: オープンな推論APIスタンダードの概要"
url: "https://huggingface.co/blog/open-responses"
date: 2026-04-03
tags: [Open Responses, Responses API, エージェントループ, MCP, 推論ストリーミング, Hugging Face, tool_choice, マルチプロバイダールーティング]
category: "agent-arch"
memo: "[HF Blog] Open Responses: What you need to know"
related: [88, 83, 430, 1310, 1669]
processed_at: "2026-04-03T09:08:31.050720"
---

## 要約

Open ResponsesはOpenAIが2025年3月に公開したResponses APIをベースに、Hugging Faceおよびオープンソースコミュニティが主導してオープン化した新しい推論APIスタンダード。従来のChat Completion形式はターン制の会話向けに設計されており、エージェント型ワークフロー（長時間の自律的な推論・計画・行動）には本質的に不適合であるという問題意識から生まれた。

主な技術的特徴は以下の通り。①ステートレス設計をデフォルトとし、プロバイダーが必要とする場合は暗号化推論（encrypted reasoning）もサポート。②ストリーミングをrawテキストやオブジェクトのデルタではなく、セマンティックイベントの系列として表現。③推論トレースの可視性を3段階（content: 生のトレース、encrypted_content: プロバイダー暗号化コンテンツ、summary: サニタイズされた要約）に整理。これにより、オープンウェイトモデルはresponse.reasoning.deltaイベントで生の推論ストリームを返せるようになる。

ツール分類では「内部ツール」（プロバイダー側で実行: ファイル検索、Google Drive連携など）と「外部ツール」（クライアント側関数、MCPサーバーなど）を明示的に区別。サブエージェントループは「リクエスト受信→モデルサンプリング→ツール呼び出し→結果フィードバック→完了まで繰り返し」のサイクルとして仕様化されており、max_tool_callsとtool_choiceパラメータで制御可能。内部ツールを使う場合、プロバイダーがループ全体を管理するため「ドキュメント検索→要約→メール下書き」のような複数ステップのワークフローが単一リクエストで完結する。

アーキテクチャ上の重要な区別として、「Model Provider（推論を提供する主体）」と「Router（複数プロバイダーを仲介する主体）」を分離しており、クライアントはリクエスト内でプロバイダー指定とプロバイダー固有オプションを渡せる設計。エンドポイントはhttps://evalstate-openresponses.hf.spaceでデモ公開されており、OpenResponses-Versionヘッダーで版を指定する。Kimi-K2-Thinking（Nebius）やGLM-4.7など複数モデルのルーティングをすでにサポートしている。

## アイデア

- 推論トレースをcontent/encrypted_content/summaryの3段階で扱う設計は、LLM-as-judgeやデバッグ目的で推論過程の透明性を制御する際に応用できる
- Model ProviderとRouterの明示的分離により、監査ログ・トレーサビリティの観点から『どのプロバイダーが何を実行したか』を構造的に追跡する基盤になりうる
- max_tool_callsによるループ上限制御は、エージェントの暴走・無限ループ防止の標準的なガードレールとして、エンタープライズ向けエージェントシステム設計のリファレンスになる
## 関連記事

- /deep_88 研究者向けMCP：AIを研究ツールに接続する方法
- /deep_83 ClaudeとHugging FaceでAI画像生成：MCP連携による実践ガイド
- /deep_430 過去のセッションを必要時のみ参照する方針でclaude-memのトークン消費を激減させた話
- /deep_1310 複雑な生成AIユースケースへのHugging Face活用事例：Writer社CTOインタビュー
- /deep_1669 倫理原則を研究ライフサイクルの核心に据える：Hugging Face マルチモーダルプロジェクトの倫理憲章

## 原文リンク

[Open Responses: オープンな推論APIスタンダードの概要](https://huggingface.co/blog/open-responses)
