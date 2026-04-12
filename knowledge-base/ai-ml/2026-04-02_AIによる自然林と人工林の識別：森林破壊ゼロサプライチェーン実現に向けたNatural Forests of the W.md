---
title: "AIによる自然林と人工林の識別：森林破壊ゼロサプライチェーン実現に向けたNatural Forests of the World 2020マップ"
url: "https://research.google/blog/separating-natural-forests-from-other-tree-cover-with-ai-for-deforestation-free-supply-chains/"
date: 2026-04-02
tags: [Vision Transformer, Sentinel-2, 衛星画像解析, マルチモーダル, 時系列分類, セマンティックセグメンテーション, EUDR, 森林モニタリング, Google DeepMind]
category: "ai-ml"
memo: "[Google AI Blog] Separating natural forests from other tree cover with AI for deforestation-free supply chains"
processed_at: "2026-04-02T12:07:19.827170"
---

## 要約

GoogleDeepMindとGoogle Researchが、世界資源研究所（WRI）および国際応用システム分析研究所（IIASA）との共同研究で、「Natural Forests of the World 2020」を発表した。このマップはNature Scientific Dataに掲載され、地球上の自然林を人工植林・農地・プランテーションと区別する初の10メートル解像度グローバルマップである。精度は独立評価データセットに対して92.2%を達成している。

背景として、EU森林破壊規制（EUDR）が2020年12月31日以降に森林破壊・劣化した土地由来のコーヒー・カカオ・ゴム・木材・パーム油のEU域内販売を禁止したことがあり、企業・政府・NGOが自然林の正確な基準マップを必要としていた。既存の「樹冠被覆（tree cover）」マップは自然林と短命プランテーションを区別せず、規制対応・保全活動に不十分だった。

技術面では、マルチモーダル時空間ビジョントランスフォーマー（MTSViT: Multi-modal Temporal-Spatial Vision Transformer）を開発。Sentinel-2衛星の1年分の季節画像（時系列）と地形データ（標高・傾斜）、地理座標を組み合わせて入力とし、1280×1280メートルのパッチ単位で各10×10ピクセルが自然林である確率を推定する。単一スナップショットではなく年間の分光・時系列・テクスチャシグネチャを解析することで、均一に成長する商業プランテーションと複雑な自然林を区別する。訓練には120万以上のグローバルパッチサンプルが使用された。

今後は2026年に、Primary Forest・Naturally Regenerating Forest・Planted Forest・Plantation Forest・Tree Crops・Other Land Coverの6クラスを識別する多年度シリーズマップを公開予定。また、研究コミュニティ向けに2つのベンチマークデータセット（64種類の植林・樹木作物を含む230万サンプルの「Planted dataset」と、20万パッチのセマンティックセグメンテーション用「ForTy」）を公開している。データはGoogle Earth Engine経由で利用可能。

## アイデア

- 1年分の時系列衛星データを単一モデルで処理するMTSViTのアーキテクチャ：静止画ではなく動的シーケンスで「文脈」を学習させることで、見た目が似た対象（自然林 vs 人工林）を高精度分類できる点は、監査対象の時系列ログからパターンを識別するエージェント設計に応用可能
- 規制コンプライアンス（EUDR）を直接ターゲットにしたAIベースライン生成：法的要件から逆算してデータセット・評価基準・精度目標を設計するアプローチは、内部監査AIにおける証拠収集・根拠形成フレームワークの設計と構造が似ている
- 120万サンプルの自己構築訓練データと独立評価データセットの分離：ラベルの信頼性を確保するために既存の別目的データセット（2015年管理分類データ）を2020年向けに再ラベリングして使用する手法は、監査領域でラベル付きデータが少ない場合の訓練データ構築戦略として参考になる
## 関連記事

- /deep_218 AIで森林の未来を予測する：損失の計測からリスク予測へ（ForestCast）
- /deep_692 スマートレースロックセンサーを用いた座位から立位への移行検出と継続時間計測
- /deep_1297 HorizonWeaver: 自動運転シーンのための汎化可能なマルチレベルセマンティック編集
- /deep_607 Car-GPT：LLMは自動運転を実現できるか？
- /deep_927 Car-GPT：LLMは自動運転を実現できるか？

## 原文リンク

[AIによる自然林と人工林の識別：森林破壊ゼロサプライチェーン実現に向けたNatural Forests of the World 2020マップ](https://research.google/blog/separating-natural-forests-from-other-tree-cover-with-ai-for-deforestation-free-supply-chains/)
