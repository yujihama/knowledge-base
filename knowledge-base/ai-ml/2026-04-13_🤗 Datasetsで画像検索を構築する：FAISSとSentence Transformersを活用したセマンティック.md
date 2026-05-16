---
title: "🤗 Datasetsで画像検索を構築する：FAISSとSentence Transformersを活用したセマンティック検索"
url: "https://huggingface.co/blog/image-search-datasets"
date: 2026-04-13
tags: [CLIP, FAISS, sentence-transformers, HuggingFace Datasets, 画像検索, セマンティック検索, ImageFolder, マルチモーダル]
category: "ai-ml"
related: [1615, 1256, 1572, 21, 577]
memo: "[HF Blog] Image search with 🤗 datasets"
processed_at: "2026-04-13T12:34:52.731069"
---

## 要約

Hugging Face の `datasets` ライブラリを使って、画像のセマンティック検索アプリケーションを構築する手順を解説したブログ記事（2022年3月公開）。

対象データセットは英国図書館がデジタル化した書籍から抽出した画像コレクション「Digitised Books - Images identified as Embellishments（c.1510〜c.1900）」のサブセット（約10,000枚）。画像にはメタデータがほとんどなく、タグ検索以上の「意味的な検索」が課題となっていた。

技術スタックは以下の通り：
- **datasets**：`ImageFolder` ローダーで画像フォルダを直接ロード、`map()` でメタデータ抽出、`push_to_hub()` でHub公開
- **Sentence Transformers**：`clip-ViT-B-32` モデルを使って各画像をベクトル埋め込みに変換。CLIPはテキストと画像を同じ埋め込み空間に射影するため、テキストクエリでも画像クエリでも検索可能
- **FAISS**：`dataset.add_faiss_index()` で埋め込みに対して効率的な近傍探索インデックスを構築。`dataset.get_nearest_examples()` でクエリベクトルに近い画像を取得

処理フローは：①画像ロード → ②CLIPで各画像をベクトル化（`dataset.map()` で `clip_embeddings` カラムを追加）→ ③FAISSインデックス追加 → ④テキスト or 画像クエリをCLIPでベクトル化 → ⑤`get_nearest_examples()` で類似画像を取得。

テキスト検索では「a dog" や "an interesting book illustration" 等のクエリで意味的に近い画像が返る。画像クエリ（既存画像を入力）でも類似画像が検索可能。

データセットとFAISSインデックスはHubに保存でき、`load_from_disk()` や `load_dataset()` で再利用できる。これにより前処理済みデータを再配布・再利用しやすい。

監査エージェント開発への示唆：文書・証憑画像の類似検索基盤として同様のパイプライン（CLIP埋め込み＋FAISS）が応用可能。監査調書や証憑ファイルの「似た事例を素早く参照」ユースケースに直結する。また `datasets` の `push_to_hub` と `add_faiss_index` の組み合わせは、RAGパイプラインにおける画像モダリティ対応の実装パターンとして参考になる。

## アイデア

- CLIPモデルがテキストと画像を同一ベクトル空間に射影する性質を利用することで、テキストクエリ→画像検索・画像クエリ→類似画像検索の両方を単一インデックスで実現できる点
- datasetsの `add_faiss_index()` がデータセットオブジェクトに直接インデックスを付与でき、`get_nearest_examples()` で検索結果と元データを同時に返すAPI設計が実用的
- push_to_hub でFAISSインデックスごとデータセットをHub保存・共有できるため、埋め込み計算コストを一度で済ませて再利用可能なアーカイブとして機能する

## 前提知識

- **CLIP** → /deep_290 DRiffusion: ドラフト＆リファイン処理による拡散モデルの並列推論フレームワーク
- **FAISS** → /deep_487 Nishika 日本酒銘柄画像検索コンペ 7位解法（備忘録）
- **Sentence Transformers** → /deep_303 Sentence TransformersがHugging Faceに移管——月間100万ユーザーの埋め込みライブラリが新体制へ
- **HuggingFace Datasets** → /deep_1488 音声データセット完全ガイド：HuggingFace Datasetsで音声データを効率的に扱う方法
- **ベクトル埋め込み** (TODO: 読むべき)

## 関連記事

- /deep_1615 🤗 Datasetsにおける音声・画像データセット対応の新ドキュメント公開
- /deep_1256 街路ビュー地理位置推定のための空間重み付きCLIP（SW-CLIP）
- /deep_1572 🧨 DiffusersによるStable Diffusion：仕組みと実装ガイド
- /deep_21 部分の総和を超えて：マルチモーダルヘイトスピーチ検出における意図変化の解読
- /deep_577 大規模音声言語モデルに対するメンバーシップ推論攻撃の体系的評価

## 原文リンク

[🤗 Datasetsで画像検索を構築する：FAISSとSentence Transformersを活用したセマンティック検索](https://huggingface.co/blog/image-search-datasets)
