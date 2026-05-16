---
title: "Claude Code subagentにローカルQwen3を繋いでOpus APIコストを1/30に削減した実践記録"
url: "https://zenn.dev/ai_arai_ally/articles/20260420-2053-claude-code-subagentllm-opus"
date: 2026-04-27
tags: [Claude Code, subagent, Qwen3, LM Studio, コスト削減, ローカルLLM, モデルルーティング, 自律AIシステム, MoE]
category: "agent-arch"
related: [2862, 2950, 2404, 2590, 1333]
memo: "[Zenn LLM] Claude Opus 4のAPI代が1/30になった。Claude Code subagentにローカルのQwen3を繋いだだけだ"
processed_at: "2026-04-27T12:11:12.475531"
---

## 要約

著者は自作の自律AIシステム「brain」を夜間バッチで稼働させており、当初はすべてのタスクをClaude Opus 4経由で実行していた。要約・下書き・ログ整形といった処理もOpusに投げていたため、1夜あたり$3.60（月換算$108）のAPI課金が発生していた。

これを解決するため、Claude Codeのsubagent機能を活用した。`~/.claude/agents/`にMarkdownファイルを置くと、Orchestrator（Claude本体）が任意のタイミングで専門エージェントを呼び出せる仕組みを利用し、subagentのモデルとしてローカルLLMを指定できる点が核心だ。

具体的なセットアップは3ステップ：①LM StudioでQwen3-30B-A3B（MoEモデル、VRAM 24GBで動作）を起動してOpenAI互換API（http://localhost:1234/v1）を有効化、②`~/.claude/settings.json`の`customApiEndpoints`にローカルエンドポイントを登録、③`~/.claude/agents/local-worker.md`でsubagentを宣言して`apiEndpoint: local-llm`と`model: qwen3-30b-a3b`を指定する。

ルーティング設計の原則は「出力が間違っていたとき後で検知・修正できるか」で判断する。コード生成・テキスト要約・ログ整形・バッチ処理はローカルQwen3に委譲し、複数エージェントのOrchestration・曖昧な仕様の解釈・最終コードレビュー・セキュリティリスク判断はOpusに残す。brainでは`model-route`スキルがタスクのcomplexity・reversibility・output_typeのメタデータを見て自動選択している。

実測値：Before（全Opus）は1サイクルあたり12,400 input＋3,100 output tokens／$0.18、夜間20サイクルで$3.60。After（ローカルルーティング導入後）はOpus消費が410 input＋230 output tokenのみ、Qwen3分はAPI課金ゼロとなり、1サイクル$0.006・夜間20サイクルで$0.12。削減率96.7%、トークン比で約30分の1を達成した。

トレードオフとして、Qwen3はOpusより指示解釈が硬く要約精度が微妙に落ちる場面があったため、プロンプトを丁寧に書き直す必要があった。またRTX 4090でQwen3-30B-A3Bを動かすと1,000トークン生成に約8秒かかり、夜間バッチには問題ないがインタラクティブ作業には不向き。最終的な品質確認はOpusが担うため、アウトプット品質の劣化は感じていないと著者は報告している。

監査エージェント開発への示唆：複数エージェントが並走するOrchestration構成において、reversibilityを判断基準にしたモデルルーティングは監査ワークフローにも直接適用できる。証跡収集・ログ整形・ドラフト生成はローカルLLMに委譲し、リスク判断・最終承認ステップのみ高性能モデルを使う設計は、コスト抑制と品質保証を両立する実践的パターンだ。

## アイデア

- reversibility（後で検知・修正できるか）を判断基準にしたモデルルーティング設計は、タスク複雑度だけでなく「失敗コスト」を軸にした実用的なヒューリスティックで、監査・コンプライアンスワークフローにも転用できる
- Claude Codeのsubagent仕様（~/.claude/agents/のMarkdownファイルでモデルとエンドポイントを宣言）により、Orchestratorはクラウド・ワーカーはローカルという非対称な分業構成がコード変更なしで実現できる点
- Qwen3-30B-A3BのようなMoEモデルがVRAM 24GBで動作し、コーディングベンチマークで旧世代GPT-4水準に達したことで、「ローカルLLMは本番品質に届かない」という前提が2026年時点で実質的に崩れており、ハイブリッド構成のコスト効率が急速に改善している

## 前提知識

- **Claude Code subagent** (TODO: 読むべき)
- **LM Studio OpenAI互換API** (TODO: 読むべき)
- **MoEアーキテクチャ** → /deep_196 MoEアーキテクチャ最適化のための包括的スケーリング則
- **Orchestrator-Worker パターン** (TODO: 読むべき)
- **モデルルーティング** → /deep_2293 【2026年】Claude APIを最安で使う方法：サブスク不要で40%以上節約

## 関連記事

- /deep_2862 Qwen3-235B-A22B を OpenCode と Ollama でローカル運用する超初心者向けガイド
- /deep_2950 同じOllama + qwen2.5-coderなのに動く/動かないが分かれる6つの構造的原因
- /deep_2404 ローカルドキュメントをAIで横断検索しレポート作成 — Local Knowledge RAG MCP Server 入門
- /deep_2590 ローカルLLMを簡単にデモする：vLLM + LiteLLM + ngrokの構成
- /deep_1333 ローカルLLMを使って積読PDFを翻訳する（LM Studio + PyMuPDF + PDFMathTranslate）

## 原文リンク

[Claude Code subagentにローカルQwen3を繋いでOpus APIコストを1/30に削減した実践記録](https://zenn.dev/ai_arai_ally/articles/20260420-2053-claude-code-subagentllm-opus)
