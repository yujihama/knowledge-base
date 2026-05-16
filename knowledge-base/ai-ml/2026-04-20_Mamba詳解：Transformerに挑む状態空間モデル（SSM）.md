---
title: "Mamba詳解：Transformerに挑む状態空間モデル（SSM）"
url: "https://thegradient.pub/mamba-explained/"
date: 2026-04-20
tags: [Mamba, SSM, State Space Model, Transformer代替, 長文脈, 選択機構, Parallel Scan, 線形スケーリング, HiPPO, S4]
category: "ai-ml"
related: [222, 833, 255, 1975, 1837]
memo: "[The Gradient] Mamba Explained"
processed_at: "2026-04-20T12:33:55.535753"
---

## 要約

MambaはGu・Dao両氏が開発したState Space Model（SSM）ベースのシーケンスモデルで、Transformerのボトルネックであるアテンション機構のO(n²)計算複雑度を根本から回避する。Transformerはすべてのトークン間でペアワイズ通信を行うため、KVキャッシュがO(n)メモリを消費し、長文脈でOOMエラーが頻発する構造的問題を抱える。Mambaはこれをコントロール理論由来のSSMで代替し、推論時O(1)メモリ、シーケンス長に対して線形スケールを実現する。

基本構造はh'(t) = Ah(t) + Bx(t)、y(t) = Ch(t) + Dx(t)という連続時間微分方程式で表される。実装上は離散化（Zero-Order Hold）が必要で、ΔをゲートとしてA・BをĀ・B̄に変換する。重要な革新はS4からMambaへの進化で、行列A・B・Cを入力xに依存させる「選択機構（Selection Mechanism）」の導入にある。従来のLTI（線形時不変）SSMは入力によらず固定のダイナミクスを持つため表現力に限界があったが、Mambaでは各トークンに応じてパラメータが動的に変化し、関連情報を選択的に記憶・忘却できる。

ハードウェア効率化のためParallel Scan（並列スキャン）を活用し、HBMとSRAM間のデータ転送を最小化するFlash-SSMに相当するカーネル融合を実装。これによりTransformerと比較して推論速度5倍、学習スループット3倍を達成。Mamba-3Bは同規模Transformerを上回り、2倍規模Transformerに匹敵するperplexityを示す。

一方、限界も明確である。Transformerのアテンションが持つ「コンテキスト内の任意トークンへの直接アクセス」という解釈可能性はMambaには存在せず、固定サイズ隠れ状態への圧縮は情報損失を伴う。In-context Learningでの比較優位性はまだ確認されておらず、Hybrid（アテンション＋SSM）アーキテクチャへの関心が高まっている。解釈可能性・AIセーフティの観点では、Mambaの隠れ状態が何を表現しているかを解析する新たな手法の開発が課題となる。監査エージェント開発への示唆として、長文書（監査調書、過去事例ログ）を百万トークン規模で処理する場面でMambaベースのバックボーンが実用的な選択肢になり得る。

## アイデア

- 選択機構（Selection Mechanism）により行列A・B・Cを入力依存にすることで、固定ダイナミクスのLTI-SSMからRecurrent NNに近い表現力を獲得しつつ、並列スキャンで学習を高速化する点が構造的に巧妙
- Δ（タイムステップ）を入力依存のソフトゲートとして使うことで「このトークンに注目するか無視するか」を制御する仕組みは、Transformerのアテンションスコアの代替として直感的に理解できる
- 隠れ状態が「過去の圧縮」として機能するMarkov的構造は、監査トレイルのような長期依存を持つシーケンスデータの処理に応用可能であり、エージェントの記憶機構設計のヒントになる

## 前提知識

- **Transformer・Self-Attention** (TODO: 読むべき)
- **KVキャッシュ** → /deep_106 TurboQuant: 極限圧縮によるAI効率の再定義
- **RNN・隠れ状態** (TODO: 読むべき)
- **HiPPO / S4** (TODO: 読むべき)
- **Parallel Scan** → /deep_263 Mambaの解説：TransformerへのState Space Modelの挑戦

## 関連記事

- /deep_222 Falcon-H1-Arabic: ハイブリッドMamba-Transformerアーキテクチャによるアラビア語AI最前線
- /deep_833 Falcon 3 ファミリー：10B以下の高性能オープンモデル群の紹介
- /deep_255 Apriel-H1: 効率的な推論モデル蒸留の意外なカギ
- /deep_1975 WUTDet: 密集した小物体を含む10万スケールの船舶検出データセットとベンチマーク
- /deep_1837 UNDO Flip-Flop：状態空間モデルにおける可逆的意味状態管理の制御プローブ

## 原文リンク

[Mamba詳解：Transformerに挑む状態空間モデル（SSM）](https://thegradient.pub/mamba-explained/)
