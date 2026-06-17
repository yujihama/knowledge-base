---
title: "音声入力をすぐIssueにしない：AmiVoiceのtoken信頼度をGeminiに渡す前処理レイヤー"
url: "https://zenn.dev/hick/articles/dee1f9ce6fd44d"
date: 2026-06-17
tags: [AmiVoice, Gemini, token-confidence, 前処理レイヤー, 音声認識, LLM, TypeScript, Next.js, Issue自動化, 不確実性管理]
category: "agent-arch"
related: [7926, 6838, 3095, 4900, 7068]
memo: "[Zenn LLM] 音声入力をすぐIssueにしない：AmiVoiceのtoken信頼度をGeminiに渡す前処理レイヤー"
processed_at: "2026-06-17T09:03:51.100166"
---

## 要約

音声認識APIと生成AIを組み合わせた自動Issue起票は便利だが、音声認識の誤変換をLLMが自然な文章に整形してしまうため「綺麗だが間違ったIssue」が生成されるリスクがある。本記事はAmiVoice APIのtoken単位のconfidence情報とGemini APIを組み合わせ、音声入力をIssue化する前に不確実性を評価する前処理レイヤーのPoCをNext.js + TypeScriptで実装した記録。

AmiVoice APIの同期HTTPレスポンスはtokenごとのconfidenceを返す。発話全体のconfidenceが0.93と高くても、「リフィル」(0.21)、「リリース」(0.25)など技術用語tokenが局所的に低い場合がある。この観測に基づき、threshold 0.75未満を低信頼候補、0.6未満をcriticalとして低信頼語句を抽出する。句読点・単独ひらがな・記号tokenはノイズとして除外し、カタカナ・英字・数字を含む短語は技術用語候補として保持。連続する低信頼tokenはphrase化して最大8件に絞る。

抽出した低信頼語句は、Geminiへのプロンプトに専用ブロック（[critical]/[warning]ラベル付き）として渡す。Geminiは低信頼語句を確定情報として断定せず確認候補に分離しつつ、GO/HOLD/STOPの3段階でアクション判定を出力する。GOは再現条件・期待結果・実際の結果・影響範囲が揃っている場合に確認前提でIssue化を許可。HOLDは技術用語・コマンド・環境名に関わる低信頼語句が多い場合に調査メモへ倒す。STOPは材料不足で保存のみ。

判定はshouldCreateIssue: booleanを含むActionTriage型で構造化され、UIの主導線制御に使われる。重要な設計判断として、低信頼語句をLLMに自動補正させない方針を採用。誤った補正が自然な文章として固定されると、汚いメモより危険な「説得力のある誤情報」になるため、人間確認に戻すことを優先する。

実APIでのE2E確認により、全体confidence高でもtokenレベルで局所的に低いケースが実在することを確認。監査エージェント開発への示唆として、エビデンス収集や観察内容の記録においても同様のアプローチが有効。音声メモや非構造化入力をワークフローに取り込む際、LLMに断定させる前に不確実性を明示するレイヤーを挟む設計パターンは、誤った前提に基づくアクション実行を防ぐ上で重要。

## アイデア

- 発話全体のconfidenceではなくtoken単位のconfidenceで局所的な不確実性を検出し、LLMの入力情報として明示的に渡すことで、LLMの「補完能力」が誤情報の固定化に働くリスクを抑制できる
- GO/HOLD/STOPの三値判定を「低信頼語句の有無」単体ではなく「低信頼語句×情報充足度」の積で決める設計は、単純なconfidence閾値ルールより実用的なトリアージを実現する
- LLMに自動補正させず人間確認に戻す方針（補正より不確実性の可視化を優先）は、監査や法的文書など「間違いのコストが高い」ドメインでのLLM活用全般に応用できる設計原則

## 前提知識

- **AmiVoice API** → /deep_7176 AmiVoice APIとLLMで作る声の公開レビューゲート
- **token-level confidence** (TODO: 読むべき)
- **Gemini API** → /deep_1736 ハーネスエンジニアリングに挑戦し、AIテニスコーチアプリをAIと作った話
- **structured output (LLM)** (TODO: 読むべき)
- **Next.js** → /deep_90 CoDD（整合性駆動開発）活用ガイド #1: spec.md → 設計書 → コードの全ステップ解説

## 関連記事

- /deep_7926 音声メモをそのままチケットにしない — AmiVoice APIと生成AIで作る声のIssue下書き
- /deep_6838 AmiVoice API × 生成AIで「音声だけで使える問い合わせフォーム」を作ってみた
- /deep_3095 伏線エンジンの設計 — 計画的伏線とAI自動生成を両立させる
- /deep_4900 マルチモーダル寄りの拡張可能コミュニケーションアバターを作ってみた（Unity × Python × LLM × 音声）
- /deep_7068 AmiVoiceとLLMで音声情報を取得・要約する実装ガイド（Next.js BFF構成）

## 原文リンク

[音声入力をすぐIssueにしない：AmiVoiceのtoken信頼度をGeminiに渡す前処理レイヤー](https://zenn.dev/hick/articles/dee1f9ce6fd44d)
