---
title: "GitHub Copilot SDKのGitHub Modelsを使ってユーザーのCopilot利用枠からLLMを呼ぶ"
url: "https://zenn.dev/nomhiro/articles/questara-github-models-rpg-learning"
date: 2026-05-21
tags: [GitHub Models, GitHub Copilot SDK, GitHub OAuth, OpenAI互換API, MCP, Microsoft Learn, AES-256-GCM, gpt-5-mini, user-to-server token]
category: "infra"
related: [5794, 5027, 4183, 5476, 5887]
memo: "[Zenn LLM] GitHub Copilot SDK の GitHub Models を使って、ユーザーの Copilot 利用枠から LLM を呼びたい"
processed_at: "2026-05-21T09:01:37.207397"
---

## 要約

WebアプリでLLMを使う際の課題として、運営者がOpenAI/Azure OpenAI APIの料金を全額負担する構造がある。本記事はその解決策として、GitHub OAuth認証で取得したuser-to-serverアクセストークンをそのままGitHub Models APIのBearerトークンに使うことで、推論コストをユーザー自身のGitHub Copilotプラン（Pro/Business/Enterprise/Pro+）の利用枠から消費させる手法を解説する。実装はOpenAI公式SDKのbaseURLを`https://models.inference.ai.azure.com`（または新エンドポイント`https://models.github.ai/inference`）に上書きし、apiKeyにOAuthトークンを渡すだけで完結する。GitHubの側からは「Copilot利用枠を持つユーザーがブラウザ経由でGitHub Modelsを叩いている」と区別できないため、料金はユーザー側に帰属する。モデルはgpt-5-mini（バランス型）、gpt-5（フラッグシップ）、gpt-5-nano（大量呼び出し向け）などを用途別に選択可能。セキュリティ面では、DBに保存するアクセストークンをAES-256-GCMで暗号化し、LLM呼び出し直前にのみ復号してメモリ展開後に破棄する設計を採用。OAuthスコープは`read:user user:email`の最小権限で十分。応用として、Microsoft Learn公式MCPの`microsoft_docs_fetch`ツールで学習ガイドのmarkdownを取得し、その周辺4000文字をプロンプトに埋め込んでgpt-5-miniに4択10問のJSONを生成させるRPG学習アプリを構築した。MCPとの組み合わせによりハルシネーションを低減できる。レート制限がユーザー単位で分離される点も運営者にとって利点。ただしGitHub Modelsはプレビュー段階のため、本番商用利用には規約確認とユーザー同意取得が必要。監査エージェント開発への応用として、社内ツールをCopilotプラン保有のユーザーに限定配布する場合、API費用ゼロで多段階LLM推論を実装できる構成として参考になる。

## アイデア

- OAuthのuser-to-serverトークンをそのままLLM APIのBearerトークンに転用することで、運営者が一切の推論コストを負担しないゼロコストLLM統合アーキテクチャを実現できる点
- GitHub ModelsとMicrosoft Learn MCPを組み合わせることで、ハルシネーション対策をプロンプトエンジニアリングではなくデータ取得層（公式markdown注入）で解決するアプローチ
- レート制限がサービス全体ではなくユーザー単位で分離されるため、一人のヘビーユーザーが他のユーザーの体験を劣化させない設計になる点

## 前提知識

- **GitHub OAuth** (TODO: 読むべき)
- **OpenAI Chat Completions API** (TODO: 読むべき)
- **GitHub Models** (TODO: 読むべき)
- **Model Context Protocol (MCP)** (TODO: 読むべき)
- **AES-256-GCM** (TODO: 読むべき)

## 関連記事

- /deep_5794 社内独自LLMでもClaude Codeみたいなエージェント開発をしたい — Continue + AGENTS.md という解
- /deep_5027 Ollama実践入門──ローカルLLMをMacBook上で動かしてRAG・MCPと組み合わせる【2026】
- /deep_4183 DeepSeek V4 APIでAIエージェントを作る完全ガイド【2026年版】
- /deep_5476 金融部門への先進AI技術導入：ガバナンス後追いとエージェント化の現在地
- /deep_5887 金融部門への先進AI技術の実装：ガバナンス後追いとボトムアップ採用の現実

## 原文リンク

[GitHub Copilot SDKのGitHub Modelsを使ってユーザーのCopilot利用枠からLLMを呼ぶ](https://zenn.dev/nomhiro/articles/questara-github-models-rpg-learning)
