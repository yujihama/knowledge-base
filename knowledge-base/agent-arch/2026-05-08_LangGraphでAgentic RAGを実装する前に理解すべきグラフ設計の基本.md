---
title: "LangGraphでAgentic RAGを実装する前に理解すべきグラフ設計の基本"
url: "https://zenn.dev/libercraft/articles/20260430-agentic-rag-langgraph-design"
date: 2026-05-08
tags: [LangGraph, Agentic RAG, StateGraph, RAG, LangChain, 動的グラフ, 条件エッジ, TypedDict]
category: "agent-arch"
related: [858, 2255, 857, 4177, 2061]
memo: "[Zenn LLM] LangGraphでAgentic RAGを実装する前に理解すべきグラフ設計の基本"
processed_at: "2026-05-08T09:39:06.857779"
---

## 要約

本記事は、通常のRAGとAgentic RAGの本質的な違いを整理した上で、LangGraphのグラフ設計に必要な概念と実務上の設計ミスを解説する実践的なガイドである。

通常のRAGは「検索→コンテキスト生成→LLM回答」という固定パイプラインで動作するため、比較・集計が必要な質問（A製品とB製品の価格差など）、前提確認が必要な質問（OSやバージョン依存の手順）、検索品質が低い場合の再検索判断、の3ケースで限界を露呈する。Agentic RAGはLLMが実行時に「再検索すべきか」「回答生成に移るか」を動的に判断する「動的グラフ」として機能することでこれらを解決する。

LangGraphは StateGraph・ノード・エッジの3概念で構成される。StateGraphは全ノード間で受け渡される共有状態（TypedDict）を定義し、フィールドの更新パターンとして「上書き（デフォルト）」と「追記（Annotated + operator.add）」を使い分ける。会話履歴・デバッグログなど蓄積が必要な情報はAnnotated[list[str], operator.add]で定義する。LangChainメッセージ型を扱う場合はlanggraph.graph.messageのadd_messagesを使う。

ノードは通常のPython関数（またはasync def）で、状態を受け取り更新差分を辞書で返す設計。非同期ノードでは asyncio.gather を使った並行検索が可能だが、同期・非同期の混在はエラーになるため統一が必要。エッジには「固定エッジ」と「条件エッジ」があり、条件エッジは文字列を返す関数で遷移先をルーティングする。これが動的分岐の核心。

実行方法は3種類：app.invoke()（結果一括取得）、app.stream()（ノード単位逐次取得・デバッグ向き）、app.astream()（非同期ストリーミング）。本番でもstream()によるログ取得を推奨している。

実務でよく見る設計ミスは4つ：①状態への詰め込みすぎ（各ノードのInput/Outputフィールドを事前に一覧化すべき）、②条件エッジの終了条件未設定による無限ループ（retry_countで上限管理）、③ノードへの副作用混在（ループ内でDB書き込みやSlack通知が繰り返し実行される問題→副作用は専用ノードに分離してループ外に配置）、④グラフのコンパイル前後での可視化確認不足（app.get_graph().draw_mermaid()で設計図と実装の一致を検証）。

監査エージェント開発への示唆として、再検索ループや前提確認ステップはエビデンス収集フローに直接応用できる。特にretry_countによるループ制御と副作用ノード分離の設計原則は、LangGraphベースの監査ワークフロー（証拠収集→品質判定→追加収集）の信頼性確保に重要。

## アイデア

- Annotated[list[str], operator.add]による状態フィールドの追記パターンは、監査ログや中間思考の蓄積に直接応用できる設計プリミティブ
- 副作用ノードをループ外に分離する原則は、DB書き込みや外部通知の冪等性確保として監査エージェントの証跡管理に不可欠
- app.stream()でノード単位の実行ログを取る設計は、監査トレイルの自動生成に転用できる（どのノードがどのフィールドを更新したかの記録）

## 前提知識

- **LangGraph** → /deep_28 IBMとUC BerkeleyがIT-BenchとMASTを使ってエンタープライズエージェントの失敗原因を診断
- **RAG** → /deep_5 Google Research at The Check Up: ヘルスケアAIの最新研究成果と実臨床への展開（2026年）
- **StateGraph** → /deep_2061 プロンプト改善は後回し: LangGraphでさっさと実装、MLflowで誤りから暗黙知を吸収&改善
- **TypedDict** (TODO: 読むべき)
- **async/await** (TODO: 読むべき)

## 関連記事

- /deep_858 【2026年最新】AIエージェントフレームワーク・ツール完全まとめ224選 — AgDex.aiディレクトリ紹介
- /deep_2255 The Colony に参加する LangChain エージェントを構築する
- /deep_857 AIエージェントフレームワーク比較【LangChain vs CrewAI vs AutoGen】実務で選ぶための完全ガイド【2026年最新】
- /deep_4177 2026年、個人開発で今すぐ試せるAI・機械学習ホットトピック4選
- /deep_2061 プロンプト改善は後回し: LangGraphでさっさと実装、MLflowで誤りから暗黙知を吸収&改善

## 原文リンク

[LangGraphでAgentic RAGを実装する前に理解すべきグラフ設計の基本](https://zenn.dev/libercraft/articles/20260430-agentic-rag-langgraph-design)
