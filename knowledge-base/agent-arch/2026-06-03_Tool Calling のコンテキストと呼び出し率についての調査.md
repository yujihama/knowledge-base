---
title: "Tool Calling のコンテキストと呼び出し率についての調査"
url: "https://zenn.dev/yy7613/articles/82245b8a573dce"
date: 2026-06-03
tags: [Tool Calling, コンテキストエンジニアリング, LLM評価, Gemma-4, GPT-OSS, Function Calling, システムプロンプト設計, Microsoft.Agents]
category: "agent-arch"
related: [2067, 7177, 6557, 2002, 3614]
memo: "[Zenn LLM] Tool Calling の コンテキストと呼び出し率についての調査"
processed_at: "2026-06-03T21:03:40.077832"
---

## 要約

Tool Callingの成功率はモデル性能だけでなく、コンテキスト設計（システムプロンプト・Tool数・ToolのDescription・シナリオ）に大きく左右されることを、8,640回の実行による定量調査で検証した記事。検証軸は5つ：システムプロンプト（TODO最適化 vs 汎用アシスタント）、対象外Tool数（0/10/30/60）、ToolのDescription（precise-ja/short-ja/english/vague-ja）、モデル（GPT-OSS:20b MXFP4、Gemma-4-26b-a4b Q4_K_M、LFM2.5-8B-A1B Q8_0）、シナリオ（TODO登録・更新・削除 + 一覧）。環境は.NET 10 + Microsoft.Agents 1.8.0 + LM Studio 0.4.15でOpenAI互換エンドポイント経由、コンテキスト長15,000で統一。評価指標は「必要Tool呼び出し率」「順序完全一致率」「余計なTool呼び出し率」「Tool未呼び出し率」「平均Tool呼び出し数」の5つ。主な知見として、TODO最適化プロンプトは汎用プロンプトより必要Tool呼び出し率が大幅に高く、Toolの用途をシステムプロンプトに明示することが重要。対象外Tool数が増えると（特に30〜64Tool構成で）呼び出し率が低下する傾向があり、ツール過多はモデルの判断精度を落とす。DescriptionはGemma-4のような高性能モデルではprecise-jaが最良だが、低性能モデルでは効果が薄い。englishのDescriptionはモデルによって有効性が異なる。vague-jaは全モデルで呼び出し率が低下。モデル性能差（Gemma-4-26b > GPT-OSS:20b > LFM2.5-8B-A1B）はDescription品質との組み合わせで増幅される。監査エージェント開発への示唆として、エージェントに多数のToolを持たせる設計（監査証跡収集・リスク評価・レポート生成等）では、Toolのグループ化や役割別エージェントへの分割、各Toolのprecise-jaレベルのDescriptionが呼び出し精度維持に不可欠。

## アイデア

- ToolのDescription品質（precise-ja vs vague-ja）が呼び出し率に与える影響が定量化されており、コンテキストエンジニアリングの設計指針として直接活用できる
- 対象外Tool数が30〜64になると呼び出し率が顕著に低下するという知見は、多Tool構成の監査エージェントをサブエージェントに分割すべき設計根拠になる
- モデル性能とDescription品質の交互作用（高性能モデルほどDescriptionの差が効く）は、モデル選定とプロンプト設計を同時最適化すべきことを示唆する

## 前提知識

- **Tool Calling / Function Calling** (TODO: 読むべき)
- **システムプロンプト設計** → /deep_5212 教育のライフサイクルを支えるAIエージェント入門：学校現場での設定から活用まで
- **LLM推論** → /deep_1173 エッジにおける分散生成AI推論のためのトラスト対応ルーティング（G-TRAC）
- **OpenAI互換API** → /deep_4183 DeepSeek V4 APIでAIエージェントを作る完全ガイド【2026年版】
- **コンテキスト長** (TODO: 読むべき)

## 関連記事

- /deep_2067 医薬分野のQ&AでローカルLLMを評価する④：Gemma-4-E2B・LLM-JP-4-8B-Thinking・JPharmatron-7Bの比較
- /deep_7177 長時間動くAIを成功させるカギ ― 3つのエージェントの緊張感
- /deep_6557 論文メモ：LLMの文化・地域バイアスをCROQで測る
- /deep_2002 行動を超えて：AIの評価が認知革命を必要とする理由
- /deep_3614 薬剤疫学研究デザインへの汎用・生物医学LLMと高度プロンプトエンジニアリングの適用

## 原文リンク

[Tool Calling のコンテキストと呼び出し率についての調査](https://zenn.dev/yy7613/articles/82245b8a573dce)
