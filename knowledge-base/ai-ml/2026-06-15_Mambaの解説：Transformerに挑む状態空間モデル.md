---
title: "Mambaの解説：Transformerに挑む状態空間モデル"
url: "https://thegradient.pub/mamba-explained/"
date: 2026-06-15
tags: [Mamba, SSM, 状態空間モデル, Transformer, 選択的状態空間, 長文脈, 線形計算量, 並列スキャン, 離散化, ZOH]
category: "ai-ml"
related: [2510, 3105, 7961, 2480, 7597]
memo: "[The Gradient] Mamba Explained"
processed_at: "2026-06-15T21:22:55.096061"
---

## 要約

MambaはAlbert GuとTri Daoが開発した状態空間モデル（SSM）ベースのシーケンスモデルで、Transformerのアテンション機構が抱える二次計算量ボトルネックを解消することを目的としている。Transformerでは全トークン間のペアワイズ通信（Attention）により訓練時O(n²)の時間計算量が発生し、KVキャッシュによりO(n)の空間も消費する。コンテキスト長が増加するほど推論速度が低下し、OOMエラーのリスクも高まる。Mambaはこの問題に対し、制御理論由来のSSMをトークン間通信に採用する。

SSMの核心は連続時間微分方程式 h'(t) = Ah(t) + Bx(t)、y(t) = Ch(t) + Dx(t) であり、隠れ状態hが過去の情報を圧縮して保持し、新たな観測xと組み合わせて出力yを予測する。これはMarkov決定過程的な設計で、状態が過去の圧縮表現として機能する。実装上は離散化（Zero-Order Hold法）により差分方程式に変換され、h_t+1 = Ā h_t + B̄ x_t の形式になる。

従来のSSM（S4等）はA, B, Cが入力に依存しない線形時不変（LTI）システムだったが、Mambaの最大の革新は**選択的状態空間（Selective SSM / S6）**の導入にある。B, C, Δを入力x_tの関数とすることで、どの情報を状態に保持し何を忘却するかをモデルが動的に制御できる。これにより「選択的コピー」や「誘導頭」相当の機能がアテンション不使用で実現される。

ただし入力依存化するとConvolution表現が使えなくなり、並列スキャン（Parallel Scan）という手法でシーケンス全体を並列処理する。さらにHardware-Aware Algorithmにより、計算をGPUのSRAM（L1キャッシュ相当）上で完結させFlash Attentionと同様の最適化を実現。結果としてTransformerより最大5倍高速な推論を達成する。

MambaブロックはSSM（通信）とMLP相当の射影（計算）で構成され、Transformerブロックのアテンション＋MLPに対応する。Mamba-3Bは同サイズのTransformerを凌駕し、2倍サイズのTransformerと同等の性能をThe Pile上で示している。言語・音声・ゲノミクスなど複数モダリティでSOTAを達成。

課題としては、固定サイズの隠れ状態によりin-context学習やプロンプトベースの操作が苦手な点、解釈可能性・AIセーフティ研究の手法（アクティベーションパッチング等）がSSM構造に適用しにくい点が挙げられる。監査エージェント開発への示唆としては、長大な監査証跡・ログシーケンスをO(n)で処理できる点が重要であり、数百万トークン規模の監査ログや契約書の連続読み込みに対してTransformerより適した基盤モデルバックボーンとなり得る。

## アイデア

- 選択的状態空間（S6）により入力に応じてB・C・Δを動的に変化させることで、アテンション機構なしに「どの情報を記憶し何を忘れるか」を制御できる点は、固定メモリを持つエージェントの設計に直接応用可能
- 隠れ状態hが過去全体の圧縮表現（Markov的）として機能する設計は、RAGや外部メモリと組み合わせた際の情報統合戦略を根本から問い直す契機になる
- Hardware-Aware Algorithmでカーネル融合とSRAM活用によりFlashAttentionと同等の最適化を実現している点は、SSMが理論的優位性だけでなく実装レベルでも競争力を持つことを示しており、今後のローカルLLMインフラ選定に影響する

## 前提知識

- **Transformer / Attention機構** (TODO: 読むべき)
- **状態空間モデル（SSM）** → /deep_926 Mamba解説：Transformerに挑む状態空間モデル（SSM）
- **畳み込みと再帰の双対性** (TODO: 読むべき)
- **FlashAttention** → /deep_221 Differential Transformer V2：カスタムカーネル不要・推論高速化を実現した差分注意機構の改良版
- **並列スキャン** → /deep_672 Mambaの解説：Transformerに挑む状態空間モデル

## 関連記事

- /deep_2510 多層SSMの表現能力と限界：深さ・精度・Chain-of-Thoughtの相互作用
- /deep_3105 Sessa: 選択的状態空間アテンション — フィードバックパス内にアテンションを組み込む新デコーダ
- /deep_7961 LLMに「睡眠」が必要な理由 ― 論文「Language Models Need Sleep」解説
- /deep_2480 量子化へのKLレンズ：混合精度SSM-Transformerモデルの高速・順伝播のみの感度分析
- /deep_7597 深層学習・生成AIの全体像を「3つの問い」で整理する｜CNNから拡散モデル・Mambaまで

## 原文リンク

[Mambaの解説：Transformerに挑む状態空間モデル](https://thegradient.pub/mamba-explained/)
