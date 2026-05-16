---
title: "未経験者がVRAM 16GBでAIキャラの台本生成を動かすまで（第1回）── VRAM不足という当たり前の壁"
url: "https://zenn.dev/isa_memoria/articles/1a026f31eb746f"
date: 2026-05-02
tags: [Ollama, Qwen3, VRAM, ローカルLLM, 量子化, RTX 5080, Tauri, Style-Bert-VITS2]
category: "infra"
related: [2105, 2862, 394, 2209, 2696]
memo: "[Zenn LLM] 未経験者がVRAM 16GBでAIキャラの台本生成を動かすまで(第1回) ── まずは「VRAM不足」という、当たり前の壁🤖"
processed_at: "2026-05-02T12:39:13.263235"
---

## 要約

プログラミング未経験から3週間の開発者が、完全ローカル環境でオリジナルAIキャラクター「イーサ・メモリア」がしゃべるYouTube動画を自動生成するWindowsデスクトップアプリを構築した記録の第1回。技術スタックはTauri(Rust)+React+TypeScript+Python/FastAPIのSidecar構成で、LLMにQwen3:14b（Ollama経由）、TTSにStyle-Bert-VITS2（GPU駆動、0.57秒/短文）、動画合成にFFmpegを採用。台本生成パイプラインは「トピック入力→あらすじ3案生成（7秒）→ユーザー選択→本格台本JSON生成（15秒）」の構成で、現時点では合計22秒で感情タグ・SEタグ付きJSONを出力できている。

最初の壁はVRAMとモデルサイズの不一致。当初Qwen3.6:27B（Q4_K_M量子化済み、17GB）をRTX 5080（VRAM 16GB）で動かそうとしたが、台本生成エンドポイント実装後にタイムアウトが多発。`ollama list`・`ollama show`・`nvidia-smi`の3コマンドで状態確認したところ、モデルサイズがVRAMを1GB超過し、推論時にモデルの一部がRAMにスワップされていたことが判明。VRAM使用量はわずか1.8GB/16GBで、大半がRAMに退避していた。Q3等へのさらなる量子化では品質が極端に劣化するため、27Bの採用を断念しQwen3:14bへ移行することで解決。

この経験から「動かない時はまず状態を測る」という原則を学んだことが記事の主題。監査エージェント開発への示唆としては、ローカルLLM推論基盤を構築する際にモデルサイズ×量子化レベル×VRAMの三者関係を事前に試算する重要性が挙げられる。RTX 3090（VRAM 24GB）であれば27B Q4_K_Mが完全にVRAMに収まり、RAMスワップなしで動作するため、重い推論タスク（LangGraphの多段エージェント等）に適している。続編ではプロンプトの一文字変更でキャラクター人格が変わる問題と、抽象的な指示が機能しない問題を扱う予定。

## アイデア

- VRAM 16GBでQ4_K_M量子化済み17GBモデルを動かそうとすると推論がRAMスワップで激遅化する——モデルサイズの計算は事前必須であり、わずか1GBのはみ出しでも実用不可レベルのタイムアウトが生じる
- claude.aiを設計・戦略、Gemini 3 Proを実装・デバッグと役割分担する多重AI支援体制——未経験者がAIエージェント群をオーケストレートする実践例として、エージェント協調設計の具体的ユースケース
- Tauri(Rust)+FastAPI Sidecar構成によるローカルLLMデスクトップアプリ——Webフロントエンド・Pythonバックエンド・Rustシェルを一体化した構成は、ローカルAIツール構築のテンプレートとして参照価値が高い

## 前提知識

- **Ollama** → /deep_52 SyGra Studio 紹介：合成データ生成のビジュアル・インタラクティブ環境
- **VRAM量子化（Q4_K_M）** (TODO: 読むべき)
- **GPU推論とRAMスワップ** (TODO: 読むべき)
- **Tauri/Sidecar構成** (TODO: 読むべき)
- **ローカルLLM推論** (TODO: 読むべき)

## 関連記事

- /deep_2105 VRAM 32GBのローカルLLM環境をコスパ重視で構築する：RTX 5060 Ti 16GB × 2枚刺し構成
- /deep_2862 Qwen3-235B-A22B を OpenCode と Ollama でローカル運用する超初心者向けガイド
- /deep_394 OpenClaw × OllamaをMacBook 16GBで動かす - ローカルLLM入門
- /deep_2209 書類からのテキスト抽出精度をオープンソースのAIモデルで比較してみた
- /deep_2696 日本語入力システムSumibiの開発 part18: ローカルLLMが閾値を超えたかも

## 原文リンク

[未経験者がVRAM 16GBでAIキャラの台本生成を動かすまで（第1回）── VRAM不足という当たり前の壁](https://zenn.dev/isa_memoria/articles/1a026f31eb746f)
