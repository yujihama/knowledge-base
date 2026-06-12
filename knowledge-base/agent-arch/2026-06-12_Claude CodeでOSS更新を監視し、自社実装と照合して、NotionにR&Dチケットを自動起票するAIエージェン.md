---
title: "Claude CodeでOSS更新を監視し、自社実装と照合して、NotionにR&Dチケットを自動起票するAIエージェント"
url: "https://zenn.dev/team_nishika/articles/ce4bedfa021726"
date: 2026-06-12
tags: [Claude Code, routine, Notion MCP, マルチエージェント, パイプライン, OSS監視, 自動起票, cron, 疎結合設計, HuggingFace]
category: "agent-arch"
related: [3, 4753, 6745, 4520, 6126]
memo: "[Zenn LLM] Claude CodeでOSS更新を監視し、自社実装と照合して、NotionにR&Dチケットを自動起票するAIエージェント"
processed_at: "2026-06-12T09:06:31.206258"
---

## 要約

NishikaのCTOが構築した、OSS更新を自動監視してNotionにR&Dチケットを自動起票するマルチエージェントパイプラインの設計と運用知見。Claude Codeのroutine機能（/scheduleで作成するクラウド上のcron定期実行エージェント）とNotion MCPだけを使い、追加インフラゼロで実現している。

パイプラインは2系統。①既存依存OSSの追跡（Whisper系等）は3層構成：月次のDependency Profile Refresh（自社repoをgrepして「何をどう使っているか」をNotionページに書き出す）、週次のWeekly Digest（上流repoの直近7日変更を🔴/🟡/🟢でtriage）、週次のTicketing（digestを読み自社実装と照合してチケット起票）。②Capability Discovery（毎週日曜）はHuggingFace HubとGitHubを横断し、まだ使っていないOSS・モデルを発掘してPoCチケットを起票する。

設計の核は「Notionページをエージェント間の共有メモリにする」こと。各routineは独立したゼロコンテキストのセッションで起動するため、前段が書いたNotionページを後段が動的検索して読む構造になっている。前段のdigestが失敗しても起票側は前週分で動け、遅延の事実を成果物に記録する疎結合設計を採用。

チケット品質のガードレールとして、(a)起票前にNotionのDBスキーマとテンプレートを毎回読み込む、(b)既存Backlog/In Progressチケットとの重複チェック、(c)書き込み範囲を「目的」セクションの概要・PR根拠・期待効果の3項目のみに限定し他セクションは人間に委ねる、(d)「該当なければチケットゼロでよい」をプロンプトに明記してノイズ抑制、の4点を設ける。

クラウド実行特有のハマりどころとして、GitHub APIのunauth rate limit（60req/h）枯れ問題はsourcesでrepoをcloneしてローカルgitで読む設計に変更することで回避。HuggingFace WAFによるデータセンターIPの403弾きはHF_TOKENの生存確認を実行冒頭に入れ、失敗時はHFセクションをスキップして申告させる部分故障設計で対処。Notionダウン時はプロンプト末尾に埋め込んだProfileスナップショットを使う。「黙って劣化するのではなく、劣化したことを記録させる」が無人実行エージェントの設計原則として強調されている。

実際のチケットにはファイルパス・行番号レベル（app/whisper.py:368等）で自社コードの対象箇所と根拠PRが構造化されており、月曜朝に人間がやるのは優先度付けのみという運用を実現している。監査エージェント開発への示唆：複数エージェントが同一DBに書き込む際の重複排除ロジック、Notionをエージェント間通信バスとして使うパターン、部分故障時の劣化モード設計は、監査ワークフロー自動化にそのまま転用できる構造。

## アイデア

- 「エージェントに読ませるための自社コンテキストを別のエージェントが整備する」再帰構造：月次Profileエージェントが実コードから自動生成するドキュメントは人間が手で書くものと違い腐らないという設計思想
- Notionページをエージェント間の共有メモリ兼人間が読める週報として二重活用し、中間生成物を見ればどの層で判断が誤ったか分かるデバッグログとナレッジが同一物になる設計
- 「チケットゼロを明示的に許可する」プロンプト記法：LLMの「何か出力しなければ」という圧力を抑制してノイズ低減に効果的という実運用知見

## 前提知識

- **Claude Code routine** → /deep_3089 LLM WikiとClaude Code Routinesで「毎朝Slackに届く自分専用Digest」を作った
- **Notion MCP** (TODO: 読むべき)
- **マルチエージェントパイプライン** (TODO: 読むべき)
- **cron式** (TODO: 読むべき)
- **GitHub Actions / ローカルgit** (TODO: 読むべき)

## 関連記事

- /deep_3 Claude Code のAIチームでLLMの品質を自動でチェックする方法
- /deep_4753 限界ClaudeCodeユーザーがoh-my-claudecodeを調べてみた：マルチエージェント実行フレームワークの全貌
- /deep_6745 自律AIエージェントの並列実装設計 — 並列度を上げて壊れた話と回避策
- /deep_4520 社内向けAIアシスタントを3か月間試験運用してみた（松尾研究所mbot事例）
- /deep_6126 無料GPUでAI論文を自動復元する——FeynmanとColab-MCPで研究パイプラインを構築した

## 原文リンク

[Claude CodeでOSS更新を監視し、自社実装と照合して、NotionにR&Dチケットを自動起票するAIエージェント](https://zenn.dev/team_nishika/articles/ce4bedfa021726)
