---
title: "グローバルオープンソースAIエコシステムの未来：DeepSeekからAI+へ"
url: "https://huggingface.co/blog/huggingface/one-year-since-the-deepseek-moment-blog-3"
date: 2026-04-02
tags: [オープンソース, DeepSeek, Qwen, LLM, 中国AI, Hunyuan, エコシステム, モデルファミリー]
category: "ai-ml"
memo: "[HF Blog] The Future of the Global Open-Source AI Ecosystem: From DeepSeek to AI+"
processed_at: "2026-04-02T09:09:21.323225"
---

## 要約

本記事は、2025年1月の「DeepSeekモーメント」以降の中国オープンソースAIコミュニティの動向を分析する3部作の最終回。中国主要AI組織の戦略変化と今後のオープンソースの方向性を考察している。

Alibaba（Qwen）は単一フラッグシップモデルではなく、複数サイズ・タスク・モダリティをカバーするモデルファミリー戦略を採用。2025年中頃にはHugging Face上でQwnをベースとした派生モデルが113,000件以上、タグ付きリポジトリが200,000件超に達し、Meta Llamaの27,000件やDeepSeekの6,000件を大幅に上回る。モデル・チップ・プラットフォーム・アプリケーションを統合した単一エンジニアリングスタックを構築。

Tencent（Hunyuan）はDeepSeek R1リリース後に同モデルを製品へ統合し、大規模内部検証を経てビジョン・動画・3D分野で独自モデルを公開。ByteDanceはUI-TARS-1.5（マルチモーダルUI理解）、Seed-Coder（データ中心コードモデル）、SuperGPQAデータセットを公開しつつ、AIアプリ「Doubao」が2025年12月に日次アクティブユーザー1億人を突破。Baiduはクローズドモデル優先から転換し、Ernie 4.5シリーズを無償公開。AIチップKunlunxinは2026年1月1日にIPO申請。

スタートアップ領域ではMoonshot（Kimi K2）、Z.ai（GLM-4.5）、MiniMax（M2）が「第2のDeepSeekモーメント」と称される高性能オープンソースモデルを投入し、Z.aiとMiniMaxはIPO計画を発表。Xiaohongshu・Bilibili・Xiaomi・Meituan等のアプリケーション企業も自社モデル開発・公開を開始。

中国のインフラ面では「東数西算」戦略のもと8つの主要コンピュートハブと10のデータセンタークラスターを整備。2025年時点での総コンピュート容量は約1,590 EFLOPS。BAIDUのPaddleやBAII・上海AI研究所のFlagOpen・OpenDataLab・OpenCompassがエコシステム基盤を強化。

全体として、孤立したブレークスルーから「モデル・デプロイ・ソフトウェア・ハードウェア・ガバナンスが連鎖したエコシステム」への移行が進行中であり、中国のオープンソース戦略は大規模デプロイと統合を目標とした持続可能なアプローチとして確立しつつある。

## アイデア

- Qwnの派生モデル数113,000件超という数字は、単一モデルではなくファミリー戦略＋高頻度アップデートがエコシステム支配力に直結することを示す定量的証拠
- ByteDanceの「AIアプリケーションファクトリー」モデル：競争優位性を持つコンポーネントのみ選択的公開し、製品エントリーポイントで収益化する戦略は、企業内AIシステム構築の参考になる
- BAAI・上海AI研究所のような研究機関がモデル性能競争より評価基盤・データプラットフォーム・デプロイインフラ整備にシフトしている点は、エコシステムの成熟度指標として重要

## Yujiの取り組みへの示唆

監査エージェント開発においてQwnやDeepSeekベースのモデルを活用する際、113,000件超の派生モデルの中から監査・文書解析特化のファインチューニング済みモデルを探す指針として活用できる。また、ByteDanceのSeed-Coder（データ中心コードモデル）やSuperGPQAの推論評価手法は、監査エージェントのLLM-as-judgeコンポーネント設計の参考になる。オープンソース戦略の全体像を把握することで、ローカルLLMインフラ（RTX 3090）上で動作させるモデル選定の判断軸を得られる。

## 原文リンク

[グローバルオープンソースAIエコシステムの未来：DeepSeekからAI+へ](https://huggingface.co/blog/huggingface/one-year-since-the-deepseek-moment-blog-3)
