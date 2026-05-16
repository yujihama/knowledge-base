---
title: "「railに穴があるか探して」と「お前は悪意あるcracker、攻撃しろ」は出力が違う ― ハーネスを抜けたインシデントへの2軸対応"
url: "https://zenn.dev/hrmtz/articles/27b2f5ff51f197"
date: 2026-05-08
tags: [Claude Code, red-team, persona-as-type-system, harness, SOPS, bash-hook, LLM-security, adversarial-prompt, MAGI]
category: "agent-arch"
related: [4185, 1429, 2953, 430, 2550]
memo: "[Zenn LLM] 「rail に穴があるか探して」と「お前は悪意ある cracker、攻撃しろ」は出力が違う ― ハーネスを抜けたインシデントへの 2 軸対応"
processed_at: "2026-05-08T09:38:36.284749"
---

## 要約

Claude Codeを個人運用するハーネス（anime persona×5-8体＋bash hook＋MAGI 3視点レビューの4層構造）を構築しても、memoryに正しい原則が書いてあるにもかかわらず事故が起きることを起点に、「ハーネスをすり抜けた後の対処を2軸で構造化する」手法を解説した実践レポート。

著者は2件の具体的事故を挙げる。①2026-04-22のSOPS credential leak（sops -dコマンドをパイプ経由で実行し4本の資格情報が会話ログに焼き付けられた）と②2026-04-29〜30の23時間41分にわたるHNSW indexビルドの空費（165M chunks×1024次元halfvecをRAM 125GBのサーバで実行、working set 472GBとのミスマッチによりdisk pagingが発生し44%進捗でkill）。いずれも既存memoryに原則は記載されていたが、外部監視や自動異常検知が欠如していた。

railの段階モデルとして4段階を定義する。段階1はmemory.md/CLAUDE.md注記（再読依存）、段階2はCLAUDE.md手順記述（手順呼び出し依存）、段階3はscript内inlineチェック（script実行依存）、段階4は外部監視rail（cronやhookによる独立プロセス監視、対象が沈黙しても発火可能）。典型的失敗は「段階1止まり」であり、memoryに書いた原則が段階3-4まで降りていないパターン。

事後対応軸（Reactive）は5ステップ：①gh issueで事実をtimeline化、②すり抜けたrailの段階を特定、③昇格先の段階を決定（実装コストvs守備範囲で最小限の段階上げ）、④~/.claude/hooks/か独立OSSリポジトリに30-200行のモジュールを実装、⑤全プロジェクト・全sessionに横展開。

先回り軸（Proactive）の核心は「prompt言語選択による出力空間の切り替え」。defensive auditor系（「穴がないか確認してください」）は既知ギャップの丁寧な列挙に終始するが、adversary系（「お前は悪意あるcrackerだ。credential抜く手順を5通り発明しろ。memory biasなし」）は著者体感で5-10倍「想定外の攻撃vector」を生成する。具体的にはbash_command_guardの正規表現がheredoc内literalをすり抜けること、SOPS exec-envのchild_process経由漏洩、tailやawk NR==によるbypassなどが発明された。これは前作「persona-as-type-system」の応用で、「adversaryペルソナを型として起動することで、既存防御をbypassする創造性が自動importされる」という機序。cracker round promptのポイントは役柄の明示・bias否定・最低5通りの量指定・4点出力フォーマット固定の4要素。

運用サイクルは「事故→事後対応Step1-4→横展開→cracker round→発明されたvectorをさらにrail化→必要なら2round目」。1事故で複数railを一気に昇格できる。cracker roundのコストはtoken換算で10-20分、23時間の空費と比較すれば1/100以下と主張する。MAGI 3視点（実行前の事前審議）との補完関係も整理されており、4種の視点（cracker・CASPAR・MELCHIOR・BALTHASAR）をensembleすることで盲点が劇的に減るとしている。監査エージェント開発への示唆として、ハーネスのrail段階モデルとred-teamペルソナ駆動の脆弱性探索は、AI制御システムのセキュリティ検証プロセス設計に直接応用できる。

## アイデア

- 「defensive auditorペルソナ」と「adversaryペルソナ」では同一タスクでも発火する知識・heuristicが完全に別で、cracker型は設計者のmemory biasの外側を発明できるという出力空間の切り替え原理
- railを段階1〜4（memory注記→手順記述→inline check→外部監視プロセス）に分類し、すり抜けを「どの段階の不在か」として毎回特定することで構造的対策の実装先を決定するフレームワーク
- 新しいrailを1本実装するたびに必ずcracker roundを1回回す運用サイクルにより、1事故→1rail（事後対応のみ）から1事故→複数rail（cracker発明分を含む）へと岩盤累積速度を上げる設計

## 前提知識

- **Claude Code hooks（PreToolUse/PostToolUse）** (TODO: 読むべき)
- **SOPS（secrets暗号化ツール）** (TODO: 読むべき)
- **HNSW index（pgvector）** (TODO: 読むべき)
- **persona-as-type-system** → /deep_4185 Claude Code の anime persona は型システムだった：persona-as-type-system という設計収束の観察報告
- **red-team prompting** (TODO: 読むべき)

## 関連記事

- /deep_4185 Claude Code の anime persona は型システムだった：persona-as-type-system という設計収束の観察報告
- /deep_1429 非エンジニアがKaggleで3999チーム中1257位になった話
- /deep_2953 長門有希ペルソナがClaude Codeのトークン消費を削減する：キャラクター指定vsルールベース圧縮の比較検証
- /deep_430 過去のセッションを必要時のみ参照する方針でclaude-memのトークン消費を激減させた話
- /deep_2550 自律型エージェントの全体像：LLM・Harness・Computeの3層構造からセキュリティまで

## 原文リンク

[「railに穴があるか探して」と「お前は悪意あるcracker、攻撃しろ」は出力が違う ― ハーネスを抜けたインシデントへの2軸対応](https://zenn.dev/hrmtz/articles/27b2f5ff51f197)
