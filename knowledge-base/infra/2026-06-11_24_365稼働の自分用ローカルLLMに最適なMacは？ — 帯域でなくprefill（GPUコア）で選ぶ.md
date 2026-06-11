---
title: "24/365稼働の自分用ローカルLLMに最適なMacは？ — 帯域でなくprefill（GPUコア）で選ぶ"
url: "https://zenn.dev/znet/articles/2026-best-mac-247-local-llm"
date: 2026-06-11
tags: [ローカルLLM, Apple Silicon, MoE, RAG, Ollama, MLX, TTFT, prefill, Mac mini, 量子化]
category: "infra"
related: [7111, 7414, 2696, 3653, 7340]
memo: "[Zenn LLM] 24/365稼働の自分用ローカルLLMに最適なMacは? — 帯域でなくprefill(GPUコア)で選ぶ"
processed_at: "2026-06-11T12:11:10.102657"
---

## 要約

MacBook Air（M4・24GB・メモリ帯域120GB/s・GPU 10コア）を使い、OllamaとMLX-LMの両エンジンでローカルLLMを実測したレポート。decode速度・prefill速度・TTFT（最初のトークンまでの時間）を短文と長文RAG（2k〜6kトークン）の両条件で計測し、従来の「帯域＝速度」という直感を複数の実測値で覆している。

**decode（生成速度）は帯域120GB/sでも十分**：26B MoEモデル（活性パラメータ約4B）を4bit量子化で動かすと、短文38.9 tok/s・RAG長文34.1 tok/sを記録。人間の読速（約7〜8 tok/s）の4倍以上であり、対話用途では問題ない。MoEはトークンごとに活性化する一部パラメータ（〜4B）だけを読み込むため、総パラメータ数に比して帯域消費が小さい。

**本当のボトルネックはprefill/TTFT**：RAGで4.5kトークンのプロンプトを投入すると、warm状態でもTTFT約7.3秒。prefill速度は2モデル×2エンジンで〜330〜380 tok/sとほぼ横並びであり、エンジン選択では改善しない。prefillは行列演算主体でGPUコア数（compute）律速であるため、TTFTを短縮するには帯域ではなくGPUコア数の多い上位チップが必要。

**MLX vs Ollamaはモデル依存**：gpt-oss 20B（MXFP4）ではMLXのdecodeがOllama比×1.8だが、gemma系26Bではほぼ同等。prefillは両モデル・両エンジンで差なし。

**dense 12B はMoE 26Bより遅い**：dense 12B（〜7.7GB）はdecode 12.9 tok/s・TTFT約36秒。MoE 26B（〜14GB）はdecode 34.1 tok/s・TTFT約7秒。ファイルサイズが小さくても活性パラメータが多い分、低帯域機では不利。

**24GBでは2モデル同時常駐不可**：OllamaがGPUに使える実効枠は約17.8GiB。13〜14GBクラスのモデル2本を同時常駐させるには64GB以上が必要。

**選定指針**：軽い短文・1モデル運用ならベースM4で十分。RAG長文・複数モデル切替・同時常駐が要件ならM4 Pro/Maxクラス＋64GBが軸。24/365常駐用途にはスリープや発熱スロットルの問題があるファンレスノートは不向きで、Mac mini/Studioなどの据え置き機を常駐サーバとして使う構成が合理的。監査エージェント開発でRAGを多用する場合、TTFTがユーザー体験を左右するため、チップ選定でGPUコア数を優先する判断が直接パフォーマンスに影響する。

## アイデア

- prefillはエンジン（Ollama/MLX）非依存でGPUコア律速という実証：2モデル×2エンジンで〜330〜380 tok/sに収束し、TTFTの改善はソフトウェアではなくハード（GPUコア数）の問題であることを示した点
- 「小さいモデル＝速い」という直感の崩壊：dense 12Bがファイルサイズ半分にもかかわらずMoE 26Bより3倍近く遅い（decode 12.9 vs 34.1 tok/s）という活性パラメータ概念の実証
- RAGアプリの満足度指標をdecodeからTTFT（prefill）に再定義：decode速度は全ティアで既に十分であり、ハード選定の主軸をメモリ帯域からGPUコア数＋容量（同時常駐）へシフトさせるという設計思想の転換

## 前提知識

- **MoE（Mixture of Experts）** (TODO: 読むべき)
- **prefill / decode** (TODO: 読むべき)
- **量子化（4bit）** (TODO: 読むべき)
- **RAG** → /deep_5 Google Research at The Check Up: ヘルスケアAIの最新研究成果と実臨床への展開（2026年）
- **ユニファイドメモリ** (TODO: 読むべき)

## 関連記事

- /deep_7111 【2026年最新】LFM2.5-8B-A1BをApple Siliconで実測 — 「1月のLFM2.5」との違いと実際の速度
- /deep_7414 M1 Pro 32GBでQwen3.6-35B-A3Bを本気で使ってみた正直な話
- /deep_2696 日本語入力システムSumibiの開発 part18: ローカルLLMが閾値を超えたかも
- /deep_3653 システムダイナミクスAIアシスタントのベンチマーク：クラウドLLM対ローカルLLMによるCLD抽出・議論タスク評価
- /deep_7340 Qwen2.5-Coder-7BをMLXで量子化してMac Mini M4 16GBにLLMサーバを構築する方法

## 原文リンク

[24/365稼働の自分用ローカルLLMに最適なMacは？ — 帯域でなくprefill（GPUコア）で選ぶ](https://zenn.dev/znet/articles/2026-best-mac-247-local-llm)
