---
title: "Mambaの解説：Transformerに挑む状態空間モデル"
url: "https://thegradient.pub/mamba-explained/"
date: 2026-06-06
tags: [Mamba, SSM, State Space Model, Transformer代替, 長文脈, 選択的SSM, Hardware-Aware Parallel Scan, 線形スケーリング, Zero-Order Hold]
category: "ai-ml"
related: [7117, 2480, 2510, 3105, 5810]
memo: "[The Gradient] Mamba Explained"
processed_at: "2026-06-06T09:18:31.352099"
---

## 要約

MambaはAlbert GuとTri Daoが提案した状態空間モデル（SSM）ベースのシーケンスモデルで、Transformerが抱える二次計算コストの問題を解消することを目的としている。Transformerのアテンション機構はトークン数nに対してO(n²)の時間計算量とO(n)のKVキャッシュメモリを必要とし、長いコンテキスト（例：100万トークン）では実用上の限界に達する。Mambaはこれをコントロール理論由来のSSMで置き換え、シーケンス長に対して線形スケーリングを実現する。

Mambaの核心は連続時間微分方程式 h'(t) = Ah(t) + Bx(t)、y(t) = Ch(t) + Dx(t) で表される状態遷移モデルにある。状態hは過去の情報を圧縮した表現であり、新たな入力xと組み合わせることで次の出力yを決定する。実装上は離散化（Zero-Order Hold法）によりこれを差分方程式に変換し、h_t = Ā h_{t-1} + B̄ x_t、y_t = C h_t の形で計算する。

従来のSSM（S4等）との違いは、MambaではA、B、Cの行列が入力x_tに依存して動的に変化する「選択的SSM」である点だ。固定パラメータのSSMは「入力に選択的に注目する」能力が低く、コピータスクや連想想起タスクで性能が劣化していた。Mambaはこれを解決するため、各タイムステップで行列値を入力から計算するが、これはバッチ処理やコンボリューションとの非互換性を生む。そこでMambaはHardware-Aware Parallel Scanというカーネルフュージョン技術を導入し、中間状態をHBMでなくSRAMに保持することでメモリ転送ボトルネックを回避し、FlashAttentionと同種のアプローチで高速化を実現する。

性能面では、Mamba-3Bは同規模のTransformerを上回り、6Bクラスのモデルと同等の性能をThe Pileベンチマークで示した。また推論速度はTransformerの最大5倍高速で、100万トークンのシーケンスでも線形時間で処理できる。一方、Mambaの隠れ状態は固定サイズであり、Transformerの正確なKVキャッシュと異なり情報が圧縮・損失される点は弱点として指摘される。In-context learningや一般化性能ではTransformerに対して若干の課題が残る可能性がある。

解釈可能性・安全性の観点では、Mambaの状態遷移行列AはTransformerのアテンション行列よりも可視化が難しく、モデルの内部動作理解という点では現時点でTransformerに劣る。ただしMamba2ではSSMとアテンションの統一的フレームワークが提案されており、ハイブリッドアーキテクチャとしての発展が期待される。監査エージェント開発への示唆としては、長大なログや監査証跡（数万〜数十万トークン）を扱う場面でMambaのような線形スケールモデルが推論コスト削減に寄与できる可能性があり、特にリアルタイム監視エージェントのバックボーンとしての採用可能性を検討する価値がある。

## アイデア

- SSMの行列A・B・Cを入力依存にする『選択的SSM』がMambaの核心であり、固定パラメータSSMとの決定的な差異である点——これはコントロール理論の静的システムと動的システムの違いに対応する
- 中間状態をHBMでなくSRAMに保持するHardware-Aware Parallel Scanは、FlashAttentionと同種のカーネルフュージョン戦略であり、アルゴリズム設計がハードウェア特性に強く依存していることを示す好例
- Mambaの隠れ状態は固定サイズの圧縮表現であり、Transformerの全トークン保持と本質的に異なる——これは損失圧縮vs無損失キャッシュのトレードオフとして、長文書監査ログ処理のアーキテクチャ選定に直結する問題意識を提供する

## 前提知識

- **Transformer / Attention機構** (TODO: 読むべき)
- **KVキャッシュ** → /deep_3482 DeepSeek-V4：エージェントが実際に使える100万トークンコンテキスト
- **状態空間モデル（SSM）** → /deep_926 Mamba解説：Transformerに挑む状態空間モデル（SSM）
- **FlashAttention** → /deep_221 Differential Transformer V2：カスタムカーネル不要・推論高速化を実現した差分注意機構の改良版
- **離散化（ZOH法）** (TODO: 読むべき)

## 関連記事

- /deep_7117 SP-MoMamba: スーパーピクセル駆動の状態空間エキスパート混合による効率的な画像超解像
- /deep_2480 量子化へのKLレンズ：混合精度SSM-Transformerモデルの高速・順伝播のみの感度分析
- /deep_2510 多層SSMの表現能力と限界：深さ・精度・Chain-of-Thoughtの相互作用
- /deep_3105 Sessa: 選択的状態空間アテンション — フィードバックパス内にアテンションを組み込む新デコーダ
- /deep_5810 MambaRain：0〜3時間降水予測のためのマルチスケールMamba-Attentionフレームワーク

## 原文リンク

[Mambaの解説：Transformerに挑む状態空間モデル](https://thegradient.pub/mamba-explained/)
