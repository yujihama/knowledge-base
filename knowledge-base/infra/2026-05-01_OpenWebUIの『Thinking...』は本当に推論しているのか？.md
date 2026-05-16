---
title: "OpenWebUIの『Thinking...』は本当に推論しているのか？"
url: "https://zenn.dev/hitama/articles/bd3c771f6984ea"
date: 2026-05-01
tags: [OpenWebUI, Chain-of-Thought, thinking, ストリーミング, ミドルウェア, LLM出力パース, reasoning_tags]
category: "infra"
related: [1928, 2366, 972, 861, 1060]
memo: "[Zenn LLM] OpenWebUIの『Thinking...』は本当に推論しているのか？"
processed_at: "2026-05-01T12:20:57.073906"
---

## 要約

OpenWebUIに表示される「Thinking...」機能の内部実装をコードベースで追跡・分析した記事。結論として、thinkingはOpenWebUI自身が推論しているのではなく、LLMが出力した`<think>...</think>`タグ付きテキストをOpenWebUIが検出・整形・表示しているに過ぎない。

処理は3層構造になっている。①`process_chat_payload`（プロンプト層）：「think step by step」等の指示をプロンプトに注入し、LLMが`<think>`タグ付きで出力するよう誘導する。②`chat_completion_handler`（中継層）：モデル出力をそのままパススルーするだけで、thinkingには一切関与しない。③`process_chat_response`（UI変換層）：`<think>`タグを検出し、reasoningブロックとして分離、`<details>`タグに変換してUIに渡す。

実装の詳細として、ストリーミング中にLLM出力をリアルタイムで蓄積し、`started_at`と`ended_at`でdurationを計測。最終的に`<details type="reasoning" done="true" duration="{N}"><summary>Thought for N seconds</summary>...</details>`というHTML構造に変換する。

`reasoning_tags`パラメータ（`{"start": "<think>", "end": "</think>"}`）はUI/APIから受け取り可能で、モデルごとに上書き設定もできる。これにより、DeepSeekのように`<think>`タグをネイティブに出力するモデルにも、プロンプト誘導でタグを出力させるモデルにも対応している。

つまりthinkingの正体は「生成ロジック」ではなく「解釈ロジック」であり、LLMの出力をOpenWebUIが意味付けして可視化したものである。監査エージェント開発への示唆として、LLMのChain-of-Thought出力をパースして構造化する同様のミドルウェア設計は、エージェントの推論過程をログ・監査証跡として記録する際に応用できる。

## アイデア

- `reasoning_tags`を外部パラメータとして設計することで、DeepSeek等のネイティブ推論モデルとプロンプト誘導モデルの両方を同一インターフェースで扱える抽象化が実現されている
- thinkingのdurationをstart/end時刻差分で計測し、UIに「Thought for N seconds」として表示する実装は、LLMの推論コスト可視化の簡易実装として参考になる
- エージェントの中間推論過程（`<think>`ブロック）をcontent_blocksとして構造化分離する設計は、監査エージェントの推論ログを証跡として保存するアーキテクチャに直接応用できる

## 前提知識

- **Chain-of-Thought** → /deep_59 EcoThink: 持続可能でアクセスしやすいエージェントのためのグリーン適応的推論フレームワーク
- **OpenWebUI** → /deep_2257 ローカルLLM + RAGでSlay the Spire 2の攻略アドバイザーを作った話：OpenWebUI実践記録
- **ストリーミングAPI** (TODO: 読むべき)
- **LLMプロンプトエンジニアリング** → /deep_1252 DSPyによる宣言的学習を用いたLLMプロンプトエンジニアリングの最適化
- **SSE/チャンクレスポンス** (TODO: 読むべき)

## 関連記事

- /deep_1928 隠れた真実を見抜く：フィールド可視化から記号的解析解を推論するVisual-to-Symbolic AI
- /deep_2366 質問と回答からLLMの思考過程を逆算合成する手法：REERの紹介
- /deep_972 論文「Learning to Reason with LLMs」を実運用視点で解説：企業導入で注意すべき5つのリスク
- /deep_861 蒸留モデルとは何か？ - DeepSeek R1の登場から1年で振り返るLLM知識蒸留の仕組みと実力
- /deep_1060 簡潔な方が良い：関数呼び出しエージェントにおけるChain-of-Thoughtの非単調な予算効果

## 原文リンク

[OpenWebUIの『Thinking...』は本当に推論しているのか？](https://zenn.dev/hitama/articles/bd3c771f6984ea)
