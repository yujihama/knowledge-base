---
title: "AIエージェントはなぜ覚えられるのか｜Memoryで理解する状態を持つLLM"
url: "https://zenn.dev/startspace/articles/3c6fb5e7d0b169"
date: 2026-04-15
tags: [Semantic Kernel, State Memory, AIエージェント, RAG, Function Calling, Short-Term Memory, Long-Term Memory, Azure OpenAI]
category: "agent-arch"
related: [1192, 1116, 1334, 861, 112]
memo: "[Zenn LLM] AIエージェントはなぜ覚えられるのか｜Memoryで理解する状態を持つLLM"
processed_at: "2026-04-15T12:16:32.764549"
---

## 要約

LLMはステートレスな関数であり、処理ごとに状態がリセットされる。AIエージェントが「覚えている」ように見える理由は、LLM自体が学習・記憶しているのではなく、外部にMemory（状態）を持つアーキテクチャによるものである。本記事はSemantic Kernelを用いた在庫管理エージェントを題材に、AIエージェントのMemory構造を3種類に分類して解説する。

**Memory の3分類：**
1. **Short-Term Memory（短期記憶）**：現在の会話履歴、ツール実行結果、途中の判断結果をコンテキストとしてLLMに渡す。セッション内の一時的な情報保持が目的。
2. **Long-Term Memory（長期記憶）**：RAGに代表されるベクトルDB等への外部知識格納。必要なタイミングで検索して取得する。
3. **State Memory（状態記憶）**：現在のタスク進捗・処理フラグ・業務上の中間状態を保持する。エージェントループの継続動作に不可欠。

**AIエージェントの動作構造：** `State → Think → Act → Observe → State更新` のループとして定式化される。Stateがなければ、在庫確認→条件判断→発注といった一連フローをプログラム側で完全に手動制御する必要がある。Stateを持つことで、エージェント自身が「現在の在庫数」「発注済みか」「業務完了か」を保持しながら次の判断を行える。

**実装例：** Semantic KernelとAzure OpenAIを組み合わせ、`InventoryState`（item_id, stock, done）というデータクラスをStateとして定義。`InventoryPlugin`に`get_stock`と`place_order`の2つのKernel Functionを実装し、`FunctionChoiceBehavior.Auto`でLLMが自律的に関数を選択する。ループ内でLLMの出力（JSON）をパースしてStateを更新し、`done=True`になるまで繰り返す構成。在庫6個の場合、閾値10未満のため発注が実行され、在庫が26個に更新されてループ終了する。

**監査エージェント開発への示唆：** 監査ワークフロー（証跡収集→リスク判定→指摘生成→承認待ち）のような多段階・継続処理において、State Memoryの設計が品質を左右する。処理の進捗フラグや中間判断結果をStateとして明示的に管理することで、エージェントの再現性・トレーサビリティを確保できる。LangGraphのGraphStateと同様の概念であり、フレームワーク横断で適用可能な設計パターン。

## アイデア

- AIエージェントのMemoryを Short-Term / Long-Term / State の3種に分類する枠組みは、LangGraphのStateやLangMemoryの設計思想と対応しており、フレームワーク非依存の設計語彙として有用
- State → Think → Act → Observe のループ構造はReActパターンの明示的な状態管理版であり、done フラグによるループ終了条件の外在化が実装上の再現性を高める
- Semantic KernelのKernel Functionと FunctionChoiceBehavior.Auto の組み合わせにより、LLMが状況に応じて関数を自律選択する構造は、ハーネス設計における「道具の提供と選択の委譲」パターンの具体例

## 前提知識

- **Semantic Kernel** (TODO: 読むべき)
- **Function Calling** → /deep_47 LLM SDKを基礎から理解する 第4回：ツール呼び出し（Function Calling）編
- **RAG** → /deep_5 Google Research at The Check Up: ヘルスケアAIの最新研究成果と実臨床への展開（2026年）
- **ステートレスLLM** (TODO: 読むべき)
- **ReAct** → /deep_1 Agent SkillにReactアプリを同梱するSkill Appアーキテクチャの実装

## 関連記事

- /deep_1192 AIが中小オンラインセラーの商品開発を変える——AlibabのAccioが示す調達エージェントの実態
- /deep_1116 🤗 Optimum IntelとfastRAGによるCPU最適化エンベディング
- /deep_1334 製造業向けRAGシステムのアクセス制御設計
- /deep_861 蒸留モデルとは何か？ - DeepSeek R1の登場から1年で振り返るLLM知識蒸留の仕組みと実力
- /deep_112 知識ベースを自然淘汰するRAG「Darwin RAG」をつくってみた

## 原文リンク

[AIエージェントはなぜ覚えられるのか｜Memoryで理解する状態を持つLLM](https://zenn.dev/startspace/articles/3c6fb5e7d0b169)
