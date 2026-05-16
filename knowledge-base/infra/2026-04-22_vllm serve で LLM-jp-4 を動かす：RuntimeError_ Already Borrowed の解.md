---
title: "vllm serve で LLM-jp-4 を動かす：RuntimeError: Already Borrowed の解決策"
url: "https://zenn.dev/yay1/articles/ad6958086670b0"
date: 2026-04-22
tags: [vLLM, LLM-jp-4, reasoning-parser, vllm serve, ローカルLLM, RuntimeError, トークナイザー]
category: "infra"
related: [2067, 419, 158, 1420, 1434]
memo: "[Zenn LLM] vllm serve でLLM-jp-4を動かす"
processed_at: "2026-04-22T12:09:40.044071"
---

## 要約

vLLM 0.18.0 を使って llm-jp/llm-jp-4-8b-thinking モデルを `vllm serve` コマンドでホスティングする際、カスタムの reasoning-parser-plugin（llmjp4_reasoning_parser.py）を `--reasoning-parser-plugin` オプションで指定すると `RuntimeError: Already borrowed` が発生する問題とその解決策を解説している。

エラーの根本原因は、vLLM の内部処理（`vllm/renderers/base.py` の `_tokenize_prompt_async`）でトークナイザーを非同期に使用している最中に、reasoning parser の初期化処理が同じトークナイザーインスタンスに並行アクセスしたことによる Rust の借用チェッカー（borrow checker）的な排他制約違反である。

解決策は、reasoning parser の `__init__` 内で `tokenizer.encode()` を呼び出している箇所をハードコードされた固定トークン ID に置き換えることである。具体的には `self._reasoning_end_prefix = tokenizer.encode("<|channel|>final")` を `[9, 2520]` に、`self._reasoning_prefill = tokenizer.encode("<|start|>assistant")` を `[10, 12811]` に変更する。これにより初期化時のトークナイザーへのアクセスが排除され、エラーが解消される。

parser 本体の実装は GptOssReasoningParser をベースにしており、`is_reasoning_end`（reasoning 終端の検出）、`extract_content_ids`（最終チャンネルのコンテンツ抽出）、`extract_reasoning_streaming`（ストリーミング時の reasoning/content デルタ分離）などのメソッドを llm-jp-4 の HarmonyMessageParser 形式に合わせて実装している。非ストリーミングの `extract_reasoning` はインターフェース制約により完全実装が困難なため workaround 実装となっており、警告が出る。

補足として、LLM-jp-4 公式 cookbook では `vllm serve` ではなく `vllm.entrypoints.cli` を使う形で CLI ホスティングを実装しており、そちらでは `import llmjp4_reasoning_parser` を明示的に行うことで初期化を通している。監査エージェント開発への示唆としては、ローカル LLM をサービングする際に vLLM の非同期トークナイザー処理と拡張プラグインの初期化タイミングの競合が発生しうる点を把握しておく必要がある。特に RTX 3090 環境で LLM-jp-4 系モデルを推論 API として公開する場合、このパッチを適用しないと起動段階でクラッシュするため注意が必要。

## アイデア

- Rust の borrow checker 由来の `Already borrowed` エラーが Python の vLLM 拡張ポイントにも波及する点：トークナイザーの内部実装が Rust (tokenizers ライブラリ) であるため、非同期コンテキストでの並行アクセスが排他制約に引っかかる
- 初期化時の `tokenizer.encode()` 呼び出しをハードコード値に置き換えることでレースコンディションを回避するアプローチ：モデルの語彙が固定である前提で成立する、実用的だが脆いワークアラウンド
- 公式 cookbook が `vllm serve` ではなく `vllm.entrypoints.cli` を採用している理由がこの問題と関係している可能性：エントリーポイントによって初期化シーケンスが異なり、plugin の import タイミングも変わる

## 前提知識

- **vLLM** → /deep_27 Holotron-12B - 高スループット・コンピュータ使用エージェント向けマルチモーダルモデル
- **ReasoningParser** (TODO: 読むべき)
- **LLM-jp-4** → /deep_2067 医薬分野のQ&AでローカルLLMを評価する④：Gemma-4-E2B・LLM-JP-4-8B-Thinking・JPharmatron-7Bの比較
- **HarmonyMessageParser** (TODO: 読むべき)
- **非同期トークナイザー** (TODO: 読むべき)

## 関連記事

- /deep_2067 医薬分野のQ&AでローカルLLMを評価する④：Gemma-4-E2B・LLM-JP-4-8B-Thinking・JPharmatron-7Bの比較
- /deep_419 連続バッチ処理（Continuous Batching）をゼロから理解する
- /deep_158 翻訳か暗唱か？極低リソース言語の機械翻訳評価スコアの較正
- /deep_1420 秘匿環境で使うAI議事録の構成を考える - パイプライン型とLLM完結型の検証
- /deep_1434 生成AIワークロードの電力プロファイル計測：データセンター全体インフラ計画のための手法

## 原文リンク

[vllm serve で LLM-jp-4 を動かす：RuntimeError: Already Borrowed の解決策](https://zenn.dev/yay1/articles/ad6958086670b0)
