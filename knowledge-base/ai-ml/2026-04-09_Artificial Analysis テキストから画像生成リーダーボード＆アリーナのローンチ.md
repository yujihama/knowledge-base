---
title: "Artificial Analysis テキストから画像生成リーダーボード＆アリーナのローンチ"
url: "https://huggingface.co/blog/leaderboard-artificial-analysis2"
date: 2026-04-09
tags: [ELOスコア, ヒューマンプレファレンス, テキストto画像, Midjourney, Stable Diffusion 3, DALL-E, Playground AI, リーダーボード, クラウドソーシング評価]
category: "ai-ml"
memo: "[HF Blog] Launching the Artificial Analysis Text to Image Leaderboard & Arena"
processed_at: "2026-04-09T09:22:33.912550"
---

## 要約

Artificial AnalysisとHugging Faceが共同で、テキストから画像生成モデルを人間の好み（ヒューマンプレファレンス）に基づいてランキングするリーダーボードとアリーナを公開した（2024年6月）。評価方法はChatbot Arenaと同様のELOスコア方式を採用しており、45,000件以上の人間による比較選択データを回帰分析してスコアを算出する。参加者はプロンプトと2枚の画像を提示され、プロンプトをより忠実に表現している画像を選択する形式で、30票投票後に個人別ランキングを確認できる。

評価対象モデルは、Midjourney、DALL·E 3 HD、DALL·E 2、Stable Diffusion 3、Playground AI v2.5など、主要なプロプライエタリ・オープンソースモデルを網羅。各モデルにつき700枚以上の画像を生成し、人物ポートレート・グループ・動物・自然・アートなど多様なカテゴリのプロンプトで評価している。

主な結果として、Midjourney、Stable Diffusion 3、DALL·E 3 HDがリーダーボード上位を占める一方、Playground AI v2.5をはじめとするオープンソースモデルがDALL·E 3を超える性能を示し、クローズドモデルとの差が縮まっていることが明らかになった。また、かつて最高水準だったDALL·E 2はアリーナで選択される割合が25%未満まで低下し、最下位グループに転落している。さらに、2024年6月12日にオープンソース化が予定されていたStable Diffusion 3 Mediumについて、Stability AI CTOがAMDとの発表の場で言及しており、SD 1.5やSDXLと同様にコミュニティによる大量のファインチューン派生モデルが生まれる可能性が高いと分析されている。

評価の客観性確保のため、モデル名は伏せた状態でA/Bテストが実施されている。同様の取り組みとしてOpen Parti Prompts LeaderboardやGenAI-Arenaなどが存在するが、本リーダーボードはプロプライエタリ・オープンソース両方を対象とした横断的な比較を特徴とする。

## アイデア

- ELOスコアによる人間の好みの定量化：45,000件以上のA/B比較データを回帰分析してモデル品質をスカラー値に落とし込む手法は、LLM評価（Chatbot Arena）と同じ枠組みを画像モダリティに拡張した実装例として興味深い
- オープンソースモデルがプロプライエタリモデルに追いつくスピード：わずか2年でDALL·E 2が最下位クラスに転落し、Playground AI v2.5がDALL·E 3を超えた事実は、オープンコミュニティによるイノベーション速度を定量的に示している
- クラウドソーシング型評価のスケーラビリティ：個人別ランキング機能（30票投票後）がデータ収集のインセンティブ設計として機能しており、評価システムとデータ収集を同一UIで達成するアーキテクチャは他の評価ベンチマーク設計に応用可能

## Yujiの取り組みへの示唆

画像生成モデルの評価方法論（ELOスコア＋クラウドソーシング）は、Yujiが開発中の監査エージェントシステムにおけるLLM-as-judgeやエージェント出力品質評価の設計に直接応用できる。特に、複数エージェントの出力をA/B比較させてELOランキングを構築する手法は、監査レポートや異常検知結果の品質評価に転用可能な枠組みである。ただし、本記事の主題は画像生成モデル評価であり、監査AI・LangGraph・GRPO等への直接的な示唆は限定的。

## 原文リンク

[Artificial Analysis テキストから画像生成リーダーボード＆アリーナのローンチ](https://huggingface.co/blog/leaderboard-artificial-analysis2)
