---
title: "Andrej Karpathyの「autoresearch」が描くAI研究自動化の未来"
url: "https://zenn.dev/aienthusiast/articles/article-20260322-094255"
date: 2026-05-09
tags: [autoresearch, 自律エージェント, AI研究自動化, Markdown駆動, nanochat, Karpathy, シングルGPU, 実験ループ]
category: "agent-arch"
related: [7, 2409, 1516, 2688, 3493]
memo: "[Zenn LLM] Andrej Karpathyの「autoresearch」が描く未来"
processed_at: "2026-05-09T09:32:23.611879"
---

## 要約

Andrej Karpathy（Tesla元AIディレクター、OpenAI創業メンバー）が公開した「autoresearch」は、AI研究サイクル全体をAIエージェントに自律実行させるPythonプロジェクトで、GitHubで48,899スター・6,802フォークを獲得している。

核心的な仕組みは、シングルGPU上で動作する自律実験ループだ。エージェントが自動でコードを修正し、約5分間のトレーニングを実行し、評価指標の改善があれば採用・なければ破棄という判断を繰り返す。これを一晩中継続することで、人間が週に数回実施する実験を、AIが一晩で数十〜数百回実行できる。

プロジェクト構成はあえてシンプルに設計されており、主要ファイルはprepare.py（データ準備・定数定義）、train.py（トレーニングループとモデル定義）、program.md（エージェントへの指示）の3つのみ。特に注目すべきは「program.md」の役割で、Markdownファイルがエージェントへのコンテキストと指示を担う「研究組織プログラミング」パラダイムを採用している点だ。研究者はPythonコードを直接操作するのではなく、Markdownで研究方向・制約条件を記述し、エージェントの行動をメタレベルで制御する。

ベースモデルにはKarpathy自身が開発したnanochatの簡易実装を使用しており、大規模インフラ不要で個人研究者でも試せる設計となっている。READMEには「2026年の架空の振り返り」として、コードベースが10,205世代を経て人間には理解不能な自己修正バイナリへ進化した未来が描かれており、プロジェクトの長期ビジョンを示している。

監査エージェント開発への示唆として、program.mdによる「Markdown駆動のエージェント制御」は、LangGraphにおけるシステムプロンプト設計やエージェントのゴール定義に直接応用できる発想だ。実験的な検証ループを自動化するアーキテクチャパターンは、監査ルールの反復的テスト・改善サイクルにも転用可能であり、LLM-as-judgeによる自己評価と組み合わせた自律型監査エージェントの設計に参考になる。

## アイデア

- program.mdというMarkdownファイルでエージェントの研究組織全体を定義する「Markdown-as-Program」パラダイムは、コードではなく自然言語構造で複雑なエージェント挙動を制御する新しい抽象化レイヤーを提案している
- 約5分のトレーニング→評価→採否判断のサイクルを一晩中自律反復することで、人間研究者の実験頻度を桁違いに上回るスループットを単一GPUで実現している点は、リソース制約下での研究民主化として重要
- コードベースが10,000世代以上の自己修正を経て「人間には理解不能」な状態になるというビジョンは、AIが生成したコードのinterpretabilityとガバナンスという新たな課題を先取りして提起している

## 前提知識

- **ReAct Agent** (TODO: 読むべき)
- **自律実験ループ** → /deep_7 Karpathy発AutoResearchで一晩100実験を自動化する仕組みと実践
- **nanochat** (TODO: 読むべき)
- **BPEトークナイザー** (TODO: 読むべき)
- **LLM-as-judge** → /deep_3 Claude Code のAIチームでLLMの品質を自動でチェックする方法

## 関連記事

- /deep_7 Karpathy発AutoResearchで一晩100実験を自動化する仕組みと実践
- /deep_2409 音声LLM評価基準DEAFや自己改善AIなどのAI技術動向まとめ（2025年3月下旬〜4月初頭）
- /deep_1516 責任経路設計はMeaningful Human Controlと何が違うのか―軍事AIのaccountability議論との接点とは
- /deep_2688 自分のバージョンアップを自分で書く — embodied-claude v0.2「Social and scripted」
- /deep_3493 人工科学者：AIが科学研究を自律実行する時代へ——現状と課題

## 原文リンク

[Andrej Karpathyの「autoresearch」が描くAI研究自動化の未来](https://zenn.dev/aienthusiast/articles/article-20260322-094255)
