---
title: "Google I/Oが示したAI駆動科学の方向性の転換：専門特化ツールから汎用エージェントへ"
url: "https://www.technologyreview.com/2026/05/22/1137813/google-i-o-showed-how-the-path-for-ai-science-is-shifting/"
date: 2026-06-04
tags: [科学AI, 汎用エージェント, AlphaFold, WeatherNext, Gemini for Science, Co-Scientist, AlphaEvolve, 再帰的自己改善, LLMエージェント]
category: "agent-arch"
related: [6461, 6370, 6733, 6251, 6299]
memo: "[MIT Technology Review AI] Google I/O showed how the path for AI-driven science is shifting"
processed_at: "2026-06-04T09:07:03.865394"
---

## 要約

2026年のGoogle I/OでDeepMind CEO Demis Hassabisは「シンギュラリティの麓に立っている」と宣言した。彼が語った文脈は科学AIセッションであり、具体的にはジャマイカに上陸したハリケーン・メリッサの事前警告を行った気象予測ソフトウェア「WeatherNext」の成果だった。この発言は、科学向けAIの2つのアプローチの間にある緊張を象徴している。

第1のアプローチは、AlphaFoldやWeatherNextのように特定の科学問題を解くために設計・訓練された専門特化ツールである。AlphaFoldはタンパク質立体構造予測問題を解決しノーベル賞を受賞、世界300万人以上の研究者に利用されている。AlphaFoldの技術を新薬開発に応用するIsomorphic Labsは直近のシリーズBラウンドで20億ドルを調達した。

第2のアプローチは、LLMベースの汎用エージェントが自律的に研究を実行するモデルである。OpenAIは今週、自社の汎用推論モデル（GPT-5.5系）が重要な数学的予想を反証したと発表した。数学者からは「生成AIが数学に貢献した最も意義深い成果」との評価を得ている。このモデルは数学専用ではなく一般目的の推論モデルである点が重要で、汎用エージェントが科学研究に独立した貢献をできることを示唆する。

Googleはエージェント主導の科学的未来に向けたリソース再配分の兆候を示している。AlphaFoldでノーベル賞を受賞したGoogle FellowのJohn JumperがAIコーディング部門に異動した事実はその象徴だ。Googleのコーディングツールは現在AnthropicやOpenAIに遅れを取っており、その巻き返しと同時に、コーディング能力がエージェント型科学システムの成否を左右するという戦略的判断が背景にある。

新たに発表された「Gemini for Science」パッケージは、仮説生成AI「Co-Scientist」とアルゴリズム最適化AI「AlphaEvolve」をLLMベースのシステムとして統合する。Co-Scientistの早期テスターであるStanford大学の遺伝学者Gary Peltzは「デルフォイの神託に相談するようだ」と評している。現時点ではまだ一般公開されていないが、研究者向けアクセス申請を受け付け始めた。

Googleはエージェントを「人間科学者の代替」ではなく「共同研究者（Co-Scientist）」と位置づけることに慎重であり、命名にもその意図が表れている。Hassabisは「今後10年はAIを科学者を助けるツールとして考えるべき」としながらも、その先については「協力者になりうる」と述べている。専門特化ツールとエージェントは排他的ではなく、エージェントがAlphaFoldを呼び出す設計も可能だが、業界の重心は汎用エージェント側に明確にシフトしている。

## アイデア

- 汎用推論モデル（GPT-5.5系）が数学的予想を反証できたという事実は、専門特化訓練なしでも科学貢献が可能なことを示し、専門ツール開発への投資対効果の根拠を揺るがす
- エージェント型科学システムの成否がコーディング能力に依存するという構造は、監査エージェント開発においても汎用コード生成・実行能力の強化が科学的推論能力に直結することを示唆する
- AlphaFoldのような「一点突破型の専門特化ツール」からGemini for Scienceのような「ツールオーケストレーター型エージェント」への移行は、LangGraphベースのマルチエージェント設計パターンとそのまま対応しており、監査エージェントの設計方針にも参照できる

## 前提知識

- **LLMエージェント** → /deep_7 Karpathy発AutoResearchで一晩100実験を自動化する仕組みと実践
- **AlphaFold** → /deep_3158 人工科学者：今AIで重要な10のこと — MIT Technology Review
- **再帰的自己改善** → /deep_6455 Google I/OはAI駆動科学の方向性がいかに変化しているかを示した
- **ReAct / 推論モデル** (TODO: 読むべき)
- **ツールオーケストレーション** (TODO: 読むべき)

## 関連記事

- /deep_6461 Google I/Oは科学AI分野での方向性がいかに変化しているかを示した
- /deep_6370 Google I/Oで期待されること：コーディング巻き返し、科学AI、そして業界の drama
- /deep_6733 Google I/Oで何を期待するか：コーディング巻き返しとAI科学の最前線
- /deep_6251 Google I/O 2026直前：コーディングAIでの遅れと科学AIでの強みを分析
- /deep_6299 Google I/O 2026で期待されること：コーディングAIの巻き返しと科学AI強化

## 原文リンク

[Google I/Oが示したAI駆動科学の方向性の転換：専門特化ツールから汎用エージェントへ](https://www.technologyreview.com/2026/05/22/1137813/google-i-o-showed-how-the-path-for-ai-science-is-shifting/)
