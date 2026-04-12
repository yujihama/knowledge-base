---
title: "Open R1 アップデート #3: OlympicCoderモデルとCodeForces-CoTsデータセットの公開"
url: "https://huggingface.co/blog/open-r1/update-3"
date: 2026-04-08
tags: [DeepSeek-R1, GRPO, SFT, Chain-of-Thought, 蒸留, 競技プログラミング, Qwen2.5, コード推論, ベンチマーク, IOI]
category: "ai-ml"
memo: "[HF Blog] Open R1: Update #3"
processed_at: "2026-04-08T09:17:45.613162"
---

## 要約

HuggingFaceのOpen R1チームが、DeepSeek-R1のコード推論再現に向けた取り組みの第3弾として、3つの主要成果を公開した。

**CodeForces-CoTsデータセット**: CodeForcesの1万問超の競技プログラミング問題（2025年まで）に対し、DeepSeek-R1にC++・Pythonでの解答を生成させた約10万サンプルのChain-of-Thoughtデータセット。問題の約60%にはコンテスト主催者による解法説明（editorial）も付属する。既存のDeepMindのCodeContestsデータセットと比べ、約3,000問が新規追加。

**テスト検証問題（Code Verifiability Crisis）**: 既存の競技プログラミングデータセットは、CodeForcesが公開するテストケースを約500文字に制限しているため、短い・簡単なケースしか含まれない。実験では、R1生成解答が公開テストケースを全パスした7問全てが、実際のCodeForcesの完全テストセットでは失敗することを確認。完全検証可能なデータセットの必要性が示された。

**IOIベンチマーク**: 国際情報オリンピック（IOI）2020〜2024の問題を活用した新ベンチマーク。IOI問題は完全なテストケースがCC-BYライセンスで公開されており、厳密な評価が可能。各問題をサブタスク単位に分割し、部分点評価に対応。OpenAIのo1がIOI'2024に実際に参加した論文に倣い、40以上のモデルを評価。50回提出戦略（ラウンドロビン方式、長い生成を優先）を採用。結果として、いずれのモデルも銅メダルラインには届かなかったが、OlympicCoder-32Bはo1-mini・DeepSeek-R1を上回り、claude-3.7-sonnet-thinkingも超えた。

**OlympicCoderモデル**: Qwen2.5 Coder Instruct 7B・32BをCodeForces-CoTsでファインチューニングしたモデル。OlympicCoder-32Bは100倍以上大きいオープンウェイトモデルを含む全テスト対象モデルを上回るトップクラスの性能を達成。蒸留元であるDeepSeek-R1自体もIOI評価で下回るという結果は、少量・高品質なCoTデータによるSFTの有効性を示す。

## アイデア

- 公開テストケースをパスしても実際のフルテストで全滅するという『検証可能性の危機』は、LLMのコード評価全般における過信リスクを示しており、RAGや監査エージェントのテスト設計にも同様の盲点が潜む可能性がある
- 蒸留元（DeepSeek-R1）よりもファインチューニングモデル（OlympicCoder-32B）の方がIOI評価で優れるという逆転現象は、高品質なCoTデータによるドメイン特化SFTが汎用大規模モデルを超えうることを実証している
- 50回提出・ラウンドロビン・長い生成を優先という提出戦略は、推論モデルの能力を最大化するサンプリング設計の重要性を示しており、エージェントの試行回数設計やベストオブN戦略に直接応用できる
## 関連記事

- /deep_773 Open R1 アップデート#2: 数学推論データセット OpenR1-Math-220k の構築
- /deep_861 蒸留モデルとは何か？ - DeepSeek R1の登場から1年で振り返るLLM知識蒸留の仕組みと実力
- /deep_1060 簡潔な方が良い：関数呼び出しエージェントにおけるChain-of-Thoughtの非単調な予算効果
- /deep_1169 広範な探索から安定した生成へ：自己回帰画像生成のためのエントロピー誘導最適化
- /deep_125 SliderQuant: LLM向け高精度ポストトレーニング量子化フレームワーク

## 原文リンク

[Open R1 アップデート #3: OlympicCoderモデルとCodeForces-CoTsデータセットの公開](https://huggingface.co/blog/open-r1/update-3)
