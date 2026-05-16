---
title: "AIの現状を理解するためのデータ集：Stanford AI Index 2026の主要チャート解説"
url: "https://www.technologyreview.com/2026/04/13/1135675/want-to-understand-the-current-state-of-ai-check-out-these-charts/"
date: 2026-04-26
tags: [Stanford AI Index, LLM benchmarks, SWE-bench, DeepSeek, AI adoption, Chatbot Arena, AI規制, EU AI Act, jagged intelligence, TSMC]
category: "ai-ml"
related: [2385, 141, 1982, 2464, 2938]
memo: "[MIT Technology Review AI] Want to understand the current state of AI? Check out these charts."
processed_at: "2026-04-26T12:29:49.550581"
---

## 要約

Stanford大学のHuman-Centered AI研究所が発表した「2026 AI Index」の主要知見をMIT Technology Reviewがまとめた記事。以下に具体的なデータポイントを整理する。

【モデル性能と米中競争】Chatbot ArenaのランキングではAnthropicが首位、xAI・Google・OpenAIが続き、DeepSeekやAlibabaなど中国モデルとの差は僅差。2023年初頭はOpenAIが明確にリードしていたが、2025年2月にDeepSeek R1が一時米国トップモデルと同水準に達した。一方、米国は5,427のデータセンターを保有（2位の国の10倍超）、中国はAI論文数・特許数・ロボティクスでリード。

【性能向上の加速】SWE-bench Verifiedにおけるトップスコアは2024年の約60%から2025年にはほぼ100%へ上昇。PhD水準の科学・数学・言語理解テストでは人間専門家と同等以上の結果も。2025年にはAIシステムが独自に天気予報を生成。ただし家庭内タスクではロボットの成功率はわずか12%にとどまり、「jagged intelligence（凸凹な知性）」という特性が顕著。

【ベンチマークの機能不全】数学能力テストの一つは設問の42%に誤りがあると指摘。モデルがベンチマークデータで訓練された場合、スコアは上がっても実際の能力向上にはならないリーク問題が存在。AIエージェントやロボット向けの体系的ベンチマークはほとんど未整備。

【普及と雇用への影響】AIは3年でグローバル人口の半数以上が使用し、PCやインターネットより速い普及速度。企業の88%、大学生の80%が利用。22〜25歳のソフトウェア開発者の雇用は2022年比で約20%減少（Stanford経済学者の2025年調査）。McKinseyの調査では組織の3分の1が今後1年以内にAIにより従業員数が減少すると回答。カスタマーサービスで14%、ソフトウェア開発で26%の生産性向上効果が確認。

【エネルギーと供給チェーンリスク】世界のAIデータセンターの総消費電力は29.6GW（ニューヨーク州のピーク需要に相当）。GPT-4o単体の年間水使用量は120万人分の飲料水需要を超える可能性。AIチップのほぼ全量をTSMC（台湾）が製造しており、地政学的脆弱性が高い。

【規制の遅れ】EU AI Actの予測的ポリシングおよび感情認識へのAI利用禁止が発効。日本・韓国・イタリアが国内AI法を制定。米国では連邦政府のAI規制を信頼しない市民が最も多く、規制が不十分になることへの懸念が過剰規制への懸念を上回る。

監査エージェント開発への示唆：SWE-benchの飽和が示すように、専門業務向けベンチマークの設計が急務。AIエージェントの評価基準未整備は監査AI領域でも同様であり、独自評価フレームワークの構築が差別化要因になりうる。

## アイデア

- SWE-bench Verifiedのスコアが1年でほぼ満点に達したことは、既存ベンチマークの天井問題を端的に示しており、監査・法律・財務など判断力を要するドメイン向けの新世代ベンチマーク設計が急務であることを示唆する
- 米中AIモデルの性能差が僅差になる中、競争軸がスコアからコスト・信頼性・実用性にシフトしており、エンタープライズ向けエージェント選定の評価基準を再設計する必要がある
- 29.6GWの電力消費とTSMCへのチップ製造集中という2つのリスクは、AI基盤インフラの脆弱性を示しており、ローカルLLMインフラの戦略的価値（エネルギー分散・サプライチェーンリスク回避）を裏付ける

## 前提知識

- **LLM benchmark** (TODO: 読むべき)
- **SWE-bench** → /deep_62 LLMチャットボットに欠けているもの：目的意識（Purposeful Dialogue）
- **Chatbot Arena** → /deep_2014 AIの現状を理解するためのチャート集：Stanford AI Index 2026レポート解説
- **EU AI Act** → /deep_11 MCPが9,700万DL、フロンティアモデル3連発 — AI業界週報 2026年第13週
- **AI Index** → /deep_1983 AIの現状を理解するためのデータ：Stanford AI Index 2026の主要チャート解説

## 関連記事

- /deep_2385 なぜAIへの評価はこれほど分かれるのか
- /deep_141 Hugging Faceにおけるオープンソースの現状：2026年春
- /deep_1982 AI評価がこれほど二極化する理由：専門家と一般公衆の間の50ポイントギャップ
- /deep_2464 AIへの評価がこれほど二分される理由：専門家と一般市民の50ポイントもの認識差
- /deep_2938 AIへの見方がなぜこれほど分断されているのか

## 原文リンク

[AIの現状を理解するためのデータ集：Stanford AI Index 2026の主要チャート解説](https://www.technologyreview.com/2026/04/13/1135675/want-to-understand-the-current-state-of-ai-check-out-these-charts/)
