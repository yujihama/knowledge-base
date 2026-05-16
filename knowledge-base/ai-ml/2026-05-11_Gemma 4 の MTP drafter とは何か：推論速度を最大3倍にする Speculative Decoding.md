---
title: "Gemma 4 の MTP drafter とは何か：推論速度を最大3倍にする Speculative Decoding の実装"
url: "https://zenn.dev/senna/articles/5737586098b4c2"
date: 2026-05-11
tags: [Speculative Decoding, MTP, Gemma 4, 推論高速化, drafter, hidden state, ローカルLLM, メモリ帯域]
category: "ai-ml"
related: [5217, 2696, 3909, 5037, 1420]
memo: "[Zenn LLM] 推論速度を最大 3 倍にした Gemma 4 の MTP drafter とは何か"
processed_at: "2026-05-11T21:31:09.123397"
---

## 要約

Googleが公開したGemma 4シリーズには、MTP（Multi-Token Prediction）draftarと呼ばれる機構が搭載されており、出力品質を劣化させずに推論速度を最大3倍に高める。

【ボトルネックの背景】ローカルマシンでのLLM推論では、1トークン生成のたびにモデルの全重みをメモリから演算ユニットへ転送し直す必要があり、メモリ帯域がボトルネックとなる。計算資源は余っているにもかかわらず重みの転送待ちが発生するという構造的な非効率がある。

【Speculative Decodingの仕組み】この遊んでいる計算資源を活用するのがSpeculative Decoding（投機的デコーディング）の発想。小さく速いdrafterモデルがK個のトークンを先読みで提案し、大きいtargetモデルが1回のforwardパスでまとめて並列検証する。重み転送コストが「1回/Nトークン」に下がるため、採用率70%の場合、1ステップで平均約3.5トークン進めることができ、2〜3倍の高速化が実現する。

【品質が落ちない理由】最終出力はtargetが承認したトークン列のみで構成される。draftが外れた位置ではtargetが自分でトークンを再サンプルするため、出力分布は数学的にtarget単独と同一に保たれる。量子化や蒸留と異なり「lossless」な高速化が実現できる。

【Gemma 4固有の密結合設計】通常のSpeculative Decodingではdrafterとtargetは完全に独立したモデルであり、語彙は共通でも埋め込み空間はそれぞれ別物。これに対しGemma 4のdrafterは、①入力埋め込みテーブルをtargetと共有（同一の意味空間で動作、追加メモリ不要）、②targetの最終層のhidden state（途中の思考状態）を直接受け取る、という2点でtargetと密結合している。draftarが「ゼロから考える」のではなく「targetの続きを書く」立場になるためトークン採用率が上がり、高速化効果が高まる。構成はtargetが通常の31B Transformer、drafterがtargetの内部状態にアクセスすることを前提に訓練された約0.5Bの補助LM。

## アイデア

- draftarがtargetのhidden stateを直接受け取る密結合設計により、独立モデル構成より高いトークン採用率を実現する点は、内部状態共有によるモデル協調の新しいパターン
- 出力分布を数学的にtargetと同一に保ちながら速度向上できる『lossless』性は、量子化・蒸留と根本的に異なる高速化アプローチであり、品質保証が必要な業務用途に適している
- 約0.5BのdrafterがアクセスするのはtargetのKVキャッシュではなく最終層のhidden stateという設計は、小型補助モデルの訓練目標と結合方式の選択として参考になる

## 前提知識

- **Speculative Decoding** → /deep_1379 アライメントフィードバックを用いたマルチドラフター投機的デコーディング
- **Transformer hidden state** (TODO: 読むべき)
- **KVキャッシュ** → /deep_3482 DeepSeek-V4：エージェントが実際に使える100万トークンコンテキスト
- **モデル蒸留** → /deep_188 DeepSeekの瞬間から1年：中国オープンソースAIエコシステムのアーキテクチャ選択
- **トークン生成（autoregressive decoding）** (TODO: 読むべき)

## 関連記事

- /deep_5217 MTP（Multi-Token Prediction）の系譜とメカニズムを徹底解説
- /deep_2696 日本語入力システムSumibiの開発 part18: ローカルLLMが閾値を超えたかも
- /deep_3909 llama.cppの設定で8GBの性能が5倍変わる — 主要オプションの最適値を出した
- /deep_5037 自分のトーン規約を渡してOllamaにZenn下書きを点検させる
- /deep_1420 秘匿環境で使うAI議事録の構成を考える - パイプライン型とLLM完結型の検証

## 原文リンク

[Gemma 4 の MTP drafter とは何か：推論速度を最大3倍にする Speculative Decoding の実装](https://zenn.dev/senna/articles/5737586098b4c2)
