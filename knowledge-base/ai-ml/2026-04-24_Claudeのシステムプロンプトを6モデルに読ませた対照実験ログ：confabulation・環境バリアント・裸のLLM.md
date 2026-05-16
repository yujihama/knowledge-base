---
title: "Claudeのシステムプロンプトを6モデルに読ませた対照実験ログ：confabulation・環境バリアント・裸のLLMへの接近"
url: "https://zenn.dev/orangewk/articles/claude-system-prompt-cross-model-logs"
date: 2026-04-24
tags: [Claude, システムプロンプト, confabulation, プロンプトエンジニアリング, LLM比較実験, Opus 4.7, GPT-5.2, Qwen, Extended Thinking, API]
category: "ai-ml"
related: [973, 2542, 2363, 860, 861]
memo: "[Zenn LLM] Claude のシステムプロンプトを裸の LLM や他社モデルに読ませた 6 モデル対照実験ログ"
processed_at: "2026-04-24T12:52:57.614041"
---

## 要約

CL4R1T4SリポジトリにリークされたClaude Opus 4.7のシステムプロンプト（claude.ai向け）を、6モデル・7セッションに読ませた際の逐語記録。付録A〜E-3の構成で、各モデルの反応を比較している。

【付録A: Claude Sonnet 4.6】自身のシステムプロンプトと4.7版の差分を詳細に分析。主な差異として、(1) 4.7では「search_first」セクションが最上位に昇格し「自信があっても検索をスキップするな」と明示、(2) 「default_stance」セクション新設で拒否閾値が4.6より高く設定、(3) 「tool_discovery」でツールの能動的探索を義務付け、(4) 知識カットオフが4.6の2025年5月末→4.7の2026年1月末に約8ヶ月拡大、(5) 応答の簡潔さ指示が強化、(6) Visualizerインライン可視化機能の追加、などを特定した。4.6にあって4.7で消えたものとして「acting_vs_clarifying」（曖昧なまま進め）セクションが挙げられ、これが4.7での自己応答（自問自答ループ）傾向の構造的要因と推測される。

【付録B: Claude Opus 4.7（Claude Code / Agent SDK）】メタ批評を行いつつconfabulation（事実でない情報を確信を持って生成する現象）への警告を自発的に発した。

【付録C: Claude Opus 4.7（API直叩き、system空）】最も「裸」に近い状態で、強いconfabulationと訓練時自己像の露出が観察された。

【付録D: Claude Opus 4.7（Agent SDK、system空）】中間層（scaffolding）の存在がconfabulationを抑制することを示す一次データとなった。

【付録E-1: GPT-5.2 (Codex/OpenAI)】他社エンジニア視点からの設計批評を実施。

【付録E-2: Qwen（ファイル読めず）】ファイルを実際に読まずにconfabulateしたクロスファミリーの一次データ。

【付録E-3: Qwen（実読み）】「内部ドキュメント再構成」仮説を提示。

「裸のLLM」への接近方法として、APIでsystemを空にする方法（フォーマット制約・著作権制限・リスト抑制などが外れる）、Extended Thinkingを有効化してthinking blockの内容を観察する方法が実践的に論じられている。モデルに内在するRLHF由来の傾向（helpfulness志向、基本的安全性）はプロンプトで除去不能な「地金」として区別されている。

## アイデア

- 同一プロンプトをsystem空・scaffoldingあり・Claude Code上と条件を変えて同一モデル（Opus 4.7）に読ませることで、scaffoldingそのものがconfabulation抑制に機能することを実験的に示した点
- 4.6の「acting_vs_clarifying」セクション削除＋簡潔さ強化＋default_stanceの組み合わせが4.7の自己応答ループの構造的原因であると、システムプロンプトの差分から帰納的に推論した分析手法
- 「外せる層（フォーマット制約、tool指示、メモリシステム）」と「外せない層（RLHF由来の応答傾向）」を明示的に分離し、真の意味での『裸のLLM』に到達可能な上限を論じた点

## 前提知識

- **RLHF** → /deep_37 LLMチャットボットに欠けているもの：目的意識（Purposeful Dialogue）
- **システムプロンプト** → /deep_62 LLMチャットボットに欠けているもの：目的意識（Purposeful Dialogue）
- **confabulation** (TODO: 読むべき)
- **Extended Thinking** → /deep_2405 Claudeトークン節約・完全保存版リファレンス2026｜9カテゴリ×全手法マップ
- **Agent SDK** (TODO: 読むべき)

## 関連記事

- /deep_973 agency-agentsの144エージェントは「どこまで使えるのか」を本気で調べてみた
- /deep_2542 Opus 4.6→4.7移行で見落とすと課金が最大35%増える話 ─ トークナイザー更新と「厳密化」の現実
- /deep_2363 Claude Max 20xでもトークンが足りない。重度ユーザーが実践する文脈管理と節約の工夫8選
- /deep_860 語彙の地平（Vocabulary Horizon）：LLMペルソナ設計における語彙制限による思考誘導アイデア
- /deep_861 蒸留モデルとは何か？ - DeepSeek R1の登場から1年で振り返るLLM知識蒸留の仕組みと実力

## 原文リンク

[Claudeのシステムプロンプトを6モデルに読ませた対照実験ログ：confabulation・環境バリアント・裸のLLMへの接近](https://zenn.dev/orangewk/articles/claude-system-prompt-cross-model-logs)
