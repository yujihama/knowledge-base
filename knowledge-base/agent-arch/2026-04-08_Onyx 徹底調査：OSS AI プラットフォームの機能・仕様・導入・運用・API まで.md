---
title: "Onyx 徹底調査：OSS AI プラットフォームの機能・仕様・導入・運用・API まで"
url: "https://zenn.dev/nekohotaru/articles/onyx-research-memo"
date: 2026-04-08
tags: [Onyx, RAG, OSS, MCP, LLM, Agent, OpenAPI, self-host, Connector, Deep Research]
category: "agent-arch"
memo: "[Zenn LLM] Onyx 徹底調査：OSS AI プラットフォームの機能・仕様・導入・運用・API まで"
processed_at: "2026-04-08T12:43:13.681708"
---

## 要約

Onyx は GitHub 上で約 22,200 stars・3,000 forks・157 releases（最新 v3.1.1、2026-04-01）を持つ OSS の統合 AI プラットフォーム。チャット UI・RAG/社内検索・カスタム Agent・外部 Action・Web 検索・コード実行・画像生成を一体化し、self-host しやすい構成が特徴。ライセンスは CE（MIT）と EE（Onyx Enterprise License）が同一リポジトリに混在する混合構成で、MIT のみを切り出した onyx-foss リポジトリも別途公開されている。主要機能は以下の通り：①Chat UI（ファイル・URL のコンテキスト付与、Projects による軽量作業コンテナ）、②Deep Research（複数サイクルの agentic 探索、通常比 10 倍超のトークンコスト）、③RAG/Internal Search（Confluence・SharePoint・Notion・Google Drive 等 50 超の Connector、embedding model 変更時は全再インデックス必要）、④Custom Agent（instructions＋knowledge＋actions の組み合わせ）、⑤Actions/OpenAPI/MCP（Internal Search・Web Search・Code Execution・Image Generation の built-in 4 種＋OpenAPI/MCP 経由のカスタム追加）、⑥Onyx MCP Server（Claude/Cursor 等の MCP client から Onyx 知識基盤にアクセス可能）、⑦Code Execution（numpy/pandas/scipy/matplotlib 内蔵、network access なしの sandboxed Python 環境）、⑧Craft beta（Next.js＋React＋shadcn/ui＋Recharts と Python sandbox で artifact 生成）。アクセス権限制御は CE では Private/Public のみで、source 側 ACL を継承する Auto Sync Permissions は EE 限定。permission-syncing は Confluence・Jira・Google Drive・Gmail・Slack・Salesforce・GitHub・SharePoint の 8 connector に限定される。導入時の注意点として、CE/EE 境界・権限制御の多くが EE 依存であること、Vespa→OpenSearch 移行に関する公式ドキュメントの揺れ、SCIM 記述の不一致を確認すべきとされている。REST API は基本的に /api/ プレフィックスを使い、Swagger UI で確認可能。

## アイデア

- Onyx MCP Server を活用することで、Claude/Cursor などの既存ツールを変えずに社内知識基盤への参照のみを Onyx に委譲できる分離設計が実用的
- Deep Research モードは通常推論の 10 倍超のトークンコストがかかる代わりに複数サイクルの agentic 探索を行う設計で、コスト対精度のトレードオフが明示されている点が参考になる
- CE/EE 混合ライセンス構成（同一リポジトリ内で MIT と Enterprise License が共存）は OSS エンタープライズ製品の一般的な収益化パターンを示しており、自社ツール設計の参考になる
## 関連記事

- /deep_36 LLMを「嘘つき」から「専門家」に変える技術 — Context Engineering 実践入門
- /deep_111 生成AIのハルシネーションは「誤出力」？ 条件付き分布・真理条件・接地から見る数理的整理
- /deep_1335 日本語入力システムSumibiの開発 part17: ピンインによる中国語入力に対応した
- /deep_95 思考とプロンプトの間にある「空白」こそが、すべてを決める
- /deep_77 パーソナルヘルスエージェントの解剖：マルチエージェント構造による個人健康支援フレームワーク

## 原文リンク

[Onyx 徹底調査：OSS AI プラットフォームの機能・仕様・導入・運用・API まで](https://zenn.dev/nekohotaru/articles/onyx-research-memo)
