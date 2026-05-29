---
title: "Google I/OはAI駆動科学の方向性がどう変化しているかを示した"
url: "https://www.technologyreview.com/2026/05/22/1137813/google-i-o-showed-how-the-path-for-ai-science-is-shifting/"
date: 2026-05-29
tags: [Gemini for Science, AI Co-Scientist, AlphaEvolve, AlphaFold, WeatherNext, agentic AI, 自律科学エージェント, recursive self-improvement]
category: "agent-arch"
related: [6370, 6733, 6435, 6825, 6140]
memo: "[MIT Technology Review AI] Google I/O showed how the path for AI-driven science is shifting"
processed_at: "2026-05-29T21:07:57.189734"
---

## 要約

2026年5月のGoogle I/Oで、Google DeepMind CEOのDemis Hassabisは「シンギュラリティの山麓に立っている」と宣言した。この文脈で発表されたのが、ハリケーン「Melissa」のジャマイカ上陸を事前予測し避難に貢献した気象予測AIシステム「WeatherNext」だ。この発表は、科学AIの2つのアプローチ間の緊張を浮き彫りにした。①特定の科学問題に特化して設計・訓練されたツール型AI（WeatherNext、AlphaFoldなど）と、②人間の関与なしに最先端研究を自律実行できる汎用エージェント型LLMシステムである。

Googleは専門特化型ツールを完全に放棄したわけではない。AlphaFoldは世界300万人以上の研究者に利用されており、Isomorphic Labsは20億ドルのシリーズBを調達。AlphaGenome（ゲノム）やAlphaEarth Foundations（地球科学）も昨年リリースされた。しかし重要なシフトの兆候も見られる。AlphaFoldでノーベル賞を受賞したGoogleフェローのJohn Jumperが、科学特化AIではなくAIコーディング分野に移行していることが報じられた。

今回の目玉発表は「Gemini for Science」パッケージで、仮説生成AI「Co-Scientist」と、アルゴリズム最適化エージェント「AlphaEvolve」を統合。現在は一般公開されていないが、研究者向けアクセス申請を受け付け開始した。スタンフォードの遺伝学者Gary Peltzは、AI Co-Scientistの使用体験を「デルフォイの神託に相談するようだ」と『Nature Medicine』誌で表現している。

同週、OpenAIは汎用推論モデル（GPT-5.5系）が重要な数学的予想を反証したと発表。これは数学者らが「生成AIの数学への最も意義深い貢献」と評価するものだ。このモデルは数学特化ではなく汎用型であり、特化ツールなしに研究貢献できる汎用エージェントの可能性を示す。

GoogleはAI Co-Scientistを「AI Scientist」ではなく「Co-Scientist（共同研究者）」と命名することで、人間中心の位置づけを維持。Hassabisは「今後10年はAIを科学者を助く優れたツールとして考えるべき。その先は協力者になりうる」と述べる。しかしHassabisが語るシンギュラリティの山麓論が正しければ、AIが人間の研究者を凌駕する可能性も視野に入る。コーディング能力強化への投資はエージェント科学の基盤でもあり、Googleは長期的に自律エージェント科学者という頂点を目指していると解釈できる。

## アイデア

- 専門特化型AIツール（AlphaFold型）から汎用エージェント型AI（Co-Scientist型）への重心移動は、監査エージェント設計でも同様のトレードオフ（特化モデルvs汎用推論モデル＋ツール呼び出し）として現れる
- AlphaEvolveのようにエージェントがアルゴリズム自体を最適化する構造は、監査エージェントのルールエンジンや判定ロジックを自己改善させるアーキテクチャ研究と直結する
- OpenAIの汎用推論モデルが数学的予想を反証した事例は、ドメイン特化なしに推論能力だけで専門的貢献が可能になる閾値の存在を示唆しており、LLM-as-judgeの信頼性評価に新たな視点を与える

## 前提知識

- **LLMエージェント** → /deep_7 Karpathy発AutoResearchで一晩100実験を自動化する仕組みと実践
- **AlphaFold** → /deep_3158 人工科学者：今AIで重要な10のこと — MIT Technology Review
- **recursive self-improvement** → /deep_6385 Google I/OはAI駆動科学の方向性がどう変化しているかを示した
- **ReAct / reasoning model** (TODO: 読むべき)
- **ツール呼び出し（Function Calling）** → /deep_47 LLM SDKを基礎から理解する 第4回：ツール呼び出し（Function Calling）編

## 関連記事

- /deep_6370 Google I/Oで期待されること：コーディング巻き返し、科学AI、そして業界の drama
- /deep_6733 Google I/Oで何を期待するか：コーディング巻き返しとAI科学の最前線
- /deep_6435 Google I/Oで何を期待すべきか——コーディングAIの巻き返しと科学AIの優位性
- /deep_6825 Google I/Oが示したAI駆動科学の方向性シフト——専用ツールから汎用エージェントへ
- /deep_6140 Google I/O 2026のAI発表を読むエンジニア・研究視点

## 原文リンク

[Google I/OはAI駆動科学の方向性がどう変化しているかを示した](https://www.technologyreview.com/2026/05/22/1137813/google-i-o-showed-how-the-path-for-ai-science-is-shifting/)
