---
title: "Google I/Oが示すAI駆動科学の転換点：専用ツールから汎用エージェントへ"
url: "https://www.technologyreview.com/2026/05/22/1137813/google-i-o-showed-how-the-path-for-ai-science-is-shifting/"
date: 2026-05-27
tags: [Gemini for Science, AlphaFold, AI Co-Scientist, AlphaEvolve, WeatherNext, 自律エージェント, 科学AI, 再帰的自己改善, Google DeepMind, 汎用推論モデル]
category: "agent-arch"
related: [6461, 6370, 6710, 6585, 3430]
memo: "[MIT Technology Review AI] Google I/O showed how the path for AI-driven science is shifting"
processed_at: "2026-05-27T21:08:33.873807"
---

## 要約

Google I/OでDeepMind CEOのDemis Hassabisは「シンギュラリティの山麓に立っている」と発言した。この発言の文脈は科学AI分野における二つのアプローチの対立を象徴している。一つ目は、WeatherNextやAlphaFoldのような特定問題に特化した専用AIツール。WeatherNextはジャマイカに上陸したハリケーン・メリッサの事前警告を提供し、AlphaFoldは世界300万人以上の研究者に利用されているタンパク質構造予測ツールで、DeepMind科学者にノーベル賞をもたらした。二つ目は、汎用LLMベースの自律エージェントシステムで、人間の関与なしに先端研究を実行することを目指す方向性。Googleは後者への軸足移動を示す具体的なシグナルを出している。AlphaFoldでノーベル賞を受賞したGoogle FellowのJohn JumperがAIコーディングの開発に移行したことは、その象徴的な動きとして報じられている（Los Angeles Times）。科学エージェント向けにコーディング能力が重要であることも、この人員配置の背景にある。新たに発表された「Gemini for Science」パッケージは、仮説生成AIであるCo-Scientistとアルゴリズム最適化ツールAlphaEvolveをGeminiブランドの下に統合したもので、現在は研究者によるアクセス申請を受け付けている。Stanford大学の遺伝学者Gary Peltzは、AI Co-Scientistを「デルフォイの神託に相談するようだ」とNature Medicine誌で表現した。同週、OpenAIのモデルが数学の重要な予想を反証したことも話題となり、これは汎用推論モデル（GPT-5.5系）によるもので、数学専用モデルではなかった点が重要。また、Google CloudのチーフサイエンティストPushmeet Kohliは「科学を支援するAIから、科学を行うAIへの移行」とDaedalus誌に寄稿している。一方でAlphaFoldは依然として現役であり、関連技術でドラッグデザインを行うIsomorphic Labsは20億ドルのシリーズB資金調達を完了したばかり。Gemini for Scienceは専用ツールを排除するものではなく、エージェントが必要に応じてAlphaFoldのような専用ツールを呼び出す設計が可能。監査エージェント開発への示唆としては、専用ツール（特定の監査チェックリストや規制判定モデル）と汎用エージェント（LangGraphベースのReActエージェント等）を組み合わせる「ハイブリッドアーキテクチャ」が実用的かつ将来性のある設計方針であることが確認される。また、「AI Co-Scientist」という命名に見られるように、エージェントをアシスタントとして位置づける設計思想は、人間監督を前提とする内部監査AI設計とも整合する。

## アイデア

- AlphaFoldのノーベル賞受賞者が科学AIからコーディングAIに移行した事実は、汎用エージェントの基盤能力としてコード生成が最重要視されていることを示す。監査エージェントでも自然言語→コード生成パイプラインが中核になりうる
- OpenAIの汎用推論モデルが数学の予想を反証した事例は、「専門特化訓練なしの汎用エージェントが高度な推論タスクを解ける」という証拠であり、ReActパターンの監査エージェントが専用学習なしで複雑な規制判断を行える可能性を示唆する
- Gemini for Scienceの設計（エージェントが必要時に専用ツールを呼び出す）は、LangGraphのToolノードパターンと直接対応しており、監査エージェントがAlphaFold相当の専用モデル（例：会計基準判定モデル）をツールとして呼び出すアーキテクチャの妥当性を裏付ける

## 前提知識

- **LLMエージェント / ReAct** (TODO: 読むべき)
- **AlphaFold** → /deep_3158 人工科学者：今AIで重要な10のこと — MIT Technology Review
- **再帰的自己改善 (RSI)** (TODO: 読むべき)
- **Gemini** → /deep_2 AIエージェント自作のための基礎知識 - Google ADK (Go) を使ったエージェント構築
- **ツール呼び出し (Function Calling)** (TODO: 読むべき)

## 関連記事

- /deep_6461 Google I/Oは科学AI分野での方向性がいかに変化しているかを示した
- /deep_6370 Google I/Oで期待されること：コーディング巻き返し、科学AI、そして業界の drama
- /deep_6710 Google I/O 2026で期待されること：コーディングAIの巻き返しと科学AI分野の動向
- /deep_6585 Google I/O 2026で何が期待されるか：コーディング巻き返し、科学AI、そして業界の争乱
- /deep_3430 人工科学者：AIが科学研究を自律的に実行する時代の到来

## 原文リンク

[Google I/Oが示すAI駆動科学の転換点：専用ツールから汎用エージェントへ](https://www.technologyreview.com/2026/05/22/1137813/google-i-o-showed-how-the-path-for-ai-science-is-shifting/)
