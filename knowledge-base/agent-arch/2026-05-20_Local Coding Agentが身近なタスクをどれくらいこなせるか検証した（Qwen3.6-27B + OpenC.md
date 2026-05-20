---
title: "Local Coding Agentが身近なタスクをどれくらいこなせるか検証した（Qwen3.6-27B + OpenCode）"
url: "https://zenn.dev/aishift/articles/5b048ff347fd7b"
date: 2026-05-20
tags: [Qwen3.6-27B, OpenCode, Local LLM, Coding Agent, mlx-lm, SWE-bench, 4bit量子化, TypeScript, Vibe Coding]
category: "agent-arch"
related: [1424, 3898, 2889, 3095, 5726]
memo: "[Zenn LLM] Local Coding Agent が身近なタスクをどれくらいこなせるのかを検証した"
processed_at: "2026-05-20T21:01:20.201794"
---

## 要約

MacBook Pro M3 Max 64GB上でQwen3.6-27B（4bit量子化、約24GB）をmlx-lmで推論サーバとして起動し、OpenCodeをharnessとして接続するLocal Coding Agent環境を構築。TypeScript + React + Honoで構成したダミーリポジトリに対し、性質の異なる6タスクを投入して実用性を検証した。

対象タスクは「ヘッダー整列（局所UI編集）」「クエリ正規化（入力正規化＋境界値テスト）」「URL自動判定（関数切り出しと既存コードへの接続）」「上限設定（既存レイヤー構造の把握）」「フィルタリング（API/Web/自動生成clientの三層同期）」「CRUD（0→1フルスタック実装）」の6種で、いずれも最初から失敗するテストを仕込みAgentがそれを通せばPassとした。

結果は全6タスクPass。所要時間は6分59秒〜45分40秒で、複雑なタスクほど長時間を要した。特にCRUDは45分超、フィルタリングは35分近くかかった。実装品質はおおむね妥当だったが、クエリ正規化ではz.enumに固執して失敗した後にアプローチを切り替える挙動、フィルタリングではAPI層・Web層・自動生成client層の三層を横断した同期修正に成功した点が注目される。

モデル比較として、フロンティアモデルのClaude Opus 4.7はSWE-bench Verifiedで87.6%を記録する一方、Qwen3.6-27BはOpen Weightモデルとして77.2%を達成し、64GB MacBook上で現実的に動作するサイズに収まる。Hacker News上ではM5 Pro 128GBで「20GBしか使わなかった」との報告もあり、32GB機でも動作可能な可能性が示唆されている。

OpenCodeを選択した理由はOpenAI互換エンドポイントを指定するだけでLocal Modelに対応できる実装容易さで、Claude Code・Aider等との差別化ポイントとして機能する。本検証はSWE-benchのスコアと手元リポジトリでの実用性のギャップを埋める実証として価値があり、ローカルLLMによるCoding Agentが「趣味レベルを超えた実務近傍タスク」に対応できることを示している。監査エージェント開発においても、コードレビュー支援や定型的な実装タスクの自動化にLocal LLM + Coding Agentを活用できる可能性がある。

## アイデア

- Qwen3.6-27Bを4bit量子化すると約24GBに収まり、64GB MacBook上でフルスタックのCoding Agentタスクが全Pass可能なことが実証された点—クラウドAPIなしでの実務近傍タスク自動化の現実性が示された
- フィルタリングタスクでAPI層・Web層・自動生成client層の三層を横断した同期修正に成功した点—単一ファイル編集を超えた多層アーキテクチャ理解がLocal LLMでも機能することを示す
- OpenCodeのOpenAI互換エンドポイント設計により、モデルを差し替えるだけで同じharnessをフロンティアモデルとLocal LLMの両方に使える構成—Coding Agent評価の再現性と比較容易性を高める設計思想

## 前提知識

- **SWE-bench** → /deep_62 LLMチャットボットに欠けているもの：目的意識（Purposeful Dialogue）
- **量子化（4bit）** (TODO: 読むべき)
- **OpenAI互換API** → /deep_4183 DeepSeek V4 APIでAIエージェントを作る完全ガイド【2026年版】
- **Coding Agent harness** (TODO: 読むべき)
- **mlx-lm** → /deep_5726 ローカルLLMって本当に開発に使える？（４）LoRA編 — Swift監査の誤検知を93%削減した話

## 関連記事

- /deep_1424 AIへの指示専用エディタ「TansenEditor（鍛洗エディタ）」を自作した話
- /deep_3898 階層型記憶3層設計 — LLMの「忘れる」問題を設計で解く
- /deep_2889 現在のAIの状況を理解するためのチャート集：Stanford AI Index 2026レポート解説
- /deep_3095 伏線エンジンの設計 — 計画的伏線とAI自動生成を両立させる
- /deep_5726 ローカルLLMって本当に開発に使える？（４）LoRA編 — Swift監査の誤検知を93%削減した話

## 原文リンク

[Local Coding Agentが身近なタスクをどれくらいこなせるか検証した（Qwen3.6-27B + OpenCode）](https://zenn.dev/aishift/articles/5b048ff347fd7b)
