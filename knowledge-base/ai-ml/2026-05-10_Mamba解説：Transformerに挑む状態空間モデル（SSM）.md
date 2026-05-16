---
title: "Mamba解説：Transformerに挑む状態空間モデル（SSM）"
url: "https://thegradient.pub/mamba-explained/"
date: 2026-05-10
tags: [Mamba, SSM, State Space Model, Transformer, 長文脈, HiPPO, FlashAttention, 選択的SSM, シーケンスモデル]
category: "ai-ml"
related: [3105, 2480, 2510, 1975, 199]
memo: "[The Gradient] Mamba Explained"
processed_at: "2026-05-10T21:12:39.181786"
---

## 要約

MambaはAlbert GuとTri Daoが開発した状態空間モデル（SSM）ベースのシーケンスモデルで、Transformerのボトルネックである二次計算量（O(n²)）を線形計算量（O(n)）に置き換えることで、最大100万トークン規模の長文脈処理を実現する。Transformerでは全トークン間のAttentionがKVキャッシュをO(n)メモリで要求し、生成速度もシーケンス長に比例して低下するが、MambaはSSMを用いた固定サイズの隠れ状態（hidden state）で過去情報を圧縮・保持する。

技術的な核心はS4（Structured State Space Sequence）モデルを進化させた選択的SSM（Selective SSM）にある。古典的SSMの行列A・B・Cは入力に依存しない定数だったが、Mambaでは入力x_tに応じてB・C・Δ（ステップサイズ）を動的に変化させる「Selection Mechanism」を導入した。これにより、関連性の高いトークンは長期記憶に保持し、不要な情報は忘却するという選択的フィルタリングが可能になった。

連続時間の微分方程式 h'(t)=Ah(t)+Bx(t)、y(t)=Ch(t)+Dx(t) をZero-Order Hold（ZOH）離散化によって差分方程式に変換し、h_t=Āh_{t-1}+B̄x_t、y_t=Ch_t として逐次計算する。訓練時はパラレルスキャン（並列プレフィックス和）を用いた畳み込み形式で高速化し、推論時はRNN的な逐次計算で実行する二重動作モードが特徴。さらにHardware-Aware Algorithmとして、行列A・Bを低ランクかつ構造化（HiPPO理論に基づくLegendre多項式最適化）することで、GPUのSRAMとHBM間のメモリ転送を最小化するFlashAttentionに類似した最適化を実現する。

Mamba-3Bは同サイズのTransformerを上回り、2倍サイズのTransformerに匹敵する性能をThe Pileで達成。推論速度はTransformer比最大5倍。ただし、インコンテキスト学習（ICL）や多段階推論タスクではAttentionの全コンテキスト参照能力に及ばない面もある。解釈可能性の観点では、Transformerのようなアテンション重みが存在せず、回路解析手法が未確立である。監査エージェント開発への示唆として、長い監査証跡ログや規制文書（100万トークン超）を単一コンテキストで処理できる可能性があり、ReActエージェントの状態管理にSSMの隠れ状態圧縮の発想を応用できる。

## アイデア

- Selection Mechanismにより入力依存でB・C・Δを動的変化させる点：これはRNNの固定ゲートとAttentionの全参照の中間的設計で、「何を記憶するか」を入力自体が決定するメタ認知的構造
- 訓練時は畳み込み（並列）、推論時はRNN（逐次）という二重動作モード：同一モデルが計算グラフを切り替えて動作する点は、ハードウェア制約に合わせてアルゴリズムを動的選択する設計思想として応用可能
- 隠れ状態が「過去の圧縮」として機能する点：監査ログや長期取引履歴のような時系列データを固定サイズのベクトルに圧縮しながら処理する用途で、メモリ効率と計算効率を両立できる可能性

## 前提知識

- **Transformer / Attention機構** (TODO: 読むべき)
- **RNN・LSTM** (TODO: 読むべき)
- **状態空間モデル（SSM）** → /deep_926 Mamba解説：Transformerに挑む状態空間モデル（SSM）
- **畳み込み演算** (TODO: 読むべき)
- **HiPPO理論** (TODO: 読むべき)

## 関連記事

- /deep_3105 Sessa: 選択的状態空間アテンション — フィードバックパス内にアテンションを組み込む新デコーダ
- /deep_2480 量子化へのKLレンズ：混合精度SSM-Transformerモデルの高速・順伝播のみの感度分析
- /deep_2510 多層SSMの表現能力と限界：深さ・精度・Chain-of-Thoughtの相互作用
- /deep_1975 WUTDet: 密集した小物体を含む10万スケールの船舶検出データセットとベンチマーク
- /deep_199 Titans + MIRAS: AIに長期記憶を持たせる新アーキテクチャ

## 原文リンク

[Mamba解説：Transformerに挑む状態空間モデル（SSM）](https://thegradient.pub/mamba-explained/)
