---
title: "AIの現状を理解するためのチャート集：Stanford AI Index 2026レポート解説"
url: "https://www.technologyreview.com/2026/04/13/1135675/want-to-understand-the-current-state-of-ai-check-out-these-charts/"
date: 2026-04-16
tags: [Stanford AI Index, LLMベンチマーク, SWE-bench, DeepSeek, Chatbot Arena, AI雇用影響, EU AI Act, AIデータセンター, jagged intelligence, モデル評価]
category: "ai-ml"
related: [1335, 1788, 1247, 94, 203]
memo: "[MIT Technology Review AI] Want to understand the current state of AI? Check out these charts."
processed_at: "2026-04-16T12:15:40.923528"
---

## 要約

Stanford大学のInstitute for Human-Centered Artificial Intelligence（HAI）が毎年発行するAI Index 2026レポートが公開された。本稿はその主要知見をMIT Technology Reviewがまとめたもの。

【モデル性能と競争構造】Chatbot ArenaによるLLMランキングでは、2023年初頭にOpenAIが優位だったが、2024年にGoogle・Anthropicが追随。2025年2月にはDeepSeekのR1が米国トップモデルに一時並んだ。2026年3月時点ではAnthropicがトップで、xAI・Google・OpenAIが続く。DeepSeek・Alibabaも僅差。米国は資本・データセンター数（5,427施設、次位の10倍超）・高性能モデルで優位、中国はAI研究論文数・特許数・ロボティクスで先行。ただし主要企業は学習コード・パラメータ数・データセット構成を非公開化しており、安全性研究への障壁となっている。

【性能向上と限界】SWE-bench Verifiedのトップスコアは2024年の60%前後から2025年にほぼ100%へ急上昇。PhD水準の科学・数学・言語理解テストでは人間専門家と同等以上の性能を示す。一方でロボットは家庭内タスクの成功率12%にとどまり、「ギザギザな知性（jagged intelligence）」が指摘される。

【ベンチマーク問題】数学能力を測る有名ベンチマークには42%の誤設問が含まれ、モデルがベンチマークデータで学習して実力なしに高スコアを出す問題も顕在化。AIエージェントやロボット向けベンチマークはほぼ未整備。企業による責任AIベンチマーク結果の非開示も増加。

【採用・経済影響】AIは世界人口の50%超が利用し、PCやインターネットより速い普及速度。企業の88%が導入済み、大学生の80%が利用。2022年比で22〜25歳のソフトウェア開発者雇用が約20%減少（Stanford経済学者2025年研究）。McKinsey 2025年調査では組織の3分の1が今後1年で人員削減を計画。AIによる生産性向上はカスタマーサービスで14%、ソフトウェア開発で26%と報告。

【社会・規制】Ipsos調査では59%が「利益が弊害を上回る」と考える一方、52%が「不安を感じる」と回答。AIの雇用影響について専門家の73%が肯定的とみるのに対し、米国一般市民は23%のみ。EUのAI Act第一弾（予測的警察活動・感情認識のAI利用禁止）が発効、日本・韓国・イタリアも国内AI法を制定。米国では逆に連邦政府によるAI規制の後退が見られる。

【インフラコスト】世界のAIデータセンターの消費電力は29.6GW（ニューヨーク州ピーク電力需要相当）。GPT-4o単体の年間水使用量は1,200万人分の飲料水需要を超える可能性。チップ製造はTSMCへの一極集中が継続しサプライチェーンリスクが高い。

監査エージェント開発への示唆：SWE-benchのほぼ満点達成はコード生成能力の実用化水準到達を示すが、判断を要するタスクでの生産性向上が限定的である点は、監査判断AIの限界と課題を示唆する。ベンチマーク問題はLLM-as-judgeの評価設計にも直結する。

## アイデア

- SWE-bench VerifiedのトップスコアがたったI年で60%→ほぼ100%に到達した速度は、コーディングエージェントの実用化フェーズ突入を示す定量的マイルストーンとして注目に値する
- 数学ベンチマークに42%の誤設問が含まれるという事実は、LLM-as-judgeやRAG評価システムを設計する際に、評価データ自体の品質保証が不可欠であることを示している
- AIエージェント・ロボット向けベンチマークがほぼ未整備という空白は、監査エージェントなど業務特化エージェントの評価手法を独自設計する必要性と機会を同時に示している

## 前提知識

- **LLMベンチマーク（SWE-bench, MMLU等）** (TODO: 読むべき)
- **Chatbot Arena / ELOレーティング** (TODO: 読むべき)
- **AI能力評価（jagged intelligence）** (TODO: 読むべき)
- **EU AI Act** → /deep_11 MCPが9,700万DL、フロンティアモデル3連発 — AI業界週報 2026年第13週
- **LLM-as-judge** → /deep_3 Claude Code のAIチームでLLMの品質を自動でチェックする方法

## 関連記事

- /deep_1335 日本語入力システムSumibiの開発 part17: ピンインによる中国語入力に対応した
- /deep_1788 ハーネスエンジニアリング入門：AIエージェントの品質を構造で高める5つの要素
- /deep_1247 ハーネスエンジニアリングとは何か：プロンプト→コンテキスト→ハーネスへ至るAIエージェント設計の変遷
- /deep_94 コーディングエージェントのエンジニアリングに対する考え方
- /deep_203 グローバルオープンソースAIエコシステムの未来：DeepSeekからAI+へ

## 原文リンク

[AIの現状を理解するためのチャート集：Stanford AI Index 2026レポート解説](https://www.technologyreview.com/2026/04/13/1135675/want-to-understand-the-current-state-of-ai-check-out-these-charts/)
