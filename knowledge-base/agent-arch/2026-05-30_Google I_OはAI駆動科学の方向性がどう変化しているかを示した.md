---
title: "Google I/OはAI駆動科学の方向性がどう変化しているかを示した"
url: "https://www.technologyreview.com/2026/05/22/1137813/google-i-o-showed-how-the-path-for-ai-science-is-shifting/"
date: 2026-05-30
tags: [Gemini for Science, AI Co-Scientist, AlphaEvolve, AlphaFold, WeatherNext, recursive self-improvement, agentic AI, 科学AI, Google DeepMind]
category: "agent-arch"
related: [6370, 6710, 6585, 3430, 6733]
memo: "[MIT Technology Review AI] Google I/O showed how the path for AI-driven science is shifting"
processed_at: "2026-05-30T21:16:44.929283"
---

## 要約

2026年5月のGoogle I/Oにて、Google DeepMind CEOのDemis Hassabisは「特化型AIツール」から「汎用エージェント型AI科学者」へのシフトを示唆した。キーノートでは気象予測ソフトウェア「WeatherNext」が昨年のハリケーン・メリッサ上陸前にジャマイカへ早期警報を提供し人命を救った事例が紹介されたが、Hassabisはこれを「シンギュラリティの麓に立っている」という文脈で語った。この対比が2つのアプローチ間の緊張を象徴している。第一のアプローチはAlphaFold（タンパク質構造予測でノーベル賞）、WeatherNext、AlphaGenome、AlphaEarth Foundationsのような特定問題に特化したAIツール群。AlphaFoldは世界300万人超の研究者に利用され、関連子会社Isomorphic Labsは20億ドルのシリーズBを調達した。第二のアプローチはLLMベースの汎用エージェントが自律的に研究を遂行するモデルで、GoogleはAI Co-Scientist（仮説生成）やAlphaEvolve（アルゴリズム最適化）を含む「Gemini for Science」パッケージとして統合し、研究者向けにアクセス申請を開放した。リソース配分にも変化の兆しがあり、AlphaFoldでノーベル賞を受賞したGoogle FellowのJohn JumperがAIコーディング部門へ異動したことが報じられた。背景には、AnthropicやOpenAIに対するコーディングツールの競争力低下がある。同週にはOpenAIの汎用推論モデル（GPT-5.5系）が数学の重要な予想を反証し、専門特化なしで研究貢献できる可能性を示した。Google Cloud主席科学者Pushmeet Kohliは「AIが科学を促進するだけでなく、科学を行う方向へ移行している」と表明。Hassabisは今後10年はAIを「科学者を助けるツール」、その先は「協働者」と位置づけ、「AI Scientist」ではなく「AI Co-Scientist」という命名も意図的な人間中心フレーミングとされる。再帰的自己改善（recursive self-improvement）によりAIが自身の進化を加速させる将来シナリオも念頭に置かれており、監査エージェント開発においても、特化型ツールと汎用推論エージェントのどちらに投資するかという同様の設計判断が問われる。

## アイデア

- 汎用推論モデル（GPT-5.5系）が専門特化なしで数学の予想を反証した事実は、特化型ツール vs 汎用エージェントの設計論争に直接的な実証データを提供している
- 「AI Co-Scientist」という命名戦略：Scientistではなく Co-Scientist とすることで人間の代替ではなく協働者として位置づけ、研究コミュニティの受容障壁を下げる意図が読み取れる
- 監査エージェント開発への示唆：AlphaFoldのような特化型ツールとLLMエージェントの組み合わせアーキテクチャ（エージェントが必要時に特化ツールを呼び出す）は、監査領域でのReActエージェント設計でも有効なパターン

## 前提知識

- **LLMエージェント** → /deep_7 Karpathy発AutoResearchで一晩100実験を自動化する仕組みと実践
- **recursive self-improvement** → /deep_6385 Google I/OはAI駆動科学の方向性がどう変化しているかを示した
- **AlphaFold** → /deep_3158 人工科学者：今AIで重要な10のこと — MIT Technology Review
- **ReAct** → /deep_1 Agent SkillにReactアプリを同梱するSkill Appアーキテクチャの実装
- **汎用推論モデル** → /deep_6385 Google I/OはAI駆動科学の方向性がどう変化しているかを示した

## 関連記事

- /deep_6370 Google I/Oで期待されること：コーディング巻き返し、科学AI、そして業界の drama
- /deep_6710 Google I/O 2026で期待されること：コーディングAIの巻き返しと科学AI分野の動向
- /deep_6585 Google I/O 2026で何が期待されるか：コーディング巻き返し、科学AI、そして業界の争乱
- /deep_3430 人工科学者：AIが科学研究を自律的に実行する時代の到来
- /deep_6733 Google I/Oで何を期待するか：コーディング巻き返しとAI科学の最前線

## 原文リンク

[Google I/OはAI駆動科学の方向性がどう変化しているかを示した](https://www.technologyreview.com/2026/05/22/1137813/google-i-o-showed-how-the-path-for-ai-science-is-shifting/)
