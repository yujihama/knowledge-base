---
title: "Mamba解説：Transformerに挑む状態空間モデル（SSM）"
url: "https://thegradient.pub/mamba-explained/"
date: 2026-06-13
tags: [Mamba, SSM, 状態空間モデル, Transformer代替, 選択的SSM, 線形スケーリング, 長文脈, S4, HiPPO, 並列スキャン]
category: "ai-ml"
related: [2510, 2480, 1837, 3105, 7117]
memo: "[The Gradient] Mamba Explained"
processed_at: "2026-06-13T09:27:19.974414"
---

## 要約

MambaはAlbert GuとTri Daoが開発した状態空間モデル（SSM）ベースの言語モデルアーキテクチャで、Transformerのアテンション機構が抱える二次計算量ボトルネックを解消することを目的としている。Transformerではトークン間の全対全通信（Attention）によりforward passがO(n²)の時間計算量となり、KVキャッシュがO(n)のメモリを消費するため、長文脈（例：100万トークン）での運用が現実的に困難である。Mambaはこの問題に対し、制御理論由来の状態空間モデルをAttentionの代替として採用する。SSMは連続時間微分方程式 h'(t)=Ah(t)+Bx(t)、y(t)=Ch(t)+Dx(t) によって定式化され、過去の情報を固定サイズの隠れ状態 h に圧縮することで線形スケーリングを実現する。連続時間方程式は離散化（Zero-Order Hold法）により実際のシーケンス処理に対応させる。従来のSSM（S4等）は行列A・B・Cが入力に依存しない固定パラメータであったため、内容に応じた選択的な情報保持が困難だった。Mambaの核心的イノベーションは「選択的SSM（Selective SSM）」であり、B・C・Δ（ステップサイズ）を入力 x から動的に生成するパラメータとすることで、関連情報を選択的に記憶・忘却する能力を獲得した。これによりMambaはTransformerのAttentionに近い表現力を持ちながら、推論時O(1)メモリ（隠れ状態のみ）・O(n)時間計算量という優位性を保持する。ハードウェア最適化としてHardware-Aware Parallel Scanアルゴリズムを採用し、GPU上での並列計算とメモリ効率（カーネルフュージョン・再計算）を両立する。Mamba-3Bは同サイズのTransformerと同等以上、2倍サイズのTransformerに匹敵する性能をThe Pileデータセットで達成し、推論速度はTransformerの最大5倍とされる。一方でMambaの課題として、固定サイズの隠れ状態による情報の「忘却」（In-Context Learningへの制約）、解釈可能性・機械的解釈の難しさ（Transformerの回路分析手法が適用困難）、そしてTransformerと比較したアテンション的な完全情報保持の欠如が挙げられる。監査エージェント開発の観点では、長文脈の監査ログ・財務報告書の効率的処理においてMambaの線形スケーリングは有効だが、証跡の正確な参照が必要な場面ではAttentionの全保持特性が依然有利な場合がある。HybridアーキテクチャとしてMamba層とAttention層を組み合わせる方向性も研究されており、実用システムへの統合経路として注目される。

## アイデア

- 隠れ状態を「過去の圧縮」と捉える設計思想は、監査ログのような長大な時系列データの要約・異常検知パイプラインに応用可能。ただし固定サイズ状態による情報損失リスクをどう管理するかが実装上の課題となる
- B・C・Δを入力依存にする「選択性」の導入が本質的なブレークスルーであり、これはAttentionのQK内積による選択的情報取得とパラレルな発想。アーキテクチャ設計において「何を記憶し何を捨てるか」を学習させる仕組みの重要性を示している
- Hardware-Aware Parallel Scanによる再計算戦略（メモリ節約のためactivationを保存せず逆伝播時に再計算）は、大規模モデルの効率化における「計算とメモリのトレードオフ設計」のケーススタディとして参考になる

## 前提知識

- **Transformer / Attention機構** (TODO: 読むべき)
- **RNN・隠れ状態** (TODO: 読むべき)
- **状態空間モデル (SSM)** (TODO: 読むべき)
- **離散化 / Zero-Order Hold** (TODO: 読むべき)
- **FlashAttention** → /deep_221 Differential Transformer V2：カスタムカーネル不要・推論高速化を実現した差分注意機構の改良版

## 関連記事

- /deep_2510 多層SSMの表現能力と限界：深さ・精度・Chain-of-Thoughtの相互作用
- /deep_2480 量子化へのKLレンズ：混合精度SSM-Transformerモデルの高速・順伝播のみの感度分析
- /deep_1837 UNDO Flip-Flop：状態空間モデルにおける可逆的意味状態管理の制御プローブ
- /deep_3105 Sessa: 選択的状態空間アテンション — フィードバックパス内にアテンションを組み込む新デコーダ
- /deep_7117 SP-MoMamba: スーパーピクセル駆動の状態空間エキスパート混合による効率的な画像超解像

## 原文リンク

[Mamba解説：Transformerに挑む状態空間モデル（SSM）](https://thegradient.pub/mamba-explained/)
