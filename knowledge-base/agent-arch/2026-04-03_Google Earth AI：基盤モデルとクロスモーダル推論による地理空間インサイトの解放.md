---
title: "Google Earth AI：基盤モデルとクロスモーダル推論による地理空間インサイトの解放"
url: "https://research.google/blog/google-earth-ai-unlocking-geospatial-insights-with-foundation-models-and-cross-modal-reasoning/"
date: 2026-04-03
tags: [geospatial-AI, foundation-model, multi-agent, Gemini, cross-modal-reasoning, vision-language-model, Earth-observation, Population-Dynamics]
category: "agent-arch"
memo: "[Google AI Blog] Google Earth AI: Unlocking geospatial insights with foundation models and cross-modal reasoning"
related: [77, 233, 61, 168, 161]
processed_at: "2026-04-03T12:05:00.887897"
---

## 要約

Google Earth AIは、複数の地理空間基盤モデルとGeminiベースの推論エージェントを組み合わせた統合AIシステム。2025年10月に発表された最新版では、衛星画像解析、人口動態分析、環境予測の3系統の基盤モデルと、それらを統合オーケストレーションする地理空間推論エージェントが中心的な構成要素となっている。

衛星画像モデル「Remote Sensing Foundations」は、ビジョン言語モデル・オープン語彙物体検出・適応型ビジョンバックボーンの3機能を提供する。自然言語クエリ（例：「洪水した道路をすべて検出せよ」）に対応し、テキストベース画像検索タスクで平均16%以上の改善を達成。ゼロショット物体検出モデルはベースラインの2倍以上の精度を記録した。物体検出モデルRS-OWL-ViT-v2はOWL-ViT-v2と比較してAP50スコアで大幅な改善を示している。

人口動態モデル「Population Dynamics Foundations」は17カ国にわたるグローバル整合性エンベディングと月次更新エンベディングの2つのイノベーションを導入。オックスフォード大学の研究では、このエンベディングをブラジルのデング熱予測モデルに組み込むことで、12ヶ月予測のR²スコアが0.456から0.656に向上した。

環境モデルでは中期気象予報・モンスーン開始・大気質・河川洪水に加え、全球降水ナウキャストと20億人をカバーする洪水予測を新たに実装した。

複数モデルの統合効果も実証されており、Population Dynamics FoundationsとAlphaEarth Foundationsのエンベディングを融合することで、FEMAの全国リスク指数（20種の自然災害）の予測R²が平均11%改善。特にトルネード（+25%）と河川洪水（+17%）で顕著な改善がみられた。

地理空間推論エージェントはGeminiをベースとしており、自然言語クエリを多段階の実行計画に分解し、環境モデル・Data Commons・Earth Engine・BigQueryなどの外部データソースと連携するサブエージェントを逐次呼び出す。モジュール型のマルチエージェント構成により、拡張性とカスタマイズ性を両立している。

## アイデア

- 複数の専門基盤モデル（画像・人口・環境）を単一の推論エージェントがオーケストレーションする「エキスパートサブエージェント」設計は、監査エージェントにおける財務・法規制・リスク評価の各専門モデルを統合するアーキテクチャの参考になる
- 自然言語クエリを動的な多段階計画に分解し外部ツール・データストアを呼び出すエージェント設計は、LangGraphのConditional EdgeやReActパターンと親和性が高く、実装レベルで応用可能
- 単一モデルでなく複数エンベディングの融合でR²が平均11%向上するという実証結果は、マルチモーダル・クロスドメインアプローチの定量的な有効性を示しており、監査エージェントの精度向上戦略に直接援用できる
## 関連記事

- /deep_77 パーソナルヘルスエージェントの解剖：マルチエージェント構造による個人健康支援フレームワーク
- /deep_233 StreetReaderAI: コンテキスト認識型マルチモーダルAIによるストリートビューのアクセシビリティ向上
- /deep_61 Googleパーソナルヘルスコーチの構築方法：Geminiを活用したマルチエージェント健康指導システム
- /deep_168 Google Research 2025年振り返り：生成モデルの効率化・量子コンピューティング・科学的発見の加速
- /deep_161 鳥の音声で訓練されたAIが水中の謎を解明：Perch 2.0の転移学習

## 原文リンク

[Google Earth AI：基盤モデルとクロスモーダル推論による地理空間インサイトの解放](https://research.google/blog/google-earth-ai-unlocking-geospatial-insights-with-foundation-models-and-cross-modal-reasoning/)
