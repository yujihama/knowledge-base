---
title: "Mamba解説：Transformerに挑む状態空間モデル"
url: "https://thegradient.pub/mamba-explained/"
date: 2026-06-07
tags: [Mamba, SSM, 状態空間モデル, Transformer, 長コンテキスト, 選択的状態空間, S4, 線形計算量, Hardware-Aware]
category: "ai-ml"
related: [2510, 3105, 222, 2480, 7597]
memo: "[The Gradient] Mamba Explained"
processed_at: "2026-06-07T09:26:46.409074"
---

## 要約

MambaはGu・Dao両氏が2024年に提案した状態空間モデル（SSM）ベースのシーケンスモデルで、Transformerの二次計算量ボトルネックを線形計算量で回避する。Transformerのアテンション機構はトークン間の全対全通信にO(n²)の時間計算量を要し、KVキャッシュがO(n)のメモリを消費するため、長コンテキスト処理（例：100万トークン）が現実的でない。Mambaはこの通信コンポーネントをSSMで置き換え、MLPスタイルの射影を計算コンポーネントとして保持する。

SSMの基本方程式は連続時間微分方程式 h'(t) = Ah(t) + Bx(t)（状態更新）と y(t) = Ch(t) + Dx(t)（出力）で表される。状態ベクトルhは過去情報の圧縮であり、新しい観測xと既知の状態ダイナミクスから次状態を推定できるため、全過去トークンを参照する必要がない。離散化にはZero-Order Hold（ZOH）手法を用い、実装上の差分方程式に変換する。

Mambaの核心的革新は「選択的状態空間モデル（S6）」にある。従来のS4等のSSMはA・B・Cが入力に依存しない時不変パラメータだったため並列計算可能な畳み込みとして扱えたが、コンテキスト依存の選択が不可能だった。MambaはB・C・∆を入力依存のパラメータとすることで選択性を実現し、関連情報の選択的保持・無関係情報の忘却を可能にした（∆が大きいと入力を重視し状態を更新、小さいと状態を維持）。これによりIn-Context Learningに相当する機能が生まれる。

ただし選択的SSMは入力依存のため畳み込みとして並列化できない。MambaはHardware-Aware Parallel Scanアルゴリズムで対処し、GUP SRAMをメモリとして活用してHBM転送を最小化（FlashAttentionと同様の発想）。これにより推論速度はTransformerの最大5倍、メモリ使用量も大幅削減を達成した。Mamba-3Bは同サイズのTransformerを上回り、2倍サイズのTransformerに匹敵する性能をThe Pile等のベンチマークで示した。

デメリットとして、固定サイズの隠れ状態への圧縮による情報損失（Transformerのアテンションは全過去トークンを参照可能）、インコンテキストでの正確な文字列コピー・検索が苦手な点、Transformerに比べた解釈可能性研究の成熟度の低さが挙げられる。監査エージェント開発への示唆としては、長期会話ログや監査証跡など超長コンテキストの処理において線形計算量のMambaが有効な代替となりうる点、状態という「圧縮された記憶」の概念がエージェントのメモリ設計に応用可能な点が注目される。

## アイデア

- 選択的SSM（S6）における∆パラメータの入力依存化が「何を記憶し何を忘れるか」の制御を可能にし、これがアテンション機構に相当する選択的情報処理を実現する仕組み
- 状態hを「過去の圧縮」として定義することで固定サイズのメモリで無限長シーケンスを処理できるが、この圧縮が情報損失を生むトレードオフが、エージェントの長期記憶設計問題と構造的に同じ
- HBMとSRAMのメモリ階層を意識したHardware-Aware Parallel Scanがアルゴリズム的非効率をハードウェア最適化で補う手法で、FlashAttentionと同一の設計思想がSSMにも適用された

## 前提知識

- **Transformer/Attention機構** (TODO: 読むべき)
- **RNN・隠れ状態** (TODO: 読むべき)
- **S4/LSSL** (TODO: 読むべき)
- **FlashAttention** → /deep_221 Differential Transformer V2：カスタムカーネル不要・推論高速化を実現した差分注意機構の改良版
- **畳み込みとシーケンスモデル** (TODO: 読むべき)

## 関連記事

- /deep_2510 多層SSMの表現能力と限界：深さ・精度・Chain-of-Thoughtの相互作用
- /deep_3105 Sessa: 選択的状態空間アテンション — フィードバックパス内にアテンションを組み込む新デコーダ
- /deep_222 Falcon-H1-Arabic: ハイブリッドMamba-Transformerアーキテクチャによるアラビア語AI最前線
- /deep_2480 量子化へのKLレンズ：混合精度SSM-Transformerモデルの高速・順伝播のみの感度分析
- /deep_7597 深層学習・生成AIの全体像を「3つの問い」で整理する｜CNNから拡散モデル・Mambaまで

## 原文リンク

[Mamba解説：Transformerに挑む状態空間モデル](https://thegradient.pub/mamba-explained/)
