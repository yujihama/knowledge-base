---
title: "ローカルLLM専用フォーク「ClosedCode」をビルドレス・ピュアvanilla JSで作っている話"
url: "https://zenn.dev/nicktominaga/articles/vanilla-closedcode"
date: 2026-06-08
tags: [ClosedCode, opencode, ローカルLLM, Ollama, vanilla JS, SolidJS, Electron, build-less, native ESM, MVC]
category: "infra"
related: [2862, 4618, 5037, 7794, 4911]
memo: "[Zenn LLM] ローカルLLM専用フォーク「ClosedCode」をビルドレス・ピュアvanilla JSで作っている話"
processed_at: "2026-06-08T12:01:16.660223"
---

## 要約

opencodeをフォークした「ClosedCode」は、LLMの通信経路をローカル／プライベートネットワークに限定したAIコーディングワークスペースツール。リポジトリ名に「vanilla」を冠し、TypeScript・JSX・ビルドステップを一切持たないという設計上のハードルールを課している。

「Closed」の意味は、OllamaやLM Studio、llama.cpp、vLLMなどOpenAI互換のローカルエンドポイントのみを対象とし、パブリックホストへのLLMリクエストを実行時にブロックすること。設定はJSONで行い、例えばOllamaなら`http://127.0.0.1:11434/v1`を指定する。Git/GitHub/MCPサーバ等LLM以外の通信はポリシー対象外。

アーキテクチャは古典的なMVC3層構成。Model（エンジン・HTTPサーバ・エージェントループ、esbuildビルド）、View（SolidJS UIレンダラ、build-less）、Controller（Electronのmain/preload、build-less）に分離。ポイントはGUIとCLIが同一エンジン（M）への兄弟フロントエンドであり、ControllerがModelをサイドカーとして起動し、ViewはHTTP SDK経由でModelと通信する設計。

「build-less」と「pure vanilla」は別概念として明確に区別している。build-lessはJSX/TSコンパイルもバンドラも不要でsrc下の.jsがそのまま動く状態（VとCは達成済み）。pure vanillaはカスタムリゾルバや互換レイヤーなし・標準ESMのみで動く状態（いずれの層も未達成）。現状は`@/foo`形式のパスエイリアス、bare importの解決、`oc://`プロトコルリゾルバ、esbuildビルドなどに依存している。

標準化はStage 1〜5で段階的に進める計画：CLIのimport alias標準化（package.json#imports）→アセット・.scmのfs標準API化→レンダラのimport maps＋native ESM化→main/preloadの非標準処理除去→esbuild依存削減。effect/ai-sdk/tree-sitter等の第三者依存が内部にCJS時代の非標準importを抱えるため、100%machinery-freeは目標としない。自前コードのみ標準ESMへ移行し、第三者依存にだけ薄いinterop層を残す現実的な落とし所を設定している。

UIソースの可読性課題として、SolidJSのJSXコンパイラ出力相当のコードをvanilla JSで手書きしているため、firstChild/nextSiblingによる位置依存のDOM配線が残存している。テンプレートにはdata-slotマーカーがあるにもかかわらず使われていない。これをquerySelectorへ置き換え、replaceChildren/addEventListenerで素直に書き直すことが残課題。

## アイデア

- LLMリクエストのみをランタイムでブロックしつつ、Git/MCPなど他の通信は許可するという粒度の細かいネットワークポリシー設計
- TypeScript・JSX・バンドラを排除した上でSolidJSのプレーンJSランタイムAPI（template/createComponent/insert/effect）を直接使いUIを構築するアプローチ
- GUIとCLIを同一エンジンへの兄弟フロントエンドとして設計することで、CLIとデスクトップアプリの機能分岐を防ぐアーキテクチャ

## 前提知識

- **Ollama** → /deep_52 SyGra Studio 紹介：合成データ生成のビジュアル・インタラクティブ環境
- **OpenAI互換API** → /deep_4183 DeepSeek V4 APIでAIエージェントを作る完全ガイド【2026年版】
- **SolidJS** (TODO: 読むべき)
- **Electron IPC** (TODO: 読むべき)
- **native ESM / import maps** (TODO: 読むべき)

## 関連記事

- /deep_2862 Qwen3-235B-A22B を OpenCode と Ollama でローカル運用する超初心者向けガイド
- /deep_4618 AIで爆速Mermaid図生成！ローカル動作のデスクトップアプリ「DiagramBuilder」を作った
- /deep_5037 自分のトーン規約を渡してOllamaにZenn下書きを点検させる
- /deep_7794 自作サイバーダッシュボードでAI相棒と会話する――ゼロから構築した記録
- /deep_4911 社内ローカルLLM構築：用途別ハードウェア選定ガイド（CPU vs GPU、Qwen3.5シリーズ対応）

## 原文リンク

[ローカルLLM専用フォーク「ClosedCode」をビルドレス・ピュアvanilla JSで作っている話](https://zenn.dev/nicktominaga/articles/vanilla-closedcode)
