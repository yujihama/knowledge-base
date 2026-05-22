---
title: "HindsightのrerankerをGPUなしCPUで9倍高速化 — batch size最適化とONNX化"
url: "https://zenn.dev/valda68k/articles/hindsight-reranker-9x-cpu-ja"
date: 2026-05-22
tags: [ONNX, reranker, cross-encoder, Hindsight, batch-size, CPU推論, ModernBERT, tokenizer, sentence-transformers, RAG]
category: "infra"
related: [707, 1116, 3085, 1440, 6085]
memo: "[Zenn 機械学習] Hindsight の reranker を GPU なし CPU で 9倍速くする — batch size 最適化と ONNX 化"
processed_at: "2026-05-22T09:11:31.553837"
---

## 要約

LLMエージェント向けセルフホスト型メモリバックエンド「Hindsight」のcross-encoder rerankerを、GPU非搭載のCPU環境（Ryzen 5 5600G）で高速化した実験記録。rerankerモデルはhotchpotch/japanese-reranker-xsmall-v2（ModernBERT-ja系、約36.8Mパラメータ）を使用。

最大の発見は「batch sizeの既定値32がCPUに不適合」という点。GPU向けにチューニングされた既定値をそのまま使うと、CPUではpaddingの無駄計算・キャッシュ溢れ・スレッドオーバーヘッドが積み重なり逆効果になる。batch size 2・4・8・16・32・64・128をsweepした結果、最速はbs=2で、reranking p95が7.98s→3.12s（-61%）。bs=128では逆に18.58s（+133%）と2.3倍悪化した。BUCKET_BATCHINGによる長さソート済みでもバッチが大きいとpaddingの無駄が支配的になることが実測で確認された。

次にPyTorchランタイムをONNX Runtime（CPUExecutionProvider）へ差し替え、3.12s→0.88sに短縮（累積9.1倍）。ただし注意点が複数あった。①intra_op_num_threads=1のままでは逆にPyTorchより遅くなる（0.48x）。スレッド数をworkloadに合わせてsweepし4に設定して初めて1.39x。②optimumでエクスポートしたONNXはraw logitを返すが、既存PyTorch pathはCrossEncoder.predict()がsigmoid済みスコアを返しHindsight側でさらにsigmoidをかける二重構造になっていたため、ONNX provider側でsigmoidを適用して挙動を一致させる必要があった。③tokenizer_config.jsonのtokenizer_class指定を古いtransformersが汎用slow pathにdispatchし、同一ペアで25トークンと55トークンという全く異なるトークン列を生成していた。これによりparity checkがSpearman 0.62で一度FAILした。対策としてtransformers経由の自動dispatchを避け、tokenizers.Tokenizer.from_file()で直接読み込む方式に変更。この修正で品質指標（keyword hit count）が13〜30%改善したが、これはONNX固有の成果ではなくbase imageのtransformersアップデートでも得られた改善であることを明示している。

speedupの内訳を正直に分解すると、9倍の大半はbatch size修正（2.6x）であり、ONNXランタイム固有の寄与はモデル推論単体で約1.4x、残りはtokenizer修正とend-to-endオーバーヘッド削減の合算。「最初に疑うべきはbatch size」という教訓が核心。監査エージェント開発においてRAGパイプラインのrerankerをCPU環境で運用する際の実践的な最適化手順として参照価値が高い。

## アイデア

- GPU向けのbatch size既定値（32）がCPUでは逆効果になるという非直感的な事実：paddingの無駄計算とキャッシュ溢れがスループット向上を打ち消し、bs=128ではbs=2の6倍遅くなる
- ONNX化単体の高速化寄与は約1.4xに過ぎず、9倍の大半はbatch size調整という「地味な設定変更」によるという定量的な分解：速度改善の帰属を正直に記述する実験設計の誠実さが参考になる
- tokenizer_config.jsonのdispatchバグがSpearman 0.62という大幅な品質劣化を引き起こした事例：ランタイム差し替え時にスコアのparity checkを行う重要性と、transformersバージョン依存を回避するためにtokenizers.Tokenizer.from_file()を直接使う手法

## 前提知識

- **cross-encoder reranker** (TODO: 読むべき)
- **ONNX Runtime** → /deep_2558 オンデバイスストリーミングASRの限界に挑む：低レイテンシ推論向け高精度コンパクト英語モデル
- **sentence-transformers** → /deep_9 LLMに長期記憶を実装する — 脳の記憶メカニズムのPython実装
- **tokenizer dispatch** (TODO: 読むべき)
- **RAGパイプライン** → /deep_2794 金融QAにおけるPDFパース・チャンキングの実証評価：RAGパイプライン設計指針

## 関連記事

- /deep_707 Sentence Transformers v4によるリランカーモデルのトレーニングとファインチューニング
- /deep_1116 🤗 Optimum IntelとfastRAGによるCPU最適化エンベディング
- /deep_3085 テキスト埋め込みはテキストを完全にエンコードするか？——vec2textによる埋め込み逆変換の実証
- /deep_1440 Sentence TransformersによるマルチモーダルEmbedding・Rerankerモデルのサポート（v5.4）
- /deep_6085 LangGraphエージェントに3種類の記憶をTiDBで実装する──脅威インテリジェンスで学ぶSQL×ベクトル×全文検索

## 原文リンク

[HindsightのrerankerをGPUなしCPUで9倍高速化 — batch size最適化とONNX化](https://zenn.dev/valda68k/articles/hindsight-reranker-9x-cpu-ja)
