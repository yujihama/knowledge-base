---
title: "Karpathyが語るvibe codingからagentic engineeringへの転換点"
url: "https://zenn.dev/aiandao/articles/karpathy-vibe-coding-agentic-engineering-20260501"
date: 2026-05-08
tags: [vibe-coding, agentic-engineering, Karpathy, jagged-intelligence, software-3.0, LLM, 強化学習, Claude Code, コンテキストウィンドウ, エージェント設計]
category: "agent-arch"
related: [2250, 2146, 1335, 1106, 95]
memo: "[Zenn LLM] Karpathy が語る vibe coding から agentic engineering への転換点"
processed_at: "2026-05-08T21:12:22.213404"
---

## 要約

2026年4月のSequoia Capital AI Ascentにおける30分対談で、Andrej Karpathyはvibe codingとagentic engineeringの違いを整理した。転換点は2025年12月で、最新モデルを使い込む中で生成コードをほぼ修正しなくなったことで信頼が高まり、より大きな指示を出すようになった。Karpathyはソフトウェアの発展をsoftware 1.0（人間がコードを書く）、2.0（ニューラルネット訓練）、3.0（プロンプトでLLMを動かす）の3段階で整理し、3.0ではコンテキストウィンドウがLLMへのレバーとなり、プログラミングが「文脈を組み立てる」行為になると主張する。OpenAI Codexのインストール手順がシェルスクリプトから「エージェントに渡すテキスト」に変わった例がその典型。vibe codingは「床を上げる」（誰でもソフトウェアを作れる）、agentic engineeringは「天井を保つ」（プロ品質を維持しながら速度を上げる）と対比される。AIはjagged intelligence（ギザギザの知能）を持ち、検証可能なドメイン（数学・コーディング）では強化学習で急激に伸びるが、検証困難なドメインは停滞する。GPT-3.5からGPT-4でチェスが強くなったのは事前学習データに棋譜を大量投入した結果であり、モデルの強さは研究所が何をデータに混ぜたかに依存する。エージェントはまだ「インターン」であり、仕様の判断（例：StripeメールとGoogleアカウントの紐付け）は人間の仕事として残る。PyTorchのdim/axis等の細かいAPIは忘れてよいが、tensorのviewとstorageの違いのような根本原理は理解必須とする。採用試験についても、パズル解法より大規模プロジェクト構築＋別エージェント10個による攻撃テストが実戦的だと提言。最後に「思考は外注できても理解は外注できない」と結論し、LLMはnarrowing knowledge baseとして活用しつつ、理解そのものは人間が引き受けるスタンスを示した。監査エージェント開発への示唆として、検証可能性の設計（RL報酬関数の構築）が自社ドメインでの差別化につながる点と、エージェントの出力品質を人間が監督する仕組みの重要性が直接適用できる。

## アイデア

- jagged intelligenceの根本原因が強化学習の報酬構造にある点：検証可能なドメインでのみ性能が急伸するため、監査AIでも「正誤が判定できる問い」を設計することがRL活用の鍵になる
- software 3.0においてプログラミングが『コードを書く』から『コンテキストを組み立てる』に変質するという認識は、エージェントへの指示設計（プロンプト・ツール仕様・メモリ構造）をエンジニアリングの主戦場として位置づける
- エージェントをsensors（入力）とactuators（出力）で捉え直す視点は、監査ワークフローのタスク分解にそのまま応用可能で、何をエージェントが観測し何を操作するかを明示的に設計するアーキテクチャ指針になる

## 前提知識

- **強化学習（RLHF/RLVR）** (TODO: 読むべき)
- **LLMコンテキストウィンドウ** (TODO: 読むべき)
- **ReActエージェント** → /deep_4188 ReActエージェントが本当に必要な業務はどれか：4象限による業務AI設計の腑分け
- **事前学習データ設計** (TODO: 読むべき)
- **ファインチューニング** → /deep_530 AIモデルカスタマイズへの移行はアーキテクチャ上の必須事項

## 関連記事

- /deep_2250 Karpathyが指摘したLLMコーディングの失敗パターンと、コミュニティが作ったCLAUDE.mdの全貌
- /deep_2146 有効なシグナルが失敗するとき：LLM特徴量とRL取引ポリシー間のレジーム境界
- /deep_1335 日本語入力システムSumibiの開発 part17: ピンインによる中国語入力に対応した
- /deep_1106 文脈的知性：強化学習の次なる飛躍
- /deep_95 思考とプロンプトの間にある「空白」こそが、すべてを決める

## 原文リンク

[Karpathyが語るvibe codingからagentic engineeringへの転換点](https://zenn.dev/aiandao/articles/karpathy-vibe-coding-agentic-engineering-20260501)
