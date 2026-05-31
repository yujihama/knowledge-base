---
title: "AnthropicのCode with Claudeが示すコーディングの未来：好むと好まざるとにかかわらず"
url: "https://www.technologyreview.com/2026/05/21/1137735/anthropics-code-with-claude-showed-off-codings-future-whether-you-like-it-or-not/"
date: 2026-05-31
tags: [Claude Code, マルチエージェント, Dreaming, Claude Managed Agents, 自律コーディング, AIエージェント]
category: "agent-arch"
related: [5496, 6126, 2215, 1245, 4753]
memo: "[MIT Technology Review AI] Anthropic’s Code with Claude showed off coding’s future—whether you like it or not"
processed_at: "2026-05-31T09:16:30.875594"
---

## 要約

2026年5月19日、AnthropicはロンドンでCode with Claudeと題した2日間の開発者向けイベントを開催した。会場では登壇者のJeremy Hadfield（Anthropicエンジニア）が「過去1週間でClaudeが完全に書いたPRをshipした人は？」と問うと半数近くが挙手し、さらに「コードを一切読まずにshipした人は？」という問いにも多くの手が残った。AnthropicのBoris Cherny（Claude Codeトップ）は基調講演で「デフォルトは『Claudeにプロンプトを送る』ではなく、『Claudeに自分自身へプロンプトさせる』ことだ」と述べ、エラーメッセージの処理や修正ループを含めた完全自律型のコーディングを目指す方針を明示した。新機能「Dreaming」はClaude Managed Agents（マルチエージェントシステム構築・実行のためのクラウド基盤、2週間前に発表）に組み込まれており、Claudeエージェントが特定タスクについてメモを記録・保存し、同じコードベースを扱う後続エージェントがそのメモを参照して学習・エラー回避を行う仕組み。複数エージェントのメモを横断的に整理してパターンや共通課題を抽出することで、コードベースへの習熟を加速させる。Spotify、Delivery Hero、Lovable、Base44、Monday.comなど複数企業がClaude Codeを中心に開発チームを再編した事例が紹介された。一方、カンファレンス外ではRedditやHacker Newsを中心に批判的な声もある。「生成されたコードが問題ないと言っているのはそれを読んでいない人だけだ」という指摘や、AI依存によるコーディング能力低下、安全でないコードによるセキュリティリスクの拡大が懸念されている。Claude engineering leadのKatelyn Lesseは「古いソフトウェア開発のベストプラクティスは今も有効。それを見失っているチームが多い」と述べた上で、「現時点でClaudeはミッドレベルエンジニア程度のコード品質」と評価。Claude product leadのAngela Jiangは「最終的な目標はClaudeが自分自身をビルドできるようになること」と語った。監査エージェント開発への示唆として、Dreamingのようなエージェント間知識共有機構（タスク固有ノートの記録・再利用）はLangGraphベースのマルチエージェント監査パイプラインにも応用可能であり、過去の調査ログや判断メモを後続エージェントに引き渡すメモリ設計パターンとして参照価値が高い。

## アイデア

- Dreamingはエージェント間の非同期知識伝播機構であり、タスク固有メモの蓄積とパターン抽出を組み合わせることでコードベース習熟を自律的に加速させる点が設計として興味深い
- 「Claudeに自分自身へプロンプトさせる」という自己ループ型の自律実行モデルは、人間のレビューレイヤーを省いたエンドツーエンドの品質保証をエージェント内部で完結させる方向性を示している
- PRをコードを読まずにshipするという実態は、AIコーディングツールのリスクが技術的品質ではなく組織的ガバナンス（誰がどこまでレビューするか）の問題にシフトしていることを示唆する

## 前提知識

- **Claude Code** → /deep_3 Claude Code のAIチームでLLMの品質を自動でチェックする方法
- **マルチエージェントシステム** → /deep_628 Mimosaフレームワーク：科学研究向け進化型マルチエージェントシステム
- **Pull Request** → /deep_6296 AnthropicのCode with Claudeイベントが示したコーディングの未来——好むと好まざるとにかかわらず
- **LLM自律エージェント** (TODO: 読むべき)
- **コード生成LLM** → /deep_1052 RTX 4080で挑む強化学習コードLLM — 実行フィードバックで1.5Bモデルを鍛える全記録

## 関連記事

- /deep_5496 記憶を持ったAIが次に記憶を整理しはじめた：AnthropicのDreamingとOutcomesの設計
- /deep_6126 無料GPUでAI論文を自動復元する——FeynmanとColab-MCPで研究パイプラインを構築した
- /deep_2215 Claudeの指示に従ったらGitHub・Hacker News・RedditでBANされた話
- /deep_1245 AIエンジニアリング進化の系譜 — 第4の波「Authority Engineering」とは何か
- /deep_4753 限界ClaudeCodeユーザーがoh-my-claudecodeを調べてみた：マルチエージェント実行フレームワークの全貌

## 原文リンク

[AnthropicのCode with Claudeが示すコーディングの未来：好むと好まざるとにかかわらず](https://www.technologyreview.com/2026/05/21/1137735/anthropics-code-with-claude-showed-off-codings-future-whether-you-like-it-or-not/)
