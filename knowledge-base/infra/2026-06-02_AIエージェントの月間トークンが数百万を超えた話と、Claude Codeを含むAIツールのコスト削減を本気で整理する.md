---
title: "AIエージェントの月間トークンが数百万を超えた話と、Claude Codeを含むAIツールのコスト削減を本気で整理する"
url: "https://zenn.dev/dx_pm_product/articles/ai-token-cost-reduction-guide"
date: 2026-06-02
tags: [Claude Code, トークンコスト削減, プロンプトキャッシング, LiteLLM, claude-code-router, RTK, ローカルLLM, DeepSeek, MCP, エージェントコスト]
category: "infra"
related: [2404, 4749, 430, 2688, 4520]
memo: "[Zenn LLM] AIエージェントの月間トークンが数百万を超えた話と、Claude Codeを含むAIツールのコスト削減を本気で整理する"
processed_at: "2026-06-02T09:06:21.084426"
---

## 要約

AIエージェントツールの普及により、1タスクあたりのトークン消費が従来の数倍に膨らみ、チーム運用では月数十万円規模の請求が発生するケースが増えている。本記事はその対策を8カテゴリ・15項目以上に体系化したもの。

**カテゴリ1：キャッシュ活用**。Anthropicは90%割引・TTL5分/1時間、OpenAIは50%・5〜10分、Geminiは75%のプロンプトキャッシュを提供。ユーザーが能動的にできることは「5分以内に連続作業する」程度で、ツール側が自動対応するため過度な最適化は不要。

**カテゴリ2：モデル選択**。同プロバイダ内でもモデルにより単価は5〜10倍異なる。Anthropicでは単純作業にHaiku 4.5、通常実装にSonnet 4.6、複雑設計のみOpus 4.7と使い分ける。Claude Codeは`/model`で切替可能。

**カテゴリ3：コンテキスト最適化**。サブエージェント（Explore等）に大量ファイル探索を委譲することで、メイン会話に最終要約のみが返り、以降ターンのトークン消費が激減する。`/clear`・`/compact`の積極活用、CLAUDE.mdへのプロジェクト規約記載、MCPサーバの不要な無効化（全ツールのJSONSchemaが毎リクエストに乗るため数千〜数万トークン節約）が有効。Rust製ツール「RTK（Rust Token Killer）」はClaude CodeのPreToolUseフックでBash出力を圧縮し、cargo test 262件の結果を4,823→11トークン（99.8%減）、30分セッション全体で150K→45K（70%減）を実測。

**カテゴリ4：出力制御**。出力トークンは入力の3〜5倍高い（OpusでMTok$75）。Editツールによる差分のみ返却、`max_tokens`上限設定、Extended thinkingの難問限定使用が効果的。

**カテゴリ5：プロバイダ・契約形態の変更**。最大の削減効果を持つ領域。API従量で月$200超なら定額（Claude Max $200/月等）の方が安い。DeepSeekはClaude Opusの1/50〜1/100の単価でコード性能はSonnet級。Claude CodeはANTHROPIC_BASE_URLを差し替えることで任意のモデルにルーティング可能で、LiteLLM（100+プロバイダ対応）やclaude-code-router（タスク種別で自動振り分け）をプロキシとして使う構成が実用的。「日常作業はClaude、軽い処理はDeepSeek、長文はGemini 2.5 Pro」のハイブリッド構成が現実解。

**カテゴリ6：ローカル/ハイブリッド構成**。RTX 4090/5090でQwen3-Coder 32B等をリアルタイム速度で動かしAPIコストを実質ゼロにできる。

監査エージェント開発への示唆：エージェントループ内での不要なツール呼び出し削減（カテゴリ7）とBash出力のRTK圧縮は、LangGraph等で構築した多ステップエージェントのコスト管理に直接適用できる。また、claude-code-routerのタスク別自動振り分け設計はReActエージェントの思考フェーズと実行フェーズでモデルを分ける構成の参考になる。

## アイデア

- RTK（Rust Token Killer）がClaude CodeのPreToolUseフックを使いBash出力をLLMコンテキストに入る前に圧縮する仕組みは、エージェントフレームワーク全般に応用できる新しいレイヤー設計
- claude-code-routerによるタスク種別（background/think/longContext）ごとの自動モデル振り分けは、ReActエージェントの推論・行動フェーズでモデルコストを最適化する設計パターンとして参照できる
- CLAUDE.mdのmemory構造（MEMORY.mdを目次として毎ターン自動ロード、個別ファイルは遅延ロード）はプレフィックスキャッシュと相性よく設計されており、長期エージェント運用の知識永続化モデルとして参考になる

## 前提知識

- **Prompt Caching** → /deep_2960 LLMを16回呼び出したら、1回より安くて高品質になった話（0.84円）
- **Claude Code hooks** → /deep_4752 ハーネスは書いて終わりではない: Self-Evolving Agentの設計
- **LiteLLM** → /deep_827 smolagentsの紹介：コードでアクションを記述するシンプルなエージェントライブラリ
- **MCP（Model Context Protocol）** → /deep_12 MCP（Model Context Protocol）をカメラとラジオで例える
- **ReActエージェント** → /deep_4188 ReActエージェントが本当に必要な業務はどれか：4象限による業務AI設計の腑分け

## 関連記事

- /deep_2404 ローカルドキュメントをAIで横断検索しレポート作成 — Local Knowledge RAG MCP Server 入門
- /deep_4749 Cognee公式Claude Codeプラグインと自作ツールキットの詳細比較：クラウドネイティブ vs 完全ローカル自己完結
- /deep_430 過去のセッションを必要時のみ参照する方針でclaude-memのトークン消費を激減させた話
- /deep_2688 自分のバージョンアップを自分で書く — embodied-claude v0.2「Social and scripted」
- /deep_4520 社内向けAIアシスタントを3か月間試験運用してみた（松尾研究所mbot事例）

## 原文リンク

[AIエージェントの月間トークンが数百万を超えた話と、Claude Codeを含むAIツールのコスト削減を本気で整理する](https://zenn.dev/dx_pm_product/articles/ai-token-cost-reduction-guide)
