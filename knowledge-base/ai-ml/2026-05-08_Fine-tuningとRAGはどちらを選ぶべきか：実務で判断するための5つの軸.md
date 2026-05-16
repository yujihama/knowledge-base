---
title: "Fine-tuningとRAGはどちらを選ぶべきか：実務で判断するための5つの軸"
url: "https://zenn.dev/libercraft/articles/20260501-finetuning-vs-rag"
date: 2026-05-08
tags: [Fine-tuning, RAG, LoRA, QLoRA, PEFT, DoRA, Unsloth, LangChain, ベクトルDB, ハルシネーション]
category: "ai-ml"
related: [1449, 405, 3956, 2998, 1214]
memo: "[Zenn LLM] Fine-tuningとRAGはどちらを選ぶべきか：実務で判断するための5つの軸"
processed_at: "2026-05-08T21:12:51.519439"
---

## 要約

Fine-tuningとRAGは「どちらが優れているか」ではなく、「振る舞いの問題か知識の問題か」によって使い分けるべき異なるアプローチである。Fine-tuningはモデルの重み（パラメータ）を更新し、スタイル・語彙・タスク特化の振る舞いを変える。RAGは推論時に外部ドキュメントを検索してコンテキストに差し込み、モデル自体は変えずに「何を見て答えるか」を制御する。

実務判断のための5軸は以下の通り。①更新頻度：月次以上で更新が必要ならRAG一択。Fine-tuningは再学習サイクル（データ収集→学習→評価→デプロイ）が必要で、頻繁な更新に対応できない。②ハルシネーションリスク：医療・法律・金融など誤情報コストが高い領域ではRAG優先。RAGは検索文書を出典として引用可能で確認可能性が高まるが、取得文書の品質が低ければハルシネーションは依然発生する。③コスト構造：GPT-4o Fine-tuningは学習コスト$25/1Mトークン、推論inputが$3.75/1M。OSS QLoRA（Unsloth使用）はGPU時間のみで重みは無料。RAGはtext-embedding-3-smallで$0.02/1Mトークン＋LLM推論費。クエリ数が多く更新頻繁ならOSS QLoRAかRAGが有利。④レイテンシ：RAGは検索ステップで数十〜数百ms遅延が加わる。Fine-tuningモデルは外部DB問い合わせ不要で低レイテンシ。ただし大規模モデルのFine-tuningは推論コスト自体が増す。⑤（記事本文で5軸目の詳細は省略されているが）プライバシー・データガバナンス等が含まれる可能性がある。

Fine-tuning技術としては、フルFine-tuning（7Bで数百GB VRAM必要）ではなくPEFT（Parameter-Efficient Fine-Tuning）が実務標準。LoRAは元の重みWを凍結しΔW=BAの小行列積のみ学習。QLoRAはLoRAに4bit量子化を組み合わせ、A100やRTX 4090でも70Bモデルまで対応可能。DoRAは重みを大きさと方向に分解し方向成分にLoRAを適用する手法でLoRAより精度が出やすいケースがある。rankは16から始めて評価指標で調整するのが現実的。監査エージェント開発においては、コンプライアンス・法令・内部規定など頻繁に改定される知識はRAGで管理し、出典付き回答による監査証跡の確保が不可欠。一方、監査特有の判断ロジックや文体・レポートフォーマットへの適応にはFine-tuningが有効という使い分けが示唆される。

## アイデア

- 「振る舞いの問題 vs 知識の問題」という二分法で選択基準を整理した点：単なるコスト比較ではなく問題の性質から設計判断を導く思考フレームとして再利用できる
- 更新頻度を軸にした判断基準（週次→RAG一択、1年以上固定→Fine-tuning検討）が具体的で実装指針として使いやすい
- 2026年時点のコスト数値（GPT-4o Fine-tuning $25/1Mトークン、text-embedding-3-small $0.02/1M）とOSS QLoRAのコスト構造の対比が実務試算に直結する

## 前提知識

- **LoRA / QLoRA** (TODO: 読むべき)
- **RAG（Retrieval-Augmented Generation）** (TODO: 読むべき)
- **PEFT** → /deep_143 LeRobot v0.5.0: あらゆる次元でのスケーリング
- **ベクトルDB** → /deep_969 RAGの最適化手法が多すぎて迷子になったので、整理したら全体像が見えた
- **LLMハルシネーション** → /deep_49 MARCH: LLMハルシネーション検出のためのマルチエージェント強化自己チェックフレームワーク

## 関連記事

- /deep_1449 🤗 PEFT：低リソースハードウェアで数十億パラメータモデルをパラメータ効率的にファインチューニング
- /deep_405 UnslothとHugging Face Jobsで無料でAIモデルをファインチューニングする方法
- /deep_3956 ShadowPEFT：シャドウネットワークによるパラメータ効率的ファインチューニング
- /deep_2998 RAGかファインチューニングか、もう迷わない——2026年版・企業LLM導入の判断フロー
- /deep_1214 LoRAを用いたRoBERTa・Llama 2・Mistral 7Bの災害ツイート分類性能比較

## 原文リンク

[Fine-tuningとRAGはどちらを選ぶべきか：実務で判断するための5つの軸](https://zenn.dev/libercraft/articles/20260501-finetuning-vs-rag)
