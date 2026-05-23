---
title: "Mamba解説：Transformerに挑む状態空間モデル（SSM）"
url: "https://thegradient.pub/mamba-explained/"
date: 2026-05-23
tags: [Mamba, SSM, 状態空間モデル, HiPPO, SelectiveSSM, 長文脈, 線形注意]
category: "ai-ml"
related: [2510, 2480, 1837, 3105, 5810]
memo: "[The Gradient] Mamba Explained"
processed_at: "2026-05-23T09:20:51.739298"
---

## 要約

MambaはAlbert GuとTri Daoが開発した状態空間モデル（SSM）ベースのシーケンスモデルで、Transformerの二次計算量ボトルネックを回避しながら同等以上の性能を実現する。Transformerのself-attentionはトークン数nに対してO(n²)の計算量とO(n)のKVキャッシュを要するため、長文脈では推論速度・メモリ双方で限界がある。Mambaはこれをコントロール理論由来のSSMで置き換え、O(n)線形スケーリングを達成する。

SSMの基本式はh'(t)=Ah(t)+Bx(t)（状態遷移）とy(t)=Ch(t)+Dx(t)（出力）の連立微分方程式で、隠れ状態hが過去の圧縮表現として機能する。連続時間微分方程式を離散化するためZero-Order Hold（ZOH）を用い、実装上の差分方程式に変換する。行列AのHiPPO初期化（Legendre多項式基底）により、遠い過去の情報を効率よく保持できる。

従来のSSMと差別化するMambaの核心は「選択的状態空間（Selective SSM / S6）」にある。行列B・C・Δ（ステップサイズ）を入力xの関数として動的に生成することで、重要なトークンを選択的に状態へ取り込み、不要な情報を無視できる。これはTransformerのattentionが入力に応じてどのトークンに注目するかを決める機構と類似しており、従来の線形時不変SSMが持っていた「全入力を等しく処理する」という制約を克服している。

しかしΔが入力依存になると、カーネル畳み込みによる並列学習トリックが使えなくなる。Mambaはこれを「ハードウェア対応パラレルスキャン（並列接頭辞和）」で解決し、HBMアクセスを最小化するFlashAttention類似のカーネル融合実装によりGPU上で効率的に動作する。

性能面では、Mamba-3Bが同サイズTransformerを凌駕し、2倍サイズのTransformerに匹敵する。推論速度はTransformerの最大5倍。ただし現時点の限界として、Transformerより大きなメモリ帯域幅を消費すること、回路解析などの解釈可能性研究がAttentionほど成熟していないこと、in-context learningでTransformerより弱い可能性があることが指摘されている。

監査エージェント開発への示唆：長文書（契約書・監査調書・取引ログ）を100万トークン規模で処理するシナリオでMambaは有力な代替backbone。ただしin-context learningの弱さは、few-shotでルールを与えるプロンプト設計に影響する可能性があり、ファインチューニング主体のアーキテクチャ設計が適切か検討が必要。

## アイデア

- 隠れ状態hを「過去の圧縮」として定式化する発想は、Transformerが全トークンを明示的にキャッシュするのと根本的に異なる情報管理哲学であり、固定サイズのRAMで無限の過去を近似する方向性はエージェントのメモリ設計にも応用可能
- B・C・Δを入力依存にした『選択的SSM』は、LSTMゲート機構の連続時間版とも解釈でき、ゲート付きRNNの系譜をSSMの枠組みで再統一した点が興味深い
- HiPPOによるA行列の初期化（Legendre多項式でタイムスタンプ重み付き内積を近似）は、単なる乱数初期化より遠距離依存を学習しやすい帰納的バイアスを与えており、時系列監査ログへの応用で有効な事前知識となりうる

## 前提知識

- **Transformer / Self-Attention** (TODO: 読むべき)
- **RNN / LSTM** (TODO: 読むべき)
- **状態空間モデル（SSM）** → /deep_926 Mamba解説：Transformerに挑む状態空間モデル（SSM）
- **HiPPO** → /deep_195 Mamba解説：TransformerへのState Space Modelによる挑戦
- **FlashAttention** → /deep_221 Differential Transformer V2：カスタムカーネル不要・推論高速化を実現した差分注意機構の改良版

## 関連記事

- /deep_2510 多層SSMの表現能力と限界：深さ・精度・Chain-of-Thoughtの相互作用
- /deep_2480 量子化へのKLレンズ：混合精度SSM-Transformerモデルの高速・順伝播のみの感度分析
- /deep_1837 UNDO Flip-Flop：状態空間モデルにおける可逆的意味状態管理の制御プローブ
- /deep_3105 Sessa: 選択的状態空間アテンション — フィードバックパス内にアテンションを組み込む新デコーダ
- /deep_5810 MambaRain：0〜3時間降水予測のためのマルチスケールMamba-Attentionフレームワーク

## 原文リンク

[Mamba解説：Transformerに挑む状態空間モデル（SSM）](https://thegradient.pub/mamba-explained/)
