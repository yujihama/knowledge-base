---
title: "テスト時拡散を用いたDeep Researcher（TTD-DR）：反復的ドラフト改善による長文レポート生成"
url: "https://research.google/blog/deep-researcher-with-test-time-diffusion/"
date: 2026-04-04
tags: [Deep Research, 拡散モデル, RAG, LLM-as-judge, 自己進化, マルチエージェント, 反復改善, 長文生成]
category: "agent-arch"
memo: "[Google AI Blog] Deep researcher with test-time diffusion"
processed_at: "2026-04-04T12:04:50.359225"
---

## 要約

GoogleのRujun HanとChen-Yu Leeが提案するTTD-DR（Test-Time Diffusion Deep Researcher）は、拡散モデルの「ノイズ除去」プロセスを研究レポート執筆に応用したDeep Researchエージェントフレームワーク。人間の研究者が草稿を書いて調査し、フィードバックを受けて加筆修正する反復プロセスを、拡散モデルのデノイジングステップとしてモデル化している点が核心的な貢献。

アーキテクチャは3層構造。(1)研究計画生成：ユーザークエリから構造化されたリサーチプランを生成。(2)反復検索：Search Question Generationサブエージェント（Stage 2a）がプランと過去の検索文脈から次の検索クエリを生成し、Answer Searchingサブエージェント（Stage 2b）がRAGシステムで文書を検索・要約回答を返す。(3)最終レポート生成：収集した全Q&Aペアとプランを統合して包括的レポートを出力。

これに加え2つの独自アルゴリズムが動作する。「コンポーネント単位の自己進化（Self-Evolution）」は各ステージで複数の回答バリアントを生成し、LLM-as-a-judgeがHelpfulnessやComprehensivenessをスコアリングしてテキストフィードバックを生成、各バリアントが自己改訂を繰り返した後にクロスオーバーで最良情報を統合する仕組み。「レポートレベルのRetrieval Denoising」は現在のドラフトをStage 2aに投入して次の検索クエリを誘導し、得られた情報でドラフトを更新するループを継続することで、ノイズの多い初期草稿を段階的に高品質化する。

評価はDeepConsult（長文レポート）、HLE-Search（Humanity's Last Exam から検索推論が必要な200件をサンプリング）、GAIAの3ベンチマークで実施。OpenAI Deep Researchとの比較でTTD-DRは長文レポート生成タスクで74.5%の勝率を達成し、多ホップ推論タスクでも全ベンチマークで上回る結果を報告している。

## アイデア

- 拡散モデルのデノイジング概念をエージェントの反復ドラフト改善に転用するメタファーが実装上も機能する点—ノイズ≒不完全な草稿、デノイズ≒検索による情報補完という対応が自然
- LLM-as-judgeを進化アルゴリズムの適合度関数として使い、複数バリアントの生成→評価→改訂→クロスオーバーというGAライクな最適化をプロンプト空間で実現している構造
- 現在のドラフト自体を次の検索クエリ生成の文脈入力として再帰的に使う設計により、「何を調べ足りないか」をモデルが自己認識して検索計画を更新できる点
## 関連記事

- /deep_21 部分の総和を超えて：マルチモーダルヘイトスピーチ検出における意図変化の解読
- /deep_931 自律走行ポートフォリオ：機関投資家向け資産運用のエージェントアーキテクチャ
- /deep_112 知識ベースを自然淘汰するRAG「Darwin RAG」をつくってみた
- /deep_858 【2026年最新】AIエージェントフレームワーク・ツール完全まとめ224選 — AgDex.aiディレクトリ紹介
- /deep_93 RAGでは足りない——LLMのための「記憶OS」を設計した（RAPTOR×Mem0ハイブリッド4層メモリアーキテクチャ）

## 原文リンク

[テスト時拡散を用いたDeep Researcher（TTD-DR）：反復的ドラフト改善による長文レポート生成](https://research.google/blog/deep-researcher-with-test-time-diffusion/)
