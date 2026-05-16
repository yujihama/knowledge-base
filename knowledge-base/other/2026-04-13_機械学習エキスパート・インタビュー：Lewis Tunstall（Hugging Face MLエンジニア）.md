---
title: "機械学習エキスパート・インタビュー：Lewis Tunstall（Hugging Face MLエンジニア）"
url: "https://huggingface.co/blog/lewis-tunstall-interview"
date: 2026-04-13
tags: [Transformers, ONNX, NLP, Hugging Face, モデル最適化, MLOps, GPT-2, 書籍]
category: "other"
related: [1445, 1015, 1668, 1578, 1448]
memo: "[HF Blog] Machine Learning Experts - Lewis Tunstall"
processed_at: "2026-04-13T12:08:30.827925"
---

## 要約

本記事はHugging FaceのMLエンジニアであるLewis Tunstallへのインタビューを収録したもの。Lewis は元理論物理学者で、2018年にスイスのスタートアップでTransformersを用いたQAタスクに初めて取り組んだことがきっかけでNLPの世界に入った。当時のライブラリ名は「pytorch-pretrained-bert」であり、ごく限定的なコードベースだった。その後Hugging Faceのエコシステムが急速に拡大したことに触発され、友人のLeandro von Werraと共同でThom Wolfにコールドメールを送り、書籍『NLP with Transformers』（O'Reilly）の執筆を提案。約1.5年の制作期間を経て出版し、この縁でLeandroともにHugging Faceに入社した。

インタビューの主要テーマの一つは、本番環境でのモデル最適化。大規模Transformerモデルはパラメータ数が多く推論レイテンシが高いため、チャットボット等のリアルタイム用途では課題となる。Lewisはこの問題に対し、PyTorchモデルをONNX形式にエクスポートする機能をTransformersライブラリに組み込む作業を担当。ONNX変換は内部的に複雑だが、ユーザー側は1行のコードで完結するよう設計されており、TensorFlowへの変換や専用ハードウェアでの実行、さらにより高速なレイテンシ・スループットの実現が可能となる。

Hugging Face Courseについても詳述。SylvainとLysandreが主導し、ソフトウェアエンジニアをNLP・Transformers入門へ橋渡しすることを目的に開発された無料コース。Lewisも参加し、モデル評価（大規模ベンチマーク）やMLOpsの課題解決に取り組んでいる。大規模言語モデルの評価においては、モデルが「知らないことを知らない」問題（ハルシネーション）が課題であり、信頼性の定量化が重要テーマとして挙げられた。GPT-2によるテキスト生成の社会的インパクト（リサイクル否定エッセイの例）にも触れ、生成AIの人間らしさが与える心理的驚きについても考察している。監査エージェント開発への示唆としては、ONNXエクスポートによるモデル軽量化・高速化の手法は、推論コストを抑えた監査ワークフローへの組み込みに直接応用可能である点が注目される。

## アイデア

- PyTorchモデルを1行のコードでONNX形式にエクスポートできるTransformersの抽象化設計は、複雑な変換処理をユーザーから隠蔽しつつ専用ハードウェア最適化を可能にする実用的アーキテクチャパターン
- LLMの評価における「モデルが知らないことを知らない」問題（ハルシネーション・信頼性の定量化）は、大規模ベンチマーク設計の核心課題であり、監査用途では特に重要
- コールドメールによる書籍共著提案からHugging Face入社に至ったキャリアパスは、オープンソース貢献と書籍執筆がコミュニティ内での信頼構築に有効であることを示す実例

## 前提知識

- **Transformer** → /deep_99 LLM Architecture Gallery徹底解説：30+モデルの内部構造を4軸で横断比較する
- **ONNX** → /deep_1307 Transformers.jsでMLパワードWebゲームを作る方法
- **PyTorch** → /deep_26 CodaとClaudeによる全員向けカスタムCUDAカーネル自動生成エージェントスキル
- **Fine-tuning** → /deep_1224 AIモデルのカスタマイズへの移行はアーキテクチャ上の必須事項
- **MLOps** → /deep_1645 雰囲気でML運用してない？Google流「ML Test Score」でMLパイプラインの信頼性を数値化する

## 関連記事

- /deep_1445 FetchがHugging FaceとAWSを活用してAIツールを統合し、開発時間を30%削減
- /deep_1015 Transformersドキュメントの再設計：混乱を整理する
- /deep_1668 Sempre HealthがExpert Acceleration Programを活用してMLロードマップを加速した事例
- /deep_1578 Hugging FaceのTensorFlow哲学：KerasネイティブなTransformersの設計方針
- /deep_1448 Hugging Face Inference Endpointsへの移行事例：ECS+FargateからのMLモデルデプロイ刷新

## 原文リンク

[機械学習エキスパート・インタビュー：Lewis Tunstall（Hugging Face MLエンジニア）](https://huggingface.co/blog/lewis-tunstall-interview)
