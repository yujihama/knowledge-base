---
title: "宇宙空間でのスケーラブルなAIインフラシステム設計の探索（Project Suncatcher）"
url: "https://research.google/blog/exploring-a-space-based-scalable-ai-infrastructure-system-design/"
date: 2026-04-03
tags: [TPU, 衛星コンステレーション, 自由空間光通信, DWDM, 太陽同期軌道, JAX, 分散MLコンピューティング, 放射線耐性, Project Suncatcher]
category: "infra"
memo: "[Google AI Blog] Exploring a space-based, scalable AI infrastructure system design"
related: [311, 1535, 312, 275, 418]
processed_at: "2026-04-03T12:02:14.838890"
---

## 要約

GoogleはProject Suncatcherと呼ばれる研究プロジェクトとして、太陽光発電衛星コンステレーションにTPUを搭載し、自由空間光通信リンク（Free-Space Optical Links）で接続することで宇宙規模のML計算基盤を構築する構想を発表した。2025年11月に公開されたプレプリント論文「Towards a future space-based, highly scalable AI infrastructure system design」がその詳細を記述している。

軌道設計として、夜明け-黄昏の太陽同期低軌道（高度650km付近）を採用し、ほぼ連続した太陽光照射を確保する。地上比最大8倍の太陽光発電効率が得られ、バッテリー重量を削減できる。

主要な技術課題は4点。第一に衛星間高帯域通信で、密波長分割多重（DWDM）トランシーバーと空間多重化により数十Tbpsの衛星間リンクを目指す。受信電力が距離の2乗に反比例するため、衛星間距離を1km以下の超密集編隊飛行で補う設計とし、ベンチスケールの実証機で単一トランシーバーペアによる1.6Tbps（各方向800Gbps）の伝送を達成済み。第二に衛星編隊制御で、Hill-Clohessy-Wiltshire方程式を出発点とし、JAXベースの微分可能モデルで地球重力場の非球面性・大気抵抗を考慮した数値精緻化を実施。衛星間距離100〜200mの編隊でも穏やかなステーションキーピングで安定維持可能と試算。第三にTPUの放射線耐性で、Google Trillium（v6e Cloud TPU）を67MeVプロトンビームで試験したところ、最も感度の高いHigh Bandwidth Memory（HBM）でも2krad(Si)まで不規則動作が生じず、5年間のシールド済み想定被曝量750rad(Si)の約3倍の耐性を確認。15krad(Si)までTIDによるハード故障なし。第四に経済的実現可能性で、打ち上げコストが2030年代中盤に200ドル/kg以下まで低下した場合、宇宙データセンターの運用コストが地上データセンターのエネルギーコストと同等水準になると試算している。

次のマイルストーンとして、衛星画像企業Planetと連携し、2027年初頭に2機のプロトタイプ衛星を打ち上げ予定。宇宙環境でのモデル動作・TPUハードウェア検証・光衛星間リンクによる分散ML処理の実証を目指す。熱管理、地上との高帯域通信、軌道上システム信頼性は今後の課題として残る。

## アイデア

- 衛星間距離を1km以下に圧縮することで、光通信の受信電力問題（距離の2乗則）を物理配置で解決するアプローチは、制約を回避するのではなく系全体の設計で吸収する典型例
- JAXの微分可能プログラミングモデルを軌道力学シミュレーションに適用している点が興味深い——ML研究用ツールが物理モデリングにも転用されている
- 商用TPU（Trillium）をそのまま宇宙環境試験にかけ、想定の3倍の放射線耐性が判明したという結果は、COTS（商用既製品）の宇宙利用可能性を示す実証データとして貴重

## 関連記事

- /deep_311 リレーショナルデータのためのグラフ基盤モデル
- /deep_1535 JAX / Flax で Stable Diffusion を高速推論する方法
- /deep_312 二階法、ファーストクラス化：曲率考慮訓練のための合成可能スタック
- /deep_275 二次法を一級市民に：曲率考慮型学習のための組み合わせ可能なスタック
- /deep_418 オープンな未来に向けて：Hugging FaceとGoogle Cloudの新たな戦略的パートナーシップ

## 原文リンク

[宇宙空間でのスケーラブルなAIインフラシステム設計の探索（Project Suncatcher）](https://research.google/blog/exploring-a-space-based-scalable-ai-infrastructure-system-design/)
