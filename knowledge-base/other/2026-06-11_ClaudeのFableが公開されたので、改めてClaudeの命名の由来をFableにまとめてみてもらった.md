---
title: "ClaudeのFableが公開されたので、改めてClaudeの命名の由来をFableにまとめてみてもらった"
url: "https://zenn.dev/yuzunatsuki/articles/47ec894f021602"
date: 2026-06-11
tags: [Claude, Anthropic, Fable, Mythos, 命名規則, LLM, モデル命名, Project Glasswing]
category: "other"
related: [3718, 6602, 3747, 3393, 3214]
memo: "[Zenn LLM] ClaudeのFableが公開されたので、改めてClaudeの命名の由来をFableにまとめてみてもらった"
processed_at: "2026-06-11T12:13:22.838580"
---

## 要約

AnthropicのAIアシスタント「Claude」のモデル名（Haiku、Sonnet、Opus、Fable、Mythos）の命名由来を、一次ソースに基づいて整理した記事。

「Claude」という名前自体については、情報理論の父クロード・シャノン（Claude Shannon）にちなむという説が広く流布しているが、Anthropicはこの由来を公式に確認したことは一度もない。The New Yorker誌（2026年）は「社内伝承によれば部分的にシャノンへのオマージュ」と報じているが、記事タイトル自体が「Claudeとは何か？Anthropicにも分からない」であり、由来が社内でも確定していないことを示す。

Opus・Sonnet・Haikuの詩に基づく命名については、CEOのDario AmodeiがLex Fridmanポッドキャスト第452回（2024年11月）で自ら語っており、俳句＝短い詩・ソネット＝中くらいの詩という対応を明言している。ただし公式ブログやモデルカードには詩との対応説明は記載がなく、「Opus＝magnum opus（大作）」などの語釈は第三者の解釈に留まる。Amodei自身「命名には驚くほど苦労している」とも発言している。

2026年6月9日に発表されたClaude Fable 5とClaude Mythos 5では、Anthropicが初めて公式文書の脚注で命名語源を明記した。Fableはラテン語のfabula（「語られるもの」）に由来し、ギリシャ語のmythosに近い語と説明。両モデルは同一基盤モデルだが、安全策（safeguards）の有無で区別され、それが別名称を採用した理由とされている。Claude Mythos 5は一般提供されず、審査制プログラム「Project Glasswing」の承認パートナーのみに提供される招待制。

モデル名の変遷としては、初期の「Instant（即時）」という機能的命名から、Claude 3（2024年3月）でHaiku・Sonnet・Opusという詩の名前に移行、2026年6月にFable・Mythosという物語系の名前へと進化している。また表記順もClaude 4世代からティア名が世代番号の前に来る形式（例：Claude Opus 4）に変更されている。一次ソースで確認できる範囲だけでも、文学的語彙を選び続ける一貫性が見て取れる。

## アイデア

- Fable/Mythosで初めてAnthropicが公式文書内で命名語源を説明したことは、透明性向上の動きとして注目に値する。安全策の有無という技術的差異が命名の分岐理由とされている点は、モデルガバナンスの観点からも興味深い
- 「公式に確認できる事実」と「広く流布しているが未確認の説」を厳密に区別する本記事のアプローチは、AI情報リテラシーの実践例として有用。CEO口頭発言と書面公式文書を区別する姿勢は監査・内部統制の情報評価にも通じる
- Instant→Haiku→Fableという命名の変遷は、機能的説明から文学的メタファーへのブランディング戦略の変化を示しており、LLM製品のポジショニング戦略を考察する上で参考になる

## 前提知識

- **Claude モデルファミリー** (TODO: 読むべき)
- **LLM ティア構造** (TODO: 読むべき)
- **Anthropic** → /deep_41 ハーネスエンジニアリング完全ガイド — 2026年、AIエージェントの「手綱」を握る技術
- **モデルカード** → /deep_1486 モデルカード：MLモデルのドキュメント化フレームワークとHugging Faceの取り組み
- **Project Glasswing** → /deep_7504 エージェントに「脆弱性を探して」はなぜ失敗するのか──CloudflareのProject Glasswingが示したharnessの正体

## 関連記事

- /deep_3718 AIが強化するサイバー犯罪：フィッシング・マルウェア・脆弱性探索の自動化と防衛の現状
- /deep_6602 Anthropic、初の四半期黒字達成へ――2026年Q2に売上109億ドル、営業利益5.6億ドルの見通し
- /deep_3747 AIによるサイバー攻撃の高度化：フィッシング・マルウェア・脆弱性探索への悪用と防御の現状
- /deep_3393 AIによるサイバー攻撃の高度化：フィッシング・マルウェア・脆弱性探索の自動化と防御の現状
- /deep_3214 AIが加速させるサイバー犯罪：フィッシング・マルウェア・脆弱性探索の自動化と防御側の対応

## 原文リンク

[ClaudeのFableが公開されたので、改めてClaudeの命名の由来をFableにまとめてみてもらった](https://zenn.dev/yuzunatsuki/articles/47ec894f021602)
