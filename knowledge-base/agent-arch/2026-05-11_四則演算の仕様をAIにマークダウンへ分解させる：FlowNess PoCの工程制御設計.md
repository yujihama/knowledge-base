---
title: "四則演算の仕様をAIにマークダウンへ分解させる：FlowNess PoCの工程制御設計"
url: "https://zenn.dev/hiro51282/articles/236112f8ff6853"
date: 2026-05-11
tags: [FlowNess, Gemini API, LLM工程制御, Stateマシン, 仕様分解, ValidationNode, PoCアーキテクチャ]
category: "agent-arch"
related: [1736, 407, 4187]
memo: "[Zenn LLM] 四則演算の仕様をAIにマークダウンに分解してもろた"
processed_at: "2026-05-11T09:10:57.139766"
---

## 要約

FlowNessというアーキテクチャ構想に基づき、LLM（Gemini API）を「工程の一部」として制御する実験的PoCの報告。入力としてrequirement.mdを受け取り、AIが四則演算APIの仕様をadd.md・sub.md・mul.md・div.mdの4ファイルに分解して出力するパイプラインを実装した。

パイプラインはStateベースのデータフローで構成され、4つのノード（DecompositionNode・ValidationNode・ApprovalNode・ExecutorNode）が順次処理を担当する。DecompositionNodeがGemini APIを呼び出し、LLMの出力をjson.loads()でパースして構造化データ化する。ValidationNodeはフォーマット成立の確認のみ（今回はゆるいチェック）。ApprovalNodeは単純なルールベースでOK/NGを判定。ExecutorNodeは分解済み仕様をファイルとして書き込むが、LLM出力の内容自体には関与しない。

ノード間の情報受け渡しはstateのみに限定し、各ノードは「stateを受け取り→処理→stateを返す」という契約で動作する。これによりLLMの生成をそのままシステムに適用せず、制御された工程として扱う構造を検証している。

PoCゆえの割り切りとして、EXPECTED_KEYSのハードコード（四則演算専用）、Stateがdictベースで型なし、Nodeインターフェースが暗黙的（runメソッドの契約がコード上に非表現）、Validation失敗時のRetry/Rollback未定義といった課題を自覚的に列挙している。

今後の拡張課題として「コード生成への応用」を想定しており、LLM出力にコードと自然言語説明が混在する問題（自然言語混入問題）への対処として、Executor前に「コード抽出層」を追加し、コードブロック（```で囲まれた部分）のみを取得・形式チェック・差分生成するレイヤーを設ける方向性を示している。

監査エージェント開発への示唆：LLMを直接信用せず「生成」と「適用」の間に制御層を挟む設計は、監査ワークフローにおけるAI出力の検証フェーズ設計と直結する。ValidationNode・ApprovalNodeの責務分離と、Retry/Rollback戦略の未定義という課題は、監査エージェントのエラー回復設計でも同様に直面する論点である。

## アイデア

- LLMを『生成器』ではなく『工程ノード』として扱い、出力をJSONパース→Validation→Approvalの順で制御する設計パターンは、LLMの非決定性をパイプライン構造で吸収する実用的アプローチ
- 『自然言語混入問題』（LLMがコードに説明文を混入させる）への対処としてExecutor前にコード抽出層を追加する発想は、コード生成エージェント全般に適用可能な防御的設計原則
- Stateがdictベースで型なし・Nodeインターフェースが暗黙的という自覚的な技術的負債の列挙は、PoCから本番設計へ移行する際のPydanticモデル導入やプロトコル定義の必要性を明示しており、LangGraph設計との比較検討素材になる

## 前提知識

- **Gemini API** → /deep_1736 ハーネスエンジニアリングに挑戦し、AIテニスコーチアプリをAIと作った話
- **Stateベースデータフロー** (TODO: 読むべき)
- **LLMパイプライン設計** (TODO: 読むべき)
- **JSONスキーマ検証** (TODO: 読むべき)
- **ノードアーキテクチャ** (TODO: 読むべき)

## 関連記事

- /deep_1736 ハーネスエンジニアリングに挑戦し、AIテニスコーチアプリをAIと作った話
- /deep_407 API vs ローカルLLM、感覚で選ぶのをやめるための判断フレームワーク
- /deep_4187 AIコーディングで「なんか思想強め」なリポジトリが爆誕した件：FlowNessという工程設計の考え方

## 原文リンク

[四則演算の仕様をAIにマークダウンへ分解させる：FlowNess PoCの工程制御設計](https://zenn.dev/hiro51282/articles/236112f8ff6853)
