---
title: "Tool Callingのシグネチャと呼び出し率についての調査"
url: "https://zenn.dev/yy7613/articles/b3264acb153f40"
date: 2026-06-06
tags: [Tool Calling, Function Calling, シグネチャ設計, コンテキストエンジニアリング, Gemma-4, GPT-OSS, LFM2.5, LM Studio, ローカルLLM, エージェント評価]
category: "agent-arch"
related: [2826, 1333, 4332, 7111, 5469]
memo: "[Zenn LLM] Tool Calling のシグネチャと呼び出し率についての調査"
processed_at: "2026-06-06T21:17:30.793186"
---

## 要約

本記事は、LLMのFunction Calling（Tool Calling）における「シグネチャ設計」が呼び出し率に与える影響を定量的に検証した実験報告である。対象モデルはGPT-OSS:20b（MXFP4）、Gemma-4-26b-a4b（Q4_K_M）、LFM2.5-8B-A1B（Q8_0）の3モデルで、ローカル環境（LM Studio経由のOpenAI互換エンドポイント）にて合計2700回実行した。

検証設計では、TODOアプリ用の4つのToolと60個のダミーToolを合わせた計64 Toolをエージェントに設定。システムプロンプトとDescriptionは固定し、Tool名・引数名・引数構造のみを5種類のシグネチャパターンで変化させた。シグネチャパターンは「標準名（canonical）」「代替名（synonym）」「曖昧引数名（ambiguous）」「最小引数（minimal）」「構造化引数（complex）」の5種。評価指標は「必要Tool呼び出し率」「順序完全一致率」「余計なTool呼び出し率」「Tool未呼び出し率」「平均Tool呼び出し数」の5軸。

全体結果では必要Tool呼び出し率98.1%・順序完全一致率88.1%を達成。モデル別ではGemma-4-26b-a4bが最安定（必要呼び出し率100%、余計呼び出し0%、順序一致93.7%）、GPT-OSS:20bは余計呼び出し率4.7%が課題、LFM2.5-8B-A1BはTool未呼び出し率2.2%が弱点だった。

シグネチャ別では代替名（synonym）が順序完全一致率95.6%で最高、次いで曖昧引数名93.5%・構造化引数93.3%・標準名92.8%。最小引数（minimal）は89.1%で最低だった。直感に反し「引数を削ってシンプルにすれば安定する」とは言えず、むしろ意味的に明確な名称と適切な引数セットを持つシグネチャが安定する結果となった。

監査エージェント開発への示唆として、64 Toolという大規模ToolセットでもGemma-4-26bクラスのローカルモデルが実用水準（必要呼び出し率100%）を達成できる点は重要。監査ワークフローで複数の手順ToolをReAct的に逐次呼び出す場面では、引数の意味が曖昧なシグネチャや最小化したシグネチャは順序崩れのリスクを高めるため、引数名に業務ドメイン語（例: auditTargetId, controlStatus）を明示することが推奨される。

## アイデア

- 引数を最小化してスキーマを単純にしても呼び出し安定性は上がらず、意味的に明確な引数名を持つシグネチャの方が順序一致率が高いという反直感的な結果
- 60個のダミーToolを混在させた64 Tool構成でも、Gemma-4-26bクラスのローカルモデルが必要Tool呼び出し率100%を達成しており、大規模Toolセットへの実用耐性を定量的に確認できる点
- ダミーToolの引数設計（汎用 vs 用途別）もモデルの選択挙動に影響する可能性があり、Tool選択の干渉効果をダミー側のシグネチャ設計で制御できるという設計観点

## 前提知識

- **Function Calling** → /deep_47 LLM SDKを基礎から理解する 第4回：ツール呼び出し（Function Calling）編
- **Tool Use** → /deep_3094 LLMに図面情報を全部見せる設計をやめた話
- **ReAct** → /deep_1 Agent SkillにReactアプリを同梱するSkill Appアーキテクチャの実装
- **OpenAI互換エンドポイント** (TODO: 読むべき)
- **JSON Schema** → /deep_6556 RustでLLMコードレビューエージェントを作った

## 関連記事

- /deep_2826 ローカルLLM用の簡易ツール拡張機能「トリガー」：シェルスクリプトをFunction Callingツールとして自動登録する仕組み
- /deep_1333 ローカルLLMを使って積読PDFを翻訳する（LM Studio + PyMuPDF + PDFMathTranslate）
- /deep_4332 ローカルLLM 6モデルサイズ別比較：gemma3 / qwen3 / gpt-oss をOllamaで実測
- /deep_7111 【2026年最新】LFM2.5-8B-A1BをApple Siliconで実測 — 「1月のLFM2.5」との違いと実際の速度
- /deep_5469 「このコード、Claudeに見せていいの？」を解決する — Claude Codeローカル運用ガイド

## 原文リンク

[Tool Callingのシグネチャと呼び出し率についての調査](https://zenn.dev/yy7613/articles/b3264acb153f40)
