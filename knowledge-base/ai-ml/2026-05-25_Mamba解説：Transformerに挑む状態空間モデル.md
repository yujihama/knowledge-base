---
title: "Mamba解説：Transformerに挑む状態空間モデル"
url: "https://thegradient.pub/mamba-explained/"
date: 2026-05-25
tags: [Mamba, SSM, 状態空間モデル, Selective SSM, Zero-Order Hold, Parallel Scan, 長文脈, LTI]
category: "ai-ml"
related: [2510, 2480, 1837, 3105, 5810]
memo: "[The Gradient] Mamba Explained"
processed_at: "2026-05-25T21:13:12.404360"
---

## 要約

MambaはAlbert GuとTri Daoが開発した状態空間モデル（SSM）ベースの新しいシーケンスモデルアーキテクチャ。Transformerの最大の弱点である「二次計算ボトルネック」を解消することを目的としている。Transformerのアテンション機構はトークン間の全ペア通信を行うため、訓練時のForwardパスはO(n²)の時間計算量となり、長いコンテキストで処理速度が指数的に低下する。またKVキャッシュのO(n)空間計算量がGPUメモリを圧迫し、OOMエラーの原因となる。MambaはこのAttentionコンポーネントをControl Theory（制御理論）由来のSSMに置き換え、線形計算量O(n)でシーケンス処理を実現する。

SSMの基本式は連続時間微分方程式 h'(t) = Ah(t) + Bx(t) および y(t) = Ch(t) + Dx(t) で表される。hは隠れ状態（過去の圧縮表現）、xは入力観測、yは出力予測を指す。この連続時間方程式を離散化（Zero-Order Hold法を使用）することで、実際のトークン列に適用可能な差分方程式に変換する。

Mambaの最大の革新は「選択的SSM（Selective SSM）」の導入にある。従来のSSMは行列A・B・Cが入力に依存しない時不変（LTI: Linear Time-Invariant）システムだったため、どの情報を保持・忘却するかを動的に制御できなかった。MambaではB・C・Δ（ステップサイズ）を入力xの関数として学習させることで、文脈に応じた選択的な情報フィルタリングを実現した。これによりTransformerのソフトアテンションに相当する「重要トークンの選択的参照」が可能になる。

実装上の工夫として「Parallel Scan」アルゴリズムを採用し、選択的SSMをGPU上で並列計算可能にしている。さらにHardware-Aware設計により、HBM（メインGPUメモリ）へのアクセスを最小化してSRAM（オンチップキャッシュ）上で演算を完結させるFlashAttention類似の最適化を施している。

ベンチマーク結果では、Mamba-3BモデルがThe Pileデータセットで同サイズのTransformerを上回り、2倍サイズのTransformerと同等の性能を示した。推論速度はTransformerの最大5倍。コンテキスト長100万トークンまでの線形スケーリングも実証されている。

ただし課題もある。コンテキストウィンドウ全体をスキャンして特定情報を正確に取り出す「in-context learning」的なタスクでTransformerより弱い傾向がある。また内部状態の解釈可能性（Interpretability）はAttentionのAttribution分析に比べ難しく、AIセーフティ観点での課題が残る。言語以外にも音声・ゲノム解析への応用が示されており、長距離依存性を持つシーケンシャルデータ全般への応用が期待される。

## アイデア

- 「状態は過去の圧縮」というSSMの設計思想はRAGのチャンク設計や監査エージェントの履歴管理に応用できる：長い監査ログを固定サイズの隠れ状態に圧縮しながらリアルタイム処理するアーキテクチャが構想できる
- 選択的SSMの入力依存パラメータ（B・C・Δ）の学習はLLM-as-judgeにおける「どの証拠トークンに注目するか」の動的制御と概念的に対応しており、判断根拠の軽量な追跡メカニズムとして興味深い
- Parallel Scanによる並列化はシーケンシャルに見える問題をGPUの並列性で解く好例であり、エージェントの逐次思考ステップを並列評価する設計パターンへのヒントになる

## 前提知識

- **Transformer** → /deep_2420 TransformersモデルをMLXに移植するSkillとテストハーネスの構築：オープンソースにおけるエージェント時代の貢献とは
- **Attention機構** → /deep_1010 LLMの金融市場への応用：価格予測・合成データ・マルチモーダル学習の可能性と限界
- **KVキャッシュ** → /deep_3482 DeepSeek-V4：エージェントが実際に使える100万トークンコンテキスト
- **RNN/LSTM** (TODO: 読むべき)
- **制御理論（状態空間）** (TODO: 読むべき)

## 関連記事

- /deep_2510 多層SSMの表現能力と限界：深さ・精度・Chain-of-Thoughtの相互作用
- /deep_2480 量子化へのKLレンズ：混合精度SSM-Transformerモデルの高速・順伝播のみの感度分析
- /deep_1837 UNDO Flip-Flop：状態空間モデルにおける可逆的意味状態管理の制御プローブ
- /deep_3105 Sessa: 選択的状態空間アテンション — フィードバックパス内にアテンションを組み込む新デコーダ
- /deep_5810 MambaRain：0〜3時間降水予測のためのマルチスケールMamba-Attentionフレームワーク

## 原文リンク

[Mamba解説：Transformerに挑む状態空間モデル](https://thegradient.pub/mamba-explained/)
