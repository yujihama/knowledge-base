---
title: "Mamba解説：TransformerへのState Space Modelによる挑戦"
url: "https://thegradient.pub/mamba-explained/"
date: 2026-05-20
tags: [Mamba, SSM, State Space Model, Transformer, 選択的SSM, Zero-Order Hold, 線形スケーリング, 長文脈]
category: "ai-ml"
related: [3105, 2480, 2510, 1975, 199]
memo: "[The Gradient] Mamba Explained"
processed_at: "2026-05-20T21:36:44.899130"
---

## 要約

MambaはAlbert GuとTri Daoが開発したState Space Model（SSM）ベースのシーケンスモデルで、Transformerが抱える二次計算量の問題を解消することを目的としている。Transformerのアテンション機構はトークン間の全対全通信を行うため、訓練時O(n²)の時間計算量・自己回帰推論時O(n)のメモリ使用量（KVキャッシュ）が必要となる。Mambaはこの「Attention」を制御理論由来のSSMで置き換え、MLP部分は維持する構造を持つ。

SSMの基本式は連続時間微分方程式 h'(t) = Ah(t) + Bx(t)、y(t) = Ch(t) + Dx(t) で表される。ここでhは隠れ状態（過去の圧縮）、xは入力、yは出力、A/B/C/Dは学習可能な行列パラメータである。実際の離散系への変換にはZero-Order Hold（ZOH）離散化を用い、差分方程式 h_t+1 = Āh_t + B̄x_t、y_t = Ch_t + Dx_t に変換する。

従来のSSM（S4等）との最大の差異はA/B/Cを入力依存（選択的）にした点で、これを「選択的SSM」と呼ぶ。固定パラメータのSSMは入力に関わらず同一のフィルタリングを行うためコンテンツ依存の情報保持・忘却が不可能だったが、Mambaでは各タイムステップのΔ（時間刻み）、B、Cを入力から動的に計算することで選択性を実現した。これはTransformerのアテンション機構が入力によってどのトークンに注目するかを変えることに類似する。

ハードウェア効率化のためHardware-Aware Parallel Scan（HAPS）を採用し、通常は逐次処理が必要なスキャン演算をGPUのSRAM上で並列化することで高速化を達成。推論速度はTransformerの最大5倍高速で、シーケンス長に対して線形スケールする。Mamba-3Bモデルは同規模Transformerを上回り、2倍規模のTransformerに匹敵する性能をThe Pileで示した。100万トークン長のシーケンスでも性能向上が確認されている。

隠れ状態hはシーケンス全体の固定サイズの圧縮であるため、推論時はO(1)空間でオートリグレッシブ生成が可能。一方、Transformerのような「文脈内学習（in-context learning）」の能力が理論上制限される可能性があり、コピータスク等で弱点が示されている。解釈可能性・AIセーフティの観点では、固定サイズの状態がボトルネックとなりTransformerより活性化の解析が困難になる懸念がある。監査エージェント開発への示唆として、長大な監査ログや連続的なトランザクション系列を低メモリ・線形時間で処理するバックボーンとしてMambaは有望であり、LangGraphベースの状態管理と組み合わせることで大量ドキュメントのストリーム処理が現実的になる。

## アイデア

- 隠れ状態hを「過去の圧縮」と定義することでマルコフ性を保ちつつ長距離依存を扱う設計思想は、RNNとTransformerの折衷として理論的に興味深い
- パラメータB/C/Δを入力から動的に生成する「選択的SSM」の仕組みは、Transformerのアテンション行列をシーケンスモデルとして解釈し直したものとも見なせる
- CUDA SRAMを活用したHardware-Aware Parallel Scanにより、逐次依存のある再帰計算を並列化するアプローチは、他のシーケンシャルモデル最適化にも応用可能

## 前提知識

- **Transformer / Self-Attention** (TODO: 読むべき)
- **RNN / 隠れ状態** (TODO: 読むべき)
- **State Space Model (S4)** (TODO: 読むべき)
- **KVキャッシュ** → /deep_3482 DeepSeek-V4：エージェントが実際に使える100万トークンコンテキスト
- **離散化（ZOH）** (TODO: 読むべき)

## 関連記事

- /deep_3105 Sessa: 選択的状態空間アテンション — フィードバックパス内にアテンションを組み込む新デコーダ
- /deep_2480 量子化へのKLレンズ：混合精度SSM-Transformerモデルの高速・順伝播のみの感度分析
- /deep_2510 多層SSMの表現能力と限界：深さ・精度・Chain-of-Thoughtの相互作用
- /deep_1975 WUTDet: 密集した小物体を含む10万スケールの船舶検出データセットとベンチマーク
- /deep_199 Titans + MIRAS: AIに長期記憶を持たせる新アーキテクチャ

## 原文リンク

[Mamba解説：TransformerへのState Space Modelによる挑戦](https://thegradient.pub/mamba-explained/)
