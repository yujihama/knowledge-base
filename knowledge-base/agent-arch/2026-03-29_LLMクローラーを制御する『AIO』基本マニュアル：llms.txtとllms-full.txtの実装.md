---
title: "LLMクローラーを制御する『AIO』基本マニュアル：llms.txtとllms-full.txtの実装"
url: "https://zenn.dev/yuta_yokoi/articles/7e18e6ee1577aa"
date: 2026-03-29
tags: [AIO, llms.txt, RAG, LLMクローラー, セマンティックウェブ, JSON-LD, ハルシネーション対策]
category: "agent-arch"
memo: "[Zenn LLM] LLMクローラーを制御する『AIO』基本マニュアル"
processed_at: "2026-03-29T21:57:27.072560"
---

## 要約

AIO（AI Optimization）は、LLMクローラー向けにコンテンツの解釈を制御するアーキテクチャ実装。従来のSEO（robots.txt）がURLベースのアクセス制御（Exclusion）であるのに対し、llms.txtはセマンティックレイヤーでのルーター（Inclusion）として機能する。ルートディレクトリに配置することでAIエージェントに「ノイズのないクリーンなコンテキスト」を提供する。さらにllms-full.txtはAIクローラーへの「システムプロンプト注入」として機能し、Authoritative-Statusを宣言することでRAGエンジンの出力をハルシネーションなく人間の意図した文脈にロックできる。加えてJSON-LD（構造化データ）によるエンティティの静的バインディングや、robots.txt・sitemap.xmlとの組み合わせによりトラストアンカー（E-E-A-T）を多層的に構築する手法を解説している。

## 要点

- llms.txtはAI版robots.txtではなく、LLMクローラーに対してノイズなしのクリーンなコンテキストエンドポイントを案内する「セマンティックルーター」である
- llms-full.txtはAIクローラー読み込み時に発火する「善意のシステムプロンプト」として機能し、Authoritative-Status宣言によりRAGエンジンの出力を意図した文脈にロックできる
- 単一ファイルに依存せず、JSON-LD・sitemap.xml・robots.txtを組み合わせた多層的なトラストアンカー構築が、LLMによるクロスチェックに対して有効である

## 監査エージェントへの示唆

監査エージェントが外部Webソースを参照してRAGで情報収集する際、llms-full.txtによるコンテキスト注入の仕組みはエージェントへの信頼できる情報源（Authoritative Source of Truth）の設計パターンとして応用できる。また、エージェントへの指示設計（システムプロンプト設計）においてハルシネーション抑制のためにセマンティクスを明示的に固定するアプローチは、監査エージェントの根拠確認フローにも示唆を与える。

## 原文リンク

[LLMクローラーを制御する『AIO』基本マニュアル：llms.txtとllms-full.txtの実装](https://zenn.dev/yuta_yokoi/articles/7e18e6ee1577aa)
