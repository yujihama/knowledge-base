---
title: "AI時代のポートフォリオはAI検索・AI採用に対応したAIOが必要：GitHub PagesでAIO実装を試みる実験"
url: "https://zenn.dev/yuta_yokoi/articles/c82fe055816454"
date: 2026-05-11
tags: [AIO, llms.txt, JSON-LD, GitHub Pages, GitHub Actions, Schema.org, AI最適化, 構造化データ, AI2AI, 静的サイト]
category: "agent-arch"
related: [10, 3648, 3373, 78, 4910]
memo: "[Zenn LLM] AI時代のポートフォリオは人間に見せるだけでは全く足りない：GitHub PagesでAIOを実装し続ける実験"
processed_at: "2026-05-11T09:09:28.974742"
---

## 要約

本記事は、GitHub Pages上で公開する静的ポートフォリオに対して、AI検索エンジン・LLM・AIエージェントが正確に読み取れるよう最適化する「AIO（AI Optimization）」の実装手法を体系的に解説した実践記事である。

従来のSEO的アプローチは人間の閲覧を前提としていたが、ChatGPT・Claude・Perplexityなどが情報収集エージェントとして機能するAI時代においては、AIが断片的にHTMLやメタデータを解析する前提の設計が必要になる。

具体的な実装層として以下を整備している：(1) `llms.txt`をルートおよび`.well-known/`の両方に配置し、AIへの読み込み順序・解釈ルール・Entity情報を明示する。(2) `llms-full.txt`をAI向け正典（Ground Truth）として設置し、誤解釈を防ぐNon-Goals（「これはAI生成テンプレートではない」）を明記する。(3) `AI2AI.md`でAIセッション間の作業引き継ぎを構造化し、フレームワーク禁止・変更の可逆性などの制約を明文化する。(4) Schema.org語彙を使ったJSON-LD構造化データをHTMLに埋め込み、Person・WebSite・ImageObject・AudioObjectを記述する。(5) WebP画像のXMPメタデータ、MP3のID3タグにもAI向け情報を付与する。(6) `.well-known/aio-manifest.json`でsha256ハッシュによるファイルダイジェストを管理し、GitHub Actionsで整合性を自動検証する。(7) `.well-known/mcp.json`をAgent discovery用の静的manifestとして設置する。

CI（GitHub Actions）では、`llms.txt`と`.well-known/llms.txt`の同一性チェック、JSON-LDスキーマ検証、バイナリファイルのAIOメタデータ確認などをPython標準ライブラリで実装し、差異があればCIを落とす設計にしている。

監査エージェント開発への示唆としては、AI2AI.mdの「制約の明文化」パターンが直接応用できる。LangGraphやReActベースのエージェントに対しても、タスク引き継ぎ時のコンテキスト文書・非交渉的制約リスト・変更の可逆性要件を構造化することで、マルチセッション・マルチエージェント環境でのドリフトを防ぐ設計思想として活用可能。

## アイデア

- AI2AI.mdによるAIセッション間引き継ぎの構造化：「制約の明文化」パターンはLangGraphエージェントのハンドオフ設計にそのまま転用できる
- sha256ダイジェストによるAIOファイルの整合性管理をCIで自動検証する設計は、エージェントが参照するナレッジベースの改ざん検知にも応用可能
- llms-full.txtにNon-Goalsを明記して誤解釈を防ぐ手法は、LLM-as-judgeのシステムプロンプト設計における「してはいけない解釈」の明示化と同じ発想

## 前提知識

- **JSON-LD** → /deep_10 LLMクローラーを制御する『AIO』基本マニュアル：llms.txtとllms-full.txtの実装
- **Schema.org** (TODO: 読むべき)
- **llms.txt** → /deep_10 LLMクローラーを制御する『AIO』基本マニュアル：llms.txtとllms-full.txtの実装
- **robots.txt** → /deep_4614 AIクローラーを一括りにするな 実践編：robots.txt・WAF・CIDRで本番制御するAIO Bot Governance
- **GitHub Actions** → /deep_1428 AIがソフトウェア開発を変える——2026年、エンジニアリングの自動化最前線

## 関連記事

- /deep_10 LLMクローラーを制御する『AIO』基本マニュアル：llms.txtとllms-full.txtの実装
- /deep_3648 機械学習論文を毎日自動収集してAIで日本語解説するサイトを作った（MLinfo）
- /deep_3373 有価証券報告書をAIに読ませる3つの選択肢——NECの93%削減事例から考える
- /deep_78 広告の届け先はAIになる — B2A (Business to Agent) Platform という未来
- /deep_4910 Windows上でDevinが動作するようになっていた、そして広がる可能性

## 原文リンク

[AI時代のポートフォリオはAI検索・AI採用に対応したAIOが必要：GitHub PagesでAIO実装を試みる実験](https://zenn.dev/yuta_yokoi/articles/c82fe055816454)
