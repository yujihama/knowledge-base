---
title: "Mamba解説：Transformerに挑む状態空間モデル"
url: "https://thegradient.pub/mamba-explained/"
date: 2026-06-10
tags: [Mamba, SSM, State Space Model, Transformer, 線形注意機構, 選択的SSM, 長文脈処理, 並列スキャン, LLM]
category: "ai-ml"
related: [3105, 7117, 7961, 833, 216]
memo: "[The Gradient] Mamba Explained"
processed_at: "2026-06-10T21:15:10.606382"
---

## 要約

MambaはAlbert GuとTri Daoが開発した状態空間モデル（SSM）ベースの言語モデルアーキテクチャで、TransformerのAttentionが持つO(n²)の計算量問題を解消することを目的としている。Transformerでは全トークン間のペアワイズ通信（Attention）が必要なため、KVキャッシュのメモリ使用量がO(n)、訓練時の計算量がO(n²)となり、長いコンテキスト（100万トークン規模）では事実上使用不可能になる。MambaはこのAttentionを制御理論に基づくSSMで置き換え、トークン間の通信をO(n)線形スケールで実現する。

理論的基盤はLinear State Space Model（LSSM）で、連続時間の微分方程式 h'(t) = Ah(t) + Bx(t)、y(t) = Ch(t) + Dx(t) として定式化される。ここでhは隠れ状態（過去の情報の圧縮）、xは入力、yは出力を表す。実装では零次ホールド（ZOH）法によって連続時間方程式を離散時間差分方程式に変換し、h_t = Āh_{t-1} + B̄x_t という形で扱う。

Mambaの核心的なイノベーションは「選択的状態空間モデル（Selective SSM）」で、行列B・C・ステップサイズΔを入力x_tに依存させることで、どの情報を隠れ状態に保持し、どれを捨てるかを動的に制御できる。従来のSSM（S4等）ではA・B・Cが時間不変（入力非依存）であり、時系列データには強いが離散トークンへの適応が困難だった。この入力依存性の導入により、Transformerのソフトアテンションが持つ「コンテキスト選択」能力を近似する。

しかし選択的SSMは畳み込み（並列訓練に有利）とRNN（高速推論に有利）の両方の性質を持ちつつ、単純な行列積への最適化が難しい。この問題をMambaはHardware-Aware Parallel Scan（並列スキャン）とGPUのSRAMへの積極的活用（FlashAttentionに類似したカーネルフュージョン）で解決している。

ベンチマーク結果として、Mamba-3BはThe Pileデータセットで同サイズのTransformerを上回り、2倍のパラメータを持つTransformerと同等の性能を示す。推論速度はTransformerの最大5倍。一方で欠点として、（1）隠れ状態のサイズが固定されているため、Transformerのように明示的に過去のトークンを参照できない「in-context learning」が弱い可能性、（2）長距離依存関係の記憶がTransformerより劣るケースがある点が指摘されている。

解釈可能性・AIセーフティの観点では、Mambaは回路理論ベースの解釈が難しく、Mechanistic Interpretabilityの研究が困難になる可能性がある。一方でゲノミクスや音声、長文書処理など長いシーケンスを扱う応用領域での可能性が大きい。監査エージェント開発への示唆として、長い監査ログや規制文書（数十万トークン規模）を扱うRAGシステムのバックボーンとして、TransformerよりもMambaが有効な選択肢となりうる。

## アイデア

- 隠れ状態h_tが「過去の圧縮」として機能するRNN的設計と、入力依存のパラメータ（B, C, Δ）によりTransformerのAttentionの選択性を近似する点が巧妙。訓練時は畳み込みとして並列化、推論時はRNNとして逐次処理できる二面性が実用上の強み
- 選択的SSMはHippo行列を用いてA行列を初期化することで、遠い過去の情報を多項式基底で効率的に圧縮できる。これはLSTMのゲート機構の連続時間版とも解釈でき、勾配消失問題への対処が構造に埋め込まれている
- 監査ログや契約書など長大な文書を扱うシステムで、O(n²)のTransformerの代替として有効。ただし「正確に特定の過去トークンを参照する」能力はTransformerが優れるため、検索精度が重要な監査エージェントではRAGとの組み合わせが現実的な設計になる

## 前提知識

- **Transformer / Attention機構** (TODO: 読むべき)
- **RNN / LSTM** (TODO: 読むべき)
- **S4 (Structured SSM)** (TODO: 読むべき)
- **FlashAttention** → /deep_221 Differential Transformer V2：カスタムカーネル不要・推論高速化を実現した差分注意機構の改良版
- **シーケンスモデリング** → /deep_1712 Decision TransformerをHugging Faceに統合：オフライン強化学習をシーケンスモデリングで解く

## 関連記事

- /deep_3105 Sessa: 選択的状態空間アテンション — フィードバックパス内にアテンションを組み込む新デコーダ
- /deep_7117 SP-MoMamba: スーパーピクセル駆動の状態空間エキスパート混合による効率的な画像超解像
- /deep_7961 LLMに「睡眠」が必要な理由 ― 論文「Language Models Need Sleep」解説
- /deep_833 Falcon 3 ファミリー：10B以下の高性能オープンモデル群の紹介
- /deep_216 金融市場へのLLM応用：価格予測・合成データ・マルチモーダル学習の可能性と限界

## 原文リンク

[Mamba解説：Transformerに挑む状態空間モデル](https://thegradient.pub/mamba-explained/)
