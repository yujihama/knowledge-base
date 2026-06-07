---
title: "Anthropic Partner Bootcamp参加レポート — AIエージェント設計の6原則"
url: "https://zenn.dev/blacook/articles/agent-engineering-principles"
date: 2026-06-07
tags: [AgentEngineering, PromptEngineering, Anthropic, LLM-as-Judge, Eval, ContextEngineering, ToolDesign, pass@k]
category: "agent-arch"
related: [1247, 4209, 6484, 4538, 4387]
memo: "[Zenn LLM] Anthropic Partner Bootcampに参加した件 ー AIエージェント設計の6原則"
processed_at: "2026-06-07T09:07:04.086224"
---

## 要約

2026年5月にサンフランシスコで開催されたAnthropicのパートナー向け2日間エンジニアリングトレーニング「Partner Bootcamp」の学びを、設計チェックリストとして使える6原則に抽象化した記事。

【原則1: モデル更新は最後の手段】LLMエージェントの不具合はPrompt層・Tool層・Context層・Orchestration層の4層構造で切り分け、モデル差し替えは他3層を排除した後の最終手段とする。BootcampではHaiku/Sonnetの制約下で全演習をプロンプトとツール定義の修正のみで解決した。

【原則2: コンテキストは容量ではなく資源】Chromaの研究「Context Rot」が示すように、入力長の増大とともに忠実性・検索性能・推論精度が劣化する。1Mトークンは物理上限であり精度上限ではない。ターン単位で「残す/捨てる/要約する/外に逃す」の4判断を明示的に実施するロジックが必要。

【原則3: 3層責務モデル】System Prompt（役割・原則）、Tool Description（目的・引数・使用条件）、Tool Implementation（入力検証・エラー返却）の3層に責務を分離し、同一責務の重複配置を避ける。ツールdescriptionは形式・制約・例を1セットで記述する人間向けドキュメントとして書く。

【原則4: Eval先行（Eval is the spec）】評価スイートを実装より先に作成しないと、評価が「現在の挙動の正当化」に流れる。Graderの種別はCode（80%）、LLM-as-Judge（15%）、Human（5%）の比率を目安とし、Codeで書けるものをJudgeに流さない。

【原則5: 平均ではなく分布で語る】temperature=0でも非決定性が存在するため、同一入力をn回実行して分布を計測する。pass@k（k回中1回成功）とpass^k（k回全成功）を用途で使い分け、SLAはp99で語る。平均90%でもpass^3が40%なら「3割の確率で壊れる」機能となる。

【原則6: 見えていない入力で汎化を測る】開発セットと評価セットを物理分離し、設計者が評価セットを見ない運用とする。実装前に「どんな入力で壊れうるか」の失敗パターン（空入力・型不一致・境界値・注入攻撃等）をカタログ化し、各カテゴリで事前テストを書く。未知入力での挙動がハンドオフの判断基準となる。

監査エージェント開発への示唆として、Tool Descriptionの厳密な記述（enumによる値域制約、エラー文言の明示）と、Eval先行開発の手法はLangGraph/Pydanticベースのエージェント品質管理に直接適用可能。特にpass^k指標は監査用途の高信頼性要件に重要。

## アイデア

- pass^k（k回全成功）指標の導入：平均精度ではなくSLAをp99・pass^kで語ることで、「3割の確率で壊れる」機能を出荷前に検出できる実践的指標
- Eval先行開発（Eval is the spec）：PRD要件をすべてassertionに翻訳することで、翻訳できない要件は設計として曖昧というサインになる逆説的品質管理
- 3層責務モデルにおける重複配置アンチパターン：同一責務を複数層に重ねると矛盾時の優先判断が不明になり、モデルの判断が揺れるという具体的な副作用の指摘

## 前提知識

- **LLMエージェント** → /deep_7 Karpathy発AutoResearchで一晩100実験を自動化する仕組みと実践
- **Tool Calling** → /deep_946 HuggingChatにコミュニティツール機能を導入：任意のSpaceをLLMツールとして利用可能に
- **Context Window** → /deep_3515 なぜAIエージェントの再現性はプロンプトだけで解決できないのか？——暗黙知の構造化と「記憶設計」への転換
- **LLM-as-Judge** → /deep_3 Claude Code のAIチームでLLMの品質を自動でチェックする方法
- **System Prompt** → /deep_36 LLMを「嘘つき」から「専門家」に変える技術 — Context Engineering 実践入門

## 関連記事

- /deep_1247 ハーネスエンジニアリングとは何か：プロンプト→コンテキスト→ハーネスへ至るAIエージェント設計の変遷
- /deep_4209 ハイプと利益の間にある欠落したステップ：AIの「ステップ2問題」
- /deep_6484 prompt / context / agent / harness: ボトルネック移動で読むLLM engineeringの系譜とその先
- /deep_4538 AIのヒープと利益の間に欠けるステップ：「Step 2：？」問題
- /deep_4387 AIのヒープと利益の間に欠けているステップ：「Step 2: ?」問題

## 原文リンク

[Anthropic Partner Bootcamp参加レポート — AIエージェント設計の6原則](https://zenn.dev/blacook/articles/agent-engineering-principles)
