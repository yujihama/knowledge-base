---
title: "Agentic Engineeringを実務に落とすためのプロンプト設計"
url: "https://zenn.dev/nobmake/articles/b0a0eea5202afe"
date: 2026-06-02
tags: [Agentic Engineering, プロンプト設計, Vibe Coding, Plan gate, Spec-first, コードレビュー, Invariants, マルチエージェント, セキュリティレビュー]
category: "agent-arch"
related: [6359, 6564, 6556, 4745, 6758]
memo: "[Zenn LLM] Agentic Engineeringを実務に落とすためのプロンプト設計"
processed_at: "2026-06-02T21:01:38.222744"
---

## 要約

Andrej KarpathyによるVibe CodingとAgentic Engineeringの対比を出発点に、本番プロダクト開発においてAIエージェントを安全に組み込むための具体的な設計手法を整理した実践ガイド。Vibe Codingが「床を上げる（誰でも作れるようにする）」のに対し、Agentic Engineeringは「天井を上げる（プロ品質を維持しながら開発速度を上げる）」と定義する。核心は「プロンプトのうまさ」ではなく、仕様・制約・検証可能性・権限・レビュー構造を設計する開発の型にある。

記事では9つの観点を体系化している。①Spec-first：コード生成前に仕様書を作らせ、「非目標」を明記することでスコープ逸脱を防ぐ。②Read before write：既存コードのエラー処理・認証方式・命名規則を先に調査させ、設計思想の破壊を防ぐ。③Plan gate：実装前に変更対象ファイル・PR分割案・ロールバック方法を含む計画を出させ、人間が承認するまでコード変更を禁止する。④Atomic delegation：1プロンプトで1つの検証可能な差分のみを担当させ、レビュー可能な粒度を維持する（例：請求書機能を7PRに分割）。⑤Verifiability first：失敗するテストを先に書かせてから実装させる。認可漏れ・IDOR・ログ漏洩などの異常系・セキュリティ観点を明示的にテスト観点に含める。⑥Diffレビュー：実装したエージェントとは別に「厳しいコードレビュアー」ペルソナでレビューさせ、Blocker/Major/Minorに分類させる。⑦Least privilege：認証・支払い・ファイルアップロードなど危険領域を明示し、攻撃者視点でSSRF・パストラバーサル・冪等性などを検証させる。⑧Invariants：「userIdでスコープする」「emailをIDとして使わない」など不変条件を明文化し、実装後に各条件がどのコードで守られているかを表で提出させる。⑨役割分離：Implementer・Reviewer・Attacker・Tester・Documenterとエージェントの役割を分け、品質レイヤーを多重化する。

監査エージェント開発への示唆：Plan gate・Invariants・役割分離の構造は、監査手続の設計（手続定義→実行→証跡レビュー）と構造的に同型であり、LangGraphによるエージェントワークフロー設計に直接応用できる。特に「非目標の明記」と「不変条件の明文化」は、監査スコープの定義や内部統制ルールのエンコードと親和性が高い。

## アイデア

- 「非目標の明記」によるスコープ逸脱防止：AIは善意でスコープを拡大しようとするため、作るものより作らないものを先に固定する設計が実務上有効
- Plan gate構造：実装前に変更対象ファイル・PR分割・ロールバック方法を含む計画を人間が承認するゲートを置くことで、高速なエージェントが誤方向へ暴走するリスクを制御できる
- Implementer/Reviewer/Attacker の役割分離：単一エージェントに全工程を任せず、ペルソナを明示的に切り替えることで品質レイヤーを多重化し、生成コードの見落としを構造的に減らす

## 前提知識

- **LLMエージェント** → /deep_7 Karpathy発AutoResearchで一晩100実験を自動化する仕組みと実践
- **プロンプトエンジニアリング** → /deep_6 Harness Engineeringとは何か？プロンプトの次に来る「AIエージェントの環境設計」を実務目線で解説
- **CI/CDパイプライン** (TODO: 読むべき)
- **OWASP / IDOR** (TODO: 読むべき)
- **TDD（テスト駆動開発）** (TODO: 読むべき)

## 関連記事

- /deep_6359 仕様書に埋もれた「決まっていない意思決定」を、マルチエージェントで炙り出す
- /deep_6564 コードを書かずに20個のプロジェクトを作った話（Vibe Coding 1年の記録）
- /deep_6556 RustでLLMコードレビューエージェントを作った
- /deep_4745 Claude Codeでキャリア戦略レポートの作り方を自動化した話：4並列調査エージェント＋検証エージェントによる楽観バイアス除去
- /deep_6758 AI時代の新Vibesカタログ — Vibe Coding、AI Slop、ハルシネーションなど54語

## 原文リンク

[Agentic Engineeringを実務に落とすためのプロンプト設計](https://zenn.dev/nobmake/articles/b0a0eea5202afe)
