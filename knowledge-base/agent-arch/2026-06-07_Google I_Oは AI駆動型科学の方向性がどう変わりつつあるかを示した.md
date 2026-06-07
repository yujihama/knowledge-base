---
title: "Google I/Oは AI駆動型科学の方向性がどう変わりつつあるかを示した"
url: "https://www.technologyreview.com/2026/05/22/1137813/google-i-o-showed-how-the-path-for-ai-science-is-shifting/"
date: 2026-06-07
tags: [Google DeepMind, Gemini for Science, AlphaFold, WeatherNext, AI Co-Scientist, AlphaEvolve, agentic AI, 科学AI, 汎用推論モデル, recursive self-improvement]
category: "agent-arch"
related: [6461, 6370, 6710, 6585, 3430]
memo: "[MIT Technology Review AI] Google I/O showed how the path for AI-driven science is shifting"
processed_at: "2026-06-07T21:25:00.660365"
---

## 要約

Google I/OのキーノートでDeepMind CEO Demis Hassabisは「シンギュラリティの山麓に立っている」と宣言した。この発言の文脈は科学AI領域であり、具体的にはWeatherNextと呼ばれる気象予測ソフトウェアがハリケーン「Melissa」のジャマイカ上陸前に高精度な早期警報を提供し、人命救助に貢献した事例が紹介された。この成果は重要だが、シンギュラリティの証拠とは言い難いものでもある。

記事の核心は、科学AI領域における2つのアプローチの対立構造にある。第1は特定科学問題向けに設計・学習された専門ツール（AlphaFold、WeatherNext、AlphaGenome、AlphaEarth Foundations等）。第2はLLMベースの汎用エージェントが人間の関与なしに最先端研究を実行するアジェンティックアプローチだ。

GoogleはAlphaFoldで3000万人超の研究者に利用されるタンパク質構造予測ツールを生み出し、ノーベル賞を受賞したJohn Jumperを擁していたが、そのJumperが現在はAIコーディング分野に異動していることがLA Timesによって報じられた。AnthropicとOpenAIにコーディングツールで後れを取るという競合上の理由もあるが、エージェント型科学AIへのコーディング能力が不可欠である点も異動の背景とみられる。

今週OpenAIは、専門化されていない汎用推論モデル（GPT-5.5系統）が重要な数学的予想を反証したと発表した。これは生成AIの数学への最も意義深い貢献の一つとされており、汎用エージェントが専門ツールなしに独自の科学的貢献を生み出せる可能性を示唆する。

GoogleはGemini for Scienceパッケージを発表し、仮説生成AI「Co-Scientist」、アルゴリズム最適化「AlphaEvolve」などのLLMベース科学ツールを統合ブランド化した。スタンフォードの遺伝学者Gary Peltzはこれを「デルフォイの神託に相談するようだ」と評した。これらはまだ一般公開されていないが、任意の研究者がアクセス申請可能になった。

Hassabisは「今後10年はAIを科学者を支援するツールとして考えるべきで、その先は協力者になり得る」と述べ、「AI Scientist」でなく「AI Co-Scientist」という命名が象徴するよう、人間中心の枠組みを維持している。しかし科学的協力者として機能するには自律的な科学能力が必要であり、エージェント型科学AIが人間を超える能力を持つ未来への布石と読むことも可能だ。

監査エージェント開発への示唆として、専門ツール vs. 汎用エージェントの二分法はAI監査においても同様に生じる。AlphaFold的な「監査専用ファインチューニングモデル」と、汎用LLMにReActループで監査手続きを実行させるアーキテクチャの選択判断は、本記事の議論と直接対応する。汎用推論モデルによる数学予想の反証という事例は、専門ドメインへの汎用エージェント適用可能性の根拠となる。

## アイデア

- 専門特化ツール（AlphaFold級）と汎用エージェントの対立は、AIが科学的発見の主体となる閾値をどこに設定するかという設計思想の分岐点であり、監査AIにおける同様のアーキテクチャ選択に直結する
- OpenAIの汎用推論モデルが専門訓練なしで数学予想を反証したという事実は、ドメイン特化FTが不要になる転換点の到来を示唆し、LLM-as-judgeや自律監査エージェントの実現可能性を高める根拠となる
- Googleが「AI Scientist」でなく「AI Co-Scientist」と命名したのは単なるマーケティングでなく、段階的な自律性移譲を前提とした製品ロードマップの反映であり、エージェント設計における人間-AI役割分担の明示的モデル化の重要性を示す

## 前提知識

- **LLMエージェント / ReAct** (TODO: 読むべき)
- **AlphaFold** → /deep_3158 人工科学者：今AIで重要な10のこと — MIT Technology Review
- **recursive self-improvement** → /deep_6385 Google I/OはAI駆動科学の方向性がどう変化しているかを示した
- **汎用推論モデル（GPT-5.5系）** (TODO: 読むべき)
- **Gemini API** → /deep_1736 ハーネスエンジニアリングに挑戦し、AIテニスコーチアプリをAIと作った話

## 関連記事

- /deep_6461 Google I/Oは科学AI分野での方向性がいかに変化しているかを示した
- /deep_6370 Google I/Oで期待されること：コーディング巻き返し、科学AI、そして業界の drama
- /deep_6710 Google I/O 2026で期待されること：コーディングAIの巻き返しと科学AI分野の動向
- /deep_6585 Google I/O 2026で何が期待されるか：コーディング巻き返し、科学AI、そして業界の争乱
- /deep_3430 人工科学者：AIが科学研究を自律的に実行する時代の到来

## 原文リンク

[Google I/Oは AI駆動型科学の方向性がどう変わりつつあるかを示した](https://www.technologyreview.com/2026/05/22/1137813/google-i-o-showed-how-the-path-for-ai-science-is-shifting/)
