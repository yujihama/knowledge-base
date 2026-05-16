---
title: "AI for Science の歩き方 #13 ― まとめとアクションプラン"
url: "https://zenn.dev/aws_japan/articles/ai4s-13-action-2026"
date: 2026-04-28
tags: [AI for Science, 再現性, Amazon Bedrock, プロンプトエンジニアリング, Model Invocation Logging, エージェンティック・サイエンス, Chain-of-Thought, Guardrails, SPReAD, 生成AI研究倫理]
category: "ai-ml"
related: [2865, 2576, 3098, 1421, 2446]
memo: "[Zenn LLM] AI for Science の歩き方 #13 ― まとめとアクションプラン"
processed_at: "2026-04-28T12:35:21.710104"
---

## 要約

本記事はAWSジャパン有志による「AI for Science の歩き方」シリーズの最終回（第13回）であり、研究者が生成AIを活用する際の再現性確保・実践アクションプラン・トレンド展望を体系的にまとめたもの。

【再現性の課題と対策】生成AIには出力の非決定性（temperature=0でも完全な決定性は保証されない）、商用モデルの予告なし更新、プロンプトの暗黙知という3つの再現性阻害要因がある。Spirling（2023）やZheng et al.（2025）はブラックボックス性を科学的検証の主要障壁として指摘。放射線医学LLM研究246件を分析したSuh et al.（2026）によれば、temperatureを報告していた研究はわずか16.7%、モデルバージョン明記も27.6%にとどまる。対策として最低限記録すべき3項目は①モデル名とバージョン（例: anthropic.claude-sonnet-4-6）、②推論パラメータ（temperature, top_p, maxTokens）、③プロンプト全文。Amazon Bedrockでの対応機能としてはModel Invocation Logging（リクエスト・レスポンスをS3/CloudWatch Logsに自動記録）、Converse APIによるパラメータ固定、Guardrailsによる出力品質の一貫性確保がある。ただし一部モデル（Claude Opus 4.7等）ではサンプリングパラメータの指定自体が不可。

【今後のトレンド6点】①AIが「道具」から「研究パートナー」へ（エージェンティック・サイエンス、MCP/A2Aプロトコルによる自律的研究遂行）、②AI＋ロボット統合による物理実験の自動化（Coscientistが先駆例）、③説明可能AI（XAI）・Chain-of-Thoughtによるブラックボックス解消、④NIH方針・EU AI Act・日本AI法など規制枠組みの整備、⑤GPU値下げ・ノーコードツール普及によるコスト低下、⑥日本の戦略方針（文科省、2026年3月）で2035年度までにTop10%論文中AI関連論文数を世界3位にする目標設定。Stanford HAI AI Index 2025によれば民間AI投資は米国$109.1Bに対し中国$9.3B、英国$4.5Bで日本は上位国と大きな差がある。

【実践アクションプラン】ステップ1（30分）: Claude無料版で研究質問を3つ投げ、回答の文献情報をCiNii/PubMedで検証。ステップ2（1〜2時間）: 機関AIポリシー・ジャーナルガイドライン確認。ステップ3（1〜2週間）: Zero-shot/Few-shot/Chain-of-Thoughtによるプロンプトエンジニアリング習得。付録としてAWSサービス一覧と用語集を収録。

監査エージェント開発への示唆: Model Invocation LoggingによるAPI呼び出しの全記録はエージェントシステムの監査証跡構築に直接応用可能。Guardrailsによる出力品質の一貫性確保はLLM-as-judgeの評価安定性向上にも活用できる。

## アイデア

- temperature=0でも完全な再現性が保証されないという事実（GPU並列計算における浮動小数点演算順序の差異が原因）は、LLM評価ハーネス設計で見落とされがちな盲点であり、評価スコアのばらつき要因として定量的に扱う必要がある
- 放射線医学LLM研究246件でtemperature記録率16.7%・モデルバージョン記録率27.6%という実態は、監査エージェントシステムの出力ログ設計において最低限記録すべき項目の根拠として引用できる定量的エビデンス
- MCP/A2Aプロトコルによるエージェント間連携とロボット統合（Coscientist型）の組み合わせが示す「実験の完全自動化ループ」は、内部監査プロセスにおける証拠収集・検証ステップの自律化アーキテクチャ設計の参照モデルになりうる

## 前提知識

- **Chain-of-Thought** → /deep_59 EcoThink: 持続可能でアクセスしやすいエージェントのためのグリーン適応的推論フレームワーク
- **Amazon Bedrock** → /deep_2247 AI for Science の歩き方 #8 ― 分野別の事例と失敗から学ぶ教訓
- **temperature（推論パラメータ）** (TODO: 読むべき)
- **プロンプトエンジニアリング** → /deep_6 Harness Engineeringとは何か？プロンプトの次に来る「AIエージェントの環境設計」を実務目線で解説
- **Guardrails** → /deep_1421 AI時代の「〇〇エンジニアリング」を馬で理解する：プロンプト・コンテキスト・ハーネスの3層構造

## 関連記事

- /deep_2865 AI for Science の歩き方 #11 ― モデルの選び方と品質管理
- /deep_2576 プロンプトエンジニアリングは
- /deep_3098 LLMプロンプトにエビデンスベースの心理学を組み込む ― 恋愛分析AIの設計
- /deep_1421 AI時代の「〇〇エンジニアリング」を馬で理解する：プロンプト・コンテキスト・ハーネスの3層構造
- /deep_2446 AI for Science の歩き方 #9 ― 実践の心得 ― 効率・データ・検証

## 原文リンク

[AI for Science の歩き方 #13 ― まとめとアクションプラン](https://zenn.dev/aws_japan/articles/ai4s-13-action-2026)
