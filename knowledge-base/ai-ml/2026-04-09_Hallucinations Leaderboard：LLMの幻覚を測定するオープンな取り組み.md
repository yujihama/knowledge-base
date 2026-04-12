---
title: "Hallucinations Leaderboard：LLMの幻覚を測定するオープンな取り組み"
url: "https://huggingface.co/blog/leaderboard-hallucinations"
date: 2026-04-09
tags: [hallucination, LLM評価, TruthfulQA, HaluEval, SelfCheckGPT, LM-Eval-Harness, factKB, BERTScore, benchmark]
category: "ai-ml"
memo: "[HF Blog] The Hallucinations Leaderboard, an Open Effort to Measure Hallucinations in Large Language Models"
related: [769, 23, 1060, 111, 212]
processed_at: "2026-04-09T21:06:48.808547"
---

## 要約

Hallucinations Leaderboardは、LLM（大規模言語モデル）が生成するハルシネーション（幻覚）を体系的に評価するオープンプラットフォーム。エジンバラ大学・UCLを中心とした研究チームが構築し、EleutherAI Language Model Evaluation Harness（LM-Eval）をバックエンドに採用している。評価タスクは大きく6カテゴリに分類される：①Closed-book Open-domain QA（NQ Open、TriviaQA、TruthfulQA）、②Summarisation（XSum、CNN/DM）、③Reading Comprehension（RACE、SQuADv2）、④Instruction Following（MemoTrap、IFEval）、⑤Fact-Checking（FEVER）、⑥Hallucination Detection（FaithDial、True-False、HaluEval）、⑦Self-Consistency（SelfCheckGPT）。ハルシネーションは「事実性ハルシネーション（Factuality Hallucination）」と「忠実性ハルシネーション（Faithfulness Hallucination）」の2種類に大別される。前者は現実世界の事実と矛盾する内容の生成（例：チャールズ・リンドバーグが月面着陸した初人物と誤答）、後者はユーザー指示やコンテキストとの不一致（例：ニュース要約で日付を誤変換）を指す。評価スコアはすべて[0,1]スケールに正規化されており、TruthfulQA MC1/MC2では0.8が80%正解率を意味する。要約タスクの忠実性評価にはROUGE、factKB、BERTScore-Precisionの3指標を組み合わせている。Zero-shot・Few-shot（2-shot、4-shot、8-shot、64-shot）の両設定でテストを実施。実験インフラはEIDF（Edinburgh International Data Facility）とエジンバラ大学クラスターのNVIDIA A100-40GB/80GB GPUを使用。コードはHugging Face Leaderboard Templateのフォークとして公開されており、新タスクの追加や計算リソース提供などコミュニティ参加を募っている。2024年1月時点で論文もarXivに公開済み。

## アイデア

- ハルシネーション評価を「事実性」と「忠実性」の2軸で分離することで、モデルの欠陥の性質（知識不足 vs 指示無視）を切り分けられる点が設計として優れている
- SelfCheckGPTによる自己整合性（Self-Consistency）評価は、外部知識ベース不要でサンプリング間の矛盾を検出できるため、ドメイン特化LLMの評価にも転用しやすい
- factKBのようなモデルベースの事実性メトリクスをROUGEと組み合わせることで、字句的一致と意味的正確性の両面をカバーするマルチメトリクス評価戦略が参考になる
## 関連記事

- /deep_769 Math-VerifyによるOpen LLMリーダーボードの数学評価修正
- /deep_23 音声エージェント評価のための新フレームワーク EVA
- /deep_1060 簡潔な方が良い：関数呼び出しエージェントにおけるChain-of-Thoughtの非単調な予算効果
- /deep_111 生成AIのハルシネーションは「誤出力」？ 条件付き分布・真理条件・接地から見る数理的整理
- /deep_212 波形から知恵へ：聴覚知能の新ベンチマーク MSEB（Massive Sound Embedding Benchmark）

## 原文リンク

[Hallucinations Leaderboard：LLMの幻覚を測定するオープンな取り組み](https://huggingface.co/blog/leaderboard-hallucinations)
