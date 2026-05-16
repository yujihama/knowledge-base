---
title: "CodeParrot 🦜 をゼロから学習する：Pythonコード生成GPT-2モデルの構築手順"
url: "https://huggingface.co/blog/codeparrot"
date: 2026-04-14
tags: [GPT-2, コード生成, CodeParrot, Hugging Face, Accelerate, DistributedTraining, Tokenizer, ConstantLengthDataset, HumanEval, スクラッチ学習]
category: "ai-ml"
related: [1709, 1758, 1531, 1754, 1331]
memo: "[HF Blog] Training CodeParrot 🦜 from Scratch"
processed_at: "2026-04-14T12:11:50.265118"
---

## 要約

本記事は、GitHub CopilotのベースとなるCodexに着想を得て、Pythonコード補完モデル「CodeParrot」をゼロからスクラッチで構築する全工程を解説したHugging Faceブログ記事（2021年12月公開）である。

**データセット構築：** Google BigQueryのGitHubダンプからPythonファイルのみを抽出し、180GB・2000万ファイルの巨大データセットを作成。重複問題が深刻で、ユニークファイルの上位0.1%が全ファイルの15%、上位1%が35%を占めるという偏りを確認。Codexペーパーの洗浄ヒューリスティクスと重複除去を適用し、最終的に50GB・約600万ファイルの`codeparrot-clean`データセットとしてHubに公開した。

**トークナイザーとモデルの初期化：** GPT-2ベーストークナイザーに対して`train_new_from_iterator()`を使いコード専用に再学習。モデルはGPT-2 large（1.5Bパラメータ）と同一ハイパーパラメータをベースに、`scale_attn_by_layer_idx`（レイヤーIDによるアテンションスケーリング）と`reorder_and_upcast_attn`（完全精度でのアテンション計算による数値安定化）を追加。

**学習ループ：** 🤗 Accelerateライブラリを採用し、ラップトップから16× A100（40GB）マルチGPU環境まで同一コードでスケーリング。データ効率化のため`ConstantLengthDataset`（IterableDataset）を自前実装し、複数サンプルをEOSトークンで連結して1024トークンの固定長チャンクを生成。ストリーミング（`streaming=True`）により50GBのデータをディスクに落とさず処理する。

**学習インフラ：** 16× A100（40GB）計8台のマシン（合計128 GPU）でDistributed Data Parallel（DDP）学習を実施し、約1週間で1500億トークンを学習（Chinchillaスケーリング則の約4倍）。勾配チェックポイント有効化でGPUメモリ使用を抑制。

**評価：** HumanEval（コード補完ベンチマーク）でpass@1=3.80%、pass@10=6.57%、pass@100=12.78%を達成。100Bトークン以降も学習損失の改善が継続しており、スケールアップの余地を示している。完全なコードとモデルはHugging Face Hub（`codeparrot/codeparrot`）で公開済み。

監査エージェント開発への示唆：コード生成モデルを社内ドキュメントや監査手続き記述に特化して学習させる場合、重複データが性能を著しく劣化させる点と、ConstantLengthDatasetによるストリーミング学習の仕組みは実装参考になる。また、Accelerateを使ったスケーリング戦略は監査ログ分析用LLMのファインチューニングにも転用可能。

## アイデア

- 重複データの偏在（上位0.1%のファイルが15%を占める）がモデル性能を著しく劣化させるという知見は、独自コーパス構築時の品質管理における重要な警告として汎用性が高い
- ConstantLengthDatasetによる複数サンプル連結＋固定長チャンク化は、可変長テキストを効率的にバッチ処理する汎用テクニックであり、監査報告書やログのLLM学習にも応用できる
- Accelerateライブラリにより、コードを1行も変えずにシングルGPUから128 GPU構成にスケールアウトできる点は、実験フェーズから本番スケール学習への移行コストを大幅に削減する

## 前提知識

- **GPT-2** → /deep_706 バイリンガルBabyLMの育成：小規模モデルを用いた多言語言語習得の研究
- **Causal Language Modeling** (TODO: 読むべき)
- **BPEトークナイザー** (TODO: 読むべき)
- **Distributed Data Parallel** (TODO: 読むべき)
- **HumanEval** → /deep_1052 RTX 4080で挑む強化学習コードLLM — 実行フィードバックで1.5Bモデルを鍛える全記録

## 関連記事

- /deep_1709 機械学習エキスパート・インタビュー：Lewis Tunstall（Hugging Face MLエンジニア）
- /deep_1758 🤗 TransformersにおけるConstrained Beam Searchによるテキスト生成の制御
- /deep_1531 🤗 EvaluateライブラリによるLLMバイアス評価
- /deep_1754 🤗 AIリサーチ・レジデンシープログラムの発表
- /deep_1331 設計支援AIは消えない。コード生成の次に残る領域

## 原文リンク

[CodeParrot 🦜 をゼロから学習する：Pythonコード生成GPT-2モデルの構築手順](https://huggingface.co/blog/codeparrot)
