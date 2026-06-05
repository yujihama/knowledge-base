---
title: "Mamba解説：Transformerに挑む状態空間モデル"
url: "https://thegradient.pub/mamba-explained/"
date: 2026-06-05
tags: [Mamba, SSM, 状態空間モデル, Transformer代替, 線形計算量, 選択的SSM, Zero-Order Hold離散化, 長文脈処理, Hardware-Aware Algorithm]
category: "ai-ml"
related: [2510, 2480, 1837, 3105, 7117]
memo: "[The Gradient] Mamba Explained"
processed_at: "2026-06-05T21:20:50.775461"
---

## 要約

MambaはAlbert GuとTri Daoが開発した状態空間モデル（SSM）ベースのシーケンスモデルで、Transformerの二次計算量ボトルネックを回避しながら同等以上の性能を実現する。Transformerのアテンション機構はトークン間の全対全通信を行うため学習時にO(n²)の時間計算量、推論時にO(n)の時間計算量とO(n)のKVキャッシュメモリが必要となり、長文脈（例：100万トークン）では実用困難になる。Mambaはこのアテンションをコントロール理論由来のSSMで置き換える。SSMの基本式はh'(t)=Ah(t)+Bx(t)（状態更新）とy(t)=Ch(t)+Dx(t)（出力）という線形微分方程式で表現される。ここでhは過去情報を圧縮した隠れ状態、A/B/C/Dはパラメータ行列、xは入力、yは出力に対応する。この連続時間方程式はZero-Order Hold（ZOH）離散化によって差分方程式に変換され、実装可能となる。従来のSSM（S4等）はA/B/Cが入力に依存しない「線形時不変（LTI）」であったため、コンテキストに応じた動的な情報選択ができないという欠点があった。Mambaの最大の革新は「選択的状態空間（Selective SSM / S6）」にあり、B、C、Δ（タイムステップ）を入力xに依存して動的に変化させる。これによりモデルは重要な情報を隠れ状態に選択的に取り込み、不要な情報を無視できる。この入力依存パラメータ化によりParallelスキャンによる効率的なGPU並列計算が困難になるが、Mamba著者はHardware-Aware Parallel Algorithmを開発し、HBMとSRAM間のメモリ転送を最小化することで推論速度をTransformerの最大5倍に改善した。Mamba-3Bモデルはthe Pileベンチマークで同サイズのGPT-3ベースモデルを上回り、2倍サイズのTransformerに匹敵する性能を示す。系列長に対して線形の計算量スケーリングを実現しており、言語・音声・ゲノミクスなど複数モダリティでSOTA性能を達成。ただし非線形性のないSSM層は理論上有界な言語を学習できないという表現力の限界も指摘されており、Transformer部分を完全に置き換えるか補完的に使うか（MambaformerやJamba等のハイブリッドアーキテクチャ）は今後の研究課題として残る。解釈可能性の観点からは隠れ状態が圧縮表現である点がアテンションより分析困難で、AI安全性研究への影響も議論されている。監査エージェント開発への示唆としては、長い監査ログや契約書全文（数万〜数十万トークン）を低メモリ・高速に処理できる点が有望で、LangGraphのステートマシンと概念的に類似した「圧縮状態遷移」の考え方はエージェント設計にも応用可能。

## アイデア

- 選択的状態空間（S6）がB/C/Δを入力依存で動的変化させる仕組みは、Transformerのアテンションスコアによる重み付けと機能的に等価な『情報選択』を異なる計算グラフで実現しており、両者の等価性・差異の理論的解明が残課題
- 隠れ状態hが『過去の圧縮』として機能する設計は、LangGraphにおけるエージェントStateの概念と同型であり、有限サイズの状態で無限の会話履歴を近似するRAGレスな長期記憶アーキテクチャへの応用可能性がある
- MambaがO(n)の線形スケーリングを実現しながら、Transformerの2倍サイズに匹敵する性能を出すというスケーリング則の類似性は、パラメータ効率より文脈長効率が重要になる次世代モデル評価軸（tokens-per-FLOP at 1M context）を示唆する

## 前提知識

- **Transformer / Self-Attention** (TODO: 読むべき)
- **KVキャッシュ** → /deep_3482 DeepSeek-V4：エージェントが実際に使える100万トークンコンテキスト
- **状態空間モデル（S4）** (TODO: 読むべき)
- **離散化（ZOH）** (TODO: 読むべき)
- **FlashAttention** → /deep_221 Differential Transformer V2：カスタムカーネル不要・推論高速化を実現した差分注意機構の改良版

## 関連記事

- /deep_2510 多層SSMの表現能力と限界：深さ・精度・Chain-of-Thoughtの相互作用
- /deep_2480 量子化へのKLレンズ：混合精度SSM-Transformerモデルの高速・順伝播のみの感度分析
- /deep_1837 UNDO Flip-Flop：状態空間モデルにおける可逆的意味状態管理の制御プローブ
- /deep_3105 Sessa: 選択的状態空間アテンション — フィードバックパス内にアテンションを組み込む新デコーダ
- /deep_7117 SP-MoMamba: スーパーピクセル駆動の状態空間エキスパート混合による効率的な画像超解像

## 原文リンク

[Mamba解説：Transformerに挑む状態空間モデル](https://thegradient.pub/mamba-explained/)
