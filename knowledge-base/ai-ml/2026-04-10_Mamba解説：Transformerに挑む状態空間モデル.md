---
title: "Mamba解説：Transformerに挑む状態空間モデル"
url: "https://thegradient.pub/mamba-explained/"
date: 2026-04-10
tags: [Mamba, SSM, 状態空間モデル, Transformer, 線形スケーリング, 選択的メカニズム, 長文脈, S6, シーケンスモデル]
category: "ai-ml"
memo: "[The Gradient] Mamba Explained"
processed_at: "2026-04-10T09:08:22.841457"
---

## 要約

MambaはAlbert GuとTri Daoが開発した状態空間モデル（SSM）ベースのシーケンスモデルで、Transformerのアテンションメカニズムが持つ二次計算量（O(n²)）の問題を解消する。Transformerでは全トークン間のペアワイズ通信が必要なため、コンテキスト長が増加するにつれて計算コストとKVキャッシュのメモリ使用量が急増するが、MambaはSSMを用いることで線形スケーリングを実現し、同じサイズのTransformerと同等以上の性能を示す。

Mambaの基本原理は制御理論に由来する連続時間微分方程式 h'(t) = Ah(t) + Bx(t)（状態遷移）および y(t) = Ch(t) + Dx(t)（出力）にある。状態hは過去の情報の圧縮表現であり、新しい観測xと組み合わせることで次の出力yを予測できる。実用上は離散化（Zero-Order Hold法）によりシーケンスデータに適用可能となる。

SSMをそのまま使うと「線形時不変（LTI）」であり、入力に依存しない固定のABCパラメータとなるため表現力が不足する。Mambaの核心的イノベーションは「選択的メカニズム（Selective State Space Model, S6）」で、ABCパラメータを入力xに依存させることで各タイムステップごとに動的に調整する。これによりモデルはどの情報を状態に保持・破棄するかを選択的に制御できる。

アーキテクチャ面ではTransformerのアテンションブロックをMambaブロック（SSM＋MLP射影）で置き換え、残差接続で積み重ねる。ハードウェア最適化として並列スキャンアルゴリズムをGPUのSRAM上で実行するfused kernelを実装しており、推論速度はTransformerの最大5倍に達する。Mamba-3Bモデルは同サイズのTransformerを上回り、2倍サイズのTransformerと同等のスケーリング則を示す。

課題としては、圧縮された固定サイズ状態に情報を詰め込む性質上、Transformerの完全なKVキャッシュに比べて「忘れやすい」点がある。インコンテキスト学習（ICL）性能はまだTransformerに劣るという報告もある。解釈可能性の観点からは、状態表現の可視化がTransformerのアテンションパターン可視化より難しいという側面もある。

## アイデア

- 選択的メカニズム（S6）により入力依存でパラメータを動的変化させる点は、エージェントが文脈に応じて注目すべき情報を選択する仕組みと概念的に類似しており、エージェントの記憶管理設計に示唆を与える
- 状態hを「過去の圧縮表現」として扱うアーキテクチャは、長期会話や監査ログのような長シーケンスを固定サイズのメモリで扱うユースケースに直接適用可能で、RAGなしで長文脈を内包するモデル設計の選択肢となる
- 並列スキャンアルゴリズムとGPU SRAM上のfused kernelによる高速化手法は、ローカルLLMインフラ（RTX 3090）での推論最適化を検討する際の参考アーキテクチャとなる
## 関連記事

- /deep_199 Titans + MIRAS: AIに長期記憶を持たせる新アーキテクチャ
- /deep_222 Falcon-H1-Arabic: ハイブリッドMamba-Transformerアーキテクチャによるアラビア語AI最前線
- /deep_833 Falcon 3 ファミリー：10B以下の高性能オープンモデル群の紹介
- /deep_255 Apriel-H1: 効率的な推論モデル蒸留の意外なカギ
- /deep_1494 🤗 TransformersによるProbabilistic時系列予測

## 原文リンク

[Mamba解説：Transformerに挑む状態空間モデル](https://thegradient.pub/mamba-explained/)
