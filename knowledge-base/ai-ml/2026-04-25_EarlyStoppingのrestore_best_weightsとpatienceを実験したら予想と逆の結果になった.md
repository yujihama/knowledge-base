---
title: "EarlyStoppingのrestore_best_weightsとpatienceを実験したら予想と逆の結果になった【Keras】"
url: "https://zenn.dev/wasurenamemo/articles/c63a35fb5f11ae"
date: 2026-04-25
tags: [Keras, EarlyStopping, restore_best_weights, patience, CIFAR-10, 過学習, ディープラーニング, TensorFlow]
category: "ai-ml"
related: [2783, 2656, 1578, 109, 1886]
memo: "[Zenn 機械学習] EarlyStoppingのrestore_best_weightsとpatience、実験したら予想と逆の結果になった【Keras】"
processed_at: "2026-04-25T12:54:40.312176"
---

## 要約

KerasのEarlyStoppingコールバックにおける2つの設定（restore_best_weights と patience）を、CIFAR-10データセット＋GAP＋Dropout=0.2のCNNモデルで実際に実験した結果をまとめた記事。一般的に「restore_best_weights=Trueにすれば精度が上がる」「patience=3は短すぎる」と言われる定説を実験で検証したところ、どちらも文脈依存であることが明らかになった。

実験①（restore_best_weights=True vs False、patience=5固定）では、TrueのパターンAがtest_accuracy 70.58%、FalseのパターンBが71.10%と、Falseの方が高精度という逆転結果になった。原因はモデルの収束速度にある。このモデルはval_lossがEp50時点でもまだ下降中であり、「最良エポック」がEp50付近に集中していたため、Trueで復元される重みとFalseの最終重みがほぼ同一エポック由来となり、差が生じにくかった。一方、過学習が進んだモデルでは最良重みと最終重みの乖離が大きくなるため、restore_best_weights=Trueの効果が顕著になる。

実験②（patience=3/10/なしをrestore_best_weights=True固定で比較、epochs=50）では、C（patience=3）がEp40で停止しtest_accuracy 67.89%、D（patience=10）がEp50まで走り71.28%、E（EarlyStoppingなし）がEp50で70.50%となった。CはEp37が最良でそこから3ep改善がなかったためEp40停止となったが、Ep39〜50でDとEはval_lossをさらに改善し続けており、patience=3が約3.4%の精度損失を招いた。

DとEの0.78%の差（71.28% vs 70.50%）はrestore_best_weightsの効果そのものであり、設定1つが実測の精度差として現れた。また3パターンとも「早期停止」として機能しなかった根本原因は、epochsの上限を50と低く設定したことにある。EarlyStoppingはepochsを十分大きく（100〜200）設定することが前提であり、上限が低すぎると「改善が止まるタイミング」自体が上限付近に来るモデルでは機能しない。

推奨設定はmonitor='val_loss'、patience=10以上、restore_best_weights=True、epochs=200。設定の効果はモデルの収束特性とepochs上限の組み合わせに強く依存するため、「定説」をそのまま適用するのではなく、モデルごとに学習曲線を確認した上で調整することが重要。監査エージェント開発における学習コスト最適化の観点でも、早期停止の誤設定による無駄な再学習リスクへの示唆がある。

## アイデア

- EarlyStoppingの効果はモデルの収束速度とepochs上限の組み合わせに依存するため、設定の「定説」が成立しない条件が存在することを実験で定量的に示した点
- restore_best_weightsとpatienceの効果を切り離して比較することで、それぞれの寄与（0.78%差と3.4%差）を独立に定量化できた実験設計の明確さ
- EarlyStoppingがepochsの上限設定によって『早期停止として機能しなくなる』という見落とされがちな前提条件を、実測データで可視化した点

## 前提知識

- **Keras EarlyStopping** (TODO: 読むべき)
- **val_loss監視** (TODO: 読むべき)
- **過学習・正則化** (TODO: 読むべき)
- **CIFAR-10** → /deep_2220 GF-Score: 公平性保証付きクラス別認定ロバストネス評価フレームワーク
- **CNN (Dropout, GAP)** (TODO: 読むべき)

## 関連記事

- /deep_2783 Kerasのmodel.summary()を正しく読む：パラメータ数の計算方法を図解
- /deep_2656 KerasのMaxPooling pool_sizeを変えたら予想外の結果になった話【GAP vs Flatten で挙動が逆転】
- /deep_1578 Hugging FaceのTensorFlow哲学：KerasネイティブなTransformersの設計方針
- /deep_109 機械学習入門講義メモ：ゼロから作るDeep Learningをベースに
- /deep_1886 ニューラルネットワーク構築における実践的デバッグ指針：シンプルな思考プロセス

## 原文リンク

[EarlyStoppingのrestore_best_weightsとpatienceを実験したら予想と逆の結果になった【Keras】](https://zenn.dev/wasurenamemo/articles/c63a35fb5f11ae)
