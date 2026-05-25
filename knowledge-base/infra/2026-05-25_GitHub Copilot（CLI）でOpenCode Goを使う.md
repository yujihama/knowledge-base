---
title: "GitHub Copilot（CLI）でOpenCode Goを使う"
url: "https://zenn.dev/arika/articles/20260524-use-opencode-go-in-github-copilot"
date: 2026-05-25
tags: [OpenCode Go, GitHub Copilot, BYOK, GLM-5, Qwen3, MiniMax, LLM定額, CLI]
category: "infra"
related: [5162, 2823, 826, 1737, 5839]
memo: "[Zenn LLM] GitHubCopilot(CLI)でOpenCode Goを使う"
processed_at: "2026-05-25T09:04:19.779745"
---

## 要約

OpenCode Goは中国系OSSモデル（GLM-5、MiniMax M2.5、Qwen3.5 Plusなど）への定額アクセスを提供するサブスクリプション型LLMサービス。月額固定料金で複数の高性能モデルを利用でき、従量課金の「Zen」プランとは異なる「Go」プランが対象。本記事では、GitHub Copilot CLIのBYOK（Bring Your Own Key）機能を利用してOpenCode GoのAPIに接続する手順を解説している。

接続方法はシンプルで、環境変数4つを設定するだけ。COPILOT_PROVIDER_API_KEYにOpenCode GoのAPIキーを、COPILOT_PROVIDER_TYPEに「openai」を、COPILOT_PROVIDER_BASE_URLに「https://opencode.ai/zen/go/v1」を、COPILOT_MODELに使用モデル名（例: glm-5）を指定してcopilotを起動する。WindowsのCLI環境での動作確認済み。

VSCode側については、BYOKのOpenAI Compatible系サポートが終了しているため現状は困難。Ollamaを経由した迂回策も検証したが、ローカルにOllamaのAPIが存在しないため失敗に終わった。

使用感としては、GLM-5モデルで簡単なコード修正タスクを実行したところ、致命的な破綻はないが「空気を読む力が足りない」と評価。既存コードの文脈に沿った補完よりも、hook/skills/agent等で細かく制御する必要がある。

コスト面では、GLM-5の1リクエストは入力700トークン・キャッシュ52,000トークン・出力150トークン相当として計算され、実際の検証タスクのAPI相当料金は$1.1（約120円）。月100リクエスト程度で上限に達する可能性があり、コスパはモデル選択に依存する。MiniMax M2.5やQwen3.5 Plusはリミットが緩く、より気軽に使えるとのこと。Claude CodeやCodex高額プランほどは不要だが手軽にコーディングAIを使いたい用途に適している。

## アイデア

- COPILOT_PROVIDER_BASE_URLをOpenAI互換エンドポイントに差し替えるだけで、GitHub Copilot CLIを任意のLLMバックエンドに向けられるBYOK設計は、ローカルLLMや他社APIへの差し替えにも応用可能
- GLM-5の1リクエスト換算（入力700トークン・キャッシュ52,000トークン・出力150トークン）という粒度設計は、長いシステムプロンプトをキャッシュで吸収する設計思想を示しており、エージェント系ワークフローのトークン最適化の参考になる
- VSCodeのBYOKがOpenAI Compatible系を打ち切っている一方でOllama経由は許容している点は、IDE統合レイヤーにおけるプロバイダー抽象化の設計判断として興味深い

## 前提知識

- **GitHub Copilot BYOK** (TODO: 読むべき)
- **OpenAI Compatible API** (TODO: 読むべき)
- **GLM-5** → /deep_1964 GLM-5.1徹底レビュー：200Kトークンコンテキストと8時間自律実行が拓くコード生成の新地平
- **Ollama** → /deep_52 SyGra Studio 紹介：合成データ生成のビジュアル・インタラクティブ環境
- **環境変数によるAPI設定** (TODO: 読むべき)

## 関連記事

- /deep_5162 GitHub CopilotのバックエンドをLM Studioのローカルモデル（Qwen3.6 35B-A3B）に差し替える手順と検証結果
- /deep_2823 GitHub Copilot CLIの使い方を学ぶ方法
- /deep_826 驚くほどシンプルな自己蒸留がコード生成を改善する
- /deep_1737 難問を「選択肢」に変える：RLVRの探索限界を突破するCog-DRIFT
- /deep_5839 生成速度2倍は本当か？Qwen3-27BのMTP（Multi-Token Prediction）をllama.cppで試す

## 原文リンク

[GitHub Copilot（CLI）でOpenCode Goを使う](https://zenn.dev/arika/articles/20260524-use-opencode-go-in-github-copilot)
