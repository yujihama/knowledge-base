---
title: "Google I/Oが示すAI科学研究の転換：専門特化ツールからエージェント型汎用AIへ"
url: "https://www.technologyreview.com/2026/05/22/1137813/google-i-o-showed-how-the-path-for-ai-science-is-shifting/"
date: 2026-06-03
tags: [Gemini for Science, AlphaFold, AI Co-Scientist, AlphaEvolve, WeatherNext, エージェント型科学AI, 汎用推論モデル, 自律研究エージェント]
category: "agent-arch"
related: [3158, 6461, 6370, 6733, 6435]
memo: "[MIT Technology Review AI] Google I/O showed how the path for AI-driven science is shifting"
processed_at: "2026-06-03T09:18:43.247519"
---

## 要約

Google I/O 2026のキーノートでDeepMind CEOのDemis Hassabisは「シンギュラリティの山麓に立っている」と発言した。その文脈は科学AI領域における二つのアプローチの対比だった。一つは天気予報システムWeatherNextやタンパク質構造予測のAlphaFoldのような、特定科学問題に特化した訓練済みツール。もう一つはLLMベースの汎用エージェントシステムで、人間の関与を最小限に研究プロジェクトを自律実行できる可能性を持つ。

AlphaFoldは世界300万人以上の研究者に利用され、DeepMindの科学者にノーベル賞をもたらした。関連技術を用いた新薬開発子会社Isomorphic Labsは20億ドルのシリーズB調達に成功するなど、特化型ツールの実績と需要は依然として高い。AlphaGenome（遺伝学）、AlphaEarth Foundations（地球科学）は2025年夏にリリースされ、WeatherNextの最新版は同年11月に公開された。

一方でリソースと関心の重心は移動しつつある。AlphaFoldでノーベル賞を受賞したGoogleフェローのJohn JumperがAIコーディング部門に異動した事実は象徴的だ。AnthropicやOpenAIにコーディングツールで後れを取るという問題への対応でもあるが、コーディング能力がエージェント型科学AIの中核能力である点も重要である。

GoogleはGoogle I/Oで「Gemini for Science」パッケージを発表。仮説生成AI「Co-Scientist」と、アルゴリズム最適化に特化した「AlphaEvolve」をGeminiベースの科学システム群として統合した。Co-ScientistはスタンフォードのGary Peltz教授がNature Medicine誌上で「デルフォイの神託への相談」と評するほどの評価を得ている。両ツールは未だ一般公開されていないが、研究者向けアクセス申請を受け付け中だ。

同週、OpenAIは汎用推論モデル（GPT-5.5系）が数学の重要な予想を反証したと発表。数学者の間では生成AIが数学に与えた最も意義深な貢献との評価もある。これは科学特化モデルでなく汎用モデルによる成果であり、エージェント型システムの可能性を裏付ける。

Googleは「AI Co-Scientist（AIサイエンティストではなく）」という命名に示されるように、人間科学者の加速装置としてのポジショニングを維持している。Hassabisも「今後10年はAIを科学者を助ける驚異的なツールとして考えるべき。その先は協力者になるかもしれない」と慎重な表現をとる。しかし実質的な人員とリソースの移動は、汎用エージェント型科学AIへの傾注を示している。監査エージェント開発への示唆として、特化型ツール（例：会計基準照合エンジン）と汎用推論エージェントの役割分担設計は、Googleの戦略転換と同じ構造的課題を抱えており、AlphaEvolve的なアルゴリズム最適化アプローチがReActエージェントの行動空間設計に応用できる可能性がある。

## アイデア

- 汎用推論モデル（GPT-5.5系）が科学特化モデルなしに数学予想を反証した事実は、特化型アーキテクチャの優位性が縮小しつつあることを示す。監査AIも特化ファインチューニングより汎用エージェント＋ツール呼び出しの設計が将来性を持つ可能性がある
- AlphaEvolveはアルゴリズム自体を進化・最適化するシステムであり、これをReActエージェントの行動選択ロジックや監査手続きの最適化に応用できるアーキテクチャパターンとして注目に値する
- Gemini for Scienceの設計思想（特化ツール群を汎用エージェントがオーケストレーション）は、監査エージェントにおいてAlphaFold相当の特化モジュール（例：不正検出モデル、法令照合エンジン）を汎用LLMエージェントが呼び出す構成の参照アーキテクチャとなりうる

## 前提知識

- **LLMエージェント（ReAct）** (TODO: 読むべき)
- **AlphaFold** → /deep_3158 人工科学者：今AIで重要な10のこと — MIT Technology Review
- **再帰的自己改善（RSI）** (TODO: 読むべき)
- **ツール呼び出し型エージェント** (TODO: 読むべき)
- **汎用推論モデル** → /deep_6385 Google I/OはAI駆動科学の方向性がどう変化しているかを示した

## 関連記事

- /deep_3158 人工科学者：今AIで重要な10のこと — MIT Technology Review
- /deep_6461 Google I/Oは科学AI分野での方向性がいかに変化しているかを示した
- /deep_6370 Google I/Oで期待されること：コーディング巻き返し、科学AI、そして業界の drama
- /deep_6733 Google I/Oで何を期待するか：コーディング巻き返しとAI科学の最前線
- /deep_6435 Google I/Oで何を期待すべきか——コーディングAIの巻き返しと科学AIの優位性

## 原文リンク

[Google I/Oが示すAI科学研究の転換：専門特化ツールからエージェント型汎用AIへ](https://www.technologyreview.com/2026/05/22/1137813/google-i-o-showed-how-the-path-for-ai-science-is-shifting/)
