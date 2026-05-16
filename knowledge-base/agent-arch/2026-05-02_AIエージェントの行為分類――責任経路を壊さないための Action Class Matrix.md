---
title: "AIエージェントの行為分類――責任経路を壊さないための Action Class Matrix"
url: "https://zenn.dev/dantarg/articles/7ee72995004c90"
date: 2026-05-02
tags: [Action Class Matrix, Responsibility Pathway Layer, エージェント設計, ツール権限, Emergency Stop, 可逆性, 承認設計, プロンプトインジェクション]
category: "agent-arch"
related: [3510, 2203, 1035, 665, 1867]
memo: "[Zenn LLM] AIエージェントの行為分類――責任経路を壊さないための Action Class Matrix"
processed_at: "2026-05-02T12:38:09.079091"
---

## 要約

本記事は、AIエージェントが持つツール実行能力を「責任経路（Responsibility Pathway Layer）」に乗せるための行為分類フレームワーク「Action Class Matrix」を提案する。

AIエージェントはWebアクセス・ファイル更新・API呼び出し・外部メール送信など多様な行為を同一フロー内で実行できる。しかし行為を一律に「AIが実行した」と扱うと、責任の所在・承認要否・ログ設計が曖昧になり、事故後の説明が困難になる。これを防ぐため、行為を影響範囲・可逆性・外部性・承認要否の4軸で6クラスに分類する。

**Class A（Observe-Only）**: WebページやドキュメントのRead専用行為。原則許可だが、読んだ内容を命令として扱うプロンプトインジェクション（入力汚染）リスクに注意が必要。

**Class B（Suggest-Only）**: 要約・分析・提案のみ。実行とは分離し、提案の採用可否を別の責任経路で判断することで「AIの提案がいつの間にか人間の判断になる」問題を防ぐ。

**Class C（Approval-Required）**: ドキュメント更新・チケットステータス変更・リポジトリコミット等の内部状態変更。変更内容・理由・担当者・変更前復元可否・変更履歴の5点を明確化した上で承認点を設ける。

**Class D（Reversible External Action）**: 外部共有ドキュメント更新・顧客ドラフト共有・外部通知送信など、原則ロールバック可能な外部影響行為。承認者・実行者・実行ログ・ロールバック方法・影響範囲・異常時連絡先の6点が必須。

**Class E（Irreversible or High-Impact Action）**: 外部メール送信・本番DB更新・権限設定変更・契約・採用・請求関連通知など不可逆または高影響行為。AIが自律実行してよい領域ではなく、組織責任者による強い人間承認・二重確認・実行ログ・ロールバック可否確認・修復責任者の明示が必要。

**Class F（Emergency Stop）**: 実行権限とは独立して定義する停止権限。ツール呼び出し停止・セッション隔離・権限剥奪・人間確認への復帰などをカバーする。実行したい主体が停止判断も持つと停止が遅れるため、安全責任者が独立して保有すべき権限として設計する。

各クラスはResponsibility Pathway Layerと接続され、Decision Owner・Approval Gate・Execution Actor・Evidence Log・Human Return Pointが異なる設計になる。監査エージェント開発においては、内部統制上の変更操作（Class C/D）と不可逆なレポート・通知配信（Class E）の境界設計が特に重要であり、ツール権限モデル・承認UI・実行ログスキーマ・ロールバック設計・Stop Authority発火条件を行為クラスに対応させることがエンタープライズ運用の前提となる。

## アイデア

- 行為分類を『危険か否かの判定』ではなく『どの責任経路を通すかの前処理』と定義することで、承認コストと安全性のトレードオフを行為クラスごとに最適化できる設計思想
- Emergency Stop権限を実行権限と分離し独立した安全責任者に帰属させる設計は、AIエージェントの自律性が高まるほど重要性が増す構造的な安全機構
- Suggest-Only（Class B）と実行クラスの明示的分離により、AIの提案が暗黙的に人間の意思決定として処理される『責任の滲み出し』問題を構造的に防止できる

## 前提知識

- **Responsibility Pathway Layer** → /deep_3510 Responsibility Pathway Layer――AIエージェントに責任経路を実装する最小構成
- **AIエージェント ツール呼び出し** (TODO: 読むべき)
- **Human-in-the-loop** → /deep_24 1対1を超えて：動的な人間とAIのグループ会話のオーサリング・シミュレーション・テスト
- **プロンプトインジェクション** → /deep_31 プロンプトインジェクションに対抗するAIエージェントの設計
- **LangGraph** → /deep_28 IBMとUC BerkeleyがIT-BenchとMASTを使ってエンタープライズエージェントの失敗原因を診断

## 関連記事

- /deep_3510 Responsibility Pathway Layer――AIエージェントに責任経路を実装する最小構成
- /deep_2203 自律型AIエージェントが生む新たな攻撃面：認証情報漏えいとプロンプトインジェクションのリスク
- /deep_1035 直交性を超えて：徳倫理学的エージェンシーとAIアラインメント
- /deep_665 直交性を超えて：徳倫理学的エージェンシーとAIアライメント
- /deep_1867 直交性の先へ：徳倫理的エージェンシーとAIアライメント

## 原文リンク

[AIエージェントの行為分類――責任経路を壊さないための Action Class Matrix](https://zenn.dev/dantarg/articles/7ee72995004c90)
