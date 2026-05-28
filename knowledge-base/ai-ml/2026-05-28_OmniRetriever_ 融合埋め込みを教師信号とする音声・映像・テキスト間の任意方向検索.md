---
title: "OmniRetriever: 融合埋め込みを教師信号とする音声・映像・テキスト間の任意方向検索"
url: "https://tldr.takara.ai/p/2605.26641"
date: 2026-05-28
tags: [multimodal-retrieval, knowledge-distillation, InfoNCE, audio-video-text, embedding, RAG, zero-shot]
category: "ai-ml"
related: [2666, 5761, 5435, 4628, 1092]
memo: "[HF Daily Papers] OmniRetriever: Any-to-Any Audio-Video-Text Retrieval via Fusion-as-Teacher Distillation"
processed_at: "2026-05-28T09:11:36.372139"
---

## 要約

OmniRetrieverは、音声（Audio）・映像（Video）・テキスト（Text）の3モダリティ間で任意方向の検索を可能にする統合マルチモーダル埋め込みモデルである。従来の音声・映像・テキスト（AVT）エンコーダは3モダリティの融合埋め込みを生成できるが、学習時の目的関数はペアワイズのInfoNCEに留まり、3モダリティが揃った際の結合シグナルを活用できていなかった。

本研究ではこの問題を「Fusion-as-Teacher蒸留」で解決する。具体的には、3モダリティを融合した埋め込みをストップグラジェントで教師信号として扱い、各単一モダリティの埋め込みをその教師に近づける蒸留損失を課す。さらに融合埋め込み自体をTuple-InfoNCE損失で直接監督することで、結合表現の品質も同時に向上させる。この手法を7Bパラメータ規模のモデルとして実装したものがOmniRetriever-7Bである。

評価は6つのゼロショット検索ベンチマークで実施された。音声検索タスクであるClothoとSoundDescsでは、クローズドソースのGemini Embedding 2を R@1 で13.3〜18.0ポイント上回る。映像・テキスト検索タスクのMSR-VTTおよびMSVDでは、同時期の最先端ゼロショット専門モデル群と同等水準に達する。

さらに本論文では、12方向（A↔V、A↔T、V↔T、AVT複合など）のAVT検索を網羅する新ベンチマーク「OmniRetriever-Bench」を公開した。このベンチマークは合計3,782トリプルから構成される。OmniRetriever-7BはAVG-allスコア34.84を達成し、Gemini Embedding 2を1.72ポイント、オープンソースの既存最良AVT手法を8.03ポイント上回る。

監査AIやエージェントへの示唆として、マルチモーダルRAGシステムにこの手法を組み込むことで、音声ログ・映像記録・テキスト文書を横断した証跡検索が可能になる。内部監査エージェントが会議録音・画面録画・議事録テキストを統一空間で検索できる基盤として活用できる。

## アイデア

- 融合埋め込みを教師信号として単一モダリティ埋め込みを蒸留するFusion-as-Teacher手法は、追加データなしに3モダリティの相互情報を学習に活かせる点が巧妙
- Tuple-InfoNCEという3要素以上のタプル単位の対照学習損失を導入することで、ペアワイズ損失では捉えられなかった3モダリティ結合の構造を直接最適化している
- OmniRetriever-Benchの公開により、12方向のAVT検索を統一評価できる標準ベンチマークが生まれ、マルチモーダルRAGの研究比較が容易になる

## 前提知識

- **InfoNCE loss** (TODO: 読むべき)
- **Knowledge Distillation** → /deep_144 LLMにベイズ推論を学習させる：確率的推論の教示フレームワーク
- **Contrastive Learning** → /deep_1110 エネルギー効率の高いコード生成のためのContrastive Prompt Tuning初期探索
- **multimodal embedding** → /deep_3383 ConeSep: ノイズアンラーニングを用いた構成画像検索のためのコーンベース頑健ネットワーク
- **CLIP** → /deep_5966 Hermes Agentが12回自己改善した。ただし間違った目標に向かって ── self-improving loop実験記録

## 関連記事

- /deep_2666 ボトルネックトークンによる統合マルチモーダル検索
- /deep_5761 論文メモ：BERTからEmbeddingを整理する
- /deep_5435 検索を超えて：コード検索のためのマルチタスクベンチマークとモデル（CoREB）
- /deep_4628 ベクトルからRAGまで、Goで手を動かして理解するまでの記録
- /deep_1092 テキスト埋め込みはテキストを完全にエンコードするか？――vec2textによる埋め込みの逆変換

## 原文リンク

[OmniRetriever: 融合埋め込みを教師信号とする音声・映像・テキスト間の任意方向検索](https://tldr.takara.ai/p/2605.26641)
