---
title: "Google I/Oが示したAI駆動科学の方向転換：専用ツールから汎用エージェントへ"
url: "https://www.technologyreview.com/2026/05/22/1137813/google-i-o-showed-how-the-path-for-ai-science-is-shifting/"
date: 2026-05-24
tags: [Gemini for Science, AI Co-Scientist, AlphaEvolve, AlphaFold, WeatherNext, 自律科学エージェント, 汎用推論モデル, recursive self-improvement]
category: "agent-arch"
related: [6370, 6391, 6140, 6170, 6049]
memo: "[MIT Technology Review AI] Google I/O showed how the path for AI-driven science is shifting"
processed_at: "2026-05-24T09:13:18.165477"
---

## 要約

2026年5月のGoogle I/Oにおいて、Google DeepMind CEOのDemis Hassabisは「シンギュラリティの麓に立っている」と宣言した。この発言の文脈は、同社の気象予測AI「WeatherNext」がハリケーン・メリッサのジャマイカ上陸前に警告を発し、人命救助に貢献したという実績紹介の場だった。この対比が、現在のAI科学における2つのアプローチの緊張を浮き彫りにする。第一は、AlphaFoldやWeatherNextのような特定科学問題に特化した専用ツール。第二は、LLMベースの汎用エージェントシステムが自律的に研究を遂行するビジョンである。

Googleは後者への傾注を鮮明にしている。I/Oの主要科学発表は「Gemini for Science」パッケージで、仮説生成AI「Co-Scientist」とアルゴリズム最適化AI「AlphaEvolve」を統合。これらは現時点で一般公開されていないが、研究者向けアクセス申請を受付中。早期テストに参加したStanford遺伝学者Gary Peltzは「デルフォイの神託に相談するようだ」とNature Medicine誌で評した。

人材配置にも変化が見られる。AlphaFoldでノーベル賞を受賞したGoogle FellowのJohn JumperがAIコーディング部門に異動したことが報じられた。これはGoogleのコーディングツールがAnthropicやOpenAIに後れを取るという課題への対応と同時に、コーディング能力が科学エージェントの中核要素であることを反映している。

同週、OpenAIは汎用推論モデル（GPT-5.5系統）が数学の重要な予想を反証したと発表。これはGenerative AIが数学に対して行った最も意義深い貢献とされ、専門特化なしの汎用エージェントが独立した研究貢献を行える可能性を示した。

一方、AlphaFoldは世界300万人以上の研究者が利用し、Google子会社Isomorphic Labsは20億ドルのシリーズB調達を完了するなど、専用ツールの需要は依然高い。Gemini for Scienceも専用ツールを排除するのではなく、エージェントが必要に応じてAlphaFold等を呼び出す設計だ。

Hassabisは「今後10年はAIを科学者を支援するツールと捉えるべき。その先はAIがコラボレーターになりうる」と述べ、「AI Co-Scientist（AI科学者ではなく）」という命名も人間中心性を意識したものだと示唆。ただし、有効な科学的協力者となるには独立した科学的能力が必要であり、エージェントの自律性向上は避けられない方向性として浮かび上がる。

監査エージェント開発への示唆：科学的仮説生成エージェント（Co-Scientist）のアーキテクチャは、監査における仮説駆動型リスク評価（どの勘定科目に不正リスクがあるか）に直接応用可能。汎用推論モデルが専門ドメインで成果を上げた事例は、監査特化モデル開発より汎用LLM＋RAGの組み合わせが有効である可能性を支持する。

## アイデア

- 汎用推論モデル（GPT-5.5系）が数学予想を反証した事例は、ドメイン特化なしの汎用エージェントが専門研究に貢献できることを示し、専用ツール開発の投資対効果を根本から問い直す
- 「Co-Scientist（共同研究者）」vs「Scientist（科学者）」という命名の差異が、AIの自律性に関する社会的受容の設計戦略を反映している点は、監査AIの役割定義にも応用できる
- ノーベル賞受賞者JumperのAIコーディング部門への異動は、コーディング能力が科学エージェントの中核インフラである事実を示す——科学的推論とコード実行の統合が次世代エージェントの鍵

## 前提知識

- **LLMエージェント** → /deep_7 Karpathy発AutoResearchで一晩100実験を自動化する仕組みと実践
- **AlphaFold** → /deep_3158 人工科学者：今AIで重要な10のこと — MIT Technology Review
- **recursive self-improvement** → /deep_6385 Google I/OはAI駆動科学の方向性がどう変化しているかを示した
- **RAG** → /deep_5 Google Research at The Check Up: ヘルスケアAIの最新研究成果と実臨床への展開（2026年）
- **マルチエージェントシステム** → /deep_628 Mimosaフレームワーク：科学研究向け進化型マルチエージェントシステム

## 関連記事

- /deep_6370 Google I/Oで期待されること：コーディング巻き返し、科学AI、そして業界の drama
- /deep_6391 Google I/Oが示したAI駆動科学の方向性がどう変化しているかを示した
- /deep_6140 Google I/O 2026のAI発表を読むエンジニア・研究視点
- /deep_6170 Google I/O 2026に向けた期待：コーディングAIの挽回、科学AI、業界ドラマ
- /deep_6049 Google I/O 2026で注目すべき3つのポイント：コーディングAIの巻き返しと科学AI

## 原文リンク

[Google I/Oが示したAI駆動科学の方向転換：専用ツールから汎用エージェントへ](https://www.technologyreview.com/2026/05/22/1137813/google-i-o-showed-how-the-path-for-ai-science-is-shifting/)
