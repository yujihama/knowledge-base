---
title: "Google I/Oが示したAI駆動科学の方向転換：専門ツールから汎用エージェントへ"
url: "https://www.technologyreview.com/2026/05/22/1137813/google-i-o-showed-how-the-path-for-ai-science-is-shifting/"
date: 2026-06-01
tags: [AI Co-Scientist, AlphaEvolve, Gemini for Science, AlphaFold, 自律科学エージェント, 汎用推論モデル, WeatherNext, recursive self-improvement]
category: "agent-arch"
related: [6461, 6370, 6733, 6435, 6391]
memo: "[MIT Technology Review AI] Google I/O showed how the path for AI-driven science is shifting"
processed_at: "2026-06-01T21:27:46.771275"
---

## 要約

2026年5月のGoogle I/Oにて、Google DeepMind CEOのDemis Hassabisは「シンギュラリティの麓にいる」と発言した。この発言の文脈は気象予測AI「WeatherNext」によるハリケーンMelissaの事前警報という具体的な事例であり、汎用AGI的言説と専門ツールの実績との乖離を象徴している。

記事はAI科学アプローチの2潮流を対比する。第一は特定問題に特化した専門ツール（AlphaFold、WeatherNext、AlphaGenome、AlphaEarth Foundations）。第二はLLMベースの自律エージェントシステム（AI Co-Scientist、AlphaEvolve）。現状ではAlphaFoldは世界300万人以上の研究者に利用され、関連技術を持つIsomorphic Labsは20億ドルのシリーズB調達を完了している。一方でAlphaFoldでノーベル賞を受賞したJohn JumperがAIコーディング領域に異動したという報道は、Googleの内部優先順位が変化しつつあることを示唆する。

Googleは今回、複数のLLMベース科学システムを「Gemini for Science」として統合発表した。仮説生成AI「AI Co-Scientist」とアルゴリズム最適化「AlphaEvolve」を含み、研究者向けアクセス申請が開始された。スタンフォード大学の遺伝学者Gary Peltzは「デルフォイの神託に相談するようだ」と評した。エージェントシステムと専門ツールは排他的でなく、エージェントがAlphaFoldをツールとして呼び出す統合設計が志向されている。

同週にはOpenAIの汎用推論モデル（GPT-5.5系）が数学の重要な予想を反証したと発表。数学者からは「生成AIの数学への最も意味ある貢献」と評価された。これは専門特化なしの汎用モデルが独立した研究貢献を行えることを示し、自律科学エージェントの実現可能性を支持する。

Hassabisは「今後10年はAIを科学者を助けるツールとして考えるべき」としつつ、その先の「協働者」としてのAIを示唆している。「AI Scientist」でなく「AI Co-Scientist」という命名は人間中心のフレーミングを意図的に維持するものだが、超人的な自律科学AIという長期ビジョンはGoogleの方向性として明確に読み取れる。

監査エージェント開発への示唆：汎用LLMエージェントが仮説生成・検証ループを実行できるなら、監査領域においても「特定ルールベースの専門ツール」から「証拠収集→仮説形成→検証を自律で回すエージェント」への移行パスが現実的になる。AI Co-ScientistのアーキテクチャはLangGraphベースのReActエージェントと親和性が高く、設計参考として価値がある。

## アイデア

- 汎用LLM推論モデル（GPT-5.5系）が数学予想を反証した事例は、専門ファインチューニングなしに独立した知的貢献が可能であることを示し、エージェント科学者の実現可能性を裏付ける具体的な根拠となっている
- 「AI Scientist」ではなく「AI Co-Scientist」という命名戦略は、技術的能力と社会的受容の両立を図るポジショニングであり、監査AIの展開においても『AI監査官』ではなく『AI監査補佐』的フレーミングが重要になりうる
- AlphaFoldノーベル賞受賞者をコーディングAI部門に異動させたGoogleの人事は、汎用コーディング能力がエージェント科学システムの基盤インフラとして専門科学ツールより優先度が高いという内部判断を反映している可能性がある

## 前提知識

- **LLMエージェント** → /deep_7 Karpathy発AutoResearchで一晩100実験を自動化する仕組みと実践
- **AlphaFold** → /deep_3158 人工科学者：今AIで重要な10のこと — MIT Technology Review
- **ReActエージェント** → /deep_4188 ReActエージェントが本当に必要な業務はどれか：4象限による業務AI設計の腑分け
- **recursive self-improvement** → /deep_6385 Google I/OはAI駆動科学の方向性がどう変化しているかを示した
- **汎用推論モデル** → /deep_6385 Google I/OはAI駆動科学の方向性がどう変化しているかを示した

## 関連記事

- /deep_6461 Google I/Oは科学AI分野での方向性がいかに変化しているかを示した
- /deep_6370 Google I/Oで期待されること：コーディング巻き返し、科学AI、そして業界の drama
- /deep_6733 Google I/Oで何を期待するか：コーディング巻き返しとAI科学の最前線
- /deep_6435 Google I/Oで何を期待すべきか——コーディングAIの巻き返しと科学AIの優位性
- /deep_6391 Google I/Oが示したAI駆動科学の方向性がどう変化しているかを示した

## 原文リンク

[Google I/Oが示したAI駆動科学の方向転換：専門ツールから汎用エージェントへ](https://www.technologyreview.com/2026/05/22/1137813/google-i-o-showed-how-the-path-for-ai-science-is-shifting/)
