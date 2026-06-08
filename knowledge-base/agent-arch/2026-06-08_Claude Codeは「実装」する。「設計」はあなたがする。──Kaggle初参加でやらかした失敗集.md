---
title: "Claude Codeは「実装」する。「設計」はあなたがする。──Kaggle初参加でやらかした失敗集"
url: "https://zenn.dev/beckento/articles/12988953749043"
date: 2026-06-08
tags: [Claude Code, Kaggle, LLM活用, 設計vs実装, BirdCLEF, 疑似ラベル, GroupKFold, Google Perch, CLAUDE.md, Adversarial Validation]
category: "agent-arch"
related: [6491, 1429, 2953, 5029, 5970]
memo: "[Zenn LLM] Claude Codeは「実装」する。「設計」はあなたがする。 ── Kaggle初参加でやらかした失敗集"
processed_at: "2026-06-08T09:05:00.766592"
---

## 要約

BirdCLEF+ 2026（鳥音声分類コンペ）への初参加を通じて、Claude Codeを活用した際に発生した設計ミス・思い込み・評価軸のズレを詳細に記録した失敗報告。失敗は4カテゴリに分類される。①思い込み：Notebook提出の90分CPU制限を知らずに1週間消費、pip不使用という誤解（実際は.whlをKaggle Datasetにアップすれば利用可能）、WSL2セットアップを「大変」と回避し続けたがClaude Codeに依頼したら10分で完了した。②設計なし実装：学習時にz-score正規化を適用したが推論パイプラインに未適用でスコアが0.746→0.813（+0.067）の損失、StratifiedKFoldで同一録音ファイルが複数チャンクに分割されているsoundscapeデータをtrain/valに混在させてデータリーク発生（GroupKFold(groups=filename)で解決）、疑似ラベルを閾値なしで全量学習させ1 fold当たり5〜6時間・5 foldで30時間超に膨張、CLAUDE.mdに指示を追記し続け肥大化してコンテキスト効率が低下。③評価軸のミス：CV判断をmacro AUCで行っていたが本番評価指標はpadded cmAPであり、AUC改善がcmAP低下を招く実験を「改善」として積み重ねた。提出スコアを正として判断し続け、CVを信じなかったことがメダリストとの根本的差異。④ドメイン知識不足：鳥音声特化の事前学習済みモデルGoogle Perchの存在を数週間後に把握、OOF予測・Adversarial Validation・疑似ラベリングの設計パターンもDiscussionを最初に読めば早期習得可能だった。GMアドバイザーエージェントを作成してメダリストの行動パターンと比較した結果、差は技術力ではなく「生データを確認する」「CVで判断する」「シンプルな手法を正確に実装する」という判断軸にあると結論。Claude Codeはコード実装速度と実験回転数を向上させるが、設計ミスの影響も速く深く広がるため、実装前に人間が評価指標・前提・パイプライン設計を確定させることが必要。監査エージェント開発においても、エージェントに実装を委ねる前に評価指標の定義とパイプライン設計を人間が明確化することが同様に重要。

## アイデア

- Claude Codeは実装速度を上げる分、設計ミスの伝播速度も上げる──ツールの増幅特性が正負両方に働くという構造的問題
- GMアドバイザーエージェントを自作してメダリストの行動パターンを診断させるという、LLM-as-judgeの自己改善的活用
- CLAUDE.mdへの無設計な指示追記がコンテキスト効率を低下させる負債化──エージェント設定ファイルにも設計が必要という盲点

## 前提知識

- **Kaggle Notebook提出** (TODO: 読むべき)
- **StratifiedKFold / GroupKFold** (TODO: 読むべき)
- **疑似ラベリング** (TODO: 読むべき)
- **padded cmAP** (TODO: 読むべき)
- **Google Perch** (TODO: 読むべき)

## 関連記事

- /deep_6491 Claude Codeを使い倒すための設定術：CLAUDE.md・自動メモリ・コンテキスト管理の3本柱
- /deep_1429 非エンジニアがKaggleで3999チーム中1257位になった話
- /deep_2953 長門有希ペルソナがClaude Codeのトークン消費を削減する：キャラクター指定vsルールベース圧縮の比較検証
- /deep_5029 ハーネスエンジニアリング入門【概要 & 実践的TIPS】
- /deep_5970 ハーネスは書いて終わりじゃなかった ── 3か月運用して動的に壊れた5つの瞬間

## 原文リンク

[Claude Codeは「実装」する。「設計」はあなたがする。──Kaggle初参加でやらかした失敗集](https://zenn.dev/beckento/articles/12988953749043)
