---
title: "TransformersとTokenizersを使ってゼロから新しい言語モデルを学習する方法"
url: "https://huggingface.co/blog/how-to-train"
date: 2026-04-15
tags: [RoBERTa, BPE, Masked Language Modeling, Transformers, Tokenizers, スクラッチ学習, HuggingFace, ファインチューニング, POS tagging]
category: "ai-ml"
related: [1529, 1760, 1214, 1852, 1448]
memo: "[HF Blog] How to train a new language model from scratch using Transformers and Tokenizers"
processed_at: "2026-04-15T12:49:34.658250"
---

## 要約

HuggingFaceのTransformersおよびTokenizersライブラリを使い、エスペラント語のコーパスからRoBERTaベースの言語モデル「EsperBERTo」をスクラッチ学習する手順を解説したチュートリアル。モデルサイズは84Mパラメータ（6層、隠れ次元768、12ヘッド）でDistilBERTと同規模。

【データ収集】INRIAのOSCARコーパス（Common Crawlから言語フィルタリング）のエスペラント語部分とLeipzig Corpora Collectionを結合し、合計約3GBのテキストコーパスを構築。

【トークナイザー学習】GPT-2と同じByte-level BPEトークナイザーを語彙数52,000で学習。WordPieceではなくByte-level BPEを採用することで、全単語をトークンに分解でき<unk>トークンが発生しない。RoBERTaと同じ特殊トークン（<s>, <pad>, </s>, <unk>, <mask>）を設定。学習時間は約5分。エスペラント固有の発音記号（ĉ, ĝ, ĥ, ĵ, ŝ, ŭ）がネイティブにエンコードされ、汎用GPT-2トークナイザーと比較してエンコード後のシーケンス長が約30%短縮される。

【モデル学習】run_language_modeling.pyスクリプトを使ってRoBERTa-likeモデルをMasked Language Modeling（MLM）タスクでスクラッチ学習。--model_name_or_pathをNoneに設定することでゼロからの学習が可能。ハイパーパラメータはlr=1e-4、エポック数5、バッチサイズ16/GPU。DatasetサブクラスでByte-level BPEトークナイザーによるバッチエンコードを実装し、パディングはバッチレベルで実施。

【評価・ファインチューニング】品詞タギング（POS tagging）の下流タスクでファインチューニングを実施。EsperBERToは多言語BERTやXLMよりも高い精度を達成し、同言語のデータで事前学習した専用モデルの優位性を実証。Perplexityはエポック進行とともに低下し、最終的に妥当な値に収束したことをTensorboardで確認。

監査エージェント開発への示唆としては、特定ドメイン（監査用語・法規制テキスト等）に特化したトークナイザーをスクラッチ学習することで、汎用モデルより効率的かつ精度の高いドメイン特化LLMを構築できる点が参考になる。3GBという比較的小規模なコーパスでも実用的なモデルが得られることは、監査ログや報告書等の限られたデータでの事前学習可能性を示唆する。

## アイデア

- Byte-level BPEトークナイザーをドメイン固有コーパスでスクラッチ学習することで、汎用トークナイザー比でシーケンス長を約30%削減できる——監査・法律ドメインでも同様の効率化が期待できる
- 3GBという小規模コーパスでも84Mパラメータのモデルが多言語BERTを品詞タギングで上回ることから、ドメイン特化小規模モデルが汎用大規模モデルに勝てる領域が存在することを実証している
- MLMによる事前学習→下流タスクファインチューニングのパイプラインをフルスクラッチで構築する手順が体系化されており、カスタムドメインLLM開発のテンプレートとして再利用可能

## 前提知識

- **Transformer** → /deep_99 LLM Architecture Gallery徹底解説：30+モデルの内部構造を4軸で横断比較する
- **BERT / RoBERTa** (TODO: 読むべき)
- **Byte-level BPE** (TODO: 読むべき)
- **Masked Language Modeling** (TODO: 読むべき)
- **ファインチューニング** → /deep_530 AIモデルカスタマイズへの移行はアーキテクチャ上の必須事項

## 関連記事

- /deep_1529 🤗 TransformersによるWhisperの多言語ASRファインチューニング
- /deep_1760 🤗 TransformersでViTを画像分類にファインチューニングする
- /deep_1214 LoRAを用いたRoBERTa・Llama 2・Mistral 7Bの災害ツイート分類性能比較
- /deep_1852 Hugging Face コースローンチ コミュニティイベント（2021年11月）
- /deep_1448 Hugging Face Inference Endpointsへの移行事例：ECS+FargateからのMLモデルデプロイ刷新

## 原文リンク

[TransformersとTokenizersを使ってゼロから新しい言語モデルを学習する方法](https://huggingface.co/blog/how-to-train)
