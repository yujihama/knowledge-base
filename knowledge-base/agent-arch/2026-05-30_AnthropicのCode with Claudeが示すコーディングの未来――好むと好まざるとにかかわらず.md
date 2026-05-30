---
title: "AnthropicのCode with Claudeが示すコーディングの未来――好むと好まざるとにかかわらず"
url: "https://www.technologyreview.com/2026/05/21/1137735/anthropics-code-with-claude-showed-off-codings-future-whether-you-like-it-or-not/"
date: 2026-05-30
tags: [Claude Code, マルチエージェント, Dreaming, Claude Managed Agents, 自律コーディング, プルリクエスト自動生成, LLM-as-developer]
category: "agent-arch"
related: [5496, 4753, 6745, 4520, 6126]
memo: "[MIT Technology Review AI] Anthropic’s Code with Claude showed off coding’s future—whether you like it or not"
processed_at: "2026-05-30T21:18:26.709909"
---

## 要約

2026年5月19日、AnthropicはロンドンでCode with Claudeを開催した。同日にGoogle I/Oが開催されたが、同社スタッフは偶然の一致と説明している。イベントの冒頭、AnthropicエンジニアのJeremy Hadfield氏が「先週、Claudeが完全に書いたプルリクエストを出荷した人」と聴衆に問いかけると、満員の会場の約半数が挙手した。さらに「コードを一切読まずに出荷した人」という問いにも、ほとんどの手が下がらなかった。Claude CodeのトップBoris Cherny氏は基調講演で、「デフォルトは『Claudeにプロンプトを送る』ではなく、『Claudeが自分自身にプロンプトを送る』になった」と述べ、AIによる自律的なコード生成・修正・テストのループを推進する方針を明示した。エンジニアのRavi Trivedi氏はこれを「Let it cook（Claudeに任せる）」と表現し、エラーメッセージを人間が見る前にClaude自身が検知・修正するモデルを目指すと説明した。新機能「Dreaming」はClaude Managed Agents（クラウドベースのマルチエージェント基盤）の機能として発表されており、エージェントがタスクに関するメモを記録・保存し、後続エージェントが同じコードベースを扱う際にその知見を再利用できる仕組みである。Dreamingはこれらのメモを横断的に読み込み、パターンや共通エラーを抽出して、エージェントの継続的な学習を支援する。登壇企業にはSpotify、Delivery Hero、Lovable、Base44、Monday.comが含まれ、いずれもClaude Codeを中心に開発体制を再構築した事例を紹介した。一方、会場外では懸念の声も上がっており、Reddit・Hacker Newsでは「AIが生成したコードを管理職がそのまま通すことで、レビュー負荷が増大している」「AI依存でコーディング能力が低下した」「生成コードにセキュリティ脆弱性が混入しやすい」といった批判が出ている。Claudeエンジニアリングリードのkatelyn Lesse氏は「従来のソフトウェア開発のベストプラクティスは今も有効」と強調しつつ、Anthropic社内の技術マネージャーが急増するコード量の把握に疲弊していることも認めた。同氏はClaudeの実力を「現状ではミドルレベルのエンジニア程度」と位置づけ、システム設計や難問のトラブルシューティングには依然として上級エンジニアが必要だと述べた。製品リードのAngela Jiang氏は「最終的にはClaudeがClaude自体をビルドできる状態を目指している」と語った。監査エージェント開発への示唆として、Dreamingのようなエージェント間知識共有メカニズムは、監査ワークフローにおける過去の判断ログや例外パターンの引き継ぎに直接応用可能であり、LangGraphベースのマルチエージェント設計においても参照すべきアーキテクチャパターンである。

## アイデア

- Dreamingは複数エージェントが同一コードベースで作業した際のメモを横断集約し、パターン・共通エラーを抽出する仕組みで、エージェント間の非同期知識継承を実現する点が新しい
- 『Claudeが自分自身にプロンプトを送る』という自己ループ型の自律修正モデルは、人間のレビューを前提としないCI/CDパイプラインの設計思想を根底から変える可能性がある
- 会場内の熱狂と会場外（Hacker News等）の批判の乖離が示す通り、AIコーディングの普及速度に対してレビュー文化・セキュリティ実践が追いついていないという制度的ギャップが顕在化している

## 前提知識

- **Claude Code** → /deep_3 Claude Code のAIチームでLLMの品質を自動でチェックする方法
- **マルチエージェントシステム** → /deep_628 Mimosaフレームワーク：科学研究向け進化型マルチエージェントシステム
- **プルリクエスト** → /deep_1665 Hugging Face Hubにプルリクエストとディスカッション機能が追加
- **LLMによるコード生成** (TODO: 読むべき)
- **自律エージェントループ** (TODO: 読むべき)

## 関連記事

- /deep_5496 記憶を持ったAIが次に記憶を整理しはじめた：AnthropicのDreamingとOutcomesの設計
- /deep_4753 限界ClaudeCodeユーザーがoh-my-claudecodeを調べてみた：マルチエージェント実行フレームワークの全貌
- /deep_6745 自律AIエージェントの並列実装設計 — 並列度を上げて壊れた話と回避策
- /deep_4520 社内向けAIアシスタントを3か月間試験運用してみた（松尾研究所mbot事例）
- /deep_6126 無料GPUでAI論文を自動復元する——FeynmanとColab-MCPで研究パイプラインを構築した

## 原文リンク

[AnthropicのCode with Claudeが示すコーディングの未来――好むと好まざるとにかかわらず](https://www.technologyreview.com/2026/05/21/1137735/anthropics-code-with-claude-showed-off-codings-future-whether-you-like-it-or-not/)
