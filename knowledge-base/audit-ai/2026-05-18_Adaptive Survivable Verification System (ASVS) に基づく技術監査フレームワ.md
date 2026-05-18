---
title: "Adaptive Survivable Verification System (ASVS) に基づく技術監査フレームワーク"
url: "https://zenn.dev/kafka2306/articles/5c3c93f798da3f"
date: 2026-05-18
tags: [ASVS, LLM-as-judge, 継続的監査, 証拠階層, ランタイムドリフト, フェイルクローズ, in-toto, Sigstore, SLSA, OWASP]
category: "audit-ai"
related: [23, 21, 3343, 251, 5496]
memo: "[Zenn LLM] Adaptive Survivable Verification System (ASVS) に基づく技術監査フレームワーク"
processed_at: "2026-05-18T09:07:54.358954"
---

## 要約

現代のAI統合・マイクロサービス環境では、システムが「非決定論的」な挙動を内包し、従来の静的文書ベース監査では「ランタイム・ドリフト」を捉えられない。本記事はこの問題に対し、Adaptive Survivable Verification System (ASVS) という継続的証拠ベース検証フレームワークを提示する。

ASVSのメタ原則は「壊れ続ける現実世界での検証可能性維持」であり、6つの核心原則を定める：①Runtime Overrides Assumptions（実行状態を真実として優先）、②Reality Overrides Documentation（READMEやLLM要約は証拠にならない）、③Official Specifications Override Local Assumptions（RFC・API定義等の公式仕様を優先）、④Observability Is Mandatory（観測不能なシステムは監査不能）、⑤State and Time Matter（長期的状態遷移・継続性・ドリフトを対象にする）、⑥Survivability Over Snapshot Correctness（点の正しさより継続的生存性を重視）。

証拠は4階層で評価される：Tier 0（直接的実行証拠：終了コード、APIレスポンス、ハッシュ値）、Tier 1（構造的証拠：ソースコード、IaCマニフェスト、Lockfile）、Tier 2（記述的証拠：README、ADR）、Tier 3（推論的証拠：LLM要約、人間の主観）。Tier 2/3のみでのPASS判定は明示的に禁止される。

22段階のUniversal Verification Workflowは3フェーズで構成される：Phase 1（Steps 1-9）でドメイン特定と期待値抽出、Phase 2（Steps 10-18）で仕様と現実の整合性検証、Phase 3（Steps 19-22）で失敗分析・修復・機械可読レポート（JSON/YAML）生成を行う。

LLM評価には固有バイアス（Self-enhancement bias、Position/Verbosity bias、Limited reasoning ability）が存在するため、確率的評価と決定論的な検証コードを組み合わせるハイブリッド検証を必須とする。また、OWASP LLM10「Unbounded Consumption」対策として検証予算ガバナンスを設け、最大トークン予算・最大再帰深度・最大修復試行回数を強制する。証跡管理はRFC 6962・Sigstore・in-toto Link Metadataの概念を採用しMerkle Treeで改ざん検知可能とする。

監査エージェント開発への示唆として、LangGraph等で実装する自律型監査エージェントにASVSの証拠階層とフェイルクローズ設計を組み込むことで、LLM-as-judgeのバイアス問題を構造的に制御し、証拠なしにPASSを出さない信頼性の高い監査システムを構築できる。

## アイデア

- 証拠を4階層（実行証拠→構造的証拠→記述的証拠→推論的証拠）に分類し、Tier 2/3のみでのPASS判定を明示禁止する設計は、LLMが生成する要約や説明を証拠として使いがちな監査エージェントの根本的な欠陥を突いている
- OWASP LLM10のUnbounded Consumptionをフレームワーク設計に取り込み、検証予算（トークン・再帰深度・修復試行回数）を強制停止条件として組み込む点は、自律エージェントのリソース制御設計に直接応用可能
- RFC 6962（Certificate Transparency）とin-toto Link MetadataをAI監査の証跡管理に転用し、STDOUT/STDERR/入出力ハッシュ・実行環境を署名付きで記録する「改ざん耐性のある監査ログ」のアーキテクチャは、GRC領域での監査証跡要件を技術的に充足する具体的手法

## 前提知識

- **LLM-as-judge** → /deep_3 Claude Code のAIチームでLLMの品質を自動でチェックする方法
- **SLSA / サプライチェーンセキュリティ** (TODO: 読むべき)
- **in-toto / Sigstore** (TODO: 読むべき)
- **OWASP LLM Top 10** → /deep_2543 【実装】あなたのAIアシスタント、一文でハイジャックされてます——PythonでPrompt Injection検出ゲートを作る
- **ISO 19011 監査原則** (TODO: 読むべき)

## 関連記事

- /deep_23 音声エージェント評価のための新フレームワーク EVA
- /deep_21 部分の総和を超えて：マルチモーダルヘイトスピーチ検出における意図変化の解読
- /deep_3343 誰の物語が語られるか？LLMによる生活語りの要約におけるポジショナリティとバイアス
- /deep_251 証明可能なプライバシーを保証するAI利用インサイト取得システム（Google Research）
- /deep_5496 記憶を持ったAIが次に記憶を整理しはじめた：AnthropicのDreamingとOutcomesの設計

## 原文リンク

[Adaptive Survivable Verification System (ASVS) に基づく技術監査フレームワーク](https://zenn.dev/kafka2306/articles/5c3c93f798da3f)
