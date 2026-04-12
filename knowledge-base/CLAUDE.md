# KB-System: パーソナルナレッジベース

## プロジェクト概要
スマホ(Telegram)から送られたURLを自動収集・要約・分類し、検索可能なナレッジベースとして蓄積するシステム。

## オーナーのプロフィール
- Deloitte Tohmatsu の AI スペシャリスト（内部監査領域）
- 監査エージェントシステムを開発中（LangGraph, Pydantic, ReAct）
- 関心領域: GRPO/RLAIF, RAG, Agent Architecture, LLM-as-judge
- ローカルLLMインフラ構築中（GALLERIA XA7C-R37T, RTX 3090 予定）

## 分類カテゴリ
- `ai-ml`: AI/ML研究（論文、モデル、学習手法、GRPO、RLAIF等）
- `audit-ai`: 監査AI・内部統制・GRC関連
- `agent-arch`: エージェントアーキテクチャ（LangGraph、MCP、マルチエージェント等）
- `infra`: インフラ・開発ツール（GPU、Docker、Ollama等）
- `other`: 上記に分類できないもの

## 要約ルール
- 日本語で出力する
- 技術的に具体的に（「すごい」「革新的」等の抽象表現を避ける）
- 監査エージェント開発への示唆があれば必ず言及する
- タグは具体的な技術用語を使う（例: GRPO, LangGraph, Pydantic）

## ディレクトリ構成
```
knowledge-base/
├── inbox/          # 未処理URL (inbox.jsonl)
├── ai-ml/          # AI/ML研究
├── audit-ai/       # 監査AI・内部統制
├── agent-arch/     # エージェントアーキテクチャ
├── infra/          # インフラ・ツール
├── other/          # その他
├── weekly-digest/  # 週次レポート
└── index/          # 将来のベクトルインデックス用
```

## graphify

This project has a graphify knowledge graph at graphify-out/.

Rules:
- Before answering architecture or codebase questions, read graphify-out/GRAPH_REPORT.md for god nodes and community structure
- If graphify-out/wiki/index.md exists, navigate it instead of reading raw files
- After modifying code files in this session, run `python3 -c "from graphify.watch import _rebuild_code; from pathlib import Path; _rebuild_code(Path('.'))"` to keep the graph current
