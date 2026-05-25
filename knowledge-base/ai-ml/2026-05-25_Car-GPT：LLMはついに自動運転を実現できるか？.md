---
title: "Car-GPT：LLMはついに自動運転を実現できるか？"
url: "https://thegradient.pub/car-gpt/"
date: 2026-05-25
tags: [自動運転, LLM, Vision Transformer, End-to-End学習, Perception, Planning, マルチモーダル, GPT-4V, DriveVLM, PromptTrack]
category: "ai-ml"
related: [4441, 3582, 4900, 1527, 1297]
memo: "[The Gradient] Car-GPT: Could LLMs finally make self-driving cars happen?"
processed_at: "2026-05-25T09:26:37.038507"
---

## 要約

自動運転の歴史は「モジュール型アプローチ」から始まった。認識（Perception）、自己位置推定（Localization）、経路計画（Planning）、制御（Control）の4モジュールを個別に設計する手法が主流だったが、2010年代後半からEnd-to-Endニューラルネットワークによる統合アプローチが台頭した。本記事はさらに踏み込み、LLM（Large Language Model）が自動運転の「予期せぬ解答」になり得るかを検討する。

LLMの基本構造としてTokenization（テキストを数値トークンに変換）、Transformer（Encoder-Decoderアーキテクチャ、Multi-head Attention）、Next-word Predictionの3要素を解説する。自動運転への適用では、入力をカメラ画像・LiDAR点群・RADARデータに置き換え、Vision TransformerやVideo Vision Transformerでトークン化する。Transformerブロック自体はトークン列を操作するため入力種別に依存しない。

自動運転タスクへの適用として活発な研究領域は4つ：①Perception（環境記述・物体検出・追跡）、②Planning（次の行動決定）、③Generation（学習データ・シナリオの拡張生成）、④Q&A（シナリオへの質問応答）。Perceptionでは、GPT-4 Visionが画像から物体を列挙できることが示されており、HiLM-D・MTD-GPT・PromptTrackなどの専用モデルがDETR等の既存検出器とLLMを組み合わせてID付きトラッキングを実現している。Planningでは、DriveVLM・DriveLLM等が鳥瞰図や多視点画像を入力に取り、「車線変更」「一時停止」等の行動をテキストで出力する。

LLMの強みとして指摘されるのは、ゼロショット／フューショット汎化能力（訓練外シナリオへの対応）と、言語インターフェースによる説明可能性（ブラックボックス問題の緩和）である。一方で課題も多い。リアルタイム推論の計算コスト（GPT-4クラスのモデルをオンボードで動かすには現状のハードウェアでは困難）、LiDAR・RADARなど非視覚センサとの統合、認知エラーの安全影響、そして自動運転に特化した大規模ファインチューニングデータの不足が挙げられる。

記事全体を通じて、LLMは自動運転の「銀の弾丸」ではなく、既存モジュールを補完・強化するコンポーネントとして有望視されている。監査エージェント開発への示唆として、LLMをドメイン特化タスク（異常検知の説明生成、監査手続きの次アクション推論）に組み込む際も同様の構造——既存ツールとLLMのハイブリッド、説明可能性の確保、計算コストとのトレードオフ——が設計上の核心になる点が参考になる。

## アイデア

- LLMのTokenization概念を非テキストデータ（LiDAR点群・RADARデータ）に拡張する発想：Transformerはトークン列を操作するため、入力モダリティを問わず同一アーキテクチャを流用できるという一般性が自動運転以外のドメイン（例：時系列監査ログの異常検知）にも適用可能
- ゼロショット汎化能力が自動運転の「ロングテール問題」（珍しいシナリオへの対応）を緩和する可能性：訓練データに含まれない交通状況に対してもCommon Senseで推論できる点は、監査において未知リスクパターンへの対応にも類似する
- LLMを既存モジュール（DETR等の物体検出器）と組み合わせるハイブリッド設計（PromptTrackの構造）：LLM単体でEnd-to-Endを置き換えるのではなく、推論・説明・QA部分に限定投入することでコスト・信頼性のバランスを取るアーキテクチャパターン

## 前提知識

- **Transformer** → /deep_2420 TransformersモデルをMLXに移植するSkillとテストハーネスの構築：オープンソースにおけるエージェント時代の貢献とは
- **Vision Transformer** → /deep_165 Car-GPT: LLMは自動運転を実現できるか？
- **End-to-End学習** → /deep_165 Car-GPT: LLMは自動運転を実現できるか？
- **LiDAR点群処理** (TODO: 読むべき)
- **Multi-head Attention** → /deep_201 【Transformerとは？ 第七回A】Self-Attentionの正体 〜Self-Attentionは何を変えたのか〜

## 関連記事

- /deep_4441 判断してから走れ：自動運転のためのCritic中心型Vision Language Actionフレームワーク
- /deep_3582 凍結LLMを地図認識型時空間推論エンジンとして活用した車両軌跡予測フレームワーク
- /deep_4900 マルチモーダル寄りの拡張可能コミュニケーションアバターを作ってみた（Unity × Python × LLM × 音声）
- /deep_1527 IoT-Brain: LLMをセマンティック・空間センサースケジューリングに接地する
- /deep_1297 HorizonWeaver: 自動運転シーンのための汎化可能なマルチレベルセマンティック編集

## 原文リンク

[Car-GPT：LLMはついに自動運転を実現できるか？](https://thegradient.pub/car-gpt/)
