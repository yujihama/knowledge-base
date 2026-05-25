---
title: "Pocket Foundation Models：表形式基盤モデルをCPU対応の勾配ブースティング木に蒸留する"
url: "https://tldr.takara.ai/p/2605.18654"
date: 2026-05-25
tags: [知識蒸留, XGBoost, CatBoost, 表形式基盤モデル, In-Context Learning, TabICLv2, OOF, CPU推論, TabTune]
category: "ai-ml"
related: [1429, 634, 569, 1116, 1936]
memo: "[HF Daily Papers] Pocket Foundation Models: Distilling TFMs into CPU-Ready Gradient-Boosted Trees"
processed_at: "2026-05-25T09:13:54.315115"
---

## 要約

表形式データ向け基盤モデル（Tabular Foundation Models, TFM）は高精度だが、GPU上でも151〜1,275 msの推論レイテンシがあり、不正検知スコアラーが要求する2 ms以下の応答時間に対応できない。本論文はこのギャップを解消するために、TFMをオフラインでXGBoostまたはCatBoostに知識蒸留し、CPUネイティブで動作させる手法「Pocket Foundation Models」を提案する。

最大の技術的課題は、In-Context Learning（ICL）型のティーチャーモデルが自身の学習セットをスコアリングする際にラベルが漏洩し、ソフトターゲットがほぼワンホットに退化してクラス間の構造情報が失われる点である。これを解決するために、Stratified Out-of-Fold（OOF）ティーチャーラベリングを採用した。訓練データをK分割し、各フォールドのサンプルはそのフォールドを除いたモデルによってスコアリングされることで、ラベル漏洩を防ぎながら適切な確率分布を持つソフトターゲットを生成する。

実験はTALENT、OpenML-CC18、TabZilla、TabArenaから収集した153の分類データセットで実施。TabICLv2をXGBoostに蒸留した結果、マクロ平均AUCは0.882（ティーチャーのAUCの96.5%）を達成し、推論速度は1.9 ms（CPU）で、ティーチャー比38〜860倍の高速化を実現。チューニング済みCatBoostベースラインに対してWilcoxon検定でp=0.0008、勝率51%と統計的に有意な優位性を示した。

4つの追加知見も重要：(1) ティーチャーのデータセット間順位がスチューデントにほぼそのまま転移する；(2) 低次元データ（特徴量21未満）でCatBoostに対して+0.011の改善が得られるが、高次元（21超）では+0.001にとどまる；(3) マルチティーチャー平均はMLPスチューデントに有効（+0.006、p=0.003）だが木モデルへの寄与は0.001未満；(4) ティーチャー自体がCatBoostに劣る高次元タスクでは蒸留が逆効果になる。

パイプライン全体はTabTuneライブラリとしてOSSで公開されている。監査エージェント開発への示唆として、リアルタイム異常検知や取引スコアリングにおいて、基盤モデルの精度を維持しながらCPUのみで高速推論を実現できる点は、エッジ環境やオンプレミス制約下での監査AIシステム構築に直接応用可能である。

## アイデア

- ICLティーチャーのラベル漏洩問題をStratified OOFで解決するアイデアは、自己参照型モデルの蒸留における汎用的な落とし穴として他ドメインにも応用できる
- ティーチャーの性能順位がスチューデントに転移するという知見は、モデル選択コストを大幅に削減できる実用的な原則になりうる
- 低次元データ（<21特徴量）でのみ蒸留効果が顕著という発見は、特徴量エンジニアリングの重要性と蒸留適用条件の指針を同時に与える

## 前提知識

- **知識蒸留** → /deep_2424 エンタープライズAIをオペレーティングレイヤーとして扱う：Ensembleが示す構造的優位性
- **XGBoost/CatBoost** (TODO: 読むべき)
- **In-Context Learning** → /deep_296 LLMによるインコンテキスト分子特性予測：記憶と知識コンフリクトに関するブラインド研究
- **Cross-validation/OOF** (TODO: 読むべき)
- **TabularFM** (TODO: 読むべき)

## 関連記事

- /deep_1429 非エンジニアがKaggleで3999チーム中1257位になった話
- /deep_634 TrialsBankを用いた臨床試験の運用成功予測のための潜在リスク認識機械学習アプローチ
- /deep_569 TrialsBankを用いた臨床試験の運用成功を予測する潜在リスク認識型機械学習アプローチ
- /deep_1116 🤗 Optimum IntelとfastRAGによるCPU最適化エンベディング
- /deep_1936 🤗 APIユーザー向けTransformer推論を100倍高速化した方法

## 原文リンク

[Pocket Foundation Models：表形式基盤モデルをCPU対応の勾配ブースティング木に蒸留する](https://tldr.takara.ai/p/2605.18654)
