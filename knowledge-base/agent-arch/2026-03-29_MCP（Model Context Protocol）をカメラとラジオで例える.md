---
title: "MCP（Model Context Protocol）をカメラとラジオで例える"
url: "https://zenn.dev/tsukitsukiss/articles/cbb3a2fea3781e"
date: 2026-03-29
tags: [MCP, Model Context Protocol, LLMエージェント, Tools, Resources, Prompts, YOLO]
category: "agent-arch"
memo: "[Zenn LLM] MCP（Model Context Protocol）をカメラとラジオで例える"
related: [88, 1475, 11, 430, 889]
processed_at: "2026-03-29T22:06:42.162594"
---

## 要約

MCPの3要素（Resources・Tools・Prompts）をカメラ操作とラジオ受信という具体的なたとえで解説した入門記事。Resourcesは現在の状態データ（露出設定、受信強度など）の読み取り先、Toolsはシャッターや周波数ダイヤルのような実行可能な操作、Promptsは「逆光時は露出補正→再撮影」のような運用手順テンプレートに対応する。LLMの動作サイクルを「見る→考える→動かす→確認する」ループとして定式化し、YOLO等の認識モデルとの役割分担（YOLOで検出→LLM+MCPで判断・操作）も整理。MCPは自律AIそのものではなく、LLMが外部世界を安全に操作するための共通インターフェース規格であるという点を強調している。

## 要点

- MCPの3要素：Resources（状態読み取り）・Tools（処理実行）・Prompts（運用手順テンプレート）は、物理デバイス制御に例えると直感的に理解しやすい
- LLMエージェントの基本動作サイクルは「見る→考える→動かす→確認する」であり、MCPはこのループを外部システムと接続するための規格
- YOLOなど専用モデルとMCP+LLMは競合せず役割分担：高速検出はYOLO、状態評価と操作判断はMCP+LLMが担う
## 関連記事

- /deep_88 研究者向けMCP：AIを研究ツールに接続する方法
- /deep_1475 Zettelkastenに基づくLLMエージェントのメモリ設計：A-Mem論文解説
- /deep_11 MCPが9,700万DL、フロンティアモデル3連発 — AI業界週報 2026年第13週
- /deep_430 過去のセッションを必要時のみ参照する方針でclaude-memのトークン消費を激減させた話
- /deep_889 自律走行のための深層ニューラルネットワークを用いた道路工事検知システム

## 原文リンク

[MCP（Model Context Protocol）をカメラとラジオで例える](https://zenn.dev/tsukitsukiss/articles/cbb3a2fea3781e)
