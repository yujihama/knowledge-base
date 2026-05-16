---
title: "Mamba解説：Transformerに挑む状態空間モデル（SSM）"
url: "https://thegradient.pub/mamba-explained/"
date: 2026-05-15
tags: [Mamba, SSM, 状態空間モデル, Transformer, 長文脈処理, HiPPO, 選択的状態空間, 線形RNN, FlashAttention, シーケンスモデル]
category: "ai-ml"
related: [2510, 199, 3105, 2480, 1975]
memo: "[The Gradient] Mamba Explained"
processed_at: "2026-05-15T21:14:43.334539"
---

## 要約

MambaはAlbert GuとTri Daoが開発した状態空間モデル（SSM）ベースのシーケンスモデルで、Transformerのアテンション機構が抱える二次計算量ボトルネックを解消することを目的としている。Transformerでは全トークン間のペアワイズ通信によりトレーニング時O(n²)の計算量、推論時O(n)のKVキャッシュメモリが必要となる。Mambaはこれをシーケンス長に対して線形スケールするSSMで置き換え、最大100万トークンの長文脈処理を可能にしつつ、Transformerと同等またはやや優れたスケーリング則を達成している。Mamba-3Bは同サイズのTransformerを上回り、2倍サイズのTransformerに匹敵する性能を示し、推論速度はTransformerの最大5倍に達する。

SSMの核心は制御理論に基づく状態遷移方程式 h'(t) = Ah(t) + Bx(t)、y(t) = Ch(t) + Dx(t) で表され、隠れ状態hが過去の情報を圧縮保持する。連続時間の微分方程式はZero-Order Hold（ZOH）離散化により差分方程式へ変換され、実装可能になる。さらにAの構造にHiPPO行列を採用することで、遠い過去の情報を数学的に最適に保持できる。

従来のSSM（S4等）との最大の違いは「選択性（Selectivity）」にある。S4のパラメータA・B・Cは入力に依存しない固定値だったが、Mambaでは入力xに応じてB・C・Δを動的に変化させる。これにより「どの情報を記憶し、どの情報を忘れるか」を文脈に応じて判断できる。例えば「私の名前はジョンです。今日の天気は？」という文で名前情報を保持しつつ天気の質問に答えるような選択的記憶が可能になる。

ハードウェア最適化として、Mamba論文はHBM（High Bandwidth Memory）へのアクセスをSRAM（L1キャッシュ相当）への再計算で代替するFlashAttentionと同様の「カーネル融合」手法を採用し、実測でのスループット向上を実現している。

Mambaの限界として、アテンションに比べて情報の圧縮が強制的であるため、固定サイズの状態にすべての文脈を詰め込む必要がある。「Jojo引用問題」（テキスト内の特定フレーズを正確に取り出す）のような事実検索タスクではTransformerに劣る傾向がある。解釈可能性の観点からも、隠れ状態の意味解釈がAttention headに比べて困難であり、AIアライメント・安全性研究への応用に課題を残す。現時点ではハイブリッドアーキテクチャ（MambaブロックとAttentionブロックの混合）が有力な実用解とみられている。

## アイデア

- SSMの「選択性」はRNNのゲート機構（LSTMのforget gate）の連続時間版とみなせるが、入力依存パラメータにより離散的なトークン列への適用を自然に拡張した点が革新的
- HiPPO行列によるAの構造化は「過去の情報をルジャンドル多項式で近似する」という数学的に最適な記憶圧縮であり、ランダム初期化より長距離依存性の学習が安定する
- 監査エージェント文脈では、監査証跡・ログのような超長シーケンス（数十万トークン）の処理にMambaのO(n)スケーリングが有効で、証跡全体を単一モデルに通すことで、Transformerでは不可能だった長期パターン検出が可能になる可能性がある

## 前提知識

- **Transformer / Attention機構** (TODO: 読むべき)
- **RNN / LSTM** (TODO: 読むべき)
- **状態空間モデル（SSM）** → /deep_926 Mamba解説：Transformerに挑む状態空間モデル（SSM）
- **HiPPO行列** → /deep_3633 Mamba解説：Transformerに挑む状態空間モデル
- **FlashAttention** → /deep_221 Differential Transformer V2：カスタムカーネル不要・推論高速化を実現した差分注意機構の改良版

## 関連記事

- /deep_2510 多層SSMの表現能力と限界：深さ・精度・Chain-of-Thoughtの相互作用
- /deep_199 Titans + MIRAS: AIに長期記憶を持たせる新アーキテクチャ
- /deep_3105 Sessa: 選択的状態空間アテンション — フィードバックパス内にアテンションを組み込む新デコーダ
- /deep_2480 量子化へのKLレンズ：混合精度SSM-Transformerモデルの高速・順伝播のみの感度分析
- /deep_1975 WUTDet: 密集した小物体を含む10万スケールの船舶検出データセットとベンチマーク

## 原文リンク

[Mamba解説：Transformerに挑む状態空間モデル（SSM）](https://thegradient.pub/mamba-explained/)
