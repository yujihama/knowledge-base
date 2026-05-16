---
title: "CNNのDense層をReLUからELUに変えたら精度が上がった話【Keras×CIFAR-10】"
url: "https://zenn.dev/wasurenamemo/articles/df23a488b99545"
date: 2026-05-02
tags: [CNN, ReLU, ELU, GELU, Keras, CIFAR-10, 活性化関数, Dying ReLU, Dense層]
category: "ai-ml"
related: [2656, 109, 2965, 3410, 2837]
memo: "[Zenn 機械学習] CNNのDense層をreluからeluに変えたら精度が上がった話【Keras×CIFAR-10】"
processed_at: "2026-05-02T12:45:03.940104"
---

## 要約

KerasでCIFAR-10を分類するCNNモデルにおいて、Dense層の活性化関数をReLU/GELU/ELUの3種で比較した実験報告。モデル構成はConv2D×2層（活性化はReLU固定）＋Global Average Pooling＋Dropout(0.2)＋Dense層で、Dense層の活性化関数のみを変数として30エポック学習した。結果はELUが68.72%、GELUが68.18%、ReLUが67.52%のテスト精度となり、ELUがReLU比で約1.2%上回った。学習時間はGELU・ELUがともに約123秒でReLUの133秒より速かった。ReLUが最下位となった原因として「死んだReLU問題（Dying ReLU）」が挙げられる。ReLUは負の入力に対して出力がゼロになり勾配も消失するため、CIFAR-10のような複雑なタスクでは負の値を持つニューロンが学習に寄与できなくなるケースが蓄積し、モデルの表現力が制限される。一方ELUは負の入力に対して指数関数的に負の値を返し（ELU(x) = α(e^x - 1), x<0）、GELUはガウス累積分布関数に基づく滑らかな近似で負領域でも非ゼロ出力を維持するため、どちらも上記の問題を回避できる。GELUはBERTやGPTなどのTransformerモデルで標準採用されており大規模モデルでの優位性が知られるが、CNN構成ではELUがわずかに上回った。今回はConv2D層のReLUを固定したまま Dense層のみを変更したため最大差は1.2%にとどまったが、全層をELU/GELUに変更すればさらに差が広がる可能性がある。MNISTでは3種の差がほぼゼロだった点との対比から、タスクの複雑度が高まるほど活性化関数の選択が精度に与える影響が顕在化することも示唆されている。監査エージェント開発への直接的な示唆は薄いが、内部分類器やスコアリング層にDenseネットワークを使う場面では、ReLUを慣習的に選択するのではなくELUやGELUを検討する価値があることを定量的に示した実用的な参考事例となる。

## アイデア

- タスクの難易度（MNIST vs CIFAR-10）によって活性化関数の選択効果が変化するという実証：単純タスクで差がなくても複雑タスクで差が出る現象は、ハイパーパラメータ探索の優先度設計に示唆を与える
- Dense層のみの変更（Conv2D固定）でも1.2%の精度差が出た点：局所的な変更が全体精度に影響する経路として、特徴量の最終統合段階における情報損失の抑制効果が確認できる
- GELUがTransformerで標準採用されているのにCNNではELUに若干劣った点：アーキテクチャのコンテキストによって最適な活性化関数が異なる可能性を示しており、転用時の注意点となる

## 前提知識

- **CNN（畳み込みニューラルネットワーク）** (TODO: 読むべき)
- **ReLU / ELU / GELU** (TODO: 読むべき)
- **Dying ReLU問題** (TODO: 読むべき)
- **Global Average Pooling** (TODO: 読むべき)
- **CIFAR-10** → /deep_2220 GF-Score: 公平性保証付きクラス別認定ロバストネス評価フレームワーク

## 関連記事

- /deep_2656 KerasのMaxPooling pool_sizeを変えたら予想外の結果になった話【GAP vs Flatten で挙動が逆転】
- /deep_109 機械学習入門講義メモ：ゼロから作るDeep Learningをベースに
- /deep_2965 EarlyStoppingのrestore_best_weightsとpatienceを実験したら予想と逆の結果になった【Keras】
- /deep_3410 Adamのlearning_rateを変えたら3パターン全部挙動が違った【Keras×CIFAR-10実験】
- /deep_2837 非対称損失関数を用いたハイブリッドCNN-BiLSTM-Attentionモデルによる産業機器の残余寿命予測と解釈可能な故障ヒートマップ

## 原文リンク

[CNNのDense層をReLUからELUに変えたら精度が上がった話【Keras×CIFAR-10】](https://zenn.dev/wasurenamemo/articles/df23a488b99545)
