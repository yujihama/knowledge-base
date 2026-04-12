---
title: "GoogleとIncluded Health、AIを活用した全米規模のランダム化比較試験による仮想医療ケア評価研究を発表"
url: "https://research.google/blog/collaborating-on-a-nationwide-randomized-study-of-ai-in-real-world-virtual-care/"
date: 2026-03-31
tags: [AMIE, conversational-AI, RCT, multi-agent, healthcare-AI, Personal-Health-Agent, LLM-clinical]
category: "ai-ml"
memo: "[Google AI Blog] Collaborating on a nationwide randomized study of AI in real-world virtual care"
processed_at: "2026-03-31T12:06:25.424562"
---

## 要約

Googleは米国の医療プロバイダーIncluded Healthと共同で、会話型AIを実際の仮想医療ワークフローで評価する全米規模の前向きランダム化比較試験（RCT）を開始すると発表した（IRB承認待ち）。この研究はシミュレーション環境や後ろ向きデータを超え、臨床現場でのAIパフォーマンスを厳格に検証する初の試みとなる。

背景として、GoogleはAMIE（Articulate Medical Intelligence Explorer）を中心に医療AIの基礎研究を積み重ねてきた。AMIEは模擬患者俳優を使った実験で、診断精度と会話品質において一般内科医と同等以上の性能を示した。さらに縦断的疾患管理（診療ガイドラインと患者履歴に基づく検査・治療計画立案）やマルチモーダル推論にも拡張されている。また、Personal Health Agent（PHA）はウェアラブルデバイスの睡眠・活動データをマルチモーダルモデルで解析し、協調型マルチエージェントアーキテクチャ（データサイエンティスト役・ドメイン専門家役・ヘルスコーチ役の3エージェント）でパーソナライズドコーチングを提供する研究も行われた。さらにWayfinding AIはユーザーのオンライン健康情報検索をプロアクティブな会話ガイダンスで支援するエージェント研究である。

直近の臨床可能性検証として、Beth Israel Deaconess Medical Centreとの単一施設フィージビリティスタディを実施し、安全監督者による介入回数などの安全性指標で良好な結果が得られている。今回のIncluded Healthとの全国RCTはこの成果を受けた次フェーズで、地域・疾患種別を横断した大規模コホートを対象に、AI支援ケアvs標準臨床実務の比較を行う。Google側の研究リードはMike SchaekermanとCameron Chen。このフェーズドアプローチは医薬品臨床試験と同水準のエビデンス生成基準を医療AIに適用するものであり、患者・医療チームの信頼構築を目的としている。

## アイデア

- 医療AIの評価をシミュレーションから実世界RCTへ段階的にエスカレーションするフェーズドエビデンス生成フレームワークは、他のハイリスクドメイン（例：監査・法務）でのAI展開評価にそのまま転用できる設計思想
- PHAのマルチエージェント構成（データサイエンティスト・ドメイン専門家・ヘルスコーチの役割分担）は、LangGraphでの監査エージェント設計における役割分離パターンと直接対応する具体的アーキテクチャ事例
- 非同期オーバーサイトパラダイム（医師がAIの会話を事後確認する構造）は、内部監査における人間-AIコラボレーションモデルとして、LLM-as-judgeの実装設計に示唆を与える

## Yujiの取り組みへの示唆

PHAの協調マルチエージェントアーキテクチャ（データサイエンティスト・ドメイン専門家・ヘルスコーチの役割分担）はLangGraphでの監査エージェント設計における役割特化エージェントの分割方針に直接応用できる。また医師による非同期AIオーバーサイトの仕組みは、監査人がAIの判断を事後レビューするヒューマン・イン・ザ・ループ構造のリファレンスとなり、LLM-as-judgeの設計で参考になる。さらにフェーズドRCTというエビデンス生成フレームワークは、監査AIシステムの社内展開時に説得力ある有効性・安全性評価を構築する方法論として活用できる。

## 原文リンク

[GoogleとIncluded Health、AIを活用した全米規模のランダム化比較試験による仮想医療ケア評価研究を発表](https://research.google/blog/collaborating-on-a-nationwide-randomized-study-of-ai-in-real-world-virtual-care/)
