---
title: "過去のセッションを必要時のみ参照する方針でclaude-memのトークン消費を激減させた話"
url: "https://zenn.dev/nishiken_zenn/articles/claude-mem-token-optimization"
date: 2026-04-07
tags: [claude-mem, Claude Code, MCP, トークン最適化, コンテキスト管理, settings.json, 永続メモリ]
category: "infra"
memo: "[Zenn LLM] 過去の session をほしい時に参照する方針で claude-mem のトークン消費を激減させた話"
related: [13, 51, 9, 89, 1245]
processed_at: "2026-04-07T09:10:15.190056"
---

## 要約

claude-memはClaude Codeにセッション間の永続メモリを付与するMCPツールだが、観測記録の蓄積に伴いセッション開始時の自動注入によるトークン消費が増大する問題がある。本記事では「事前の自動注入を極限まで絞り、必要な情報は都度取得する」という方針で~/.claude-mem/settings.jsonを最適化する方法を紹介する。

主要な設定変更は以下の通り。CLAUDE_MEM_CONTEXT_OBSERVATIONS=1（デフォルト50）: セッション開始時のインデックスを直近1件のみに限定。1件あたり50〜100トークンのため、50件から1件への削減だけで最大約5,000トークンの節約となる。CLAUDE_MEM_CONTEXT_FULL_COUNT=0（デフォルト0のまま）: 全文展開を完全に無効化し、詳細は都度get_observationsで取得する。CLAUDE_MEM_CONTEXT_SESSION_COUNT=1（デフォルト10）: 直近1セッション分のみ保持。CLAUDE_MEM_CONTEXT_SHOW_LAST_SUMMARY=false、CLAUDE_MEM_CONTEXT_SHOW_LAST_MESSAGE=false: 前セッションの要約・最終メッセージの自動注入を無効化。

記録のノイズ削減として、CLAUDE_MEM_SKIP_TOOLS=Read,Glob,Grep,ListMcpResourcesTool,SlashCommand,Skill,TodoWrite,AskUserQuestion を設定。Read/Glob/Grepは1セッションで数十〜数百回発火するが状態を変更しないため、除外することで観測記録の品質が向上しsearchの精度が改善する。

CLAUDE_MEM_CONTEXT_OBSERVATION_TYPES=''、CLAUDE_MEM_CONTEXT_OBSERVATION_CONCEPTS=''は表示時フィルタ（DBへの記録には無影響）であるため空文字にし、Context Indexへの自動表示をゼロにする。CLAUDE_MEM_FOLDER_CLAUDEMD_ENABLED=falseはclaude-mem側のCLAUDE.md自動生成を無効化し、Claude Code本体との重複注入を防ぐ。

この設定により、DBには全観測記録が保持されたままで、セッション開始時のトークン消費を大幅削減できる。必要な過去情報はsearch→get_observationsで明示的に取得するため、情報アクセスは一切失われない。チューニング中はSHOW_*系設定をtrueにすることで各設定項目のトークン消費量を数値で可視化できる。

## アイデア

- 「全量を事前注入するより、インデックスのみ保持して都度フェッチする」パターンはRAGのlazy retrievalと同じ思想であり、エージェントのメモリ設計全般に応用できる
- Read/Glob/Grepのような状態変化を伴わない読み取り系ツールをスキップすることで観測記録のS/N比を上げる手法は、LangGraphの観測ログ設計にも転用できる
- OBSERVATION_TYPESやCONCEPTSが表示時フィルタに過ぎずDB記録には無影響という事実をソースコード解析で確認したアプローチは、ツールの仕様を正確に把握する上でのLLM活用例として参考になる
## 関連記事

- /deep_13 SkillにアプリケーションをAgent-App共生モデルとして組み込む実装
- /deep_51 SaaSを個人開発して運営しているが、本当に「SaaS is Dead」を感じ始めている
- /deep_9 LLMに長期記憶を実装する — 脳の記憶メカニズムのPython実装
- /deep_89 Claude CodeとCodexのPlan Modeはどこに何を保存しているのか
- /deep_1245 AIエンジニアリング進化の系譜 — 第4の波「Authority Engineering」とは何か

## 原文リンク

[過去のセッションを必要時のみ参照する方針でclaude-memのトークン消費を激減させた話](https://zenn.dev/nishiken_zenn/articles/claude-mem-token-optimization)
