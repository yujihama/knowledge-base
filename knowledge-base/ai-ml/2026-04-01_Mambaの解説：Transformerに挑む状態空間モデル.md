---
title: "Mambaの解説：Transformerに挑む状態空間モデル"
url: "https://thegradient.pub/mamba-explained/"
date: 2026-04-01
tags: [Mamba, SSM, 状態空間モデル, Transformer, 長文脈, 選択的SSM, S6, ZOH離散化, Hardware-Aware]
category: "ai-ml"
memo: "[The Gradient] Mamba Explained"
related: [199, 222, 833, 255, 1494]
processed_at: "2026-04-01T21:05:51.881010"
---

## 要約

MambaはAlbert GuとTri Daoが開発した状態空間モデル（SSM）ベースのシーケンスモデルで、Transformerのコアボトルネックである二次計算複雑度（O(n²)）を解消する。Transformerはアテンション機構によりすべてのトークンが過去のすべてのトークンを参照するため、学習時O(n²)・推論時O(n)の時間計算量とO(n)のKVキャッシュメモリを要する。これに対しMambaは制御理論由来のSSMを採用し、線形時間O(n)でシーケンスを処理する。

基本となる連続時間SSMの数式はh'(t) = Ah(t) + Bx(t)、y(t) = Ch(t) + Dx(t)で表され、隠れ状態hが過去の情報を圧縮する。実際の離散系への変換（離散化）にはZero-Order Hold（ZOH）法を用い、離散パラメータĀ・B̄を導出する。畳み込み表現を用いると学習を並列化できるため効率的なGPU活用が可能になる。

Mambaの最大の革新は「選択的状態空間モデル（S6）」の導入にある。従来のS4等の線形時不変SSMは固定パラメータA・B・Cを用いるため、どの情報を保持・破棄するかをコンテキストに応じて動的に変えられなかった。MambaではB・C・ステップサイズΔを入力依存にすることで、関連性の高い情報を選択的に記憶し不要な情報を忘却できる。これはTransformerのアテンション機構と類似したコンテンツベースの情報選択を実現する。

ただし入力依存パラメータはバッチ処理や畳み込み計算が困難になるため、通常のGPUメモリ階層では非効率になる。これをHardware-Aware Parallel Algorithmで解決し、HBMとSRAM間のデータ転送を最小化するFlashAttention類似の手法でカーネル融合を実施。結果としてTransformerと比較して推論速度最大5倍・メモリ使用量の大幅削減を達成した。

Mamba-3Bモデルはthe Pileベンチマークで同サイズのTransformerを上回り、2倍サイズのTransformerと同等の性能を示す。言語・音声・ゲノミクスなど複数モダリティでSOTA性能を達成。100万トークン規模のシーケンスでも線形スケーリングを維持する。

課題として、隠れ状態が固定サイズの圧縮表現であるため、完全な過去の参照が必要なタスク（例：超長文書の特定箇所の正確な再現）ではTransformerのKVキャッシュに劣る可能性がある。また解釈可能性の観点では、Transformerのアテンションパターン可視化と異なりSSMの隠れ状態は解釈が難しく、AIセーフティ研究への応用は現時点で限定的とされる。

## アイデア

- 隠れ状態を「過去の圧縮」として定式化することで、無限長の履歴を固定サイズベクトルで近似できる点は、エージェントの会話履歴管理に応用できる発想
- 入力依存パラメータ（選択的SSM）により「今この入力に関連する情報だけを状態に保持する」動的フィルタリングが実現しており、RAGの代替として長文書の内部表現に活用できる可能性
- Hardware-Aware Parallel Algorithmでカーネル融合とメモリ階層最適化を組み合わせることで、アルゴリズムの理論的制約をハードウェア工学で克服するアプローチは、RTX 3090環境でのローカルLLM最適化にも参考になる
## 関連記事

- /deep_199 Titans + MIRAS: AIに長期記憶を持たせる新アーキテクチャ
- /deep_222 Falcon-H1-Arabic: ハイブリッドMamba-Transformerアーキテクチャによるアラビア語AI最前線
- /deep_833 Falcon 3 ファミリー：10B以下の高性能オープンモデル群の紹介
- /deep_255 Apriel-H1: 効率的な推論モデル蒸留の意外なカギ
- /deep_1494 🤗 TransformersによるProbabilistic時系列予測

## 原文リンク

[Mambaの解説：Transformerに挑む状態空間モデル](https://thegradient.pub/mamba-explained/)
