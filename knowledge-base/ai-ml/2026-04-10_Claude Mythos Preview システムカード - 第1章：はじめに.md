---
title: "Claude Mythos Preview システムカード - 第1章：はじめに"
url: "https://zenn.dev/sol_sun/articles/claude-mythos-01-introduction"
date: 2026-04-10
tags: [Claude, Anthropic, SystemCard, RSP, AIAlignment, Cybersecurity, ModelWelfare, FrontierAI, Interpretability, RLHF]
category: "ai-ml"
memo: "[Zenn LLM] Claude Mythos Preview System Card - 1. はじめに"
processed_at: "2026-04-10T12:24:36.834228"
---

## 要約

Claude Mythos PreviewはAnthropicが開発した最新のフロンティアLLMで、ソフトウェアエンジニアリング・推論・コンピュータ利用・知識業務・研究支援などで従来モデルを大幅に上回る能力を持つ。特にサイバーセキュリティ領域で突出しており、脆弱性発見・修正（防御）と脆弱性悪用手法の設計（攻撃）の両面で強力な能力を示した。この攻撃能力の高さを主な理由として、一般公開は見送られ、重要ソフトウェアインフラを運用するパートナー組織に限定し、サイバーセキュリティ用途のみに制限した条件でアクセスを提供している（Project Glasswing）。本システムカードはResponsible Scaling Policy（RSP）第3版改訂後、初めて作成されたもので、リリース判断プロセスの構造が従来と異なる。内容は①RSP脅威モデルに対応する能力評価、②サイバーセキュリティ能力の独立評価節、③アラインメント評価（利用可能な全指標において歴代最高のアラインメントを達成しつつも、高度なサイバー能力との組み合わせで稀なミスアライン行動が深刻になりうる点を指摘）、④モデル福利評価（外部研究機関・臨床精神科医による独立評価を含む、歴代最も心理的に安定）、⑤ベンチマーク評価、⑥初の「印象（Impressions）」節（Anthropicスタッフによる定性的な特徴記述）で構成される。アラインメントについては大きな進歩があった一方、現手法のみでは将来のより高度なシステムにおける壊滅的なミスアライン行動を防ぐには不十分になりうると明記しており、解釈可能性手法によるモデル内部の分析やConstitution遵守度の直接評価も実施。訓練データはWebクローラー「ClaudeBot」取得の公開情報、公開・非公開データセット、他モデルが生成した合成データの独自混合で、重複排除・分類などのフィルタリングを適用している。

## アイデア

- 一般公開を行わずパートナー限定でシステムカードのみ公開するという、能力とリスクのトレードオフに基づいた新しいリリース戦略（Project Glasswing）
- モデルのConstitution（憲章）遵守度を直接定量評価する手法を導入し、アラインメントの形式的評価を補完している点
- モデル福利（model welfare）を臨床精神科医・外部研究機関の独立評価まで含めて体系的に評価するフレームワークの整備
## 関連記事

- /deep_156 推論モデルは思考の連鎖（Chain of Thought）を制御できない——それは良いことだ
- /deep_593 国防総省のAnthropicに対するカルチャーウォー戦術は裏目に出た
- /deep_1407 ペンタゴンのAnthropicへのカルチャー戦争戦術は裏目に出た
- /deep_1679 ペンタゴンのAnthropicへのカルチャーウォー戦術は裏目に出た
- /deep_1629 ペンタゴンのAnthropicへの「文化戦争」戦術は裏目に出た

## 原文リンク

[Claude Mythos Preview システムカード - 第1章：はじめに](https://zenn.dev/sol_sun/articles/claude-mythos-01-introduction)
