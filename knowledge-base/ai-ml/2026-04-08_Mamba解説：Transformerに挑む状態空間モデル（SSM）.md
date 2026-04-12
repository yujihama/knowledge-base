---
title: "Mamba解説：Transformerに挑む状態空間モデル（SSM）"
url: "https://thegradient.pub/mamba-explained/"
date: 2026-04-08
tags: [Mamba, SSM, 状態空間モデル, SelectiveSSM, 線形スキャン, 長文脈推論, アーキテクチャ比較, Transformer代替]
category: "ai-ml"
memo: "[The Gradient] Mamba Explained"
processed_at: "2026-04-08T21:26:34.582461"
---

## 要約

MambaはAlbert GuとTri Daoが開発した状態空間モデル（SSM）ベースのシーケンスモデルで、Transformerのアテンション機構が抱える二次計算量ボトルネックを解消することを目指している。Transformerでは全トークン間のペアワイズ通信によりトレーニング時O(n²)の計算量、KVキャッシュのO(n)メモリが必要となり、長文脈（例：100万トークン）では実用的でない。Mambaはこれをコントロール理論由来のSSMで代替し、推論時O(1)の状態更新（線形スキャン）、トレーニング時O(n log n)の並列スキャンを実現する。

中核となるSSMは連続時間微分方程式 h'(t) = Ah(t) + Bx(t)、y(t) = Ch(t) + Dx(t) として定式化され、Zero-Order Hold（ZOH）法で離散化される。従来のS4等の線形時不変SSMと異なり、MambaはSelectiveSSMと呼ばれる選択的機構を導入：行列B・C・Δをトークン入力xに依存させることで「どの情報を状態に保持するか」を動的に制御する。この選択性こそがTransformerのコンテキスト依存的な注意に相当する能力をSSMに持たせるキーアイデアである。

ハードウェア面ではFlashAttentionと類似した手法でGPUのHBMアクセスを最小化するHardware-Aware Parallel Scanを実装。ただしTransformerとは異なりKVキャッシュ相当のものが存在しないため、単純な「既存トークンの参照」はできない（例：「最初のトークンを繰り返せ」といったタスクは苦手）。実験では3BパラメータのMamba-3BがThe Pileベンチマーク上で同サイズのTransformerと同等、2倍サイズのTransformerにも匹敵する性能を示し、推論速度はTransformerの最大5倍。

アーキテクチャ解釈の観点では、Mambaの状態hは「過去の圧縮表現」であり、固定サイズの隠れ状態に全文脈を圧縮するという設計上、Transformerに比べてメカニスティック解釈性が難しい側面もある。スケーリング則についても初期研究では概ねTransformerに匹敵するとされるが、長文脈タスクや特定のin-context learningベンチマークではTransformerが依然優位なケースもある。応用領域としてはゲノム解析・音声・長文書処理での成果が報告されている。

## アイデア

- 選択的SSM（SelectiveSSM）の設計思想：入力依存のパラメータB・C・Δによって「何を記憶し何を忘れるか」を動的制御することで、固定サイズ状態でも文脈感応的な表現が可能になるという原理は、RAGや長文書処理における情報圧縮の新しい視点を提供する
- 推論時O(1)状態更新という特性：自己回帰生成においてKVキャッシュが不要で固定サイズの隠れ状態のみを保持するため、無制限に長い会話履歴を一定メモリで扱える可能性があり、オンデバイス・エッジLLMとの相性が良い
- 解釈性のトレードオフ：Transformerのアテンションマップに相当する明示的な「どのトークンを参照したか」という可視化が困難であり、監査や説明可能性が求められるユースケースでの採用には慎重な検討が必要
## 関連記事

- /deep_222 Falcon-H1-Arabic: ハイブリッドMamba-Transformerアーキテクチャによるアラビア語AI最前線
- /deep_833 Falcon 3 ファミリー：10B以下の高性能オープンモデル群の紹介
- /deep_255 Apriel-H1: 効率的な推論モデル蒸留の意外なカギ
- /deep_617 ワーキングペーパー：人工汎用知能のための圏論的比較フレームワークに向けて
- /deep_410 Transformers.js v4：NPMで正式リリース — WebGPUランタイム完全刷新とブラウザ・サーバ横断対応

## 原文リンク

[Mamba解説：Transformerに挑む状態空間モデル（SSM）](https://thegradient.pub/mamba-explained/)
