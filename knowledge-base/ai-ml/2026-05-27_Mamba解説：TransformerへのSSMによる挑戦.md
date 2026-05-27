---
title: "Mamba解説：TransformerへのSSMによる挑戦"
url: "https://thegradient.pub/mamba-explained/"
date: 2026-05-27
tags: [Mamba, SSM, State Space Model, Transformer, 線形アテンション, セレクティビティ, S6, シーケンスモデル, 長文脈]
category: "ai-ml"
related: [3105, 2480, 2510, 1975, 199]
memo: "[The Gradient] Mamba Explained"
processed_at: "2026-05-27T09:24:08.767838"
---

## 要約

Mambaは、Albert GuとTri Daoが2023年に発表したState Space Model（SSM）ベースのシーケンスモデルで、Transformerのコアボトルネックである注意機構の二次計算複雑度O(n²)を線形O(n)に削減することを目的としている。

TransformerはKVキャッシュにO(n)のメモリを要し、長いシーケンスでのOOMエラーが問題だが、Mambaは制御理論由来の状態空間モデルを使って「状態（state）」という圧縮された過去情報を保持することで、全トークン間のペアワイズ通信を不要にする。数式上は連続時間の微分方程式 h'(t) = Ah(t) + Bx(t)、y(t) = Ch(t) + Dx(t) を、Zero-Order Hold（ZOH）離散化により差分方程式へ変換して実装される。

SSMの歴史的な問題として「選択性の欠如」があった。S4等の古典的SSMはA・B・Cが入力に依存しない固定パラメータであるため、特定の情報を選択的に保持・忘却する能力に乏しく、言語タスクでの文脈把握が弱かった。Mambaの最大の革新は「セレクティビティ（Selectivity）」で、B・C・ΔパラメータをS6アルゴリズムにより入力x_tに依存させることで、どの情報を状態に取り込み、どれを無視するかを動的に制御できるようにした点にある。この選択機構によりコピータスクや言語理解での大幅な性能向上が実現された。

ただし、入力依存パラメータはバッチ処理時の行列並列化を阻害するため、通常のSSM畳み込み計算が使えない。Mambaはこれをパラレルスキャン（parallel scan）アルゴリズムとGPUのSRAM/HBM間のメモリ効率を最適化したカーネルフュージョンで解決し、Transformerと比べて最大5倍の推論速度を達成した。

Mamba-3BはThe PileベンチマークでTransformer同サイズモデルを上回り、2倍サイズのTransformerに匹敵するperplexityを達成。言語・音声・ゲノミクス等の複数モダリティでSOTA性能を示した。1Mトークンまで線形にスケールするため、長文脈が必要なアプリケーション（全会話履歴を記憶するチャットボット等）での優位性がある。

アーキテクチャとしては、Mambaブロックを積み重ねた構造を取り、各ブロック内でSSM（通信）とMLP投影（計算）を組み合わせる点はTransformerブロックの注意機構＋MLPと対応する。解釈可能性・AIセーフティ面では、Transformerの注意ヘッドに相当する解析手法がMambaにはまだ確立されていない課題もある。監査エージェント開発への示唆として、長い監査証跡・ログシーケンスを低コストで処理できるバックボーンとして活用可能性がある。

## アイデア

- セレクティビティ（B・C・Δの入力依存化）によりSSMがTransformerに匹敵する文脈選択能力を獲得した点：固定パラメータSSMとの差分が言語タスクの性能差を説明する鍵
- パラレルスキャンとGPUカーネルフュージョンの組み合わせにより、選択的SSMの本来の並列化困難性を克服した工学的アプローチ
- 状態を「過去の圧縮」と捉える設計思想：Transformerがすべての過去トークンを参照するのに対し、Mambaは固定サイズの隠れ状態に情報を凝縮するため、長文脈処理における記憶とコストのトレードオフが異なる

## 前提知識

- **Transformer** → /deep_2420 TransformersモデルをMLXに移植するSkillとテストハーネスの構築：オープンソースにおけるエージェント時代の貢献とは
- **Attention機構** → /deep_1010 LLMの金融市場への応用：価格予測・合成データ・マルチモーダル学習の可能性と限界
- **State Space Model** → /deep_195 Mamba解説：TransformerへのState Space Modelによる挑戦
- **RNN/LSTM** (TODO: 読むべき)
- **離散化（ZOH）** (TODO: 読むべき)

## 関連記事

- /deep_3105 Sessa: 選択的状態空間アテンション — フィードバックパス内にアテンションを組み込む新デコーダ
- /deep_2480 量子化へのKLレンズ：混合精度SSM-Transformerモデルの高速・順伝播のみの感度分析
- /deep_2510 多層SSMの表現能力と限界：深さ・精度・Chain-of-Thoughtの相互作用
- /deep_1975 WUTDet: 密集した小物体を含む10万スケールの船舶検出データセットとベンチマーク
- /deep_199 Titans + MIRAS: AIに長期記憶を持たせる新アーキテクチャ

## 原文リンク

[Mamba解説：TransformerへのSSMによる挑戦](https://thegradient.pub/mamba-explained/)
