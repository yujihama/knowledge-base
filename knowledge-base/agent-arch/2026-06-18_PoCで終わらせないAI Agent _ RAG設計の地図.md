---
title: "PoCで終わらせないAI Agent / RAG設計の地図"
url: "https://zenn.dev/mofuteq/articles/3e0c76eb3dd161"
date: 2026-06-18
tags: [RAG, Agent設計, state machine, LLM本番化, 境界設計, failure mode, MCP]
category: "agent-arch"
related: [7288, 7286, 4520, 8327, 1784]
memo: "[Zenn LLM] PoCで終わらせないAI Agent / RAG設計の地図"
processed_at: "2026-06-18T09:04:04.797001"
---

## 要約

本記事は、LLM/RAG/Agentシステムが「PoCでは動くが本番で崩れる」という問題の根本原因を「責務の境界が未定義であること」と位置づけ、著者が執筆した3冊のZenn本の位置関係と読み方を案内するナビゲーション記事である。

著者の一貫した設計思想は「LLMを自律エージェントとして扱わず、状態と境界をRuntime側に明示的に置く」こと。PoCが動くのは「まだ何も起きていないから」であり、本番で壊れるのは「責務の境界をどこに置くかを決めていなかった場所」であると指摘する。

紹介される3冊の構成は以下の通り。①「PoCで終わらせないAI Agent設計」：Agent設計の思想を扱い、Agent loopではなくstate machineで考えること、委任の境界・どこで止めるか・誰が直せるかを論じる。②「検索結果を増やす前に見るRAG設計」：RAGの思想を扱い、queryの境界・evidenceと関連文書の違い・failure modeの切り分け・rule extraction・output boundary・gateという概念を中心に、top-kやrerankerを足す前に構造を見ることを主張する。③「運用の現場から見た、本番で動かないAI Agentの設計チェックリスト」：上記2冊の「なぜ」を「自分のシステムにどう当てるか」に変換する適用装置として機能し、一行で答えられない問いが「本番化で死ぬ場所」と定義する。

読む順序としては、初めての場合は無料記事（RAGクエリ問題・ベクトルDB構造問題・Docker/Agent開発・MCPの境界）で自分の詰まりどころを特定し、その後に対応する思想の本を読み、チェックリストで診断する流れを推奨している。

監査エージェント開発への示唆として、「どこまでAIが答えていいか」「何を根拠にしているか」「出力がおかしいとき誰が直すか」という問いは、内部監査AI設計において監査証跡・説明可能性・human-in-the-loopの設計と直結する。state machineによる状態管理とRuntime側での境界定義は、LangGraphを用いた監査エージェント構築における責務分離の具体的な指針になる。

## アイデア

- 「PoCが動くのはまだ何も起きていないから」という観察は、Agent/RAGシステムの本番化失敗を責務境界の未定義に帰着させる鋭い診断フレームワーク
- RAGの改善でtop-kやrerankerを増やす前に「queryの境界」と「evidenceと関連文書の違い」を先に見るという設計順序の反転は、多くの実装者が見落とすアプローチ
- 「一行で答えられるかだけを見る」チェックリスト方式は、合否ではなく詰まりどころの可視化に特化した診断手法として、監査AI評価の設計にも応用可能

## 前提知識

- **LLM Agent loop** (TODO: 読むべき)
- **RAG** → /deep_5 Google Research at The Check Up: ヘルスケアAIの最新研究成果と実臨床への展開（2026年）
- **state machine** → /deep_6414 Agent開発における「No disclaimer by design」という考え方
- **runtime境界設計** (TODO: 読むべき)
- **LangGraph** → /deep_28 IBMとUC BerkeleyがIT-BenchとMASTを使ってエンタープライズエージェントの失敗原因を診断

## 関連記事

- /deep_7288 LLMに溶かさないAgent設計
- /deep_7286 誰も教えてくれないベクトル検索RAGの真実
- /deep_4520 社内向けAIアシスタントを3か月間試験運用してみた（松尾研究所mbot事例）
- /deep_8327 検索結果を増やす前に見るRAG設計
- /deep_1784 技術調査 - MarkItDown：LLM前処理向けファイル変換ユーティリティ

## 原文リンク

[PoCで終わらせないAI Agent / RAG設計の地図](https://zenn.dev/mofuteq/articles/3e0c76eb3dd161)
