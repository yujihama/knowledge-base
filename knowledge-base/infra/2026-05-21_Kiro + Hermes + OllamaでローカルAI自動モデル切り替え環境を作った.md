---
title: "Kiro + Hermes + OllamaでローカルAI自動モデル切り替え環境を作った"
url: "https://zenn.dev/guardianlab/articles/76ccd7dfdab4ba"
date: 2026-05-21
tags: [Ollama, Brain-Router, モデルルーティング, ローカルLLM, OpenAI互換API, Hermes-Agent, qwen3, gemma4, TUI]
category: "infra"
related: [5723, 3903, 5266, 3642, 4176]
memo: "[Zenn LLM] Kiro + Hermes + OllamaでローカルAI自動モデル切り替え環境を作った"
processed_at: "2026-05-21T09:02:33.800282"
---

## 要約

Claude APIなどクラウドAIの利用コストを削減するため、Ollama上の複数ローカルモデルを用途別に自動ルーティングする環境を構築した事例。中心となるのはBrain Routerと呼ばれるOpenAI互換ローカルプロキシ（localhost:11435）で、リクエストのmodelフィールドに「auto」を指定すると、ユーザー入力の内容を分析して適切なモデルへ振り分ける。モデル構成は4種類：普通の会話にはgemma4:e4b（高速チャット）、軽いコード修正にはOmniCoder-9B、本格的なコーディングにはqwen3-coder:latest、深い推論・設計レビューにはqwen3.6:35b-a3b（35Bパラメータ）を割り当てている。フロントエンドは2系統あり、1つはSCORPION BRAIN TUIというサイバーパンク風のターミナルUIで、どの入力がどのモデルへルーティングされたかをリアルタイム表示しつつストリーミング応答・会話履歴保存・/modeによる手動切り替えが可能。もう1つはHermes Agentとの統合で、「hermes -m auto --provider brain-router」コマンドからMCP連携やツール機能を使いながらローカルモデルを自動切り替えできる。速度改善策として、gemma4:e4bをkeep_alive=-1で常駐させてVRAMからの追い出しを防ぎ、コード系の会話が予測された際にCoderモデルを事前プリロードする仕組みを導入。Hyprland（Linuxウィンドウマネージャ）起動時にも自動プリロードすることで、PC起動直後から待ち時間なく利用できる。Kiro CLIはクレジット制のクラウドAIであるため、日常利用ではなく壊れた環境の修復・重要な設計作業・Brain Routerのアーキテクチャ設計など「ここぞ」という場面に限定して使う方針を採用。監査エージェント開発への示唆としては、LangGraph等のエージェントフレームワークでタスクの複雑度に応じてモデルを動的に選択するルーティング層を設けることで、推論コストを抑えつつ精度が必要なステップには大型モデルを充てる設計パターンが参考になる。OpenAI互換APIとしてプロキシを挟む構造は、エージェントコードを変更せずにバックエンドモデルを差し替えられる点で、ローカル検証→クラウド本番の切り替えにも応用できる。

## アイデア

- OpenAI互換プロキシとしてBrain Routerを挟むことで、クライアント側のコードを一切変えずにバックエンドモデルを用途別に自動切り替えできるアーキテクチャ
- keep_alive=-1とHyprland起動時プリロードを組み合わせて、ローカルモデルを「常駐AI」として扱い初回レスポンス遅延をほぼ排除する速度最適化手法
- 普段はローカルモデルで完結させ、重要な設計・修復時のみクラウドAI（Kiro）を使うハイブリッド運用により、課金を最小化しながら高品質な出力が必要な場面をカバーする使い分け戦略

## 前提知識

- **Ollama** → /deep_52 SyGra Studio 紹介：合成データ生成のビジュアル・インタラクティブ環境
- **OpenAI互換API** → /deep_4183 DeepSeek V4 APIでAIエージェントを作る完全ガイド【2026年版】
- **LLMルーティング** → /deep_689 ParetoBandit: 非定常LLMサービングのための予算ペーシング適応型ルーティング
- **MCP** → /deep_1 Agent SkillにReactアプリを同梱するSkill Appアーキテクチャの実装
- **VRAM管理** (TODO: 読むべき)

## 関連記事

- /deep_5723 OllamaでローカルLLMを動かす：MacのGPUを使ってQwen3.5・Gemma4・Phi-4 Miniを動かすまでの手順
- /deep_3903 Github/GitLabのPR/MRをローカルLLMでコードレビューさせるスクリプトを作ってみた
- /deep_5266 13モデル実測比較：HumanEval/HumanEval+でわかるLLMコーディング実力ランキング2026
- /deep_3642 未経験者がVRAM 16GBでAIキャラの台本生成を動かすまで（第1回）── VRAM不足という当たり前の壁
- /deep_4176 完全ローカルAIコードレビュー運用編：Ollamaスパイク対策とnum_ctx切り詰め

## 原文リンク

[Kiro + Hermes + OllamaでローカルAI自動モデル切り替え環境を作った](https://zenn.dev/guardianlab/articles/76ccd7dfdab4ba)
