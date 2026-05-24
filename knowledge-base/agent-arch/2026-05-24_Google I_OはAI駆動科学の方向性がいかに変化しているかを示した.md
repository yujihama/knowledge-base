---
title: "Google I/OはAI駆動科学の方向性がいかに変化しているかを示した"
url: "https://www.technologyreview.com/2026/05/22/1137813/google-i-o-showed-how-the-path-for-ai-science-is-shifting/"
date: 2026-05-24
tags: [AI-for-Science, Gemini, AlphaFold, エージェント型AI, WeatherNext, Co-Scientist, AlphaEvolve, 汎用推論モデル, 再帰的自己改善]
category: "agent-arch"
related: [6251, 6102, 6220, 3220, 6370]
memo: "[MIT Technology Review AI] Google I/O showed how the path for AI-driven science is shifting"
processed_at: "2026-05-24T21:02:49.144757"
---

## 要約

Google I/OにてDeepMind CEOのDemis Hassabisは「シンギュラリティの山麓に立っている」と発言し、AIによる科学研究の将来像を示した。発表の中心は、ハリケーン「Melissa」のジャマイカ上陸を事前予測した気象予報ソフト「WeatherNext」だったが、記事が指摘するのはこの具体的な成果と壮大な修辞の間にある緊張関係だ。

AI for Scienceには2つのアプローチが存在する。第1は特定科学問題に特化した専用ツール（AlphaFold、WeatherNext、AlphaGenome等）、第2はLLMベースのエージェントシステムによる自律的研究遂行だ。GoogleはこれまでAlphaFoldでノーベル賞級の成果を上げ、AlphaFoldのタンパク質構造予測は全世界300万人超の研究者に利用されている。傘下のIsomorphic Labsは創薬目的で20億ドルのシリーズB資金調達を完了した。

一方で、Googleは明確にエージェント志向へのシフトを見せている。AlphaFoldでノーベル賞を受賞したJohn Jumper研究員がAIコーディング部門に異動したことは、汎用エージェントへの人材・資源の再配分を示唆する。コーディング能力はAIエージェントが科学研究を遂行する際の基盤技術であり、AnthropicやOpenAIにコーディングツールで後れを取るGoogleがこの領域を強化する動機は複合的だ。

Google I/Oで発表されたGemini for Scienceは、仮説生成AI「Co-Scientist」とアルゴリズム最適化「AlphaEvolve」を統合したLLMベースの科学研究プラットフォームで、研究者からのアクセス申請受付を開始した。Stanford遺伝学者Gary PeltzはCo-Scientistを「デルフォイの神託に相談するよう」と評した（Nature Medicine掲載）。また今週OpenAIは汎用推論モデル（GPT-5.5系）が重要な数学的予想を反証したと発表しており、数学者らはこれをGenerative AIの数学分野への最も重要な貢献と評価している。

Hassabisは「今後10年はAIを科学者を支援する優れたツールとして考えるべきだが、それ以降はコラボレーターになり得る」と述べており、「AI Co-Scientist」という命名自体が人間中心性を意図している。しかし効果的な科学的協力者であるためには独立した科学的能力が必要であり、記事は超人的AIエージェント科学者という将来像への示唆でまとめている。監査エージェント開発の観点では、汎用推論モデルが専門知識領域（数学・科学）で自律的貢献を果たし始めている点は、監査・内部統制領域のエージェント設計においても参照すべき事例となる。

## アイデア

- 汎用推論モデル（GPT-5.5系）が数学的予想を反証した事例は、専門特化ツール不要論を強化し、エージェント型AIが専門領域（監査・法務等）でも自律的貢献できる可能性を示す
- AlphaFold受賞者がコーディング部門へ異動した人事は、専用科学ツールから汎用エージェント基盤へのリソース移行を示す組織シグナルであり、AI戦略の優先度変化を人事から読み解く手法として参考になる
- Gemini for ScienceはCo-ScientistとAlphaEvolveを統合し、仮説生成→アルゴリズム最適化→専用ツール呼び出しのパイプラインを構築しており、マルチエージェント＋特化ツール呼び出しの設計パターンとして監査エージェントアーキテクチャに応用できる

## 前提知識

- **LLMエージェント** → /deep_7 Karpathy発AutoResearchで一晩100実験を自動化する仕組みと実践
- **AlphaFold** → /deep_3158 人工科学者：今AIで重要な10のこと — MIT Technology Review
- **再帰的自己改善 (RSI)** (TODO: 読むべき)
- **汎用推論モデル** → /deep_6385 Google I/OはAI駆動科学の方向性がどう変化しているかを示した
- **マルチエージェントシステム** → /deep_628 Mimosaフレームワーク：科学研究向け進化型マルチエージェントシステム

## 関連記事

- /deep_6251 Google I/O 2026直前：コーディングAIでの遅れと科学AIでの強みを分析
- /deep_6102 Google I/O 2026で何を期待するか：コーディングAIの劣勢、科学AI、そしてAI業界の内紛
- /deep_6220 Google I/O 2026で何を期待すべきか：コーディング巻き返しと科学AI
- /deep_3220 人工科学者：AIが科学研究を自律的に推進する時代の到来と課題
- /deep_6370 Google I/Oで期待されること：コーディング巻き返し、科学AI、そして業界の drama

## 原文リンク

[Google I/OはAI駆動科学の方向性がいかに変化しているかを示した](https://www.technologyreview.com/2026/05/22/1137813/google-i-o-showed-how-the-path-for-ai-science-is-shifting/)
