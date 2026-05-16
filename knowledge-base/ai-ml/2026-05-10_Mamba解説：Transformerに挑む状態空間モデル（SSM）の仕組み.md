---
title: "Mamba解説：Transformerに挑む状態空間モデル（SSM）の仕組み"
url: "https://thegradient.pub/mamba-explained/"
date: 2026-05-10
tags: [Mamba, SSM, State Space Model, Transformer, シーケンスモデル, 線形スケーリング, 離散化, ZOH, 選択性, 長文脈]
category: "ai-ml"
related: [3105, 2480, 2510, 1975, 199]
memo: "[The Gradient] Mamba Explained"
processed_at: "2026-05-10T09:26:05.449622"
---

## 要約

MambaはAlbert GuとTri Daoが開発した状態空間モデル（SSM）ベースのシーケンスモデルで、Transformerのアテンション機構が抱える計算量の問題を解消することを目的としている。Transformerは全トークン間のペアワイズ通信を行うため、訓練時の計算量がO(n²)、推論時のKVキャッシュがO(n)となり、コンテキスト長の増大に伴って速度・メモリが急激に劣化する。Mambaはこの「二次ボトルネック」をControl Theory（制御理論）由来のSSMで置き換えることで、シーケンス長に対して線形スケーリングを実現する。

基本的な数式は連続時間の微分方程式 h'(t) = Ah(t) + Bx(t)、y(t) = Ch(t) + Dx(t) であり、隠れ状態hが過去の情報を圧縮した「状態」として機能する。実装上は連続時間方程式をZero-Order Hold（ZOH）離散化によって差分方程式に変換し、h_t = Ā·h_{t-1} + B̄·x_t、y_t = C·h_t の形で計算する。この離散化によりリカレントなステップ更新（推論時：O(1)）と並列畳み込み（訓練時：O(n log n)）の両方が可能になる。

SSMの核心的な革新はSelectivity（選択性）にある。従来のS4等のSSMはA・B・Cが入力非依存の固定行列だったが、Mambaではこれらを入力x_tに依存して動的に変化させる（B, C, Δを入力から生成）。これにより「どの情報を記憶し、どの情報を忘れるか」を文脈に応じて制御できる。たとえば「The animal didn't cross the street because it was too tired」という文で「it」が何を指すかを判断する際、Mambaは選択的に関連情報を状態に保持できる。

ハードウェア面ではFlashAttentionと同様の手法でHBM（高帯域メモリ）とSRAM間のデータ転送を最小化するKernel Fusionを実装しており、Transformerと比較して推論速度は最大5倍、メモリ使用量を大幅削減する。Mamba-3Bは同サイズのTransformerと同等以上、2倍サイズのTransformerに匹敵する性能を事前訓練・下流タスクの両方で示した。

ただし課題もある。In-context Learningの能力がTransformerより弱い、長大な依存関係（100万トークン以上）の保持は隠れ状態の圧縮能力に依存する、という制約が指摘されている。また解釈可能性の観点では、Transformerのアテンション重みに相当する可視化手段がSSMには存在しないため、AI安全性・機構的解釈可能性の研究が困難になる可能性がある。監査AIへの示唆としては、超長文書（監査調書・契約書全文等）の一括処理において線形スケーリングは実用上の利点が大きく、長期履歴追跡が必要なエージェントの状態管理手法としても参考になる。

## アイデア

- SSMの隠れ状態は「過去の圧縮」として機能し、Transformerのような全履歴参照なしにMarkov的な次状態予測を実現する点が、リカレント型と注意型の中間的アーキテクチャとして興味深い
- B・C・Δを入力依存にするSelectivity（選択的状態空間）は、LSTMのゲート機構の一般化とも解釈でき、『何を覚え何を忘れるか』を明示的に学習させるアプローチとして設計思想が明快
- 訓練時は畳み込みとして並列計算し、推論時はリカレントとして逐次計算するという二重表現の切り替えが、速度・精度の両立を可能にしており、ハードウェア寄りの最適化視点が独自

## 前提知識

- **Transformer** → /deep_2420 TransformersモデルをMLXに移植するSkillとテストハーネスの構築：オープンソースにおけるエージェント時代の貢献とは
- **Attention機構** → /deep_1010 LLMの金融市場への応用：価格予測・合成データ・マルチモーダル学習の可能性と限界
- **RNN/LSTM** (TODO: 読むべき)
- **KVキャッシュ** → /deep_3482 DeepSeek-V4：エージェントが実際に使える100万トークンコンテキスト
- **FlashAttention** → /deep_221 Differential Transformer V2：カスタムカーネル不要・推論高速化を実現した差分注意機構の改良版

## 関連記事

- /deep_3105 Sessa: 選択的状態空間アテンション — フィードバックパス内にアテンションを組み込む新デコーダ
- /deep_2480 量子化へのKLレンズ：混合精度SSM-Transformerモデルの高速・順伝播のみの感度分析
- /deep_2510 多層SSMの表現能力と限界：深さ・精度・Chain-of-Thoughtの相互作用
- /deep_1975 WUTDet: 密集した小物体を含む10万スケールの船舶検出データセットとベンチマーク
- /deep_199 Titans + MIRAS: AIに長期記憶を持たせる新アーキテクチャ

## 原文リンク

[Mamba解説：Transformerに挑む状態空間モデル（SSM）の仕組み](https://thegradient.pub/mamba-explained/)
