---
title: "fairseq WMT19翻訳システムをTransformersへ移植する"
url: "https://huggingface.co/blog/porting-fsmt"
date: 2026-04-15
tags: [fairseq, Transformers, WMT19, 機械翻訳, BPE, チェックポイント変換, Moses, seq2seq, 移植]
category: "ai-ml"
related: [1529, 1266, 1807, 1760, 158]
memo: "[HF Blog] Porting fairseq wmt19 translation system to transformers"
processed_at: "2026-04-15T12:26:09.151102"
---

## 要約

本記事は、FacebookのFAIRが開発しWMT19ニュース翻訳タスクで使用した高品質翻訳システム（fairseq wmt19）を、Hugging Face Transformersライブラリへ移植した詳細な作業記録である。移植対象はen-ru/ru-en（英語⇔ロシア語）およびde-en/en-de（ドイツ語⇔英語）の4言語ペアで、各言語ペアに4つのチェックポイント（各約3.5GB）が存在する。

移植作業は主に以下の構成ファイルの新規作成から成る：設定クラス（configuration_fsmt.py）、チェックポイント変換スクリプト（convert_fsmt_original_pytorch_checkpoint_to_pytorch.py）、モデルアーキテクチャ実装（modeling_fsmt.py）、トークナイザ（tokenization_fsmt.py）、テストコード（test_modeling_fsmt.py / test_tokenization_fsmt.py）。

技術的な難所の一つが「語彙（vocabulary）の扱い」である。en-ru/ru-enは2つの別個の辞書（dict.en.txt / dict.ru.txt）を使用するのに対し、de-en/en-deは共有マージ済み語彙を使用する。両パターンをサポートするため、FSMTConfigにsrc_vocab_size/tgt_vocab_sizeの独立フィールドを設け、2辞書構造を優先的に実装した後、マージ語彙を簡易ケースとして吸収する設計を採用した。

fairseqのTransformerモデルの重みテンソル形状がHugging FaceのBARTモデルと異なる部分が複数存在したため、変換スクリプト内で形状変換（transpose）や名前マッピングを丁寧に行っている。特にself-attention用のQKV重みは、fairseqがqkv_proj.weight（3次元テンソル）として格納するのに対し、Transformersは個別のq_proj/k_proj/v_projとして管理するため、手動分割が必要だった。

数値的等価性（numerical equivalency）の検証は移植の正確性確認において中心的な作業であり、fairseqの出力テンソルとTransformers側の出力テンソルをtorch.allcloseで比較しながら、layer単位で一致を確認する手順が詳述されている。最終的にトークナイザ・エンコーダ・デコーダを含むEnd-to-Endの翻訳出力が一致することを確認している。

トークナイザにはMosesデコーダとfastBPE（Byte Pair Encoding）が組み合わされており、前処理（tokenize→BPE encode）と後処理（BPE decode→detokenize）の両方をtokenization_fsmt.pyに実装した。これにより従来はfairseq環境外で利用不可能だったWMT19翻訳モデルを、Transformers標準APIから直接利用できるようになった。

監査エージェント開発への示唆としては、外部ツールやフレームワークの成果物（学習済みモデル、ルール定義）を自組織のエージェントパイプラインへ取り込む際の「変換・検証パターン」が参考になる。特に「小さなチートから始めてプロキシで動作確認し、段階的に本格移植する」アプローチは、LangGraphベースの監査エージェントに外部モデルを統合する際の設計手順として応用できる。

## アイデア

- 「まずプロキシAPIで動作確認してから本格移植」というチート戦略は、大規模モデル統合時のリスク低減に有効
- 2語彙（src/tgt分離）と共有語彙の両方をFSMTConfigのsrc_vocab_size/tgt_vocab_sizeで統一的に表現する設計は、多言語対応の汎用性を高める
- layer単位でのtorch.allclose検証によりデバッグ箇所を特定する「数値等価性テスト」は、モデル変換・量子化・蒸留プロセス全般に転用できる品質保証手法

## 前提知識

- **Transformer（seq2seq）** (TODO: 読むべき)
- **BPE（Byte Pair Encoding）** (TODO: 読むべき)
- **fairseq** (TODO: 読むべき)
- **Hugging Face Transformers** → /deep_1573 Hugging Face TransformersとHabana GaudiでBERTをスクラッチから事前学習する
- **PyTorch state_dict** (TODO: 読むべき)

## 関連記事

- /deep_1529 🤗 TransformersによるWhisperの多言語ASRファインチューニング
- /deep_1266 🤗 Transformersでネイティブサポートされる量子化スキームの概要
- /deep_1807 🤗 TransformersでWav2Vec2にn-gramを組み合わせて音声認識精度を向上させる
- /deep_1760 🤗 TransformersでViTを画像分類にファインチューニングする
- /deep_158 翻訳か暗唱か？極低リソース言語の機械翻訳評価スコアの較正

## 原文リンク

[fairseq WMT19翻訳システムをTransformersへ移植する](https://huggingface.co/blog/porting-fsmt)
