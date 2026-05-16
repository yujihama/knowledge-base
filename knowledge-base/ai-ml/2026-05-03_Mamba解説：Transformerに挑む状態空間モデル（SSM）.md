---
title: "Mamba解説：Transformerに挑む状態空間モデル（SSM）"
url: "https://thegradient.pub/mamba-explained/"
date: 2026-05-03
tags: [Mamba, SSM, 状態空間モデル, Transformer, 線形RNN, 選択的メカニズム, S4, 並列スキャン, 長文脈, シーケンスモデル]
category: "ai-ml"
related: [2510, 199, 3105, 2480, 1975]
memo: "[The Gradient] Mamba Explained"
processed_at: "2026-05-03T12:50:24.756538"
---

## 要約

MambaはAlbert GuとTri Daoが開発した状態空間モデル（SSM）ベースのシーケンスモデルで、Transformerのアテンション機構が持つO(n²)の計算複雑性問題を解決しようとする。Transformerではすべてのトークンが過去の全トークンを参照するKVキャッシュを必要とし、メモリ使用量O(n)・推論レイテンシのO(n)増加が生じる。Mambaはこの「二次ボトルネック」を取り除き、シーケンス長に対して線形スケーリングを実現する。

Mambaの理論的基盤は制御理論の状態空間表現で、連続時間微分方程式 h'(t) = Ah(t) + Bx(t)、y(t) = Ch(t) + Dx(t) により状態の遷移を記述する。現実の離散データへの適用にはZero-Order Hold（ZOH）離散化を使用し、行列A・Bを離散化したĀ・B̄に変換する。この離散化SSMはRNNとして（自己回帰推論時）またはCNNとして（学習時）解釈でき、並列スキャンアルゴリズムにより学習時の効率を確保する。

従来のSSM（S4等）との最大の違いは「選択的メカニズム（Selective SSM / S6）」である。S4ではA・B・C行列が入力に依存せず固定だったが、MambaではB・C・∆（タイムステップ）を入力xの関数として動的に変化させる。これにより「どの情報を状態に保持するか」をコンテキストに応じて選択でき、無関係な情報を状態から除去できる。たとえば選択的コピータスクでは、S4が失敗する一方Mambaは完全に解ける。

ハードウェア面ではFlash Attentionに対応するFlash Associative Scanを実装し、HBMとSRAM間のメモリ転送を最適化することで高速処理を実現する。Mamba-3Bは同サイズのTransformerを上回り、2倍サイズのTransformerと同等の性能をThe Pile事前学習・下流評価の両方で示した。推論速度はTransformerの最大5倍高速。

一方で制限もある。（1）インコンテキスト学習（ICL）ではTransformerより性能が低い傾向。（2）隠れ状態が圧縮であるため情報ロスが生じ、GPT-4に比べて完全な情報検索が難しい。（3）解釈可能性の観点では、Transformerのアテンションヘッドのような分析手法が確立されていない。

Mamba2ではSemiseparable行列理論でSSMとアテンションを統一的に扱うState Space Dualityを導入し、さらなる高速化を実現している。監査エージェント開発への示唆としては、長大な監査ログや取引履歴など100万トークン規模のシーケンスをメモリ効率よく処理できる点が有望であり、RNNライクな逐次推論特性はオンライン異常検知にも適合しうる。

## アイデア

- B・C・∆を入力依存にする「選択的SSM」により、固定パラメータのS4が解けない選択的コピータスクを解けるようになる点は、情報フィルタリング機構としての設計思想が面白い
- 同一モデルが学習時はCNN（並列畳み込み）として、推論時はRNN（逐次再帰）として動作するという二重の解釈が成り立ち、両者のメリットを同時に享受できる構造
- State Space Duality（Mamba2）によりSSMとアテンションが同一の半可分行列クラスとして統一的に定式化され、両者を連続したスペクトム上の設計選択として捉えられる点

## 前提知識

- **Transformer / Attention機構** (TODO: 読むべき)
- **RNN / LSTM** (TODO: 読むべき)
- **状態空間モデル（SSM）** → /deep_926 Mamba解説：Transformerに挑む状態空間モデル（SSM）
- **畳み込みニューラルネットワーク（CNN）** (TODO: 読むべき)
- **FlashAttention** → /deep_221 Differential Transformer V2：カスタムカーネル不要・推論高速化を実現した差分注意機構の改良版

## 関連記事

- /deep_2510 多層SSMの表現能力と限界：深さ・精度・Chain-of-Thoughtの相互作用
- /deep_199 Titans + MIRAS: AIに長期記憶を持たせる新アーキテクチャ
- /deep_3105 Sessa: 選択的状態空間アテンション — フィードバックパス内にアテンションを組み込む新デコーダ
- /deep_2480 量子化へのKLレンズ：混合精度SSM-Transformerモデルの高速・順伝播のみの感度分析
- /deep_1975 WUTDet: 密集した小物体を含む10万スケールの船舶検出データセットとベンチマーク

## 原文リンク

[Mamba解説：Transformerに挑む状態空間モデル（SSM）](https://thegradient.pub/mamba-explained/)
