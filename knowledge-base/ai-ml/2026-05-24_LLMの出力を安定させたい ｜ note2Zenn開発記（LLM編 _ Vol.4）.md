---
title: "LLMの出力を安定させたい ｜ note2Zenn開発記（LLM編 / Vol.4）"
url: "https://zenn.dev/hanav1ye/articles/note2zenn-vol4"
date: 2026-05-24
tags: [LLM, プロンプトエンジニアリング, few-shot, Gemma, OpenAI, ローカルLLM, Markdown, 出力制御]
category: "ai-ml"
related: [5037, 5647, 6361, 892, 4036]
memo: "[Zenn LLM] LLMの出力を安定させたい ｜ note2Zenn開発記（LLM編 / Vol.4）"
processed_at: "2026-05-24T09:01:06.365499"
---

## 要約

note2ZennはnoteのURLを入力としてZennの下書きを自動生成するアプリケーションで、本記事はLLM出力の品質安定化に取り組んだ第4弾。処理フローは①Markdownへの構造変換（ソース側）→②Zenn向け文体変換（LLM側）の2段階で構成される。LLMに渡す固定ルール（システムプロンプト）として、出力をMarkdown本文のみに制限、画像パス形式`/images/{slug}/filename`の維持、見出しレベルの保持、noteのハッシュタグや著者プロフィールの除去、補足説明への`:::message`記法適用など15項目以上の制約を設定している。カスタム性の実現には3つのアプローチを組み合わせた。①数値パラメータ（0.0〜1.0）：`logical_density`（論理密度）、`technical_focus`（技術用語度）、`emotional_retention`（情緒表現度）、`politeness_level`（丁寧語度）の4軸を定義。②few-shot：入力→出力の変換例を与え文体制御。③自由記述（`free_instruction`）：ユーザーが直接プロンプトを補完できる余地を設けた。検証結果として、all_0.5設定とカスタム設定（logical_density:0.68、technical_focus:0.62、emotional_retention:0.28、politeness_level:0.72）を比較した。`logical_density`は文接続の変化に効果あり、`politeness_level`は話し言葉表現（「やつ」「そこらへん」）の是正に効果あり。一方`technical_focus`と`emotional_retention`は元記事の特性上、差異が確認しにくかった。Gemma4 E2Bでは同一プロンプトで全く異なる出力が得られ、OpenAI向けに最適化した固定ルールがローカルLLMでは過剰なコンテキストとして機能した可能性を指摘。「LLMごとに特徴を抑えたプロンプトであるべき」という知見を得ており、Gemma利用時はカスタム性無効化も検討中。ファインチューニングは費用対効果と個人スケールの観点から今回は不採用とし、Modelfileによる固定ルールで対応する方針をとっている。監査エージェント開発への示唆としては、LLM出力の品質制御をプロンプトエンジニアリングで実現する手法は、監査レポート生成や構造化アウトプットが求められる場面でも応用可能。特に数値パラメータによる出力トーン制御は、監査調書の形式統一や記述スタイルの標準化に転用できる考え方である。

## アイデア

- 数値パラメータ（0.0〜1.0）で文体を多軸制御するアプローチは、監査レポートや技術文書など形式が求められるアウトプット生成に応用できる
- 構造変換をソース側で先行させてからLLMに渡すことで、LLMが扱いやすい構造化入力を確保しつつ役割を分離するパイプライン設計
- 同一プロンプトでOpenAIとGemma4 E2Bの出力が大きく乖離した事例は、モデルごとにプロンプト戦略を分岐させる必要性を実証している

## 前提知識

- **few-shot prompting** → /deep_514 レビューから要件へ：LLMは人間のようなユーザーストーリーを生成できるか？
- **システムプロンプト** → /deep_62 LLMチャットボットに欠けているもの：目的意識（Purposeful Dialogue）
- **Gemma** → /deep_6361 AIを型で律する「設計図」の書き方 ｜ note2Zenn開発記（構成編 / Vol.3）
- **Modelfile** → /deep_392 OllamaでローカルLLM：導入から最新エコシステムまでを解説（2026年版）
- **Markdown** → /deep_1962 llm-wikiの発想を自分のObsidian vaultに持ち込んでみた

## 関連記事

- /deep_5037 自分のトーン規約を渡してOllamaにZenn下書きを点検させる
- /deep_5647 note2Zenn開発記（コンセプト編 Vol.1）：LLMを使ったnote→Zenn自動投稿ツールの構想
- /deep_6361 AIを型で律する「設計図」の書き方 ｜ note2Zenn開発記（構成編 / Vol.3）
- /deep_892 重み空間モデルマージによる大規模言語モデルの壊滅的忘却対策と指示追従能力の改善
- /deep_4036 未経験者がVRAM 16GBでAIキャラの台本生成を動かすまで(第4回) ── 「きみ」を消したら、品質も消えた話

## 原文リンク

[LLMの出力を安定させたい ｜ note2Zenn開発記（LLM編 / Vol.4）](https://zenn.dev/hanav1ye/articles/note2zenn-vol4)
