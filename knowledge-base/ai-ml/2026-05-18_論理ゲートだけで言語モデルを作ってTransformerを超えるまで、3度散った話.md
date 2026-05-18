---
title: "論理ゲートだけで言語モデルを作ってTransformerを超えるまで、3度散った話"
url: "https://zenn.dev/karumaru/articles/24bca710a2db62"
date: 2026-05-18
tags: [DLGN, Boolean回路, Transformer, 知識蒸留, char-LM, HBA, Perplexity, 量子化誤差, born-again networks]
category: "ai-ml"
related: [1494, 1794, 2732, 113, 216]
memo: "[Zenn 機械学習] 論理ゲートだけで言語モデルを作って Transformer を超えるまで、3 度散った話"
processed_at: "2026-05-18T09:09:39.587722"
---

## 要約

GPUを使わずAND・OR・XORなどの論理ゲートのみで言語モデルを構築し、最終的にTransformer（Perplexity 4.86）を0.13上回るPPL 4.73を達成した個人研究の失敗録。

**第1章（DLGN flat）**: Petersen et al. (2022)のDLGN（Deep Differentiable Logic Gate Networks）を使い、16種類のブール関数をsoftmaxで混合して勾配を流す手法を4段積んでTinyShakespeare（80KB）のchar-LMを学習。PPL 11.83を達成したが、Transformerの4.86には遠く届かなかった。

**第2章（LoopedDLGN）**: Universal Transformerの発想をBoolean化し、同一DLGNブロックをT回繰り返す設計を試みた。バナッハの縮小写像定理で理論武装した美しい設計だったが、結果はPPL 754.31。反復ごとにハード量子化誤差（εtotal ≳ Σ||f_hard(x^(t)) - f_soft(x^(t))||）が線形以上に蓄積し、反復系とBoolean量子化が構造的に相性最悪であることが判明。

**第3章（HBA: Hierarchical Boolean Attention）**: Attentionを「ルーティング（QK→どこを見るか）」と「値の集約（V→加重平均）」の2段階に分解し、ルーティング部分のみをBoolean（-1, +1の離散値）にする設計へ転換。値の集約はfloatのまま保持することで、量子化誤差の深さ方向伝播を断ち切った。HBA v2（Early stop・ハード閾値校正・温度warm_hold等の正則化を導入）でHard PPL 6.54を達成。LoopedDLGNから115倍の改善。

**第4章（知識蒸留）**: 通常のTransformerを教師、HBA v2を生徒とするHinton式知識蒸留（α=0.3, T=8のKLダイバージェンス損失）を適用。10分の学習でStudent PPL 4.73を達成し、Teacher（4.86）を逆転。Furlanello et al. (2018)のborn-again networksとして知られる現象（ソフトラベルがデータ拡張として機能し生徒が教師を上回る）が実際に発生した。

**第5章（ChatHBA崩壊）**: 5,377件の英語Q&Aデータでfine-tuneを試みたが、char-LMのコンテキスト長64文字ではFrance→Parisのような長距離依存を学べず、データ量も中途半端で汎化に至らず完全崩壊（「Otewkia」「::: h.」等の出力）。数値ベンチマークと実用品質の乖離を実体験。

今後の展望として、HBAはSpeculative Decodingのドラフトモデル等の軽量・高速ルーティングが必要な特化用途での実用可能性が言及されている。監査エージェント開発への示唆として、離散化・量子化を導入する際は誤差伝播経路の設計が決定的に重要であり、アーキテクチャのどの層を離散化するかという設計判断がシステム全体の品質を左右する点は、エッジ推論やリソース制約環境でのエージェント実装にも応用できる視点を提供する。

## アイデア

- AttentionのルーティングのみをBoolean化（HBA）し、値の集約をfloatに残すことで量子化誤差の深さ方向伝播を構造的に断ち切るアーキテクチャ分割の発想が巧妙
- 知識蒸留のborn-again networks現象（生徒が教師を逆転）を意図的に利用し、論理回路ベースモデルでTransformerを超えた点は、軽量モデル設計の実践的示唆が大きい
- 失敗経緯（PPL 754→6.54→4.73）を段階的に公開することで、反復系×Boolean量子化の相性問題という再現性ある知見として残している点が個人研究の価値を高めている

## 前提知識

- **Transformer** → /deep_2420 TransformersモデルをMLXに移植するSkillとテストハーネスの構築：オープンソースにおけるエージェント時代の貢献とは
- **Perplexity (PPL)** (TODO: 読むべき)
- **DLGN** → /deep_3608 シリコン対応ニューラルネットワーク：差分論理ゲートネットワークのカスタムASIC実装
- **知識蒸留** → /deep_2424 エンタープライズAIをオペレーティングレイヤーとして扱う：Ensembleが示す構造的優位性
- **Boolean回路** (TODO: 読むべき)

## 関連記事

- /deep_1494 🤗 TransformersによるProbabilistic時系列予測
- /deep_1794 長期埋め込み（LTE）によるバランスの取れたパーソナライゼーション
- /deep_2732 長期マルチモーダル深層検索エージェント：LMM-Searcherの提案
- /deep_113 金融時系列予測でLightGBM / LSTM / Transformerを比較してみた
- /deep_216 金融市場へのLLM応用：価格予測・合成データ・マルチモーダル学習の可能性と限界

## 原文リンク

[論理ゲートだけで言語モデルを作ってTransformerを超えるまで、3度散った話](https://zenn.dev/karumaru/articles/24bca710a2db62)
