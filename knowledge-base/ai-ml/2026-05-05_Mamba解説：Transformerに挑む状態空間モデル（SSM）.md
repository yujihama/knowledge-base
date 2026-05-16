---
title: "Mamba解説：Transformerに挑む状態空間モデル（SSM）"
url: "https://thegradient.pub/mamba-explained/"
date: 2026-05-05
tags: [Mamba, SSM, 状態空間モデル, Transformer, 選択的状態空間, HiPPO, S4, 長コンテキスト, 線形スケーリング, シーケンスモデル]
category: "ai-ml"
related: [2510, 3105, 222, 2480, 1975]
memo: "[The Gradient] Mamba Explained"
processed_at: "2026-05-05T12:40:48.649440"
---

## 要約

MambaはAlbert GuとTri Daoが提案した状態空間モデル（SSM）ベースのシーケンスモデルで、Transformerのアテンション機構が抱える二次計算量（O(n²)）の問題を解決する。Transformerでは全トークン間のペアワイズ通信が必要なため、コンテキスト長が増えるにつれて推論速度が低下し、KVキャッシュによるメモリ消費も線形に増大する。Mambaはこれを制御理論由来のSSMで置き換え、シーケンス長に対して線形スケーリング（O(n)）を実現する。

SSMの基本式は連続時間微分方程式 h'(t) = Ah(t) + Bx(t)、y(t) = Ch(t) + Dx(t) として表され、隠れ状態hが過去の情報を圧縮・保持する。実際のシーケンス処理には離散化が必要で、Mambaはゼロ次ホールド（ZOH）法を用いて差分方程式に変換する。

SSMの先行研究としてHiPPO（2020）、S4（2021）があるが、これらはA・B・C行列が入力に依存しない「時不変」な設計だった。Mambaの最大の革新は「選択的状態空間モデル」で、各ステップの入力x_tに応じてB、C、Δ（タイムステップ）を動的に変化させる点にある。これにより関連情報を選択的に状態に取り込み、不要な情報を忘却する機構（コンテンツベースの推論）が実現される。代償として並列スキャンによる畳み込みトリックが使えなくなるが、HardwareAware AlgorithmによるGPUのSRAM活用（FlashAttentionと類似の手法）で高速化を達成している。

性能面では、Mamba-3Bが同サイズのTransformerを上回り、2倍サイズのTransformerに匹敵する。推論速度はTransformerより最大5倍高速で、100万トークン長のシーケンスにも対応する。言語・音声・ゲノミクスなど複数モダリティで有効性が示されている。

一方、課題もある。Mambaの圧縮された固定サイズの状態は、厳密な情報検索（特定の文字列の正確な記憶など）が苦手で、「ニードル・イン・ア・ヘイスタック」タスクではTransformerに劣る。また状態が単一ベクトルに圧縮されるため、解釈可能性の観点では各トークンの寄与を直接追跡できず、Transformerのアテンションパターン分析のような手法が適用しにくい。AI安全性の文脈では、Mambaのシンプルな構造がより解釈しやすい可能性もある一方、過去情報の圧縮方法の理解が課題となる。監査エージェント開発への示唆として、長大なログや取引履歴などを扱う際のシーケンスモデルバックボーンとしてMambaは有力候補となり得る。特に長期コンテキストを保持しながら軽量に動作するエージェントの設計に応用可能。

## アイデア

- 選択的状態空間（B・C・Δを入力依存にする）という設計が、RNNの固定遷移行列問題とTransformerの二次計算量問題を同時に解決しようとする点が巧妙。情報の選択的記憶・忘却がアーキテクチャレベルで実現される
- HardwareAware Algorithmで行列Āの具体的な計算を回避し、スキャン演算をGPUのSRAMに収めることで理論計算量と実測速度のギャップを埋めている点——アルゴリズムと実装の共同設計という発想がFlashAttentionと同系統
- 固定サイズの隠れ状態への圧縮はマルコフ性を仮定するため、厳密な情報検索（Induction Head的タスク）が苦手という弱点は、Mamba単体より「Mamba＋Attention」ハイブリッド（Jamba等）の方向性を示唆しており、アーキテクチャ選択の設計指針になる

## 前提知識

- **Transformer・Attention機構** (TODO: 読むべき)
- **RNN・LSTM** (TODO: 読むべき)
- **状態空間モデル（SSM）** → /deep_926 Mamba解説：Transformerに挑む状態空間モデル（SSM）
- **FlashAttention** → /deep_221 Differential Transformer V2：カスタムカーネル不要・推論高速化を実現した差分注意機構の改良版
- **HiPPO / S4** (TODO: 読むべき)

## 関連記事

- /deep_2510 多層SSMの表現能力と限界：深さ・精度・Chain-of-Thoughtの相互作用
- /deep_3105 Sessa: 選択的状態空間アテンション — フィードバックパス内にアテンションを組み込む新デコーダ
- /deep_222 Falcon-H1-Arabic: ハイブリッドMamba-Transformerアーキテクチャによるアラビア語AI最前線
- /deep_2480 量子化へのKLレンズ：混合精度SSM-Transformerモデルの高速・順伝播のみの感度分析
- /deep_1975 WUTDet: 密集した小物体を含む10万スケールの船舶検出データセットとベンチマーク

## 原文リンク

[Mamba解説：Transformerに挑む状態空間モデル（SSM）](https://thegradient.pub/mamba-explained/)
