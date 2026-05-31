---
title: "Mamba解説：Transformerに挑む状態空間モデル"
url: "https://thegradient.pub/mamba-explained/"
date: 2026-05-31
tags: [Mamba, SSM, State Space Model, Transformer, 線形スケーリング, 選択メカニズム, HiPPO, S4, 長文脈処理, CUDA最適化]
category: "ai-ml"
related: [3105, 2480, 2510, 1975, 199]
memo: "[The Gradient] Mamba Explained"
processed_at: "2026-05-31T21:12:34.484181"
---

## 要約

MambaはAlbert GuとTri Daoが開発した状態空間モデル（SSM）ベースの言語モデルアーキテクチャで、Transformerが抱える二次複雑度（O(n²)）の問題を解決する。Transformerのアテンション機構はすべてのトークン間のペアワイズ通信を行うため、学習時はシーケンス長nに対してO(n²)の時間計算量、自己回帰生成時はO(n)の時間計算量を持つ。さらにKVキャッシュにO(n)のメモリが必要で、長文脈では実用上のボトルネックとなる。Mambaはこれを線形スケーリングO(n)で代替する。

技術的な核心は制御理論に由来するSSMで、連続時間の微分方程式 h'(t) = Ah(t) + Bx(t)、y(t) = Ch(t) + Dx(t) として定式化される。hが隠れ状態（過去の圧縮）、xが入力観測値、yが出力。これをZero-Order Hold（ZOH）法で離散化し、実際の系列データに適用する。畳み込みとしても再帰としても計算でき、学習時は並列畳み込み、推論時は効率的なRNN的再帰で動作する（デュアルフォーム）。

S4（Structured State Space Sequence Model）までの先行SSMはA行列をHiPPO理論で初期化し長距離依存を捉えるが、A,B,Cが入力に依存しない（time-invariant）ため、コンテキスト依存の選択的な情報保持が困難だった。Mambaの最大の革新は「選択メカニズム（Selective SSM）」で、B、C、Δ（ステップサイズ）を入力x_tの関数として動的に変化させること（time-varying）。これにより重要なトークンを選択的に記憶・忘却できる。

実装上はHardware-Aware Parallel Scan（HAPS）をCUDAカーネルで実装し、Selective Scanの再帰計算をGPU上で効率化。Mamba-3BはThe Pileでの事前学習・下流評価においてTransformer同サイズを上回り、2倍サイズのTransformerと同等の性能を示す。推論速度はTransformerの最大5倍。100万トークン規模の長文脈でも実用的に動作する。

解釈可能性の観点では、Transformerのアテンションヘッドは可視化しやすいが、MambaのSSMの隠れ状態は高次元かつ連続的で解釈が難しい。AIセーフティの文脈でもアライメント研究のツールとして確立されたアテンション分析手法がそのまま使えない課題がある。監査エージェント開発への示唆として、長文書（監査調書、規程類等）を1Mトークン規模で処理できる可能性と、選択的状態更新による重要情報の動的保持機構はRAGの代替または補完として注目に値する。

## アイデア

- 選択メカニズム（Selective SSM）により、入力依存でB/C/Δを動的変化させることで「何を記憶し何を忘れるか」をモデルが学習できる点は、長期文書理解における情報フィルタリングの新しいアプローチ
- 学習時は並列畳み込み、推論時はRNN的再帰という「デュアルフォーム」の切り替えが、GPUの並列性を最大活用しつつ自己回帰生成の効率も確保するという設計の妙
- 隠れ状態hが「過去の圧縮」として機能するという定式化は、監査エージェントにおける長期文書コンテキスト保持（KVキャッシュ爆発の回避）への応用可能性を持つ

## 前提知識

- **Transformer** → /deep_2420 TransformersモデルをMLXに移植するSkillとテストハーネスの構築：オープンソースにおけるエージェント時代の貢献とは
- **Attention機構** → /deep_1010 LLMの金融市場への応用：価格予測・合成データ・マルチモーダル学習の可能性と限界
- **RNN** → /deep_115 AIを活用した都市型鉄砲水予測で都市を守る：Googleの新手法
- **畳み込みニューラルネット** → /deep_750 EEGの周波数帯域別特徴分析とグラフ畳み込みニューラルネットワーク（GCN）を用いたてんかん発作検出
- **S4/SSM** (TODO: 読むべき)

## 関連記事

- /deep_3105 Sessa: 選択的状態空間アテンション — フィードバックパス内にアテンションを組み込む新デコーダ
- /deep_2480 量子化へのKLレンズ：混合精度SSM-Transformerモデルの高速・順伝播のみの感度分析
- /deep_2510 多層SSMの表現能力と限界：深さ・精度・Chain-of-Thoughtの相互作用
- /deep_1975 WUTDet: 密集した小物体を含む10万スケールの船舶検出データセットとベンチマーク
- /deep_199 Titans + MIRAS: AIに長期記憶を持たせる新アーキテクチャ

## 原文リンク

[Mamba解説：Transformerに挑む状態空間モデル](https://thegradient.pub/mamba-explained/)
