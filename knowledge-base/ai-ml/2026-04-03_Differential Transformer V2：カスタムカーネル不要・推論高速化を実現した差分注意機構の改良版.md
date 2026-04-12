---
title: "Differential Transformer V2：カスタムカーネル不要・推論高速化を実現した差分注意機構の改良版"
url: "https://huggingface.co/blog/microsoft/diff-attn-v2"
date: 2026-04-03
tags: [Differential Attention, GQA, FlashAttention, attention-sink, Transformer, アーキテクチャ改良, RMSNorm, KVキャッシュ, YOCO, Microsoft]
category: "ai-ml"
memo: "[HF Blog] Differential Transformer V2"
processed_at: "2026-04-03T09:07:27.155727"
---

## 要約

Differential Transformer V2（DIFF V2）は、Microsoftが2026年1月に発表したDIFF V1の改良版アーキテクチャ。DIFF V1の課題であった「カスタムAttentionカーネルの必要性」「デコード速度の低下」「大規模学習時の数値不安定性」を解決する3つの主要変更を導入した。

**V1からV2への主要変更点：**
1. **KVヘッド数を増やさずQヘッド数を2倍化**：DIFF V1はQ/K/Vすべてを2セット持つ設計だったが、V2はQヘッドのみ2h本に増やし、KVヘッドはh本のまま維持する。差分操作（attn1 - sigmoid(λ) × attn2）はGQA同一グループ内の隣接ヘッド間で行われる。これによりKVキャッシュサイズは標準Transformerと同等となり、メモリバウンドなデコード速度が維持される。
2. **per-head RMSNormの除去**：DIFF V1では差分後にRMSNormを適用していたが、長さn=8192のシーケンスでは√nすなわち約90.5倍の拡大スケールが生じ、大規模学習で勾配スパイクが発生していた。V2ではλをトークン・ヘッドごとにXから投影するper-token設計に変更したことでRMSNorm不要となり、勾配ノルムスケールが標準Transformerと同等になった。
3. **λのper-token投影とsigmoid適用**：DIFF V1では層インデックスと学習可能スカラーから算出されるグローバル共有λだったが、V2ではXから線形投影されたλにsigmoidを適用するper-token・per-headの動的λを採用。これによりコンテキストRMSの範囲が標準Softmax注意の[1/√n, 1)から(0, √2)へ拡張され、アテンションシンクの解消と学習安定性向上が実現した。

**実験結果：** 標準Transformerおよびその他の効率化手法と比較した事前学習実験では、DIFF V2が言語モデリングのパープレキシティで優位性を示した。FlashAttentionカーネル（H/Bシリーズ GPU）使用時の事前学習スループット低下はわずか。長コンテキストのプリフィル時はYOCO（Gemma 3nでも採用）との組み合わせを推奨。コード実装はmicrosoft/unilmリポジトリで公開。

## アイデア

- per-token λ投影によりアテンション分布を動的に制御する設計は、特定トークンへの過剰集中（アテンションシンク）を構造的に抑制する手法として、RAGやlong-context推論の品質向上に応用できる
- KVヘッドを増やさずQヘッドのみ2倍化するという非対称設計は、GQAの枠組みを活用しつつデコード速度を維持する実装上の妙手であり、推論コスト重視の本番LLMに直接適用可能
- RMSNormが√nスケールの勾配爆発を引き起こすという定量的分析は、カスタムアーキテクチャ設計時の数値安定性チェックリストとして一般化できる知見

## Yujiの取り組みへの示唆

監査エージェントでは長文書（財務報告書・監査証跡）の処理が中心となるため、long-contextでのアテンションシンク解消と推論速度維持を両立するDIFF V2のアーキテクチャは、将来のローカルLLMインフラ（RTX 3090）上でのベースモデル選定や自作エージェント向けモデルのファインチューニング設計に参照価値がある。またper-token λ投影によるアテンション制御は、ReActエージェントでの証拠トークン選択精度向上のメカニズム理解にも役立つ。

## 原文リンク

[Differential Transformer V2：カスタムカーネル不要・推論高速化を実現した差分注意機構の改良版](https://huggingface.co/blog/microsoft/diff-attn-v2)
