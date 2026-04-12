---
title: "Zettelkastenに基づくLLMエージェントのメモリ設計：A-Mem論文解説"
url: "https://zenn.dev/tsurubee/articles/amem-llm-agent-memory-design"
date: 2026-04-10
tags: [A-Mem, Zettelkasten, LLMエージェント, メモリアーキテクチャ, MCP, RAG, MemGPT, マルチホップ推論, NeurIPS2025]
category: "agent-arch"
memo: "[Zenn LLM] Zettelkastenに基づくLLMエージェントのメモリ設計：A-Mem論文解説"
processed_at: "2026-04-10T21:04:05.809380"
---

## 要約

本記事は、NeurIPS 2025採択論文「A-Mem: Agentic Memory for LLM Agents」（Xu et al.）を解説する。LLMエージェントの長期記憶には外部メモリが不可欠だが、MemGPT・MemoryBank・Mem0などの既存手法には3つの共通課題がある：①操作の固定性（ワークフローが事前設計されエージェントが柔軟に変えられない）、②接続の欠如（メモリ同士の意味的リンクを自動生成できない）、③構造の静的さ（既存メモリが新知識追加で更新されない）。A-Memはドイツの社会学者ルーマンが開発したZettelkasten（原子性・リンキング・進化の3原則）をLLMで自律実装することでこれらを解決する。アーキテクチャは4コンポーネント構成：(1)Note Construction——対話記録からLLMがKeywords・Tags・Contextを自動生成し構造化ノートとして保存、(2)Link Generation——新ノート追加時にall-MiniLM-l6-v2の埋め込みでtop-k候補を絞り込み、LLMが因果・対比・上位下位関係を識別してリンクを形成、(3)Memory Evolution——リンク先の既存メモリのContext・Keywords・Tagsを新メモリとの関係を踏まえ書き換え、(4)Memory Retrieval——ベクトル検索でtop-kを取得後、リンクで接続されたボックス内メモリを芋づる式に引き出す。評価はLoCoMo（平均9Kトークン・最大35セッション・7,512 QAペア）とDialSim（Friends等3作品・1,300セッション・約350,000トークン）の2データセットでGPT-4o-miniほか6モデルを使用。特にMulti-Hop F1スコアでGPT-4o使用時にA-Memが32.86と他手法を上回り、リンク構造による関連メモリの連鎖取得の効果が顕著。Ablation StudyではLink GenerationとMemory Evolutionが相補的に機能することが確認された。スケーリング面では100万件でも検索時間3.70μsと実用的。実装はPythonライブラリとして公開されており、Claude CodeとはA-MemのAPIをMCPサーバーでラップしsave_memory/search_memoryツールとして公開する統合が自然な形として提案されている。

## アイデア

- メモリ側にもLLMを持たせ、書き込みをトリガーに既存メモリのContextやTagsを自律的に書き換える『Memory Evolution』は、人間の学習プロセス（新知識取得による既存理解の変化）をシステム化した点が独創的
- 埋め込みベクトルでtop-k候補を絞り込んでからLLMで因果・対比・概念階層などの意味的関係を識別する2段階リンク生成は、コストと精度のトレードオフを合理的に解決している
- リンクで接続されたメモリを『ボックス』として管理し検索時に芋づる式取得する設計により、直接類似しないが文脈的に関連する情報をマルチホップ推論で活用できる

## Yujiの取り組みへの示唆

LangGraphで構築中の監査エージェントにA-MemをMCPサーバー経由で統合することで、監査手続の実行履歴・発見事項・判断根拠をZettelkasten的に相互リンクさせた長期メモリ層を実装できる。特にMulti-Hop推論での強みは、複数の内部統制上の事象を横断して根本原因を特定するシナリオ（例：A部門の異常→B取引→C承認者の関与を辿る）に直接応用可能。Memory Evolutionにより新たな監査発見が過去の関連メモリの文脈を更新する仕組みは、LLM-as-judgeの評価精度向上にも寄与し得る。

## 原文リンク

[Zettelkastenに基づくLLMエージェントのメモリ設計：A-Mem論文解説](https://zenn.dev/tsurubee/articles/amem-llm-agent-memory-design)
