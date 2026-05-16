---
title: "3DモデルのセマンティックSearch検証：OpenCLIP×VLM×Qdrantによるマルチモーダル検索"
url: "https://zenn.dev/bestat/articles/5ced8b355ad8cf"
date: 2026-05-07
tags: [OpenCLIP, Qdrant, VLM, セマンティック検索, マルチモーダル, RRF, Objaverse, 3Dモデル, ベクトルDB, Gemini]
category: "ai-ml"
related: [1757, 21, 2511, 1974, 986]
memo: "[Zenn LLM] 3Dモデルのセマンティック検索にトライしてみた"
processed_at: "2026-05-07T09:47:05.730996"
---

## 要約

bestat株式会社が開発する産業向け3Dプラットフォーム「3D.Core」において、大量の3Dモデルを効率的に検索する基盤を構築するための検証報告。インデックス手法として2パターンを比較した。①3Dモデルを8視点からレンダリングし、Gemini 3 Flash Preview（Vertex AI経由）でVLM説明文を生成し、その説明文をOpenCLIP（ViT-L/14、laion2b_s32b_b82k、768次元）のテキストエンコーダでベクトル化（vlm_text）。②同じレンダリング画像をOpenCLIPの画像エンコーダで直接ベクトル化し平均プーリングで集約（clip_image）。ベクトルDBにはQdrantを使用し、Named vectorとして両方を同一Pointに格納。検証データはObjaverseのフルーツタグ付き3Dモデル545個を使用。検索クエリごとの特性が明確に分かれた。「Banana」テキスト検索ではvlm_textが意図せず強調表現（「BANANA!!!!!!!」）に引きずられた。「Spherical fruits」（球体のフルーツ）ではclip_imageが形状情報を内包しており優位。「Rotten fruits」（腐ったフルーツ）ではvlm_textが優位（形状だけでは腐敗を判別困難）。RRF（Reciprocal Rank Fusion）でfusionした結果は概ね良好で、各手法の強みが補完的に機能した。画像クエリ（クエリ自体にバナナ画像を入力）も実装しclip_imageで有効な結果を確認。今後の改善としてUni3Dによる3D表現そのもののベクトル化（形状クエリ対応）、LLM/VLMベースのリランク導入を検討。なお、検索UIはClaude Codeを使ってコーディングエージェントで迅速に作成しており、開発速度のデモとしても機能している。監査エージェント開発への示唆：マルチモーダルなembeddingを組み合わせてRRFでfusionする手法は、非構造化データ（PDF帳票、画像、テキスト）が混在する監査証拠の検索にも応用可能。クエリ特性に応じてvector空間を使い分けるアーキテクチャは、RAGパイプラインの精度向上に参考になる。

## アイデア

- 8視点レンダリング＋平均プーリングで3Dモデルを2D画像エンコーダのembedding空間に射影する手法は、3D専用エンコーダ不要で即実装可能な実用的アプローチ
- vlm_textとclip_imageのNamed vectorを同一Pointに持たせてRRFでfusionすることで、クエリの性質（形状/意味/テキスト）ごとに強みが補完しあう検索が実現できる
- 「腐ったフルーツ」のような概念的属性は画像エンコーダでは捉えにくくVLMテキストが優位という結果は、マルチモーダルRAGで用途別にembedding戦略を設計する重要性を示す

## 前提知識

- **OpenCLIP** (TODO: 読むべき)
- **Qdrant** → /deep_2877 SemiFA：半導体故障解析レポートを自律生成するエージェント型マルチモーダルフレームワーク
- **RRF（Reciprocal Rank Fusion）** (TODO: 読むべき)
- **VLM（Vision Language Model）** (TODO: 読むべき)
- **Named vector** (TODO: 読むべき)

## 関連記事

- /deep_1757 🤗 Datasetsで画像検索を構築する：FAISSとSentence Transformersを活用したセマンティック検索
- /deep_21 部分の総和を超えて：マルチモーダルヘイトスピーチ検出における意図変化の解読
- /deep_2511 患者教育をマルチターン・マルチモーダルインタラクションとして再考する
- /deep_1974 予測的埋め込みによるマルチモーダル潜在空間推論：Pearl フレームワーク
- /deep_986 ドキュメント画像向けマルチモーダルTextImageデータ拡張の紹介

## 原文リンク

[3DモデルのセマンティックSearch検証：OpenCLIP×VLM×Qdrantによるマルチモーダル検索](https://zenn.dev/bestat/articles/5ced8b355ad8cf)
