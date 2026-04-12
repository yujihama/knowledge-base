---
title: "StreetReaderAI: コンテキスト認識型マルチモーダルAIによるストリートビューのアクセシビリティ向上"
url: "https://research.google/blog/streetreaderai-towards-making-street-view-accessible-via-context-aware-multimodal-ai/"
date: 2026-04-03
tags: [multimodal-AI, Gemini, accessibility, context-aware, Gemini-Live, function-calling, vision-language-model, street-view]
category: "ai-ml"
memo: "[Google AI Blog] StreetReaderAI: Towards making street view accessible via context-aware multimodal AI"
processed_at: "2026-04-03T12:03:56.469311"
---

## 要約

GoogleのStreetReaderAIは、視覚障害者・弱視者がGoogle Street Viewを音声インターフェースで探索できるようにするプロトタイプシステム。UIST'25で発表された研究成果。

システムの中核はGeminiをバックエンドとする2つのAIサブシステム。①「AI Describer」は現在のStreet View画像とGoogleマップの地理情報（近隣の場所、道路情報、進行方向）を組み合わせ、リアルタイムの音声シーン説明を生成する。モードは「デフォルト」（歩行者の安全・ナビゲーション重視）と「ツアーガイド」（観光・建築・歴史情報を追加）の2種類。②「AI Chat」はGoogle Multimodal Live APIを使用し、セッション内での会話履歴を保持しながらユーザーの質問に答える。コンテキストウィンドウは最大1,048,576入力トークン（4,000枚以上の入力画像相当）に設定されており、「さっきのバス停はどこだっけ？」といった過去の視点に関する質問にも「背後12メートル」などと具体的に回答できる。

ナビゲーションはキーボード（矢印キー）と音声コマンドの両方に対応。左右キーで視点を回転させると現在の方位（北、北東など）が読み上げられ、上下キーで仮想的な前後移動が可能。さらに「ジャンプ」「テレポート」機能で遠隔地への即時移動もサポートする。

ユーザー評価として、盲目のスクリーンリーダーユーザー11名による対面ラボスタディを実施。350以上のパノラマを訪問し、1,000件超のAIリクエストが生成された。総合有用性の中央値は7点満点中7点（平均6.4点、SD=0.9）と高評価。AI ChatはAI Describerの6倍の頻度で使用され、説明よりも対話的な質問応答への強い需要が確認された。一方で、空間的方向付けの困難さ、AI回答の信頼性判断の難しさ、AIの知識限界の把握といった課題も残る。

システムはGemini Liveのリアルタイム関数呼び出し機能を活用し、地理情報APIとStreet View画像を動的に組み合わせることで、静的なalt textでは実現できないコンテキスト依存の説明生成を実現している。

## アイデア

- コンテキストウィンドウを1Mトークン（画像4,000枚相当）に設定し、セッション全体の移動履歴をエージェントの記憶として保持する設計は、監査エージェントが長期的な証跡をたどる際のコンテキスト管理手法として参考になる
- 静的プロンプトと動的コンテキスト（現在地・視野・地理情報）を分離し、ユーザープロファイルも注入する構造は、エージェントのシステムプロンプト設計パターンとして汎用性が高い
- AI ChatがAI Describerの6倍使われた事実は、ユーザーが一方向の説明より双方向の対話を強く好むことを示しており、エージェントUIのデフォルトモードを対話型にする根拠となりうる

## Yujiの取り組みへの示唆

監査エージェント開発における直接的な関連性は薄いが、「静的プロンプト＋動的コンテキスト（直近の操作履歴・地理情報・現在の視野）をGeminiに渡す」設計は、LangGraphで構築する監査エージェントが「現在調査中の仕訳・過去の調査履歴・リスク評価コンテキスト」を動的にモデルへ渡すアーキテクチャと構造的に同一。また、Gemini LiveのMultimodal Live APIによるリアルタイム関数呼び出しは、監査エージェントがリアルタイムでERPや会計システムのAPIをコールするツール設計の参考事例として活用できる。

## 原文リンク

[StreetReaderAI: コンテキスト認識型マルチモーダルAIによるストリートビューのアクセシビリティ向上](https://research.google/blog/streetreaderai-towards-making-street-view-accessible-via-context-aware-multimodal-ai/)
