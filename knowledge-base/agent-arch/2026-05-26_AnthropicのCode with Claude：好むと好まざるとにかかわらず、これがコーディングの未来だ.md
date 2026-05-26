---
title: "AnthropicのCode with Claude：好むと好まざるとにかかわらず、これがコーディングの未来だ"
url: "https://www.technologyreview.com/2026/05/21/1137735/anthropics-code-with-claude-showed-off-codings-future-whether-you-like-it-or-not/"
date: 2026-05-26
tags: [Claude Code, AIコーディング, dreaming機能, 自律エージェント, マルチエージェント, プルリクエスト自動化, Anthropic]
category: "agent-arch"
related: [4753, 5160, 2688, 4520, 6126]
memo: "[MIT Technology Review AI] Anthropic’s Code with Claude showed off coding’s future—whether you like it or not"
processed_at: "2026-05-26T09:17:49.881267"
---

## 要約

2026年5月19日、AnthropicはロンドンでCode with Claudeと題した2日間の開発者向けイベントを開催した。同日にGoogleがI/Oを開催したことは偶然とのことだが、タイミングの競合が象徴するようにAIコーディングの主導権争いは激化している。

イベントの冒頭、AnthropicエンジニアのJeremy Hadfieldが「先週、Claudeが完全に書いたプルリクエストをShipした人は？」と問いかけると、会場の約半数が挙手した。さらに「コードをまったく読まずにShipした人は？」との問いにも、多くの手が下がらなかった。これはAIコーディングが単なる補助ツールから、主要な開発主体へと移行しつつあることを如実に示している。

Claude Code責任者のBoris Chernyはキーノートで「デフォルトが『Claudeにプロンプトを送る』ではなく、『Claudeが自らにプロンプトを送る』になった」と述べ、人間の介入を最小化した自律的なコーディングループを目指す方針を明示した。エラーメッセージはClaude自身が処理し、テストと修正を繰り返して最終的に人間の目に触れないまま問題を解決するという設計思想だ。

技術的に注目すべき新機能として「dreaming（夢想）」が発表された（2週間前に公開済み）。これはClaude Codeエージェントがタスク実行中にメモを記録・保存し、後続のエージェントがそのメモを参照して同一コードベースに素早く適応できる仕組みだ。dreamingはこれらのメモを横断的に読み込んでパターンや共通エラーを抽出・統合し、特定のコードベースに対するパフォーマンスを継続的に向上させる。マルチエージェント間の知識継承を実現するメモリ機構と言える。

イベントにはSpotify、Delivery Hero、Lovable、Base44、Monday.comなど、Claude Codeを中心に開発体制を再構築した企業が参加し、成功事例を共有した。「AnthropicのソフトウェアのほとんどはもうClaudeが書いている。Claude CodeのコードもClaudeが書いた」とHadfieldは述べた。

一方でイベント外では懸念の声も上がっている。RedditやHacker Newsでは「AIが生成したコードをレビューする手間が増え、かえって開発効率が下がる」「生成コードで問題ないと言う人はそもそもコードを読んでいない」といった批判が出ている。開発者のコーディング能力低下を懸念する声や、AIが生成するコードのセキュリティリスクを指摘する研究者の報告もある。

ClaudeエンジニアリングリードのKatelyn Lesseは「従来のソフトウェア開発のベストプラクティスは今でも有効。見失っているチームが多いだけ」と応答したが、同時にAnthropicの技術マネージャーがチームの急増するコード量の管理に疲弊していることも認めた。「現時点でClaudeはミドルレベルのエンジニアと同等の能力」とし、システム設計や難易度の高い問題解決には引き続きエキスパートエンジニアが必要との認識を示した。Claude製品リードのAngela Jiangは「最終的にClaudeが自分自身をビルドできるようにしたい」と述べ、完全自律的なソフトウェア開発を長期目標として掲げた。

## アイデア

- dreamingはマルチエージェント間のメモリ継承機構であり、監査エージェントにも応用可能。複数の監査サブエージェントが過去の調査メモを共有・統合することで、同一クライアントや制度への適応速度を向上させられる
- 「Claudeが自らにプロンプトを送る」という自己ループ型エージェントアーキテクチャは、人間のフィードバックループをなくした純粋なLLM-as-judgeの実装例として、ReActエージェントの発展形として参照価値が高い
- コードレビューの省略が常態化しつつあるという現実は、監査分野でのAI導入における承認・レビュープロセス設計に対する反面教師として機能する。AI出力の自動信頼は内部統制の観点から構造的リスクになり得る

## 前提知識

- **Claude Code** → /deep_3 Claude Code のAIチームでLLMの品質を自動でチェックする方法
- **LLMエージェント** → /deep_7 Karpathy発AutoResearchで一晩100実験を自動化する仕組みと実践
- **プルリクエスト** → /deep_1665 Hugging Face Hubにプルリクエストとディスカッション機能が追加
- **マルチエージェントメモリ** (TODO: 読むべき)
- **LLM-as-judge** → /deep_3 Claude Code のAIチームでLLMの品質を自動でチェックする方法

## 関連記事

- /deep_4753 限界ClaudeCodeユーザーがoh-my-claudecodeを調べてみた：マルチエージェント実行フレームワークの全貌
- /deep_5160 通勤中に育てたAIが、放置していたアイデアを勝手に形にした【OpenClawエージェント4体を止めるまで①】
- /deep_2688 自分のバージョンアップを自分で書く — embodied-claude v0.2「Social and scripted」
- /deep_4520 社内向けAIアシスタントを3か月間試験運用してみた（松尾研究所mbot事例）
- /deep_6126 無料GPUでAI論文を自動復元する——FeynmanとColab-MCPで研究パイプラインを構築した

## 原文リンク

[AnthropicのCode with Claude：好むと好まざるとにかかわらず、これがコーディングの未来だ](https://www.technologyreview.com/2026/05/21/1137735/anthropics-code-with-claude-showed-off-codings-future-whether-you-like-it-or-not/)
