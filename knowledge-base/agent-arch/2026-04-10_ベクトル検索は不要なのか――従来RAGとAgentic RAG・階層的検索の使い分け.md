---
title: "ベクトル検索は不要なのか――従来RAGとAgentic RAG・階層的検索の使い分け"
url: "https://zenn.dev/nttdata_tech/articles/694e39ceff58b7"
date: 2026-04-10
tags: [RAG, Agentic-RAG, ベクトル検索, 階層的検索, PageIndex, DeepRead, LlamaIndex, Gemini-Embedding2, Progressive-Disclosure]
category: "agent-arch"
memo: "[Zenn LLM] ベクトル検索は不要なのか"
processed_at: "2026-04-10T21:01:31.191930"
---

## 要約

本記事はNTT DATAの技術者によるRAGアーキテクチャの再整理。結論は「ベクトル検索が不要になったのではなく、手法ごとの得意不得意が明確になった」。

従来のベクトル型RAGは、文書をチャンク分割→Embeddingモデルでベクトル化→コサイン類似度で検索するアーキテクチャ。大規模データや高速スループットが必要な場面では依然有効だが、チャンク設計・更新サイクル・精度の個別最適化が避けられないという構造的課題を持つ。

Agentic RAGはAI自身が「どのクエリで何回検索するか」を自律的に決定し、ツールとして検索を実行する。A-RAG（arXiv:2602.03442）はキーワード・ベクトル・チャンクの階層的取得を組み合わせ、Du et al. 2026の研究として発表。

ファイル検索型Agentic RAGとして、grepベースのツールを持たせたエージェントとベクトルRAGを比較した論文（arXiv:2602.23368）では、金融文書でベクトルRAGを上回る精度を示した。LlamaIndexの実験（Bertelli et al. 2026）では、論文数本規模ではファイル検索Agentic RAGが精度で大幅優位だが、数百本規模では従来RAGが速度・精度ともに優位という規模依存の結果が得られた。

構造認識型RAGとして、PageIndex（チャンク分割なし・ベクトル検索フリー、文書を階層ツリーに変換してAIが辿る）がFinanceBenchで98.7%の正解率でSOTAを達成。DeepRead（arXiv:2602.05014）はMarkdown変換で文書階層を抽出し、「Retrieve（検索）」と「ReadSection（読解）」の2ツールを使い分け、複数長文QAデータセットで既存Agentic RAGを凌駕。

著者の持論として「階層的検索」が次世代RAGの鍵とされる。理由は2点：(1) ベクトル型RAGはフォルダ構造を破壊して並列インデックスに変換するが、これは人間のファイル管理文化と乖離している；(2) Claude Skillsが採用するProgressive Disclosure（段階的開示）のように、コンテキストウィンドウを効率的に使うにはAIが段階的に情報取得するべきという考え方。

余談として、Gemini Embedding2はテキスト・画像・動画・音声・PDFを単一の特徴空間に埋め込み可能な完全マルチモーダル埋め込みモデルとして紹介（テキスト最大8192トークン、画像6枚/リクエスト、動画120分、音声80秒、PDF6ページ）。画像付きPDFの分離処理が不要になるため、従来RAGの前処理コストを削減できる。

## アイデア

- ファイル検索型Agentic RAG（grep/glob/read）は小〜中規模文書では精度でベクトルRAGを上回るが、数百文書規模では逆転する——スケールに応じたハイブリッド設計が現実解
- PageIndexのチャンク分割なし・階層ツリー構造traversalがFinanceBenchで98.7%というSOTAを達成した事実は、「構造保持＋AIによる能動的ナビゲーション」の有効性を強く示唆する
- Claude SkillsのProgressive Disclosure（必要な情報だけ段階的にロード）という設計思想をRAGに適用することで、コンテキストウィンドウの浪費を抑えながら検索精度を高める方向性が開けている
## 関連記事

- /deep_858 【2026年最新】AIエージェントフレームワーク・ツール完全まとめ224選 — AgDex.aiディレクトリ紹介
- /deep_1337 RAGの検索をAIに任せたら精度が79%上がった（Agentic RAG / A-RAG）
- /deep_9 LLMに長期記憶を実装する — 脳の記憶メカニズムのPython実装
- /deep_1116 🤗 Optimum IntelとfastRAGによるCPU最適化エンベディング
- /deep_1334 製造業向けRAGシステムのアクセス制御設計

## 原文リンク

[ベクトル検索は不要なのか――従来RAGとAgentic RAG・階層的検索の使い分け](https://zenn.dev/nttdata_tech/articles/694e39ceff58b7)
