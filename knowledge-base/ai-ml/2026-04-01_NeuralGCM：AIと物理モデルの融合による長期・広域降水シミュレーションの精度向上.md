---
title: "NeuralGCM：AIと物理モデルの融合による長期・広域降水シミュレーションの精度向上"
url: "https://research.google/blog/neuralgcm-harnesses-ai-to-better-simulate-long-range-global-precipitation/"
date: 2026-04-01
tags: [NeuralGCM, hybrid-model, neural-parameterization, precipitation-forecast, climate-simulation, differential-dynamics, satellite-observation, WeatherBench2, ECMWF, IMERG]
category: "ai-ml"
memo: "[Google AI Blog] NeuralGCM harnesses AI to better simulate long-range global precipitation"
related: [116, 115]
processed_at: "2026-04-01T09:11:13.078882"
---

## 要約

GoogleリサーチのJanni Yuval氏らが、ハイブリッド大気モデル「NeuralGCM」を降水シミュレーション向けに強化した研究をScience Advancesに発表した。NeuralGCMは従来の流体力学ソルバー（物理ベース）とニューラルネットワーク（機械学習）を組み合わせたハイブリッドアーキテクチャを採用しており、雲形成・放射・降水といった小スケール物理過程をMLで近似する。

従来の気象・気候モデルは「パラメータ化」と呼ばれる近似式で小スケール過程を表現するが、これには降水極端値や日周期の再現において限界があった。NeuralGCMの旧バージョンを含む多くのMLモデルは、再解析データ（物理モデルと観測を統合した過去大気状態の再現データ）を学習データとして使用しており、再解析の弱点をそのまま引き継ぐ問題があった。

今回の改良では、NeuralGCMの微分可能な動力学コア（differential dynamical core）インフラを活用し、MLコンポーネントをNASAの衛星降水観測データ（GPM/IMERG、2001〜2018年）で直接学習させた。これにより再解析を経由せずに高品質な実観測から降水パラメータ化を学習できる点が本手法の核心である。

評価結果として、WeatherBench 2ベンチマークを用いた2020年全日の15日先予報において、NeuralGCMはECMWF（欧州中期予報センター）の低解像度物理モデルを24時間・6時間積算降水量の両指標で全15日間にわたり有意に上回った。長期評価では、IPCC最新報告書で使用される主要大気モデル群（AMIP）と比較してNeuralGCMの平均絶対誤差が0.5mm/日未満となり、平均誤差を約40%削減、陸上ではさらに大きな改善を達成した。また降水極端値（上位0.1%の豪雨イベント）の再現精度でも大幅な改善が確認された。

現在の解像度は280kmであり、運用的な天気予報には粗すぎるが、手法の有効性は示されており、より高解像度への適用が今後の課題とされている。NeuralGCMはオープンソースとして公開されており、Earth AIの取り組みの一環としてWeatherNext 2などAI専用モデルと相補的な位置づけとされている。

## アイデア

- 再解析データではなく実観測（衛星データ）でMLコンポーネントを直接学習させる手法：物理ソルバーの微分可能性があってはじめて実現できるアーキテクチャ設計で、「データソースの品質がそのままモデル性能の上限を決める」という原則の実践例
- 物理モデル＋MLのハイブリッドアーキテクチャにおける役割分担：大スケール過程は物理ソルバー、小スケール過程（雲・降水）はNN、という分業が精度・解釈性・汎化性能を両立する設計パターンとして参考になる
- 280km解像度でも極端値（上位0.1%豪雨）の再現精度が大幅改善：スケール不一致の問題を統計的学習で補完する手法は、他ドメインの異常検知・リスク定量化にも転用可能な発想
## 関連記事

- /deep_116 AIを活用した都市型鉄砲水（フラッシュフラッド）予測システムの展開
- /deep_115 AIを活用した都市型鉄砲水予測で都市を守る：Googleの新手法

## 原文リンク

[NeuralGCM：AIと物理モデルの融合による長期・広域降水シミュレーションの精度向上](https://research.google/blog/neuralgcm-harnesses-ai-to-better-simulate-long-range-global-precipitation/)
