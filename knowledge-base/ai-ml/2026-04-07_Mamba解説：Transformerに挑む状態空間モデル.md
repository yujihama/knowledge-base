---
title: "Mamba解説：Transformerに挑む状態空間モデル"
url: "https://thegradient.pub/mamba-explained/"
date: 2026-04-07
tags: [Mamba, SSM, 状態空間モデル, Transformer, HiPPO, ZOH離散化, 選択的状態空間, 長文コンテキスト, 線形スケーリング]
category: "ai-ml"
memo: "[The Gradient] Mamba Explained"
related: [199, 222, 833, 255, 1494]
processed_at: "2026-04-07T12:32:05.801225"
---

## 要約

MambaはAlbert GuとTri Daoが開発した状態空間モデル（SSM）ベースのシーケンスモデルで、Transformerのアテンション機構が抱える二次計算量問題（O(n²)）を回避しつつ、同等のスケーリング則を実現する。Transformerはすべてのトークン間のペアワイズ通信（KVキャッシュ）により、長いコンテキストでは計算・メモリコストが爆発的に増加する。Mambaはこれをコントロール理論に基づくSSMで置き換え、シーケンス長に対して線形スケーリング（O(n)）を達成する。

SSMの核心は隠れ状態hを微分方程式で表現することにある：h'(t) = Ah(t) + Bx(t)、y(t) = Ch(t) + Dx(t)。これを離散化（Zero-Order Hold法）することで、RNNに近い逐次的な推論が可能になる。古典的SSMと異なるMambaの革新点は「選択性（Selectivity）」で、行列A・B・C・Δを入力依存（input-dependent）にした点である。これにより特定のトークンを選択的に記憶・忘却する能力を持ち、従来の固定パラメータSSMが苦手とした「選択的コピー」や「誘導ヘッド」タスクをこなせるようになった。

ハードウェア面では、HiPPOと呼ばれる行列初期化手法（長距離依存の学習を安定化）と、CUDA用のカーネルフュージョン最適化（並列スキャンアルゴリズム）により、Transformerより最大5倍高速な推論を実現する。Mamba-3Bは同サイズのTransformerを凌駕し、2倍サイズのTransformerに匹敵するパフォーマンスをThe Pileベンチマークで示した。言語・音声・ゲノミクスなど複数モダリティでstate-of-the-artを達成している。

一方でMambaの限界も指摘されている。情報をコンパクトな隠れ状態に圧縮する性質上、Transformerが得意な「正確な情報検索（Exact Lookup）」が苦手。また選択的な状態更新により、内部表現の解釈可能性がTransformerのアテンションヘッドより難しく、回路ベースのメカニスティック解釈性研究への適用が課題となる。Transformerとのハイブリッドアーキテクチャ（一部レイヤーをMambaに置換）や、Vision・強化学習への応用研究も進行中。

## アイデア

- 入力依存のパラメータ化（選択性）によりRNN的な逐次構造に「どの情報を記憶するか」を動的に制御できる点は、エージェントの長期記憶設計に応用可能
- 隠れ状態が「過去の圧縮」として機能するSSMの設計思想は、マルコフ決定過程の観点から長期文脈を扱うシーケンスモデルの理論的基盤を提供する
- Transformerが正確な検索に強くMambaが長距離圧縮に強いというトレードオフは、ハイブリッドアーキテクチャの設計指針として重要
## 関連記事

- /deep_199 Titans + MIRAS: AIに長期記憶を持たせる新アーキテクチャ
- /deep_222 Falcon-H1-Arabic: ハイブリッドMamba-Transformerアーキテクチャによるアラビア語AI最前線
- /deep_833 Falcon 3 ファミリー：10B以下の高性能オープンモデル群の紹介
- /deep_255 Apriel-H1: 効率的な推論モデル蒸留の意外なカギ
- /deep_1494 🤗 TransformersによるProbabilistic時系列予測

## 原文リンク

[Mamba解説：Transformerに挑む状態空間モデル](https://thegradient.pub/mamba-explained/)
