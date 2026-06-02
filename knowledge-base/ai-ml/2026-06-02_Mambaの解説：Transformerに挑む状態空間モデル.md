---
title: "Mambaの解説：Transformerに挑む状態空間モデル"
url: "https://thegradient.pub/mamba-explained/"
date: 2026-06-02
tags: [Mamba, SSM, 状態空間モデル, Transformer代替, 長文脈処理, 選択的状態空間, 線形スケーリング, Parallel Scan, 離散化, ZOH]
category: "ai-ml"
related: [2510, 2480, 1837, 3105, 7117]
memo: "[The Gradient] Mamba Explained"
processed_at: "2026-06-02T21:34:52.300425"
---

## 要約

MambaはAlbert GuとTri Daoが開発した状態空間モデル（SSM）ベースのシーケンスモデルで、TransformerのAttention機構が抱える二次計算量ボトルネックを解消することを目的としている。Transformerでは全トークン間のペアワイズ通信によりトレーニング時のフォワードパスがO(n²)の時間計算量を必要とし、KVキャッシュもO(n)のメモリを消費する。これに対しMambaはシーケンス長に対して線形スケーリングを実現し、最大100万トークンの長文脈でも実用的な速度を保つ。推論速度はTransformerの最大5倍速い。

Mambaの核心はSSMにある。連続時間の微分方程式 h'(t) = Ah(t) + Bx(t)、y(t) = Ch(t) + Dx(t) を基盤とし、Zero-Order Hold（ZOH）離散化によって実際の離散時間ステップで動作可能な差分方程式へ変換する。この「状態」はマルコフ性を持ち、過去全体を固定サイズの隠れ状態hに圧縮する設計思想である。

古典的SSMのS4との最大の違いは「選択性（selectivity）」にある。従来のSSMではA・B・Cが入力に依存しない固定パラメータだったが、MambaではB、C、さらにステップサイズΔを入力xの関数として動的に決定する。これにより「どの情報を状態に保持・忘却するか」をモデルが制御でき、Transformerのソフト注意と同様の選択的情報処理が可能になる。

ハードウェア効率化のため、MambaはHBM（高帯域メモリ）とSRAM（静的RAM）の帯域差を活用した「Parallel Scan」をCUDA上で実装し、畳み込み的な並列計算とリカレント的な逐次推論を切り替える。トレーニング時は並列畳み込みで効率を確保し、推論時はリカレントモードで高速なトークン生成を実現する。

Mamba-3BはThe Pileベンチマークで同サイズのTransformerを上回り、2倍サイズのTransformerと同等の性能を示した。言語・音声・ゲノミクス等の複数モダリティでState-of-the-Artを達成している。

解釈可能性の観点では、Attentionヘッドとは異なりMambaの内部状態は一定サイズの圧縮表現であるため、どの過去情報が保持されているかの解析手法はまだ発展途上。AI安全性の観点でも、選択的圧縮による情報の損失特性はTransformerと異なり、長期記憶の忠実性についての研究課題が残る。監査エージェントへの示唆としては、長大なログや文書チェーンを線形コストで処理できる点が注目に値する。

## アイデア

- 選択性（selectivity）の導入：B・C・Δを入力依存にすることで固定圧縮だったSSMがコンテキスト適応型になり、Attentionなしで動的な情報選択が可能になる点
- トレーニング時は並列畳み込み・推論時はリカレントという二重モード動作により、TransformerのKVキャッシュ問題を根本から回避しつつGPU並列性も活かせる設計
- 状態はマルコフ性を持つ固定サイズの圧縮表現であるため、100万トークンの文脈でも一定メモリで動作できる一方、情報損失の制御がどこまで可能かという解釈可能性・安全性の新たな研究課題を生む

## 前提知識

- **Transformer** → /deep_2420 TransformersモデルをMLXに移植するSkillとテストハーネスの構築：オープンソースにおけるエージェント時代の貢献とは
- **Attention機構** → /deep_1010 LLMの金融市場への応用：価格予測・合成データ・マルチモーダル学習の可能性と限界
- **RNN/LSTM** (TODO: 読むべき)
- **S4モデル** (TODO: 読むべき)
- **CUDA最適化** → /deep_1012 Mambaの解説：TransformerへのState Space Modelによる挑戦

## 関連記事

- /deep_2510 多層SSMの表現能力と限界：深さ・精度・Chain-of-Thoughtの相互作用
- /deep_2480 量子化へのKLレンズ：混合精度SSM-Transformerモデルの高速・順伝播のみの感度分析
- /deep_1837 UNDO Flip-Flop：状態空間モデルにおける可逆的意味状態管理の制御プローブ
- /deep_3105 Sessa: 選択的状態空間アテンション — フィードバックパス内にアテンションを組み込む新デコーダ
- /deep_7117 SP-MoMamba: スーパーピクセル駆動の状態空間エキスパート混合による効率的な画像超解像

## 原文リンク

[Mambaの解説：Transformerに挑む状態空間モデル](https://thegradient.pub/mamba-explained/)
