---
title: "同じOllama + qwen2.5-coderなのに動く/動かないが分かれる6つの構造的原因"
url: "https://zenn.dev/zephel01/articles/799e9707e51040"
date: 2026-04-25
tags: [Ollama, Claude Code, qwen2.5-coder, num_ctx, num_predict, SSE, tool_use, reasoning-leak, CodeRouter, ローカルLLM]
category: "infra"
related: [2404, 2209, 2257, 2691, 2105]
memo: "[Zenn LLM] 同じ Ollama + qwen2.5-coder なのに、なぜ人によって動く / 動かないが分かれるのか"
processed_at: "2026-04-25T12:46:41.695521"
---

## 要約

ローカルOllama + Claude Codeの構成で、同一モデル・同一Ollamaバージョンを使ってもユーザーによって動作の有無が分かれる問題を、CodeRouterのdoctor --check-modelが実装する6プローブで体系的に診断する手法を解説した記事。

観測される失敗症状は「タイムアウト」「途中で切れる」「tool未呼出し」「JSONパース破壊」「thinkingタグ漏れ」「応答品質低下」の6種類以上あるが、症状と原因は1:1対応しないため、ヒューリスティクスでなく実地プローブで因果を切り分けることが唯一の安定解とされる。

6プローブの概要は以下の通り。①authプローブ: Ollamaは未知ヘッダを無視するため「Bearer dummyでも200を返す」という誤判定を避けるため、base_urlが:11434か否かでauth検証をスキップ。②num_ctxプローブ: Ollamaのnum_ctx既定値は2048であり、Claude Codeの初期プロンプト（5K〜10Kトークン）がサイレントに先頭から切り詰められる。対策として32文字のランダム16進文字列をcanaryとしてプロンプト先頭に置き、末尾でエコーを指示して切り詰め有無を判定する。num_ctx: 32768のYAMLパッチを自動提示。③toolsプローブ: get_timeのような単純なtoolを使って実際のtool_calls形式が正しく返るかを確認。引数名の誤訳・生テキスト出力・nullなど複数のNGパターンを識別。④streamingプローブ: num_predictの既定値が古いバージョンでは128と短く、tool呼び出しを含む応答がfinish_reason: lengthで途中切断される。「1から30まで数える」テストでfinish_reasonと数字個数を確認し、num_predict: 4096パッチを提示。⑤reasoning-leakプローブ: DeepSeek-R1蒸留系・QwQ・Qwen3などが出力する<think>タグ、非標準フィールドmessage.reasoning、stop marker（<|eot_id|>等）を、CodeRouterの通常アダプタを経由せずhttpxで直叩きして生ボディを観測。アダプタのstrip層を通すと漏れを検出できないため。⑥anthropic-thinkingプローブ: Claude 3.7以降のthinking: {type: "enabled"}フィールドを古いHaikuモデルに送ると400エラーになるため、200/400で capability有無を判定しYAMLへパッチ提案。

プローブの順序はauth→num_ctx→tools→streaming→reasoning→thinkingの順で固定されており、根本原因から順に診断することで誤帰責を防ぐ。v0.7B以前はtools NGをモデルのcapability不足と誤判定していたが、canaryプローブ挿入（v1.0-B）でnum_ctxが真因だったケースの誤パッチが解消された。終了コードは0=全OK・1=UNREACHABLE・2=NEEDS_TUNINGと区別されCIに組み込める。監査エージェント開発観点では、ローカルLLMのプロンプト切り詰めや出力切断はエージェントのtool利用失敗に直結するため、num_ctx/num_predictのチューニングとプローブ検証の仕組みはLangGraphベースのエージェント実装でも参考になる。

## アイデア

- 「canaryをプロンプト先頭に埋め、末尾でエコーを指示する」というnum_ctx診断手法は、学習データに存在しないランダム16進文字列を使うことでモデルの知識ではなくコンテキスト窓の物理的な切り詰めを直接観測できる点が巧妙
- CodeRouterのreasoning-leakプローブが自社のアダプタを経由せずhttpxで直叩きする設計は「自分のプロダクト内部を信用せず1枚下のレイヤを観測する」というプローブ設計原則を体現しており、診断ツール全般に応用できる
- プローブの順序をauth→num_ctx→tools→streaming→reasoning→thinkingと「パイプラインの上流から」固定することで、後段プローブのNG原因が前段の未解決問題に誤帰責されるのを防ぐ依存グラフ的な診断設計

## 前提知識

- **Ollama** → /deep_52 SyGra Studio 紹介：合成データ生成のビジュアル・インタラクティブ環境
- **OpenAI Chat Completions API** (TODO: 読むべき)
- **SSE（Server-Sent Events）** (TODO: 読むべき)
- **tool_use / function calling** (TODO: 読むべき)
- **context window** (TODO: 読むべき)

## 関連記事

- /deep_2404 ローカルドキュメントをAIで横断検索しレポート作成 — Local Knowledge RAG MCP Server 入門
- /deep_2209 書類からのテキスト抽出精度をオープンソースのAIモデルで比較してみた
- /deep_2257 ローカルLLM + RAGでSlay the Spire 2の攻略アドバイザーを作った話：OpenWebUI実践記録
- /deep_2691 カンニング用AIをアップグレードしようとしたら、RAGの限界にぶつかった話
- /deep_2105 VRAM 32GBのローカルLLM環境をコスパ重視で構築する：RTX 5060 Ti 16GB × 2枚刺し構成

## 原文リンク

[同じOllama + qwen2.5-coderなのに動く/動かないが分かれる6つの構造的原因](https://zenn.dev/zephel01/articles/799e9707e51040)
