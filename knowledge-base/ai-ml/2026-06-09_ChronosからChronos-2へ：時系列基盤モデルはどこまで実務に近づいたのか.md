---
title: "ChronosからChronos-2へ：時系列基盤モデルはどこまで実務に近づいたのか"
url: "https://zenn.dev/yuyu1/articles/20ae73561a6f77"
date: 2026-06-09
tags: [Chronos, Chronos-2, 時系列基盤モデル, Patch Embedding, Group Attention, Time Attention, 共変量予測, 分位点予測, zero-shot forecasting, T5]
category: "ai-ml"
related: [1758, 1489, 5981, 7409, 6929]
memo: "[Zenn 機械学習] ChronosからChronos-2へ：時系列基盤モデルはどこまで実務に近づいたのか"
processed_at: "2026-06-09T09:09:24.749843"
---

## 要約

AmazonのChronosは、時系列データを量子化によって離散トークンに変換し、T5ベースの言語モデルで次トークンを予測するアプローチを採用した時系列基盤モデルである。数値をスケーリング後に区間分割してトークンIDに変換することで、連続値回帰ではなくクロスエントロピー損失による分類問題として扱い、確率的サンプリングでP10/P50/P90などの予測区間を出力できる。ただし元のChronosは単変量予測に特化しており、価格・キャンペーン・休日などの共変量（covariates）を明示的に扱えない、カレンダー情報を使わない、量子化による情報損失が生じるという限界があった。

Chronos-2はこれらの課題に対応した発展版であり、最大の変更点は3つある。第一に、トークン化からPatch Embeddingへの転換。時系列をpatch length=16点単位で切り出し、連続的な埋め込みベクトルとして扱うことで、context length=8192点を512パッチに圧縮して計算量を抑制しつつ長期履歴を参照できる。第二に、Time AttentionとGroup Attentionの二段階アテンション機構。Time Attentionは単一時系列内の時間方向の依存関係を捉え、Group Attentionは同一グループ内の複数時系列・共変量間の関係を統合する。これにより「売上＋価格＋キャンペーン＋休日」を一つのgroupとして入力し、相互参照しながら予測できる。第三に、単変量・多変量・共変量付き予測を単一モデルで学習する混合学習戦略。context length 2048で基礎能力を学習後、8192に拡張して長期季節性を習得する2段階学習を採用。出力は21分位点（P10〜P99）の確率的予測。

実験（fev-bench、GIFT-Eval、Chronos Benchmark II）では、共変量を使用するタスクで特に強みが現れ、多変量のみのタスクでは改善幅が小さいケースもある。限界として、groupの構成はユーザーが設計する必要があり、無関係な変数を混入するとノイズになる点、テキスト形式の非構造化データは扱えない点、合成データ依存がある点が残る。MOMENTとの比較では、Chronos-2はforecastingに特化した実務向け汎用予測モデルで、MOMENTは分類・異常検知・補完など複数タスクをカバーする表現モデルという位置づけの違いがある。

## アイデア

- トークン化から連続Patch Embeddingへの転換：元のChronosが量子化による情報損失を抱えていたのに対し、Chronos-2はpatch単位の連続埋め込みに移行することで、精度と長文脈処理の両立を図った設計転換が興味深い
- Group Attentionによるcold-start対応：履歴が短い新規時系列でも、同一グループ内の関連変数からGroup Attentionで情報を補完できる可能性があり、監査エージェントでの異常検知（新規データソース追加時）への応用が考えられる
- groupの構成がドメイン知識に依存する問題：どの変数を同一groupに含めるかの設計はユーザー責任であり、これはRAGにおける検索粒度設計やエージェントのツール選択設計と構造的に類似した「知識構造化」の問題として捉えられる

## 前提知識

- **Transformer** → /deep_2420 TransformersモデルをMLXに移植するSkillとテストハーネスの構築：オープンソースにおけるエージェント時代の貢献とは
- **T5** → /deep_267 Speculative Cascades：LLM推論を高速化・高品質化するハイブリッドアプローチ
- **量子化（Quantization）** (TODO: 読むべき)
- **時系列予測** → /deep_113 金融時系列予測でLightGBM / LSTM / Transformerを比較してみた
- **Patch Embedding** (TODO: 読むべき)

## 関連記事

- /deep_1758 🤗 TransformersにおけるConstrained Beam Searchによるテキスト生成の制御
- /deep_1489 高速トレーニングと推論: Habana Gaudi2 vs Nvidia A100 80GB ベンチマーク比較
- /deep_5981 事前学習済みエンコーダ・デコーダTransformerを用いたSeq2Seq構成素解析
- /deep_7409 【図解】BERT・GPT・T5は何が違う？ エンコーダ/デコーダ/エンコーダデコーダを具体例で整理
- /deep_6929 【全13回】時系列予測の最前線——ARIMAからFoundation Models・LLMまで、実務で「どの手法を選ぶか」を決める

## 原文リンク

[ChronosからChronos-2へ：時系列基盤モデルはどこまで実務に近づいたのか](https://zenn.dev/yuyu1/articles/20ae73561a6f77)
