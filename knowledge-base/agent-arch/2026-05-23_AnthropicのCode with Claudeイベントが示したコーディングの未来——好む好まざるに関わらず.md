---
title: "AnthropicのCode with Claudeイベントが示したコーディングの未来——好む好まざるに関わらず"
url: "https://www.technologyreview.com/2026/05/21/1137735/anthropics-code-with-claude-showed-off-codings-future-whether-you-like-it-or-not/"
date: 2026-05-23
tags: [Claude Code, Dreaming, コーディングエージェント, 自律エージェント, Anthropic, エージェントメモリ, LLMコード生成]
category: "agent-arch"
related: [2688, 764, 2541, 2205, 3504]
memo: "[MIT Technology Review AI] Anthropic’s Code with Claude showed off coding’s future—whether you like it or not"
processed_at: "2026-05-23T12:00:41.834073"
---

## 要約

2026年5月19日、AnthropicはロンドンでCode with Claudeという2日間の開発者向けイベントを開催した。同日にGoogle I/Oが開催されたが、Anthropicスタッフは偶然の一致と説明している。

イベントの冒頭、AnthropicエンジニアのJeremy Hadfieldが「先週、Claudeが完全に書いたPRをマージした人は？」と問うと、会場の約半数が挙手。さらに「コードを一切読まずにマージした人は？」という問いにも、多くの手が下がらなかった。Hadfieldは「Anthropicのソフトウェアのほとんどは今やClaudeが書いており、Claude Code自体のコードの大半もClaudeが書いた」と述べた。OpenAI・Google・Microsoftも同様の主張をしている。

Claude Codeの責任者Boris Chernyは基調講演で「デフォルトが『Claudeにプロンプトを送る』ではなく、『ClaudeがClaudeにプロンプトを送る』になった」と宣言。人間が一切エラーメッセージを見ることなく、Claudeが自律的にテスト・修正を繰り返すことを目標としている。

注目の新機能として「Dreaming（夢想）」が紹介された。これはClaude Codeエージェントが特定タスクに関するメモを記録・保存し、後続エージェントがそのメモを参照して素早く文脈を把握し、過去のエラーから学習できる仕組みだ。Dreamingシステムはこれらのメモを横断的に読み込み、パターンや共通の問題点を整理することで、特定のコードベースに対するClaude Codeの精度を継続的に向上させる。

イベントにはSpotify、Delivery Hero、Lovable、Base44、Monday.comなどが登壇し、Claude Codeを軸に開発体制を再構築した事例を共有した。

一方、会場外では懸念も広がっている。RedditやHacker Newsでは「AIツールはマネージャーが生産性向上を追い求めて導入しているが、実際には確認すべきコードが増えて開発が難しくなっている」という声が上がる。またAIに依存することで自身のコーディング能力が低下しているという報告や、生成コードのセキュリティ脆弱性を警告する研究者の声もある。

Claude engineering leadのKatelyn Lesseは「旧来のソフトウェア開発のベストプラクティスは依然として有効であり、ただそれを見失っているチームが多い」と語った。また「現時点でClaudeはミッドレベルエンジニア程度のコード品質を持つ」と評価し、システム設計や困難な問題解決には専門家が必要としつつも、将来的にはそれらも担えるよう改善を目指すと述べた。Claude product leadのAngela Jiangは「最終的にはClaudeがClaudeをビルドできる状態を目指している」と明言した。

監査エージェント開発への示唆：Dreamingのような「エージェントが自らのメモを蓄積し、後続エージェントが学習する」アーキテクチャは、監査エージェントが過去の監査手続きや発見事項をナレッジとして蓄積・再利用する設計に直接応用可能。また「人間がエラーを見ない」レベルの自律実行は、監査証跡の設計や人間の監督義務と緊張関係を生じさせる点にも注意が必要。

## アイデア

- Dreamingは複数エージェントが同一コードベースを継続的に改善するための「共有メモリ・知識蒸留」機構であり、マルチエージェントシステムにおける知識継承の実装例として参考になる
- 「ClaudeがClaudeにプロンプトする」という自己駆動型コーディングループは、ReActパターンの延長として捉えられ、エージェントのself-correctionとself-evaluationを生産コードレベルで実現している
- 生成コードを人間がレビューしないまま本番マージするケースが増加しており、ソフトウェア開発における人間の監督義務とAI自律化のバランスが今後の規制・ガバナンス議論の焦点になる

## 前提知識

- **Claude Code** → /deep_3 Claude Code のAIチームでLLMの品質を自動でチェックする方法
- **自律エージェント** → /deep_17 AI vs. アンチボット：LLMが書き換えるウェブスクレイピングの全ルール
- **ReAct** → /deep_1 Agent SkillにReactアプリを同梱するSkill Appアーキテクチャの実装
- **マルチエージェントメモリ** (TODO: 読むべき)
- **LLMコード生成** → /deep_19 LLMのコード生成はなぜ同じミスを繰り返すのか — 失敗を「演算子」にして生成過程を書き換える

## 関連記事

- /deep_2688 自分のバージョンアップを自分で書く — embodied-claude v0.2「Social and scripted」
- /deep_764 生成しながら実行する：LLMコード生成における実行レイテンシの隠蔽
- /deep_2541 なぜLLM AIにはリファクタリングを「委任」してはいけないのか？
- /deep_2205 なぜAnthropicは軍と戦う？1億ドルPartner NetworkとAI研究所の全貌
- /deep_3504 harness engineering を5層で整理する — Pythonで1から書いて見えたこと

## 原文リンク

[AnthropicのCode with Claudeイベントが示したコーディングの未来——好む好まざるに関わらず](https://www.technologyreview.com/2026/05/21/1137735/anthropics-code-with-claude-showed-off-codings-future-whether-you-like-it-or-not/)
