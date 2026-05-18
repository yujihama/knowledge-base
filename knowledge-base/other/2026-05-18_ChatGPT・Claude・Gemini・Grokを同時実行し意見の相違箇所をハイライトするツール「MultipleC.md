---
title: "ChatGPT・Claude・Gemini・Grokを同時実行し意見の相違箇所をハイライトするツール「MultipleChat」"
url: "https://zenn.dev/mellisaoez/articles/ff450d230b8260"
date: 2026-05-18
tags: [MultipleChat, マルチモデル, LLM比較, Disagreement Detection, ハルシネーション検知, プロンプトチェーン]
category: "other"
related: [2590, 496, 3924, 432, 2390]
memo: "[Zenn LLM] ChatGPT・Claude・Gemini・Grokを4つ同時に動かして、意見が割れた箇所だけハイライするツールを作った（MultipleC"
processed_at: "2026-05-18T09:06:05.546603"
---

## 要約

MultipleChatは、ChatGPT・Claude・Gemini・Grokの4モデルを1つのインターフェースから同時に利用できるWebサービス。開発背景として、同じ質問を複数モデルにコピペする非効率（1回あたり約5分のロス）と、単一モデルのハルシネーション検知不能という課題がある。主な機能は4種類。①Soloモード：4モデルのうち1つを選択して通常チャット。各モデル個別サブスク不要のため料金節約にも使える。②Side-by-Sideモード：1つのプロンプトを全モデルに同時投下し、回答を横並び表示。③Collaborateモード：モデル間でプロンプトチェーンを組み、ChatGPTが初稿→Claudeが論理チェック→Geminiが最新情報補強という順次処理をノーコードで構成可能。④Disagreement Detection：4モデルの回答を解析し、意見が割れている箇所だけを自動ハイライト。実例として「PostgreSQL 16のlogical replicationを本番で使うべきか」というクエリでは、ChatGPTが一般論、Claudeがpgoutputプラグインの制限を列挙、Geminiが16.1の既知バグ、Grokが公式ドキュメントとissue trackerのリンクを提示し、Disagreement Detectionが「レプリケーションラグの許容範囲」での食い違いを指摘した。料金面では、ChatGPT Plus＋Claude Pro＋Gemini Advancedを個別契約すると月60ドル以上かかるところ、MultipleChatは1サブスクで全モデルにアクセス可能（無料プランあり、クレカ不要）。監査エージェント開発への示唆として、Disagreement DetectionはLLM-as-judgeのアンサンブル評価に近い概念であり、複数モデルの回答分散を「要確認ポイント」として自動検出する仕組みは、監査AIにおける判断の信頼性スコアリングや矛盾検出ロジックの設計参考になる。

## アイデア

- Disagreement Detectionは複数LLMの回答ベクトルを比較して意見相違箇所を自動抽出する仕組みで、LLM-as-judgeのアンサンブル版として捉えられる
- Collaborateモードのモデル間プロンプトチェーンはノーコードで組めるが、これはLangGraphのような明示的なグラフ定義なしに順次エージェント処理を実現している点で興味深い
- モデルごとの得意分野（コード→Claude、最新情報→Gemini/Grok、長文要約→ChatGPT）をルーティングロジックに落とし込む設計は、マルチエージェントオーケストレーションの実装パターンとして参考になる

## 前提知識

- **LLM API** → /deep_409 Hugging Face SpacesにGGUFモデルをデプロイして無料LLM APIを構築する方法
- **ハルシネーション** → /deep_28 IBMとUC BerkeleyがIT-BenchとMASTを使ってエンタープライズエージェントの失敗原因を診断
- **プロンプトチェーン** (TODO: 読むべき)
- **LLM-as-judge** → /deep_3 Claude Code のAIチームでLLMの品質を自動でチェックする方法
- **マルチエージェント** → /deep_2 AIエージェント自作のための基礎知識 - Google ADK (Go) を使ったエージェント構築

## 関連記事

- /deep_2590 ローカルLLMを簡単にデモする：vLLM + LiteLLM + ngrokの構成
- /deep_496 コストおよびキャパシティ制約下でのLLMバッチレベルクエリルーティング
- /deep_3924 エンタープライズAIのためのデータスタック再構築：統合・ガバナンス・アーキテクチャの要件
- /deep_432 AIはもう1つじゃない——チームで使う時代のAI完全ガイド
- /deep_2390 AIが中小セラーの商品開発を変える：AlibabaのAccioが示すAIソーシング・エージェントの実態

## 原文リンク

[ChatGPT・Claude・Gemini・Grokを同時実行し意見の相違箇所をハイライトするツール「MultipleChat」](https://zenn.dev/mellisaoez/articles/ff450d230b8260)
