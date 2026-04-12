---
title: "Claudeを使ってCUDAカーネルを構築し、オープンモデルに教える「upskill」ツールの紹介"
url: "https://huggingface.co/blog/upskill"
date: 2026-04-02
tags: [agent-skills, CUDA, Claude Opus 4.5, upskill, knowledge-transfer, model-evaluation, HuggingFace, diffusers]
category: "agent-arch"
memo: "[HF Blog] We Got Claude to Build CUDA Kernels and teach open models!"
processed_at: "2026-04-02T12:01:32.364508"
---

## 要約

HuggingFaceが公開したブログ記事では、「upskill」というツールを使い、大規模モデル（Claude Opus 4.5）が獲得した専門的スキルを小規模・オープンソースモデルに転移させるプロセスを解説している。「エージェントスキル」とは、モデルのコンテキストをMarkdownの指示書やスクリプトとしてファイル化したもので、`{agent}/skills/{skill_name}/SKILL.md`という形式で保存される。codex、cursor、opencodeなど主要ツールが同形式を採用している。

具体的なユースケースとして、HuggingFaceのdiffusersモデル向けCUDAカーネル開発を取り上げている。ワークフローは3段階：(1) Claude Opus 4.5がインタラクティブにカーネルを構築しながらトレースをエクスポート、(2) upskillがトレースからスキルファイルとテストケースを自動生成、(3) 生成スキルを小規模モデルに適用して`upskill eval`でスキルあり・なしの精度とトークン使用量を比較評価。

評価結果の示唆は重要で、スキルがすべてのモデルで有効なわけではない。`moonshotai/Kimi-K2-Thinking`では精度・トークン効率ともに改善したが、Claude Opus 4.5自身にはスキル適用でトークン使用量が増加し精度向上もなかった。つまりスキルの有効性はモデル依存であり、eval必須という結論。

CUDAカーネルのスキルファイルには「H100はcompute capability 9.0」「共有メモリは128バイトアライン」「非同期メモリコピーは`__CUDA_ARCH__ >= 900`が必要」といった具体的なドメイン知識が約500トークンに凝縮される。インストールは`pip install upskill`で完了し、`upskill generate`でスキル生成、`upskill eval`で評価、ローカルモデル（OpenAI互換エンドポイント）も`--eval-base-url`で対応可能。

## アイデア

- 大規模モデルのトレースから小規模モデル向けスキルを自動生成する「知識蒸留のエージェント版」という発想は、コスト削減と専門タスクの民主化を同時に実現する
- スキルの有効性はモデルごとに異なり、精度だけでなくトークン消費量も評価軸にすることで、本番運用時のコスト最適化が可能になる
- スキルファイルをMarkdown+スクリプトというシンプルな形式に標準化することで、複数のエージェントツール間でスキルをポータブルに共有できる点が実用的
## 関連記事

- /deep_26 CodaとClaudeによる全員向けカスタムCUDAカーネル自動生成エージェントスキル
- /deep_1572 🧨 DiffusersによるStable Diffusion：仕組みと実装ガイド
- /deep_1302 🤗 Diffusers 1周年記念：1年間の主要機能まとめ
- /deep_1389 無料Google ColabでDeepFloyd IFをDiffusersで動かす方法
- /deep_1265 Würstchen：42倍圧縮による高速・低コスト画像生成拡散モデルの紹介

## 原文リンク

[Claudeを使ってCUDAカーネルを構築し、オープンモデルに教える「upskill」ツールの紹介](https://huggingface.co/blog/upskill)
