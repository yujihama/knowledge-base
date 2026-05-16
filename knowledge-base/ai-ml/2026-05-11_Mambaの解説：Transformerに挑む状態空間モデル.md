---
title: "Mambaの解説：Transformerに挑む状態空間モデル"
url: "https://thegradient.pub/mamba-explained/"
date: 2026-05-11
tags: [Mamba, SSM, 状態空間モデル, Transformer代替, 線形計算量, 選択機構, 離散化, ZOH, Selective SSM, 長文脈]
category: "ai-ml"
related: [2510, 2480, 1837, 3105, 222]
memo: "[The Gradient] Mamba Explained"
processed_at: "2026-05-11T21:25:13.731661"
---

## 要約

Mambaは、Gu and Daoが提案した状態空間モデル（SSM）ベースのシーケンスモデルアーキテクチャであり、Transformerの二次計算量ボトルネックを克服することを目的としている。Transformerのアテンション機構はトークン間のペアワイズ通信を行うため、訓練時にO(n²)の時間計算量、推論時にO(n)のKVキャッシュメモリを要する。これにより長文脈（100万トークン規模）での使用が現実的でなくなる。Mambaはこの問題を、制御理論に由来するSSMを通信コンポーネントとして採用することで解決する。基本形式は連続時間微分方程式 h'(t) = Ah(t) + Bx(t) および y(t) = Ch(t) + Dx(t) で表され、これをZero-Order Hold（ZOH）離散化により差分方程式に変換して実装する。離散化後のSSMは畳み込みとして並列訓練が可能であり、再帰として線形時間推論が可能という二面性を持つ。従来のSSM（S4等）の課題は、行列A・B・Cが入力に依存しない（time-invariant）ため、入力内容に応じた動的な情報選択ができない点だった。Mambaはこれを「選択機構（Selective SSM）」で解決し、B・C・∆を入力xの関数として生成することでtime-varyingなシステムを実現する。ただしこの変更により畳み込みによる並列化が使えなくなるため、MambaはHardware-Aware Parallel Scanアルゴリズムを採用し、GPU HBMとSRAM間のメモリ転送を最適化することで最大5倍のTransformer比高速化を達成している。Mamba-3BはThe Pileベンチマークで同サイズのTransformerと同等以上、2倍サイズのTransformerに匹敵する性能を示す。ただし制限もあり：In-Context Learning（ICL）能力はTransformerより劣る可能性があり、Recall性能はRetrieval系タスクで弱いとされる。また状態サイズが固定（通常16）であるため、状態圧縮が不完全な場合に情報が失われる。解釈可能性の観点では、Mambaの隠れ状態はTransformerのアテンションヘッドに比べ解釈が難しく、メカニスティック解釈可能性研究への新たな課題を提示する。監査エージェントシステムへの応用としては、長い監査ログや証跡データの処理において線形計算量は大きなメリットとなり、特に数万トークン規模の内部統制文書の継続的な文脈保持に有効と考えられる。

## アイデア

- SSMを畳み込み（並列訓練）と再帰（線形推論）の両方として解釈できる二面性は、訓練と推論で計算グラフを切り替えるエレガントな設計であり、同様の発想を他のアーキテクチャ設計に応用できる
- 入力依存のB・C・∆パラメータ生成（選択機構）により、モデルが「何を記憶し何を忘れるか」を動的に制御できる点は、LSTMのゲート機構の連続時間版とも解釈でき、長期依存の学習に本質的なアプローチを示している
- Hardware-Aware Parallel Scanによるカーネルフュージョンとメモリ階層最適化は、アルゴリズム設計とGPUアーキテクチャの共同最適化の重要性を示しており、将来のハードウェア専用設計SSMの可能性を示唆する

## 前提知識

- **Transformer / Attention機構** (TODO: 読むべき)
- **RNN / 再帰ニューラルネット** (TODO: 読むべき)
- **畳み込みニューラルネット（CNN）** (TODO: 読むべき)
- **KVキャッシュ** → /deep_3482 DeepSeek-V4：エージェントが実際に使える100万トークンコンテキスト
- **FlashAttention** → /deep_221 Differential Transformer V2：カスタムカーネル不要・推論高速化を実現した差分注意機構の改良版

## 関連記事

- /deep_2510 多層SSMの表現能力と限界：深さ・精度・Chain-of-Thoughtの相互作用
- /deep_2480 量子化へのKLレンズ：混合精度SSM-Transformerモデルの高速・順伝播のみの感度分析
- /deep_1837 UNDO Flip-Flop：状態空間モデルにおける可逆的意味状態管理の制御プローブ
- /deep_3105 Sessa: 選択的状態空間アテンション — フィードバックパス内にアテンションを組み込む新デコーダ
- /deep_222 Falcon-H1-Arabic: ハイブリッドMamba-Transformerアーキテクチャによるアラビア語AI最前線

## 原文リンク

[Mambaの解説：Transformerに挑む状態空間モデル](https://thegradient.pub/mamba-explained/)
