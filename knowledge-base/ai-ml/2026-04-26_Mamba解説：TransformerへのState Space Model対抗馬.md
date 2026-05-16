---
title: "Mamba解説：TransformerへのState Space Model対抗馬"
url: "https://thegradient.pub/mamba-explained/"
date: 2026-04-26
tags: [Mamba, State Space Model, SSM, Transformer, 長コンテキスト, 選択的SSM, 並列スキャン, ZOH離散化, シーケンスモデル]
category: "ai-ml"
related: [222, 2480, 2510, 1975, 199]
memo: "[The Gradient] Mamba Explained"
processed_at: "2026-04-26T12:47:01.852646"
---

## 要約

MambaはAlbert GuとTri Daoが開発した状態空間モデル（SSM）ベースのシーケンスモデルで、Transformerが抱える二次計算コスト問題を解決することを目指している。Transformerはすべてのトークンが過去のすべてのトークンを参照するAttentionを使うため、学習時にO(n²)の時間複雑度、推論時にO(n)の時間複雑度、KVキャッシュにO(n)の空間複雑度が発生する。コンテキスト長が増えるほど速度・メモリ消費が悪化し、100万トークン規模の長コンテキストでは実用上困難となる。

Mambaはこの問題をSSMで解決する。SSMの核心は制御理論に由来する連続時間微分方程式 h'(t) = Ah(t) + Bx(t)、y(t) = Ch(t) + Dx(t) であり、隠れ状態hが「過去の圧縮」として機能する。実装上は連続時間をゼロ次ホールド（ZOH）離散化によって差分方程式に変換し、h_t = Ā·h_{t-1} + B̄·x_t、y_t = C·h_t という形で逐次計算する。これにより推論は固定サイズの隠れ状態のみを保持すればよく、O(1)の空間複雑度で動作する。

従来のSSM（S4等）はA・B・C行列が入力に依存しない線形時不変（LTI）システムであり、畳み込みとして並列計算が可能な一方で、文脈依存の選択が困難だった。Mambaの核心的革新は「選択的SSM」であり、B・C・Δ（ステップサイズ）を入力x_tの関数として動的に生成する（入力依存パラメータ化）。これにより「どの情報を状態に残すか」をトークンごとに適応的に制御できる。

ただし選択性を導入すると行列が入力依存になるため、通常の畳み込みとして並列計算できなくなる。これをHardware-Aware Parallel Scan（並列スキャン）とカーネルフュージョンによってGPU SRAM上で効率的に処理する点がMambaのエンジニアリング上の要点である。結果として推論速度はTransformerの最大5倍、Mamba-3BはThe PileベンチマークでTransformer同規模を上回り、2倍規模のTransformerに匹敵する性能を示した。

解釈可能性・安全性の観点では、SSMの隠れ状態がTransformerのKVキャッシュより大幅にコンパクトであり、情報がどのように圧縮されているかの分析が課題となる。監査エージェント開発への示唆としては、長い監査ログや規程文書（数十万トークン規模）を固定メモリで処理できる可能性があり、Transformerベースのコンテキスト制限を回避しつつシーケンシャルなイベント系列の追跡に適した特性を持つ。

## アイデア

- 隠れ状態を「過去の圧縮」と捉えることで、Transformerの全トークン参照を不要にし、推論をO(1)空間・線形時間で実現する設計思想
- B・C・Δを入力依存にする「選択性」の導入により、LTI-SSMが持てなかった文脈依存フィルタリング能力を獲得した点（選択的忘却・記憶）
- GPU SRAM上のカーネルフュージョンと並列スキャンで、理論上は逐次計算にしかなれないSSMを実用的な速度で学習させるHardware-Awareな実装戦略

## 前提知識

- **Transformer / Attention** (TODO: 読むべき)
- **State Space Model** → /deep_195 Mamba解説：TransformerへのState Space Modelによる挑戦
- **RNN / 隠れ状態** (TODO: 読むべき)
- **離散化（ZOH）** (TODO: 読むべき)
- **並列スキャン** → /deep_672 Mambaの解説：Transformerに挑む状態空間モデル

## 関連記事

- /deep_222 Falcon-H1-Arabic: ハイブリッドMamba-Transformerアーキテクチャによるアラビア語AI最前線
- /deep_2480 量子化へのKLレンズ：混合精度SSM-Transformerモデルの高速・順伝播のみの感度分析
- /deep_2510 多層SSMの表現能力と限界：深さ・精度・Chain-of-Thoughtの相互作用
- /deep_1975 WUTDet: 密集した小物体を含む10万スケールの船舶検出データセットとベンチマーク
- /deep_199 Titans + MIRAS: AIに長期記憶を持たせる新アーキテクチャ

## 原文リンク

[Mamba解説：TransformerへのState Space Model対抗馬](https://thegradient.pub/mamba-explained/)
