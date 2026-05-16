---
title: "Mamba解説：Transformerに挑む状態空間モデル（SSM）"
url: "https://thegradient.pub/mamba-explained/"
date: 2026-05-09
tags: [Mamba, SSM, State Space Model, Transformer, 長文脈処理, 選択的状態空間, 線形スケーリング, Selective SSM, HiPPO, シーケンスモデル]
category: "ai-ml"
related: [3105, 2480, 2510, 1975, 199]
memo: "[The Gradient] Mamba Explained"
processed_at: "2026-05-09T21:50:31.191444"
---

## 要約

MambaはAlbert GuとTri Daoが開発した状態空間モデル（SSM）ベースのシーケンスモデルで、Transformerのアテンション機構が持つO(n²)の計算複雑性問題を解消することを目的としている。Transformerでは全トークン間のペアワイズ通信によりKVキャッシュがO(n)のメモリを消費し、長文脈になるほど推論速度が低下する。Mambaはこの「二乗ボトルネック」を排除し、シーケンス長に対して線形スケーリングを実現。推論速度はTransformerの最大5倍速とされる。

MambaのアーキテクチャはSSMによるトークン間通信とMLPスタイルの射影による計算の組み合わせで構成される。SSMの基本式は連続時間微分方程式 h'(t) = Ah(t) + Bx(t) と出力方程式 y(t) = Ch(t) + Dx(t) で表現され、隠れ状態hが過去の情報を圧縮する。この連続時間モデルをゼロ次ホールド（ZOH）法で離散化することで実際のシーケンス処理に対応する。

Mambaの核心的な革新はSelective State Spaceで、入力に応じてSSMのパラメータ（B、C、Δ）を動的に変化させる選択的機構（S4→S6）を導入した点にある。従来のSSMは線形時不変（LTI）であったが、Mambaは入力依存型にすることでコンテンツベースの選択的記憶・忘却が可能になった。長いテキストで「選択的コピー」や「誘導ヘッド」タスクに対応できる。

ハードウェア効率化のためにParallel Scan アルゴリズムとカーネルフュージョン技術でGPUのSRAM/HBM間転送を最小化するHardware-Aware Algorithmを採用している。Mamba-3BモデルはThe Pileベンチマークで同サイズのTransformerを上回り、2倍サイズのTransformerと同等の性能を示した。

ただしMambaにはデメリットもある。Selective SSMはRecurrent Networkと類似した情報フローを持つため、インコンテキスト学習（ICL）能力がTransformerより劣る可能性がある。また解釈可能性研究の観点では、Transformerで確立されたAttention Head分析やCircuit解析の手法がそのまま適用できない。Mamba2ではMulti-Head SSM（SSD）構造を導入し、Transformerとの構造的類似性を高めながら8倍の高速化を実現した。

監査エージェント開発への示唆として、監査ログや取引履歴のような超長シーケンス（数十万件のイベント）を一括処理する際にMambaアーキテクチャは有効な選択肢になり得る。特にコスト制約のある推論環境でTransformer代替を検討する際に参照価値がある。

## アイデア

- 「状態は過去の圧縮である」というSSMの概念は、Transformerのフルアテンションに対する根本的な設計哲学の違いを示しており、情報ボトルネックの観点から記憶と忘却のトレードオフを明示的にモデル化している点が興味深い
- 入力依存でSSMパラメータを動的変化させるSelective機構（S4→S6）により、固定パラメータのLTIシステムから脱却し「何を覚えて何を忘れるか」をコンテンツ駆動で決定できる点は、長期依存性の学習効率を根本から変える可能性がある
- Parallel ScanによりRecurrentな計算をGPU並列実行可能にする手法は、逐次処理と並列処理のトレードオフをアルゴリズムレベルで解決しており、ハードウェアアーキテクチャとモデル設計の共同最適化の好例

## 前提知識

- **Transformer** → /deep_2420 TransformersモデルをMLXに移植するSkillとテストハーネスの構築：オープンソースにおけるエージェント時代の貢献とは
- **Attention機構** → /deep_1010 LLMの金融市場への応用：価格予測・合成データ・マルチモーダル学習の可能性と限界
- **RNN/LSTM** (TODO: 読むべき)
- **状態空間モデル** → /deep_170 Mambaの解説：Transformerに挑む状態空間モデル
- **FlashAttention** → /deep_221 Differential Transformer V2：カスタムカーネル不要・推論高速化を実現した差分注意機構の改良版

## 関連記事

- /deep_3105 Sessa: 選択的状態空間アテンション — フィードバックパス内にアテンションを組み込む新デコーダ
- /deep_2480 量子化へのKLレンズ：混合精度SSM-Transformerモデルの高速・順伝播のみの感度分析
- /deep_2510 多層SSMの表現能力と限界：深さ・精度・Chain-of-Thoughtの相互作用
- /deep_1975 WUTDet: 密集した小物体を含む10万スケールの船舶検出データセットとベンチマーク
- /deep_199 Titans + MIRAS: AIに長期記憶を持たせる新アーキテクチャ

## 原文リンク

[Mamba解説：Transformerに挑む状態空間モデル（SSM）](https://thegradient.pub/mamba-explained/)
