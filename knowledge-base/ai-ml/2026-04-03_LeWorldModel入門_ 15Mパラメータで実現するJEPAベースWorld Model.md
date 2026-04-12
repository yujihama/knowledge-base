---
title: "LeWorldModel入門: 15Mパラメータで実現するJEPAベースWorld Model"
url: "https://zenn.dev/0h_n0/articles/4da62f49ba81e1"
date: 2026-04-03
tags: [JEPA, World Model, ViT, SIGReg, 表現崩壊, 自己教師あり学習, ロボティクス, 潜在空間モデル, PyTorch]
category: "ai-ml"
memo: "[Zenn 機械学習] LeWorldModel入門 15Mパラメータで実現するJEPAベースWorld Model"
processed_at: "2026-04-03T21:07:17.982655"
---

## 要約

LeWorldModel（LeWM）はYann LeCunらが2026年3月に発表した研究（arXiv: 2603.19312）で、JEPA（Joint Embedding Predictive Architecture）を生ピクセルからend-to-endで安定学習する初の手法として報告されている。従来のWorld Modelには生成型（DreamerV3、IRISなど）と潜在空間型（TD-MPC2、DINO-WMなど）の2系統があり、いずれも計算コストや表現崩壊（representation collapse）という課題を抱えていた。LeWMはこれらの問題をアーキテクチャの工夫と新規正則化手法で解決する。

アーキテクチャはエンコーダ（ViT-Tiny、5Mパラメータ）とプレディクタ（Transformer、10Mパラメータ）の2コンポーネントで構成され、合計15Mパラメータ。エンコーダはDINO-WMと異なり事前学習済みモデルに依存せず、ゼロからend-to-endで学習する。出力は192次元の潜在トークンで、DINO-WMの約200分の1のトークン数で環境を表現する。

核心技術はSIGReg（Sketched-Isotropic-Gaussian Regularizer）と呼ばれる正則化手法で、Cramér-Wold定理に基づく。「高次元分布のすべての1次元射影がガウス分布に従えば元の分布は多変量ガウス分布」という定理を活用し、M個のランダム方向ベクトルへの射影に対してEpps-Pulley検定統計量を計算することで、潜在表現が等方的ガウス分布N(0,I)に近づくよう正則化する。損失関数は予測ロス（MSE）とSIGRegの2項のみで、実質的な調整ハイパーパラメータはλ=0.1の1つだけ。従来手法PLDMの7項目・6ハイパーパラメータと比べて大幅にシンプル。さらにstop-gradientもEMAも不要でend-to-end学習が可能という点が新規性の中心。

ベンチマーク結果では、Push-Tロボティクスタスクで96%の成功率を達成し、プランニング速度はDINO-WM比で48倍高速（0.98秒 vs 47秒）。一方、Two-RoomやOGBench-Cubeなど複雑な視覚入力や離散的タスクではDINO-WMに劣後するケースもある。単一GPUで数時間の学習が可能であり、大規模計算資源を持たない研究者・エンジニアがWorld Model研究に参入しやすくなる成果として位置付けられる。

## アイデア

- SIGRegによるCramér-Wold定理の活用：end-to-endJEPA学習の表現崩壊をstop-gradientやEMAなしに解決できる点は、他の自己教師あり学習タスクにも応用可能な汎用的な正則化アイデア
- 損失関数のシンプル化（2項・1ハイパーパラメータ）：複雑な多項目ロスを排除することで再現性と調整コストを大幅に下げた設計思想は、実用システム構築における教訓として価値がある
- 潜在表現の200分の1圧縮によるプランニング48倍高速化：モデルの軽量化が推論速度に直結することを示す実例であり、エッジデバイスやリアルタイム制御への応用可能性を示唆している
## 関連記事

- /deep_1478 TC-AE: 深圧縮オートエンコーダのトークン容量を解放する新アーキテクチャ
- /deep_884 PI-JEPA: 演算子分割潜在予測によるマルチフィジックスシミュレーションのラベルフリーサロゲート事前学習
- /deep_812 PI-JEPA: オペレータ分割潜在予測による連成マルチフィジクスシミュレーションのラベルフリーサロゲート事前学習
- /deep_294 Le MuMo JEPA：学習可能な融合トークンによるマルチモーダル自己教師あり表現学習
- /deep_113 金融時系列予測でLightGBM / LSTM / Transformerを比較してみた

## 原文リンク

[LeWorldModel入門: 15Mパラメータで実現するJEPAベースWorld Model](https://zenn.dev/0h_n0/articles/4da62f49ba81e1)
