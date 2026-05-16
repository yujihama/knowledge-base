---
title: "Mamba解説：Transformerに挑む状態空間モデル（SSM）の仕組みと可能性"
url: "https://thegradient.pub/mamba-explained/"
date: 2026-04-27
tags: [Mamba, SSM, State Space Model, Transformer, 長文脈, Selective SSM, Zero-Order Hold, 線形スケーリング, RNN, 並列スキャン]
category: "ai-ml"
related: [2480, 2510, 201, 1975, 199]
memo: "[The Gradient] Mamba Explained"
processed_at: "2026-04-27T12:54:24.367909"
---

## 要約

MambaはAlbert GuとTri Daoが開発した状態空間モデル（SSM）ベースのシーケンスモデルで、Transformerが抱える二次計算量ボトルネックを解消することを目的としている。Transformerはアテンション機構によりすべてのトークン間でO(n²)の計算とO(n)のKVキャッシュが必要となり、長文脈での推論が現実的でない。これに対しMambaは制御理論由来のSSMをアテンションの代替として採用し、シーケンス長に対して線形のスケーリングを実現する。

基本的な数式は連続時間微分方程式 h'(t) = Ah(t) + Bx(t)、y(t) = Ch(t) + Dx(t) で表され、現在の隠れ状態hと新規入力xから次の出力yを予測する。これをZero-Order Hold（ZOH）離散化により差分方程式に変換し、実用的なシーケンスデータへ適用する。隠れ状態hは過去の情報の圧縮として機能し、マルコフ決定過程として定式化される。

SSMは畳み込みとしての並列訓練とRNNスタイルの逐次推論という二つの計算形式を持ち、学習時は並列畳み込みで高速化、推論時は逐次RNNとして定数メモリで動作する。ただし古典的SSMは行列A・B・Cが入力依存でない（Linear Time Invariant）ため、選択的な情報保持が困難だった。Mambaではこれを「Selective SSM」として解決し、B・C・Δを入力xtの関数とすることで動的な情報フィルタリングを実現している。さらに並列スキャンアルゴリズムとカーネルフュージョンによりGPU上での効率的な実装（FlashMamba相当）も提供する。

Mamba-3Bは同サイズのTransformerと同等かそれ以上の性能を示し、2倍サイズのTransformerにも匹敵する結果をThe Pileで達成している。推論速度はTransformerより最大5倍高速。ただし、Transformerのように任意トークン間の直接参照は難しく、インコンテキスト学習（ICL）や想起タスクでの性能はTransformerに劣る場合がある。また、Mambaの隠れ状態は固定サイズであるため情報圧縮に限界があり、解釈可能性の観点では研究が発展途上。監査エージェントへの示唆として、長い監査ログや取引履歴など超長文脈データの処理においてMambaの線形スケーリングは有望で、KVキャッシュ爆発を回避しながら状態を圧縮保持するアーキテクチャは継続的な監査証跡分析に適合する可能性がある。

## アイデア

- SSMの隠れ状態は『過去の圧縮』として機能するため、固定サイズのメモリで任意長シーケンスを扱える点が監査ログの逐次処理に直接応用できる
- Selective SSM（入力依存のB・C・Δ）により、モデルが文脈に応じて何を記憶・忘却するかを動的に制御する仕組みはRAGの代替メモリ機構として興味深い
- 訓練時は並列畳み込み・推論時はRNNとして動作するデュアルモードの計算グラフは、エージェントのオフライン学習とオンライン推論の分離設計に示唆を与える

## 前提知識

- **Transformer / Attention** (TODO: 読むべき)
- **RNN** → /deep_115 AIを活用した都市型鉄砲水予測で都市を守る：Googleの新手法
- **畳み込み (CNN)** (TODO: 読むべき)
- **制御理論 / 状態方程式** (TODO: 読むべき)
- **FlashAttention** → /deep_221 Differential Transformer V2：カスタムカーネル不要・推論高速化を実現した差分注意機構の改良版

## 関連記事

- /deep_2480 量子化へのKLレンズ：混合精度SSM-Transformerモデルの高速・順伝播のみの感度分析
- /deep_2510 多層SSMの表現能力と限界：深さ・精度・Chain-of-Thoughtの相互作用
- /deep_201 【Transformerとは？ 第七回A】Self-Attentionの正体 〜Self-Attentionは何を変えたのか〜
- /deep_1975 WUTDet: 密集した小物体を含む10万スケールの船舶検出データセットとベンチマーク
- /deep_199 Titans + MIRAS: AIに長期記憶を持たせる新アーキテクチャ

## 原文リンク

[Mamba解説：Transformerに挑む状態空間モデル（SSM）の仕組みと可能性](https://thegradient.pub/mamba-explained/)
