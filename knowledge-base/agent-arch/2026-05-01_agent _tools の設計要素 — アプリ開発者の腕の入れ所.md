---
title: "agent /tools の設計要素 — アプリ開発者の腕の入れ所"
url: "https://zenn.dev/loglass/articles/5512010213b87e"
date: 2026-05-01
tags: [ハーネスエンジニアリング, tool設計, agent設計, sub-agent, system-prompt, Zod, Few-shot, 決定論的パイプライン, LLM]
category: "agent-arch"
related: [892, 2361, 36, 1421, 1266]
memo: "[Zenn LLM] agent /tools の設計要素 — アプリ開発者の腕の入れ所"
processed_at: "2026-05-01T12:21:28.803823"
---

## 要約

本記事は、LLMエージェント開発においてSDK/ライブラリが吸収する定型処理（モデル呼び出し、tool callループ、streaming、会話履歴管理）の外側に残るアプリ開発者の設計領域を体系的に整理したもの。

エージェント設計の核心を「agent = system prompt × tool × context のカプセル化」として捉え、OOPの object = state + method + domain logic に対応させる補助線を提示している。この視点から、agentの切り出し単位は「知識の特化」×「許されたアクション」×「受け持つコンテキスト」の凝集体として定義される。

tool設計については、tool = Intent → Outcome（+ 副作用）というモデルで整理し、構成要素をdescription・I/O・pipelineの3つに分解する。descriptionはtoolの取説であり、「呼ぶべき場面」「呼ぶべきでない場面（代替tool名付き）」を明示することでLLMの判断精度を高める。I/O設計ではZodの.describe()による属性レベルの意図明示と、inputExamplesによるFew-shot効果を活用できる。

pipeline設計では、tool内部を「決定論的関数と非決定論的関数の組み合わせパイプライン」として捉える点が実践的。ECサイトの棒グラフ作成toolを例に、「外部APIで商品カテゴリ取得（決定論的）→ LLMでチャート構成推論（非決定論的）→ チャート作成API呼び出し（決定論的）」という3段パイプラインを示す。非決定論的関数についても、動的試行錯誤が不要ならワンショットLLM関数、必要なら agent tool loop と使い分ける指針を提示。

sub agent as tool パターンも解説し、main agentのコンテキスト肥大化を避けるために業務単位でカプセル化したsub agentをtoolとして登録する構成を示す。

最後に、agent spec テンプレート（Profile / System Prompt / Registered Tools / Sub Agents / Context の5セクション）を提供。eval容易性（筋のよいagent分割がevalの部分化に直結）とmemory設計（agent単位でmemoryの検索・更新・破棄範囲を定める）への発展も示唆している。

監査エージェント開発への示唆：監査手続をagent単位で切り出す際、「何の業務知識を持たせ（system prompt）、どの操作を許可し（tool）、どの実行時情報を閉じ込めるか（context）」という3軸の設計判断は、LangGraph上でのnode/edge設計とほぼ直交する概念として活用できる。特にtool descriptionの「呼ぶべきでない場面＋代替tool名」パターンは、監査証跡取得・仕訳検証・リスク評価といった複数toolが共存する場面でのLLM誤選択を抑制する実践的手法になる。

## アイデア

- tool内部を『決定論的関数と非決定論的関数の組み合わせパイプライン』として設計する視点は、関数合成の観点でI/Oスキーマを厳格に定義することで前後の接続を保証できる点が実装上の具体的価値を持つ
- tool descriptionに『呼ぶべきでない場面＋代替tool名』を明示するパターンは、LLMが類似toolを混同しやすい状況での誤選択を抑制するprompt engineeringの実用的テクニックになっている
- agent = context + tool + prompt というOOP的補助線により、agentの切り出し粒度の判断が『コンテキストの凝集度』という既存のソフトウェア設計原則（高凝集・低結合）に接続できる

## 前提知識

- **LLM tool call** (TODO: 読むべき)
- **agent loop** (TODO: 読むべき)
- **system prompt** → /deep_36 LLMを「嘘つき」から「専門家」に変える技術 — Context Engineering 実践入門
- **Zod schema** (TODO: 読むべき)
- **sub-agent** → /deep_2550 自律型エージェントの全体像：LLM・Harness・Computeの3層構造からセキュリティまで

## 関連記事

- /deep_892 重み空間モデルマージによる大規模言語モデルの壊滅的忘却対策と指示追従能力の改善
- /deep_2361 MCPサーバー開発におけるTool数の上限について考える
- /deep_36 LLMを「嘘つき」から「専門家」に変える技術 — Context Engineering 実践入門
- /deep_1421 AI時代の「〇〇エンジニアリング」を馬で理解する：プロンプト・コンテキスト・ハーネスの3層構造
- /deep_1266 🤗 Transformersでネイティブサポートされる量子化スキームの概要

## 原文リンク

[agent /tools の設計要素 — アプリ開発者の腕の入れ所](https://zenn.dev/loglass/articles/5512010213b87e)
