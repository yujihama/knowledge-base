---
title: "Google I/OはAI駆動科学の方向性がどう変わりつつあるかを示した"
url: "https://www.technologyreview.com/2026/05/22/1137813/google-i-o-showed-how-the-path-for-ai-science-is-shifting/"
date: 2026-06-07
tags: [Gemini for Science, AI Co-Scientist, AlphaEvolve, AlphaFold, WeatherNext, 自律エージェント, 科学AI, recursive self-improvement, 汎用推論モデル]
category: "agent-arch"
related: [6461, 6370, 6710, 6585, 3430]
memo: "[MIT Technology Review AI] Google I/O showed how the path for AI-driven science is shifting"
processed_at: "2026-06-07T09:22:03.664607"
---

## 要約

Google I/OにてDeepMind CEO Demis Hassabisは「シンギュラリティの山麓に立っている」と発言した。その文脈は科学AIセッションであり、WeatherNextによるハリケーン・メリッサの早期警報提供という具体的な成果が紹介された。この発言は、科学AIの二つのアプローチ間の緊張を浮き彫りにしている。一つは特定問題解決に特化したツール型AI（AlphaFold、WeatherNext等）、もう一つはLLMベースの自律エージェントが研究全体を実行するアプローチだ。Googleは後者へのシフトを示す具体的なシグナルを出している。ノーベル賞受賞者のJohn JumperがAlphaFold関連研究からAIコーディング担当に異動したことや、仮説生成AIである「AI Co-Scientist」と最適化アルゴリズムを進化させる「AlphaEvolve」を含む「Gemini for Science」パッケージの発表がその証拠だ。Gemini for Scienceはまだ一般公開されていないが、研究者向けアクセス申請の受付が開始された。スタンフォード大の遺伝学者Gary Peltzは、AI Co-Scientistの利用体験を「デルポイの神託に相談するようだ」とNature Medicine誌で述べている。一方で特化型ツールも依然として強力であり、AlphaFoldのタンパク質構造予測は世界300万人以上の研究者に利用され、関連技術を活用するIsomorphic Labsは20億ドルのシリーズB資金調達を完了した。OpenAIも今週、汎用推論モデルが重要な数学的予想を反証したと発表しており、特化型でない汎用エージェントが独立した研究貢献を行える可能性を示した。Googleはエージェントを「人間科学者の代替」ではなく「加速装置」と位置付けており、「AI Scientist」でなく「AI Co-Scientist」という命名にその意図が表れている。ただし監査エージェント開発の観点では、汎用推論モデルが専門知識不要で研究貢献できるという実績は重要な示唆を持つ。監査領域でも特化型ルールエンジンよりもLLMエージェントが「Co-Auditor」として機能する設計が有効になりうることを示唆している。

## アイデア

- 汎用推論モデル（GPT-5.5相当）が数学的予想を反証したという事実は、特化型モデルなしに科学的貢献が可能になりつつあることを示しており、ドメイン特化AIの存在意義を問い直す転換点になりうる
- 「AI Co-Scientist」という命名は意図的であり、自律AIへの移行期において人間との協調フレーミングが社会受容と規制対応の戦略として機能している点が興味深い
- AlphaFold開発者Jumperのコーディング部門異動は、科学的専門性よりもコーディング能力がエージェント型科学AIの基盤として重視されていることを示しており、エージェントアーキテクチャにおけるコード生成の中心性を裏付ける

## 前提知識

- **LLMエージェント** → /deep_7 Karpathy発AutoResearchで一晩100実験を自動化する仕組みと実践
- **AlphaFold** → /deep_3158 人工科学者：今AIで重要な10のこと — MIT Technology Review
- **recursive self-improvement** → /deep_6385 Google I/OはAI駆動科学の方向性がどう変化しているかを示した
- **汎用推論モデル** → /deep_6385 Google I/OはAI駆動科学の方向性がどう変化しているかを示した
- **マルチエージェントシステム** → /deep_628 Mimosaフレームワーク：科学研究向け進化型マルチエージェントシステム

## 関連記事

- /deep_6461 Google I/Oは科学AI分野での方向性がいかに変化しているかを示した
- /deep_6370 Google I/Oで期待されること：コーディング巻き返し、科学AI、そして業界の drama
- /deep_6710 Google I/O 2026で期待されること：コーディングAIの巻き返しと科学AI分野の動向
- /deep_6585 Google I/O 2026で何が期待されるか：コーディング巻き返し、科学AI、そして業界の争乱
- /deep_3430 人工科学者：AIが科学研究を自律的に実行する時代の到来

## 原文リンク

[Google I/OはAI駆動科学の方向性がどう変わりつつあるかを示した](https://www.technologyreview.com/2026/05/22/1137813/google-i-o-showed-how-the-path-for-ai-science-is-shifting/)
