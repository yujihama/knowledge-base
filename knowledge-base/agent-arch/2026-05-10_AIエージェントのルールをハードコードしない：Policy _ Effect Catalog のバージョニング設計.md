---
title: "AIエージェントのルールをハードコードしない：Policy / Effect Catalog のバージョニング設計"
url: "https://zenn.dev/kanaria007/articles/d02ea13d9163fd"
date: 2026-05-10
tags: [Effect Catalog, Policy Versioning, AIエージェント設計, TypeScript, receipt管理, ガードレール, human-in-the-loop, rollback設計]
category: "agent-arch"
related: [4623, 4620, 3898, 1704, 1619]
memo: "[Zenn LLM] AIエージェントのルールをハードコードしない：Policy / Effect Catalog の versioning 設計"
processed_at: "2026-05-10T12:49:32.439021"
---

## 要約

本番業務フローにLLM・AIエージェントを組み込む際、「この操作は自動実行可か」「どのロールの承認が必要か」「rollbackできるか」といったルールが、バックエンドのif文・フロントエンドのdisabled条件・プロンプト注記・runbookなど複数箇所に散在し、変更・監査・再現が困難になる問題を解決するアーキテクチャパターン。

解決策の核心は、effect_typeを`EffectCatalogEntry`として型定義し、boundary（support-only / review-only / effect-bearing）・reversibility（reversible / compensatable / irreversible）・auto_execute_allowed・required_receipts・required_reviewer_roles・required_plansをすべてカタログに集約することだ。たとえば`add_github_label`はauto_execute_allowed=true・reversible・rollback_plan必須、`send_email`はauto_execute_allowed=false・compensatable・review_receipt+compensation_plan必須+support_leadの承認が必要、という形でエントリーを定義する。

Gate関数は固定if文ではなくカタログを参照して判定し、receipt不足の場合はいきなりREJECTではなくDEGRADE（必要なreceiptを追加すれば再開可能）を返す。review_receiptの有効性検証では、reviewer_roleの一致だけでなくproposal_idの一致も確認し、別proposalへの承認を誤流用しない設計になっている。

ポリシーのバージョニング管理では、PolicyVersionオブジェクトにapplies_to（new_cases / all_cases / pending_cases）フィールドを持たせ、処理中ケースへの適用範囲を明示的に制御する。古いpolicy_versionのケースを再評価する際は、そのケースに紐づくpolicy_versionを参照して実行可否を判断する。

UI・バックエンド・エージェントの全レイヤーが同一カタログを参照することで、ルールの一貫性が保たれ、ルール変更時は1箇所の更新で全箇所に伝播する。監査エージェント開発への示唆として、内部統制の承認ルール（誰がどのアクションを承認できるか）・証跡要件（どのreceiptが揃えば実行合法か）・policy変更時の既存ケース扱いという3要素は、まさに内部監査のコントロール設計と同型であり、LangGraphベースのワークフローにこのカタログパターンを組み込むことで、監査可能で変更耐性のあるエージェントを構築できる。

## アイデア

- ルールをif文でなくEffectCatalogEntryの型として定義することで、UI・バックエンド・エージェントが同一ソースから判断できる単一真実源（Single Source of Truth）を実現する点
- receipt不足時にREJECTでなくDEGRADE（再開可能な中断）を返す設計により、ワークフローの継続性を保ちながらコンプライアンスを担保できる点
- policy_versionをカタログエントリに持たせ、applies_toフィールドで新規ケース/全ケース/処理中ケースへの適用範囲を制御することで、ポリシー変更の影響範囲を宣言的に管理できる点

## 前提知識

- **AIエージェント** → /deep_2 AIエージェント自作のための基礎知識 - Google ADK (Go) を使ったエージェント構築
- **Receipt Pattern** (TODO: 読むべき)
- **TypeScript型システム** (TODO: 読むべき)
- **human-in-the-loop** → /deep_24 1対1を超えて：動的な人間とAIのグループ会話のオーサリング・シミュレーション・テスト
- **LLMワークフロー** → /deep_4188 ReActエージェントが本当に必要な業務はどれか：4象限による業務AI設計の腑分け

## 関連記事

- /deep_4623 AI自動化にRollbackを設計する：失敗しても戻せるLLMワークフロー
- /deep_4620 厳密性が要求される業務プロセスへのAIエージェント応用設計：ポリシー制約評価・専門家判断・中期記憶・段階的自律化によるアーキテクチャ
- /deep_3898 階層型記憶3層設計 — LLMの「忘れる」問題を設計で解く
- /deep_1704 機械学習ディレクターたちの現場インサイト【前編】：メディア・製薬・研究分野での実践知
- /deep_1619 敵対的データを用いた動的モデル訓練の方法（MNISTを例に）

## 原文リンク

[AIエージェントのルールをハードコードしない：Policy / Effect Catalog のバージョニング設計](https://zenn.dev/kanaria007/articles/d02ea13d9163fd)
