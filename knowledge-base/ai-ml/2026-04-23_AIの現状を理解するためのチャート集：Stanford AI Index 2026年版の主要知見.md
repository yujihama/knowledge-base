---
title: "AIの現状を理解するためのチャート集：Stanford AI Index 2026年版の主要知見"
url: "https://www.technologyreview.com/2026/04/13/1135675/want-to-understand-the-current-state-of-ai-check-out-these-charts/"
date: 2026-04-23
tags: [Stanford AI Index, LLM評価, SWE-bench, DeepSeek, Chatbot Arena, AI労働市場, ベンチマーク, 米中AI競争, jagged intelligence, AI規制]
category: "ai-ml"
related: [1907, 2002, 1068, 899, 2067]
memo: "[MIT Technology Review AI] Want to understand the current state of AI? Check out these charts."
processed_at: "2026-04-23T12:01:16.956172"
---

## 要約

Stanford大学のHuman-Centered AI研究所が発表した「AI Index 2026」の主要データをMIT Technology Reviewが整理した記事。以下の6つの観点から現状を定量的に示している。

【米中AI競争】Chatbot Arenaのランキングでは、2023年初頭はOpenAIが先行していたが、2024年にGoogleとAnthropicが追随。2025年2月にはDeepSeekのR1モデルがChatGPTと同水準に達し、2026年3月時点ではAnthropicが首位、xAI・Google・OpenAIが続く。DeepSeekとAlibaba（Qwen系）はわずかに遅れる程度。米国はデータセンター数5,427か所（2位の10倍超）と資本力で優位だが、中国はAI論文・特許数・ロボティクスでリード。一方でOpenAI・Anthropic・Googleはモデルの学習コード・パラメータ数・データセットサイズを非公開化しており、独立研究者による安全性検証が困難になっている。

【モデル性能の向上】SWE-bench Verifiedのスコアは2024年の約60%から2025年にほぼ100%へ急上昇。PhD水準の科学・数学・言語理解テストで人間専門家と同等以上の性能を示す領域も存在する。一方で家庭内タスクにおけるロボットの成功率は12%にとどまり、「凸凹な知能（jagged intelligence）」が顕著。

【ベンチマークの機能不全】数学能力を測る主要ベンチマークの誤答率が42%に上るなど設計の粗さが指摘される。モデルがベンチマークデータで学習（汚染）することでスコアのみ向上する問題、および実世界タスクとの乖離も深刻。責任あるAIベンチマークの結果を公開しない企業が増加している。

【労働市場への影響】AI普及率は個人で世界人口の50%超、組織では88%に達し、大学生の80%が利用。普及スピードはPCやインターネットを上回る。Stanford経済学者の2025年研究では、22〜25歳のソフトウェア開発者の雇用が2022年比で約20%減少。McKinsey調査ではAIが来年中に自社人員を削減すると回答した組織が1/3。カスタマーサービスで14%、ソフトウェア開発で26%の生産性向上効果が示されている。

【社会的受容と不安】Ipsos調査では59%が「メリットが上回る」と回答する一方、52%が「不安を感じる」と回答。Pew調査では専門家の73%がAIの仕事への影響を肯定的に評価するのに対し、米国一般市民では23%にとどまり、認識の乖離が顕著。

【エネルギー・インフラリスク】世界のAIデータセンターの総消費電力は29.6GW（ニューヨーク州のピーク需要に相当）。GPT-4oの年間水使用量は単体で120万人分の飲料水需要を超える可能性。チップ製造はTSMC（台湾）に過度に集中しており、サプライチェーンの脆弱性が地政学リスクとなっている。監査エージェント開発への示唆として、ベンチマークの信頼性低下とモデルの不透明化は、LLM-as-judgeや自動評価パイプライン設計において独立した評価基準の構築が不可欠であることを示す。

## アイデア

- SWE-benchスコアが1年で60%→100%近くに急上昇した事実は、コーディングエージェントの実用化フェーズへの移行を示す強力な定量的根拠となる
- 責任あるAIベンチマークを公開しない企業が増加しているという指摘は、LLM-as-judgeを監査システムに組み込む際に第三者評価と独立検証の設計が必須であることを強調する
- 米国の専門家と一般市民のAI認識ギャップ（仕事への肯定的評価：73% vs 23%）は、AI導入プロジェクトにおいてステークホルダーコミュニケーション設計が技術実装と同等に重要であることを示す

## 前提知識

- **Chatbot Arena** → /deep_2014 AIの現状を理解するためのチャート集：Stanford AI Index 2026レポート解説
- **SWE-bench** → /deep_62 LLMチャットボットに欠けているもの：目的意識（Purposeful Dialogue）
- **LLM benchmark** (TODO: 読むべき)
- **TSMC供給リスク** (TODO: 読むべき)
- **jagged intelligence** → /deep_1983 AIの現状を理解するためのデータ：Stanford AI Index 2026の主要チャート解説

## 関連記事

- /deep_1907 SWE-Bench解説：コーディングエージェント評価ベンチマークの仕組みと現状
- /deep_2002 行動を超えて：AIの評価が認知革命を必要とする理由
- /deep_1068 構造化生成によるプロンプト一貫性の改善
- /deep_899 大規模言語モデルのディベート評価：初の多言語LLMディベートコンペティション（FlagEval Debate）
- /deep_2067 医薬分野のQ&AでローカルLLMを評価する④：Gemma-4-E2B・LLM-JP-4-8B-Thinking・JPharmatron-7Bの比較

## 原文リンク

[AIの現状を理解するためのチャート集：Stanford AI Index 2026年版の主要知見](https://www.technologyreview.com/2026/04/13/1135675/want-to-understand-the-current-state-of-ai-check-out-these-charts/)
