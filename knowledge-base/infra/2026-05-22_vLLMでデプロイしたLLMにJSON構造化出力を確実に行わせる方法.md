---
title: "vLLMでデプロイしたLLMにJSON構造化出力を確実に行わせる方法"
url: "https://zenn.dev/k_eclaire39/articles/991a53229004c1"
date: 2026-05-22
tags: [vLLM, 構造化出力, JSON Schema, Constrained Decoding, xgrammar, ローカルLLM, Llama-3]
category: "infra"
related: [5969, 2590, 2591, 4043, 419]
memo: "[Zenn LLM] VLLMでデプロイしたLLMにうまくJSONを書かせる方法"
processed_at: "2026-05-22T09:02:43.320691"
---

## 要約

ローカルデプロイしたLLMにJSONを出力させる際、プロンプトだけで制御しようとするとフィールド名が期待通りにならないなどの問題が頻発する。vLLM（バージョン0.15.0）には構造化出力（Structured Outputs）機能が内蔵されており、これを利用することでJSONスキーマに完全準拠した出力を強制できる。

手順は3ステップ。①`vllm serve meta-llama/Llama-3-8B-Instruct`でサーバを起動する。特別なオプションなしでバックエンドが自動選択されるが、Tokenizerによっては`--structured-outputs-config.backend xgrammar`のように明示指定が有効な場合もある。②出力させたいJSONのスキーマをJSON Schema形式で定義する（type, properties, requiredフィールドを使用）。③PythonのOpenAIクライアントでリクエストを送る際、`extra_body`パラメータに`{"structured_outputs": {"json": schema}}`を渡す。

技術的背景として、vLLMはLogit処理レイヤーでJSON Schemaに基づくトークン制約（Constrained Decoding）を行っており、スキーマに違反するトークンの確率をゼロに落とすことで出力を強制する。xgrammarはその制約バックエンドの一実装であり、Grammar-based制約をGPU上で高速処理する。OpenAIのAPIが安定したJSON出力を返すのと同様のメカニズムをローカルLLMで再現できる。

PythonコードはOpenAIライブラリをそのまま流用し、`base_url`をlocalhost:8000に向けるだけで動作する。`extra_body`によるカスタムパラメータ渡しがポイント。出力後は`json.loads()`でパース検証するコードも示されており、本番組み込み前の動作確認手順が明確。

監査エージェント開発への示唆：LangGraphやReActベースのエージェントでツール呼び出し結果やサブエージェント出力をJSON形式で統一する際、ローカルLLM（Ollama等ではなくvLLM）を使う選択肢が現実的になる。スキーマ定義さえ行えばPydanticモデルのフィールド定義とほぼ同じ感覚でLLM出力を構造化できるため、LLM-as-judgeの評価結果やエビデンス抽出結果を安定したデータ型として扱えるようになる。

## アイデア

- xgrammarによるGrammar-based Constrained DecodingをGPUレイヤーで実行することで、プロンプトエンジニアリング不要でスキーマ準拠出力を強制できる点
- OpenAIクライアントライブラリの`extra_body`パラメータでvLLM固有の拡張機能を渡せるため、既存のOpenAI向けコードベースをほぼそのままローカルLLMに流用できる点
- LangGraph等のエージェントフレームワークと組み合わせると、Pydanticスキーマ定義をそのままJSON Schema変換してLLM出力の型安全性を確保できる可能性がある点

## 前提知識

- **vLLM** → /deep_27 Holotron-12B - 高スループット・コンピュータ使用エージェント向けマルチモーダルモデル
- **JSON Schema** (TODO: 読むべき)
- **Constrained Decoding** → /deep_4869 NeocorRAG：証拠チェーンによる無関連情報の削減・明示的根拠の強化・効果的な想起の実現
- **OpenAI API互換** (TODO: 読むべき)
- **xgrammar** (TODO: 読むべき)

## 関連記事

- /deep_5969 初めて作るオレオレAIデータセンター③：DGX SparkとRTX PRO 6000 Blackwell MAX-Qを比較する
- /deep_2590 ローカルLLMを簡単にデモする：vLLM + LiteLLM + ngrokの構成
- /deep_2591 vllm serve で LLM-jp-4 を動かす：RuntimeError: Already Borrowed の解決策
- /deep_4043 DeepSeek ローカル実行完全ガイド2026 — Ollama・LM Studio・vLLMで自分のPCに導入
- /deep_419 連続バッチ処理（Continuous Batching）をゼロから理解する

## 原文リンク

[vLLMでデプロイしたLLMにJSON構造化出力を確実に行わせる方法](https://zenn.dev/k_eclaire39/articles/991a53229004c1)
