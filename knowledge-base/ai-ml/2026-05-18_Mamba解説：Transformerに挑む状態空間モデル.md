---
title: "Mamba解説：Transformerに挑む状態空間モデル"
url: "https://thegradient.pub/mamba-explained/"
date: 2026-05-18
tags: [Mamba, SSM, 状態空間モデル, HiPPO, 選択的状態空間, 線形注意, 長文脈処理, 離散化, FlashAttention]
category: "ai-ml"
related: [2510, 2480, 1837, 3105, 5810]
memo: "[The Gradient] Mamba Explained"
processed_at: "2026-05-18T21:09:47.799750"
---

## 要約

MambaはAlbert GuとTri Daoが開発した状態空間モデル（SSM）ベースの言語モデルアーキテクチャで、Transformerが抱える二次的計算複雑性の問題を克服することを目的としている。Transformerでは全トークン間のAttention計算がO(n²)の時間計算量を要し、KVキャッシュがO(n)のメモリを消費するため、長文脈（例：100万トークン）での処理が現実的でない。Mambaはこの「二次ボトルネック」を排除し、系列長に対して線形スケーリングを実現する。

アーキテクチャの核心は制御理論に由来する連続時間微分方程式 h'(t) = Ah(t) + Bx(t)、y(t) = Ch(t) + Dx(t) に基づくSSMである。これを離散化（Zero-Order Hold法）することで、実際のシーケンスデータに適用可能な差分方程式へ変換する。行列A、B、Cはデータに依存しない固定パラメータから出発するが、Mambaの最大の革新はこれらを「入力依存（input-selective）」にした点にある。具体的には、各時刻の入力xからB、C、Δ（ステップサイズ）をNNで動的に生成し、状態更新の選択性を持たせる。これにより「無関係な情報を無視し、関連情報を長期保持する」という能力を獲得した。

HiPPO理論に基づく行列Aの初期化により、モデルは長距離依存関係を効率的に圧縮・保持できる。また、選択的SSMはRNNとConvolutionの二重性を持ち、訓練時は並列畳み込みで高速化、推論時はRNNスタイルで逐次処理を行う。ハードウェア面ではFlash Attentionと同様のカーネルフュージョン技術をHBM-SRAM間転送の削減に活用し、Transformerより最大5倍高速な推論を実現する。

Mamba-3Bは同サイズのTransformerを上回り、2倍サイズのTransformerと同等の性能をThe Pileベンチマークで達成した。言語・音声・ゲノミクスなど複数モダリティでSoTAを示す。

監査エージェント開発への示唆として、Mambaの「状態」概念はエージェントの長期記憶・コンテキスト管理に直結する。特に監査トレイルの大量ドキュメント処理（長文脈RAG）や、過去の監査証跡から現在のリスク状態を圧縮保持するエージェント状態管理において、Transformerより効率的な代替として有望である。ただし、現状ではin-context learningやfew-shotタスクではTransformerに劣る面もあり、適用領域の見極めが必要。

## アイデア

- SSMの「状態は過去の圧縮」という概念は、エージェントの記憶設計（何を保持し何を忘れるか）と直接対応しており、LangGraphのエージェント状態管理の改善に応用できる可能性がある
- 入力依存ゲーティング（B、C、Δを動的生成）により、無関係なトークンをゼロリセット・重要情報を完全保持できる選択的記憶機構は、RAGにおける関連証拠の選択的保持メカニズムとして参考になる
- 訓練時は畳み込み（並列）・推論時はRNN（逐次）という二重性により、同一モデルが訓練効率と推論効率を両立する設計思想は、監査ログ解析のような大量バッチ処理とリアルタイム判定が混在するシステム設計に示唆を与える

## 前提知識

- **Transformer / Self-Attention** (TODO: 読むべき)
- **RNN / LSTM** (TODO: 読むべき)
- **状態空間モデル（SSM）** → /deep_926 Mamba解説：Transformerに挑む状態空間モデル（SSM）
- **HiPPO理論** (TODO: 読むべき)
- **FlashAttention** → /deep_221 Differential Transformer V2：カスタムカーネル不要・推論高速化を実現した差分注意機構の改良版

## 関連記事

- /deep_2510 多層SSMの表現能力と限界：深さ・精度・Chain-of-Thoughtの相互作用
- /deep_2480 量子化へのKLレンズ：混合精度SSM-Transformerモデルの高速・順伝播のみの感度分析
- /deep_1837 UNDO Flip-Flop：状態空間モデルにおける可逆的意味状態管理の制御プローブ
- /deep_3105 Sessa: 選択的状態空間アテンション — フィードバックパス内にアテンションを組み込む新デコーダ
- /deep_5810 MambaRain：0〜3時間降水予測のためのマルチスケールMamba-Attentionフレームワーク

## 原文リンク

[Mamba解説：Transformerに挑む状態空間モデル](https://thegradient.pub/mamba-explained/)
