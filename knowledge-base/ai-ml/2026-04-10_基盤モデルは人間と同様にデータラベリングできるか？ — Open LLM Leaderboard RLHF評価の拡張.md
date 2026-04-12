---
title: "基盤モデルは人間と同様にデータラベリングできるか？ — Open LLM Leaderboard RLHF評価の拡張"
url: "https://huggingface.co/blog/open-llm-leaderboard-rlhf"
date: 2026-04-10
tags: [RLHF, LLM-as-judge, Elo, human-preference, evaluation, Open-LLM-Leaderboard, GPT-4-eval, Vicuna, Scale-AI]
category: "ai-ml"
memo: "[HF Blog] Can foundation models label data like humans?"
related: [963, 1137, 544, 888, 1296]
processed_at: "2026-04-10T09:42:39.146210"
---

## 要約

本記事は、Hugging FaceがOpen LLM Leaderboardの評価スイートを拡張し、GPT-4による自動評価と人間アノテーターによる評価を比較した研究報告である。背景として、ChatGPT以降のLLM評価は「GPT-4評価でChatGPTよりN%好まれる」という形式が蔓延しているが、これが本来の人間評価と整合しているかが不明確であった。そこで、Koala-13B、Vicuna-13B、OpenAssistant-12B、Dolly-12Bの4モデルを対象に、Self-Instructの327プロンプト（生成・ブレインストーミング・QA・要約・常識推論・コーディング等）を用いた盲検テストセットを構築。Scale AIと提携して人間アノテーターによるペアワイズ比較（Likertスケール1〜8）を実施し、ブートストラップEloスコアを算出した。人間評価の結果はVicuna-13B（Elo中央値1140）＞Koala-13B（1073）＞Oasst-12B（986）＞Dolly-12B（802）の順。GPT-4評価でも同じ順序が得られ（Vicuna: 1134、Koala: 1082、Oasst: 972、Dolly: 812）、モデルの相対ランキングは一致した。ただし各モデル間のEloマージン（差の大きさ）は人間評価とGPT-4評価で異なり、GPT-4が人間ラベルの完全な代替にはならないことが示唆された。タイ判定（スコア4または5をタイとみなす）を導入しても相対順位に大きな変化はなく、KoalaとVicunaの間に最多96タイが観測された（327比較中）。コーディングタスクに関しては、GPT-4が人間よりもコード品質を正確に評価できる可能性が示された。総合的な知見として、GPT-4評価は反復速度が高くコスト効率が良い一方、人間評価との較正（calibration）が不可欠であり、タスクドメインによって信頼性が異なる点を認識した上で使用する必要がある。

## アイデア

- GPT-4評価と人間評価はモデルの相対順位は一致するが、Eloマージン（モデル間の差の大きさ）が異なる——どちらの評価を信頼するかはタスクドメインによって使い分ける必要がある
- コーディングタスクではGPT-4が人間より高精度に評価できる可能性があり、ドメイン特化型LLM-as-judgeの有効性を示唆している
- ブートストラップEloはペアワイズ比較のみからグローバルランキングを構築できる手法であり、監査エージェントの出力品質をリアルタイムでランク付けする評価フレームワークに転用可能
## 関連記事

- /deep_963 ウェルビーイングに根ざしたAIのポジティブなビジョンが必要だ
- /deep_1137 ウェルビーイングに根ざしたAIのポジティブなビジョンが必要だ
- /deep_544 ウェルビーイングに基づくAIのポジティブなビジョンが必要だ
- /deep_888 RIFT: ルーブリック失敗モード分類体系と自動診断
- /deep_1296 PSY-STEP: 積極的カウンセリング対話システムのための治療目標と行動シーケンスの構造化

## 原文リンク

[基盤モデルは人間と同様にデータラベリングできるか？ — Open LLM Leaderboard RLHF評価の拡張](https://huggingface.co/blog/open-llm-leaderboard-rlhf)
