---
title: "Whisperの10倍速以上: NVIDIAの高速ASRモデル Canary-1B-v2 & Parakeet-TDT-0.6B-v3"
url: "https://zenn.dev/team_nishika/articles/1ab82243c2cf7b"
date: 2026-06-03
tags: [ASR, FastConformer, TDT, 音声認識, NVIDIA, NeMo, 多言語モデル, 疑似ラベル, Parakeet, Canary]
category: "ai-ml"
related: [264, 3012, 1884, 1807, 2454]
memo: "[Zenn LLM] 【Nishika 論文サク読み 第12回】Whisperの10倍速: Canary-1B-v2 & Parakeet-TDT-0.6B-v3"
processed_at: "2026-06-03T21:00:38.044576"
---

## 要約

NVIDIAは多言語音声認識（ASR）モデルの精度・速度・サイズのトレードオフを改善するため、2つのモデルを同時リリースした。Canary-1B-v2（1.2B）はASRと音声翻訳（AST）の多機能モデル、Parakeet-TDT-0.6B-v3（0.6B）はASR特化の超高速モデルである。両モデルともCC-BY-4.0ライセンスで商用利用可能。

アーキテクチャの核心はFastConformerというエンコーダで、TransformerとCNNを組み合わせた通常のConformerに対し3点の改善を施している：①8倍ダウンサンプリングで入力を圧縮、②Depthwise Separable Convolutionで畳み込みを軽量化、③カーネルサイズを31→9に縮小。これによりエンコーダ単体で2〜3倍の高速化を実現。なおnGPT（全埋め込みを単位超球面に制約するアーキテクチャ）も実験したが、fine-tuning後の最終精度でFastConformerが上回ったため採用された。

デコーダはモデルごとに異なる。Canary-1B-v2はTransformer（自己回帰）デコーダを使い翻訳も対応。Parakeet-TDT-0.6B-v3はTDT（Token & Duration Transducer）デコーダを採用し、「次のトークン」と「その継続時間」を同時予測することでデコードステップ数を削減、タイムスタンプも直接取得可能。

データ設計が最大の工夫で、合計170万時間を3つの戦略で整備している。①NVIDIAが構築したGranary（約100万時間の疑似ラベルデータ）、NeMo ASR Set 3.0（22.7万時間の人手ラベル）、補助翻訳データ（約48万時間）を組み合わせ。②無音でもテキストを出力するWhisperベースの疑似ラベルのハルシネーション問題に対し、非音声データ3.6万時間に空文字列ターゲットを付与して学習。③英語が40%を占める言語不均衡に対し、言語内バランシング（α=0.5）→言語間バランシング（β=0.5）の2段階サンプリングを適用（順序が重要で逆にすると低リソース言語が消滅する）。

学習はStage 1（X→En翻訳＋英語ASR、A100×64で150,000ステップ）、Stage 2（全タスク・全データ、100,000ステップ追加）、Stage 3（高品質サブセットのみで各言語200時間に均一化してfine-tuning）の3段階構成。

性能面では、HF Open ASR LeaderboardにおいてParakeet-TDT-0.6B-v3のRTFx（リアルタイム倍率）が3,332でWhisper-large-v3（145）の約23倍速く、平均WER 6.32%とWhisperの7.44%を上回る。Canary-1B-v2もRTFx 749（約5倍速）でWER 7.15%。多言語・翻訳ではSeamlessM4T-v2-large（2.3B、商用不可）と比較して1.2Bの半分以下のサイズで競争力のある精度を達成した。

## アイデア

- TDTデコーダがトークンと継続時間を同時予測することでデコードステップを削減し、タイムスタンプを追加コストゼロで取得できる設計は、ストリーミングASRや字幕生成パイプラインへの応用可能性が高い
- 言語内バランシング→言語間バランシングという順序制約が低リソース言語の保護に直結するという発見は、多言語データ混合の設計パターンとして汎用的に参考になる
- nGPTは事前学習の収束速度でFastConformerを上回ったにもかかわらず、fine-tuning後の精度で逆転された点は、新アーキテクチャの評価をfine-tuning後まで行う重要性を示している

## 前提知識

- **Conformer** → /deep_264 Open ASR リーダーボード：多言語・長時間音声認識トラック追加とトレンド分析
- **Transducer (RNN-T)** (TODO: 読むべき)
- **Whisper** → /deep_5160 通勤中に育てたAIが、放置していたアイデアを勝手に形にした【OpenClawエージェント4体を止めるまで①】
- **疑似ラベリング** (TODO: 読むべき)
- **自己回帰デコーダ** (TODO: 読むべき)

## 関連記事

- /deep_264 Open ASR リーダーボード：多言語・長時間音声認識トラック追加とトレンド分析
- /deep_3012 BlasBench：アイルランド語音声認識のためのオープンベンチマーク
- /deep_1884 🤗 TransformersでWav2Vec2を英語音声認識（ASR）にファインチューニングする
- /deep_1807 🤗 TransformersでWav2Vec2にn-gramを組み合わせて音声認識精度を向上させる
- /deep_2454 音声認識のための拡散言語モデル：MDLM・USDMによるASR仮説リスコアリングとCTC結合デコーディング

## 原文リンク

[Whisperの10倍速以上: NVIDIAの高速ASRモデル Canary-1B-v2 & Parakeet-TDT-0.6B-v3](https://zenn.dev/team_nishika/articles/1ab82243c2cf7b)
