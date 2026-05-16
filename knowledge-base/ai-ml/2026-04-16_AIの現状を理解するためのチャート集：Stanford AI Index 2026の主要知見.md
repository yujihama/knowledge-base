---
title: "AIの現状を理解するためのチャート集：Stanford AI Index 2026の主要知見"
url: "https://www.technologyreview.com/2026/04/13/1135675/want-to-understand-the-current-state-of-ai-check-out-these-charts/"
date: 2026-04-16
tags: [Stanford AI Index, LLMベンチマーク, SWE-bench, DeepSeek, Arena, 米中AI競争, jagged intelligence, AIガバナンス, 雇用影響, エネルギー消費]
category: "ai-ml"
related: [1516, 1335, 1895, 1227, 1788]
memo: "[MIT Technology Review AI] Want to understand the current state of AI? Check out these charts."
processed_at: "2026-04-16T12:52:38.879349"
---

## 要約

Stanford大学のHuman-Centered AI研究所（HAI）が発表した「AI Index 2026」の主要知見を、MIT Technology Reviewがチャートとともに解説した記事。以下の6つの軸でAIの現状を整理している。

【モデル性能・米中競争】Arena（LLMの比較プラットフォーム）のランキングによると、2023年初頭にはOpenAIが先行していたが、2025年2月にDeepSeekのR1が一時トップに並び、2026年3月時点ではAnthropicが首位、xAI・Google・OpenAIが僅差で追随。DeepSeekやAlibabaの中国モデルも僅差で続く。米国はモデル性能・資本・データセンター数（5,427施設）で優位、中国はAI論文・特許・ロボティクスで優位という非対称な競争構造が明確化。

【技術進歩の速度】SWE-bench Verifiedのトップスコアは2024年の約60%から2025年にはほぼ100%へ急上昇。PhD水準の科学・数学・言語理解テストで人間専門家と同等以上の性能を示す。一方でロボットは家庭内タスクの成功率12%にとどまり、「jagged intelligence（凸凹知性）」と評される。

【ベンチマークの機能不全】数学能力テストベンチマークの42%がエラーを含むなど設計品質の問題が顕在化。モデルがテストデータで訓練される「汚染」問題、実世界性能との乖離、エージェント・ロボット向けベンチマークの未整備など、評価インフラが技術進歩に追いついていない。

【雇用への影響】世界の50%超がAIを利用（普及速度はPCやインターネットを超過）。Stanfordの経済学者による2025年研究では、22〜25歳のソフトウェア開発者雇用が2022年比で約20%減少。McKinseyの2025年調査では組織の3分の1が今後1年で人員削減を予定。一方、カスタマーサービスで14%、ソフトウェア開発で26%の生産性向上が計測されている。

【社会的認識】Ipsos調査では59%が「メリット>デメリット」と回答する一方、52%が「不安を感じる」と回答。Pew調査では専門家の73%がAIの仕事への影響をポジティブと評価する一方、一般米国人では23%にとどまる。

【エネルギー・インフラリスク】世界のAIデータセンターの総消費電力は29.6GW（ニューヨーク州のピーク需要相当）。GPT-4o単体の年間水消費量は1,200万人分の飲料水を超える推計。チップ供給はTSMC（台湾）1社への依存が高く、地政学的リスクとして指摘される。

監査エージェント開発への示唆：ベンチマークの機能不全と透明性の低下は、AIシステムの監査可能性（auditability）に直結する構造的課題。AI企業が責任あるAIベンチマーク結果を非開示にする傾向は、内部統制・GRCの観点から監査設計の難度を高める。

## アイデア

- SWE-bench Verifiedのスコアが1年で60%→100%近くに急上昇しているが、これはベンチマーク自体の限界（天井効果）を示すと同時に、コーディングエージェントの実用化が現実的になったことを意味する。監査エージェントの自動コード生成・修正機能の実装判断に直接関係する。
- 数学ベンチマークの42%エラー率という問題は、評価インフラ全体の信頼性を問う。LLM-as-judgeによる評価パイプラインを設計する際、評価基準自体の品質保証（QA of QA）が必要であることを示唆する。
- AI企業が責任あるAIベンチマーク結果を非公開にする傾向は「不開示自体がシグナル」という観点で注目に値する。監査設計においてモデル選定時に開示姿勢を評価指標の一つとして組み込む可能性がある。

## 前提知識

- **LLMベンチマーク** → /deep_760 EvolveTool-Bench: LLMが生成するツールライブラリをソフトウェア成果物として評価するベンチマーク
- **SWE-bench** → /deep_62 LLMチャットボットに欠けているもの：目的意識（Purposeful Dialogue）
- **Arena (Chatbot Arena)** (TODO: 読むべき)
- **Responsible AI** (TODO: 読むべき)
- **AIガバナンス** → /deep_1516 責任経路設計はMeaningful Human Controlと何が違うのか―軍事AIのaccountability議論との接点とは

## 関連記事

- /deep_1516 責任経路設計はMeaningful Human Controlと何が違うのか―軍事AIのaccountability議論との接点とは
- /deep_1335 日本語入力システムSumibiの開発 part17: ピンインによる中国語入力に対応した
- /deep_1895 ペンタゴンのAnthropicへの「カルチャーウォー」戦術は裏目に出た
- /deep_1227 ペンタゴンのAnthropicに対するカルチャーウォー戦術が裏目に：サプライチェーンリスク指定を巡る法廷闘争
- /deep_1788 ハーネスエンジニアリング入門：AIエージェントの品質を構造で高める5つの要素

## 原文リンク

[AIの現状を理解するためのチャート集：Stanford AI Index 2026の主要知見](https://www.technologyreview.com/2026/04/13/1135675/want-to-understand-the-current-state-of-ai-check-out-these-charts/)
