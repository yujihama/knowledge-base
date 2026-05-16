---
title: "markdownとClaude Codeだけでアプリを作る：Spec-as-Appという新しいアーキテクチャ"
url: "https://zenn.dev/biscuit/articles/spec-as-app-markdown-claude-code"
date: 2026-05-08
tags: [Spec-as-App, Claude Code, LLM Wiki, Literate Programming, markdown, エージェントアーキテクチャ, CLAUDE.md, Infrastructure as Code]
category: "agent-arch"
related: [2954, 2821, 2953, 3506, 2547]
memo: "[Zenn LLM] markdownとClaude Codeだけでアプリを作る : Spec-as-Appという新しいアーキテクチャ"
processed_at: "2026-05-08T09:44:33.430320"
---

## 要約

「Spec-as-App」とは、markdownで書いた仕様書がそのままAIエージェント（Claude Code）への命令になり、Pythonや JavaScriptなどのコードへの翻訳なしに動作するアーキテクチャパターン。著者は個人の知識ベース（LLM Wiki）を.pyも.jsも存在しないmarkdownのみのリポジトリとして運用しており、記事取り込み・インデックス更新・リント・外部記事キュレーションといった処理が日々実行されていることから、この概念を抽出・命名した。

Spec-as-Appが成立する条件は3つ：①自然言語の仕様書がそのままエージェントへの命令になる、②エージェントが仕様を読んで自律的に実行する、③状態と振る舞いがmarkdownファイルで管理できる。従来Webアプリとの対比では、データ層がRDB→markdownのfrontmatter、スキーマ変更がmigrationスクリプト→markdownの編集＋commit、ビジネスロジックがコード＋テスト→markdownで記述したskill/rule、ランタイムが決定論的（JVM/V8等）→確率的（LLM）、デプロイがCI/CDパイプライン→git commitに置き換わる。

ディレクトリ構成はCLAUDE.md（システム全体の仕様書）、.claude/skills/（機能モジュール）、.claude/routines/（cron式＋プロンプトで定義する定期実行タスク）、wiki/（知識ベース本体）の4層。Claude Codeがコンパイラとして機能し、raw/の未処理ファイルをソースとしてwiki/index.mdという「実行可能バイナリ」を生成するアナロジーで説明される。

Donald Knuthが1984年に提唱したLiterate Programming（「散文が一次、コードはその副産物」）との対比では、当時はtangleと呼ばれる変換ステップが必須だったが、Spec-as-AppではLLMがそのtangleを引き受けることで二重管理が消滅している点が本質的な差異。

革命的な点として①仕様＝実装の一致（仕様書が古くなると挙動が壊れるため最新化インセンティブが構造的に生まれる）、②編集の民主化（プログラミング言語の文法不要）、③git diffで全変更が統合される、④エージェントが「読み手」と「実行者」を兼ねる点を挙げる。一方で限界として、非決定性（同一入力で異なる出力の可能性）、LLM呼び出しコストの非線形増加、レイテンシの大きさ、スタックトレースがなくデバッグが困難な点、仕様書の「腐敗」リスクを認める。適用境界は「人間がmarkdownを直接読み書きしても破綻しない規模・速度・確定性」であり、個人〜小規模チームの知識管理・社内手順書の自動化・PoCには向くが、トランザクション処理・リアルタイムUX・規制業種・大規模データ処理には不向きと整理している。監査エージェント開発への示唆として、内部統制手順書や監査チェックリストをSpec-as-Appパターンで記述すれば、手順書の更新がそのままエージェントの振る舞い変更に直結する設計が可能だが、金融・監査領域の確定性要件とLLMの非決定性の矛盾を慎重に評価する必要がある。

## アイデア

- 仕様書が古くなると実装が壊れる構造により、ソフトウェア史上初めて「仕様書を最新に保つインセンティブ」が構造的に成立する点：ドキュメントと実装の乖離問題への根本的アプローチ
- Donald KnuthのLiterate Programmingが1984年に諦めざるを得なかった『散文→機械実行の無翻訳変換』を、LLMがtangleステップを引き受けることで初めて実現している点
- コンパイラアナロジー：raw/をソース、wiki/index.mdを実行可能バイナリとして捉え、Claude Codeがコンパイラとして機能するという概念モデルが、エージェントシステムの設計パターンとして応用可能

## 前提知識

- **Claude Code** → /deep_3 Claude Code のAIチームでLLMの品質を自動でチェックする方法
- **LLMエージェント** → /deep_7 Karpathy発AutoResearchで一晩100実験を自動化する仕組みと実践
- **Literate Programming** (TODO: 読むべき)
- **CLAUDE.md / skills設計** (TODO: 読むべき)
- **Infrastructure as Code** (TODO: 読むべき)

## 関連記事

- /deep_2954 ObsidianとClaude Codeで「育つ知識ベース」を作った話
- /deep_2821 AIに「自分」を記憶させる仕組みを作った：LLM WikiをClaude Codeで実装した話
- /deep_2953 長門有希ペルソナがClaude Codeのトークン消費を削減する：キャラクター指定vsルールベース圧縮の比較検証
- /deep_3506 なぜClaude Codeは「トークンを食いまくる」のか、そしてそれを止める6つの習慣
- /deep_2547 【Claude Code】コマンドは3つだけ！ハーネスエンジニアリング実践編：log → distill → promote

## 原文リンク

[markdownとClaude Codeだけでアプリを作る：Spec-as-Appという新しいアーキテクチャ](https://zenn.dev/biscuit/articles/spec-as-app-markdown-claude-code)
