---
title: "OllamaのOLLAMA_NUM_PARALLELの最適値はどう決める？"
url: "https://zenn.dev/kspace_trk/articles/8348150e37bbbc"
date: 2026-04-24
tags: [Ollama, OLLAMA_NUM_PARALLEL, KVキャッシュ, VRAM, ggml, Flash Attention, 並列推論, vast.ai, GPU]
category: "infra"
related: [1264, 2105, 394, 408, 637]
memo: "[Zenn LLM] ollamaの OLLAMA_NUM_PARALLEL の数、どうやって決める？"
processed_at: "2026-04-24T12:30:07.902019"
---

## 要約

OllamaでLLM並列推論を行う際の`OLLAMA_NUM_PARALLEL`設定の決め方と、実環境での落とし穴を整理した実践的な備忘録。

**VRAMの消費構造：** 総VRAM消費は「モデルサイズ（固定）＋KVキャッシュ×OLLAMA_NUM_PARALLEL」で決まる。KVキャッシュはリクエストがなくても設定値分が起動時に即時予約されるため、「余裕があるときだけ使う」という設計は機能しない。WorkerとNUM_PARALLELは原則一致させる必要がある。

**VRAMが余っているのにクラッシュする問題：** gemma4:e2bを32GB VRAMで動かした実測では、VRAM計算上75並列が可能なはずが、並列数40付近で`ggml_nbytes(src0) <= INT_MAX`アサートで落ちる現象が発生した。原因はggml-cudaの一部カーネルがint型でバイトオフセットを扱うため、2GiB（INT_MAX）を超える中間テンソルを確保しようとする際にクラッシュする。この中間テンソルサイズは`OLLAMA_NUM_PARALLEL × コンテキスト長`に比例し、総KVトークン数100万付近から問題が顕在化する。具体的にはctx=32768で40並列（総KVトークン1,310,720）がクラッシュ、24並列（786,432）でOK、20並列（655,360）が安全という結果が得られた。対策はctxを8192に下げてNUM_PARALLEL=32とすることで、総KVトークンを262,144に抑えること。

**Flash AttentionとKV量子化のセット指定：** `OLLAMA_KV_CACHE_TYPE=q8_0`はFlash Attentionが有効でないとf16にフォールバックする。量子化で見積もり削減したつもりがOOMになる罠があるため、`OLLAMA_FLASH_ATTENTION=1`と必ずセットで指定する。

**curlとアプリで動作が異なる問題：** curlで未指定の場合はサーバーのデフォルトコンテキスト長（VRAM自動算出で32768等）が使われ、アプリ側が8192を明示していると同じNUM_PARALLEL=100でもcurl側はクラッシュ・アプリ側は動作するという非対称な結果になる。検証時はOLLAMA_CONTEXT_LENGTHを本番と揃えること。

**ボトルネック分析：** I/O主体のWebスクレイピング＋LLMバッチ処理ではGPU使用率が13〜30%にとどまり、ネットワークI/Oがボトルネックとなった。この場合は同一マシンの並列数増加より、PostgreSQLとFOR UPDATE SKIP LOCKEDを使ったタスクキュー＋vast.aiによる分散Worker構成が有効。

## アイデア

- KVキャッシュはリクエスト有無に関わらず起動時にNUM_PARALLEL分全量予約されるため、「余裕があれば使う」的な設定は意味をなさず、Workerと1:1対応が原則
- VRAMが余っていてもggml-cudaのint型オフセット制限（INT_MAX=2GiB）で中間テンソルがクラッシュするため、VRAM使用率だけ見ていると原因が特定できない
- curlとアプリでnum_ctxのデフォルト値が異なることで同一NUM_PARALLELでも動作が分岐するため、検証環境と本番でOLLAMA_CONTEXT_LENGTHを必ず明示的に揃える必要がある

## 前提知識

- **KVキャッシュ** → /deep_106 TurboQuant: 極限圧縮によるAI効率の再定義
- **VRAM** → /deep_2062 Dense vs MoE推論モデルの実力比較：Gemma 4, Phi-4, Qwen3を徹底検証
- **Flash Attention** → /deep_831 BERTの後継モデル登場：ModernBERTの紹介
- **ggml-cuda** (TODO: 読むべき)
- **コンテキスト長** (TODO: 読むべき)

## 関連記事

- /deep_1264 本番環境でのLLM最適化：低精度・Flash Attention・アーキテクチャ革新
- /deep_2105 VRAM 32GBのローカルLLM環境をコスパ重視で構築する：RTX 5060 Ti 16GB × 2枚刺し構成
- /deep_394 OpenClaw × OllamaをMacBook 16GBで動かす - ローカルLLM入門
- /deep_408 Google Cloud の GPU 付き Cloud Run で Ollama + ローカル LLM を動かす
- /deep_637 視覚メモリ機構によるマルチモーダル大規模言語モデルの長尺動画理解のスケーリング

## 原文リンク

[OllamaのOLLAMA_NUM_PARALLELの最適値はどう決める？](https://zenn.dev/kspace_trk/articles/8348150e37bbbc)
