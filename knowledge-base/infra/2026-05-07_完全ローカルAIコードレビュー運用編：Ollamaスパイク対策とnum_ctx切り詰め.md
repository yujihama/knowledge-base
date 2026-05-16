---
title: "完全ローカルAIコードレビュー運用編：Ollamaスパイク対策とnum_ctx切り詰め"
url: "https://zenn.dev/motowo/articles/local-ai-code-review-operations"
date: 2026-05-07
tags: [Ollama, Gitea Actions, num_ctx, Apple Silicon, Metal GPU, コードレビュー, LLM推論, gemma4, ローカルLLM, num_gpu]
category: "infra"
related: [4029, 2950, 2257, 2691, 2105]
memo: "[Zenn LLM] 完全ローカル AI コードレビュー (3/3) 運用編：Ollama スパイク対策と num_ctx 切り詰め"
processed_at: "2026-05-07T21:11:50.136769"
---

## 要約

Gitea ActionsとOllamaを組み合わせたローカルAIコードレビューシステムの運用フェーズで発生する4つの主要障害（G8〜G11）とその対処法を症状別ランブック形式でまとめた記事。

【G8: Diff取得失敗】GitHubではなくGiteaのAPIエンドポイントを使う必要があり、取得失敗時はAPIレスポンスのステータスコードから原因を特定する。

【G9: num_ctxと文字列切り詰めの二重制約】ai_review.pyで100,000文字に切り詰めたDiffであっても、Ollamaのnum_ctx（デフォルト4096トークン）でさらに切り詰められる。「1文字≈0.25トークン」換算でnum_ctx×4-余裕バイトを切り詰め上限に揃えることが必要。270KB（約4,000行）の大PRでnum_ctx=4096のままだとレビューが「大量の繰り返しテキストが存在します」程度の抽象論に留まる。対策はnum_ctx=8192〜16384への引き上げ（KVキャッシュメモリーが2〜4倍）またはファイル別代表hunk抜粋への設計変更。

【G10: PAT90日期限切れ】Gitea Personal Access Tokenは90日で失効し、401 Unauthorizedでコメント投稿が止まる。カレンダーリマインダーによる定期ローテーションが必要。

【G11: Apple Silicon Ollamaの瞬間スパイク】OllamaはApple SiliconでデフォルトMetal GPU（num_gpu=-1の自動判定）を使うため、num_thread=4で絞ってもMetal側は制御できず、ollama serveのCPU使用率が瞬間数百%・メモリーが数GB跳ね上がる。CUDAのCUDA_VISIBLE_DEVICES=-1やAMDのROCR_VISIBLE_DEVICES=-1に相当するMetalの無効化envが存在しないため、/api/generateのoptions.num_gpu=0が実質唯一の手段。本プロジェクトではnum_gpu=0+num_thread=1+num_predict=384をai_review.pyに固定し、推論4〜6分の遅さを許容してスパイクを根絶。

E2Eテスト計測においては、AIコメント投稿自体がissue_commentイベントを再発火してskipped runを生む「自己発火問題」があり、run IDではなくissueコメントのcreated_at差分で所要時間を測定する必要がある。T1（小〜中PR）実測128秒、T4（パフォーマンス観点指定）実測104秒。ログはnohupのrunner.logが1週間で数GBになるためnewsyslogで10MB×5世代ローテを設定することを推奨。

## アイデア

- num_ctxとアプリ側の文字数切り詰めが独立した二重制約になっており、どちらか一方だけ調整しても品質が上がらない構造的な罠は、LLMをAPIでなくローカルで使う際に広く発生しうる問題
- Apple SiliconのMetalバックエンドにはCUDA_VISIBLE_DEVICES相当のenv変数が存在せず、per-requestのoptions.num_gpu=0が唯一の無効化手段という制約は、Ollamaを使ったエージェントの負荷制御設計に直接影響する
- Gitea ActionsはIF条件がfalseでもskipped runレコードを必ず作成する仕様のため、AIコメント投稿による自己発火skippedと区別するためにcreated_at差分計測が必要という計測設計の工夫

## 前提知識

- **Ollama** → /deep_52 SyGra Studio 紹介：合成データ生成のビジュアル・インタラクティブ環境
- **Gitea Actions** (TODO: 読むべき)
- **num_ctx / KVキャッシュ** (TODO: 読むべき)
- **Metal GPU（Apple Silicon）** (TODO: 読むべき)
- **Personal Access Token（PAT）** (TODO: 読むべき)

## 関連記事

- /deep_4029 完全ローカル AI コードレビュー (1/3) 設計編：Gitea × Ollama の基盤
- /deep_2950 同じOllama + qwen2.5-coderなのに動く/動かないが分かれる6つの構造的原因
- /deep_2257 ローカルLLM + RAGでSlay the Spire 2の攻略アドバイザーを作った話：OpenWebUI実践記録
- /deep_2691 カンニング用AIをアップグレードしようとしたら、RAGの限界にぶつかった話
- /deep_2105 VRAM 32GBのローカルLLM環境をコスパ重視で構築する：RTX 5060 Ti 16GB × 2枚刺し構成

## 原文リンク

[完全ローカルAIコードレビュー運用編：Ollamaスパイク対策とnum_ctx切り詰め](https://zenn.dev/motowo/articles/local-ai-code-review-operations)
