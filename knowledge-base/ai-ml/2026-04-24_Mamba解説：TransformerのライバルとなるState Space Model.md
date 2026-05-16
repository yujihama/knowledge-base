---
title: "Mamba解説：TransformerのライバルとなるState Space Model"
url: "https://thegradient.pub/mamba-explained/"
date: 2026-04-24
tags: [Mamba, SSM, State Space Model, Transformer, 選択的状態空間, S6, 長文脈, 線形スケーリング, 制御理論, HBM最適化]
category: "ai-ml"
related: [2480, 2510, 1975, 199, 222]
memo: "[The Gradient] Mamba Explained"
processed_at: "2026-04-24T12:24:21.859996"
---

## 要約

MambaはAlbert GuとTri Daoが開発したState Space Model（SSM）ベースのシーケンスモデルで、Transformerが抱える二次計算量ボトルネックを回避しながら同等以上の性能を実現する。Transformerでは全トークン間のAttentionによりO(n²)の時間計算量とO(n)のKVキャッシュが必要になるが、Mambaは線形時間O(n)で動作し、シーケンス長に対してスケールする。

Mambaの核心は制御理論由来のSSM。状態方程式 h'(t) = Ah(t) + Bx(t) と出力方程式 y(t) = Ch(t) + Dx(t) により、隠れ状態hが過去の情報を圧縮して保持する。連続時間の微分方程式をZero-Order Hold（ZOH）離散化によって差分方程式に変換し、デジタルシステムとして実装する。

従来SSMの問題点は行列A・Bが入力xに依存しない（time-invariant）ことで、入力内容に応じて何に注目すべきかを選択できなかった。Mambaが提案するS6（Selective State Space）は、Δ・B・Cをxから動的に生成することで選択性（selectivity）を実現する。これによりモデルは関連情報を状態に保持し、無関係な情報を「忘れる」判断が可能になる。

実装上の課題として、選択的SSMは畳み込みで並列化できないため、単純実装では遅い。これをHardware-Aware Algorithmで解決する：再計算によってActivationの保存を回避しHBMアクセスを削減するカーネルフュージョン手法を用いる。結果として従来Transformerより最大5倍の高速推論を達成。

Mamba-3BはThe Pile評価でTransformerと同等以上の性能を示し、プリトレーニング・ダウンストリーム双方で自分と同サイズのTransformerを上回り、2倍サイズのTransformerに匹敵する。また音声・ゲノミクスなど複数モダリティでSoTAを記録。

アーキテクチャはMambaブロックを積み重ねた構成で、1ブロック内はSSM（Communication担当）＋Linear Projection（Computation担当）で構成され、TransformerのAttention+MLPに対応する。推論時は固定サイズの隠れ状態のみ保持すれば良いためメモリ効率が高く、100万トークン超のコンテキストを現実的なリソースで処理できる可能性がある。

解釈可能性・AI安全性の観点では、Transformerより内部状態の解釈が難しい面がある。隠れ状態は情報の圧縮であり、Mechanistic Interpretabilityの手法がそのまま適用できるかは研究途上。

監査エージェント開発への示唆：長大なログや監査証跡（監査証跡は数百万トークン相当になり得る）を効率的に処理するバックボーンとして、Mambaベースのモデルは有力な選択肢となる。特に逐次的な状態追跡（取引フローの異常検知等）は、SSMの「状態圧縮」というコンセプトと親和性が高い。

## アイデア

- 選択性（Selectivity）をΔ・B・Cの入力依存化で実現する点：入力に応じて動的にSSMパラメータを変えることで、Attentionに近い柔軟な情報選択をRecurrentな構造で実現している。この「入力に条件付けた忘却・記憶」メカニズムはエージェントのメモリ設計にも応用できる
- 推論時にO(1)メモリ（固定サイズ隠れ状態）でシーケンスを処理できる点：Transformerと異なりKVキャッシュが増大しないため、長期会話・長期監査ログ処理でGPUメモリOOMリスクを根本から排除できる
- Hardware-Aware Algorithmによる並列化の工夫：選択的SSMは数学的には並列化不可だが、再計算（recomputation）でActivation保存を省き、カーネルフュージョンでHBMラウンドトリップを削減することでGPUで高速実行する実装手法は、LLM推論最適化の汎用的なパターンとして参考になる

## 前提知識

- **Transformer** → /deep_2420 TransformersモデルをMLXに移植するSkillとテストハーネスの構築：オープンソースにおけるエージェント時代の貢献とは
- **Attention機構** → /deep_1010 LLMの金融市場への応用：価格予測・合成データ・マルチモーダル学習の可能性と限界
- **RNN/LSTM** (TODO: 読むべき)
- **State Space Model** → /deep_195 Mamba解説：TransformerへのState Space Modelによる挑戦
- **連続時間離散化** (TODO: 読むべき)

## 関連記事

- /deep_2480 量子化へのKLレンズ：混合精度SSM-Transformerモデルの高速・順伝播のみの感度分析
- /deep_2510 多層SSMの表現能力と限界：深さ・精度・Chain-of-Thoughtの相互作用
- /deep_1975 WUTDet: 密集した小物体を含む10万スケールの船舶検出データセットとベンチマーク
- /deep_199 Titans + MIRAS: AIに長期記憶を持たせる新アーキテクチャ
- /deep_222 Falcon-H1-Arabic: ハイブリッドMamba-Transformerアーキテクチャによるアラビア語AI最前線

## 原文リンク

[Mamba解説：TransformerのライバルとなるState Space Model](https://thegradient.pub/mamba-explained/)
