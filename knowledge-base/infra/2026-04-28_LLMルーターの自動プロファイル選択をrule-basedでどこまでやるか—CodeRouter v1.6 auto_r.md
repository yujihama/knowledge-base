---
title: "LLMルーターの自動プロファイル選択をrule-basedでどこまでやるか—CodeRouter v1.6 auto_router"
url: "https://zenn.dev/zephel01/articles/7614011eef3e76"
date: 2026-04-28
tags: [LLMルーター, CodeRouter, rule-based分類, Pydantic, FastAPI, プロファイル選択, ローカルLLM, 可観測性]
category: "infra"
related: [2950, 2951, 1420, 2209, 2696]
memo: "[Zenn LLM] LLMルーターの自動プロファイル選択をrule-basedでどこまでやるか—CodeRouter v1.6 auto_router"
processed_at: "2026-04-28T12:33:09.278949"
---

## 要約

CodeRouter v1.6で実装されたauto_router機能の設計判断を詳説した記事。auto_routerは「リクエスト本文を解析して、どのモデルプロファイル（coding/multi/writing等）に振り分けるか」を自動決定する分類器。

【LLM-as-classifierを見送った理由】最初に0.5b級の小型LLMを常駐させる案を検討したが、(1)常駐プロセス追加による運用負荷、(2)初回リクエストへの+200〜500msレイテンシ、(3)ストリーミング開始後のプロファイル切り替え不可、(4)分類根拠がログから人間に読めない—という4点でコストが重く断念。特に「ログ＝観測の単一ソース」というCodeRouterの哲学と整合しないことが決定打となり、rule_idと閾値が確定的に残るrule-basedを採用した。

【Precedence設計】プロファイル優先順位はbody.profile > X-CodeRouter-Profile > X-CodeRouter-Mode > auto_router > default_profileの順。auto_routerはdefault_profile == "auto"という番兵値が設定されたときだけ発火するopt-in設計で、既存ユーザーは設定変更なしに動作変化ゼロを保証。

【Matcher 4種類の設計】has_image / code_fence_ratio / content_contains / content_regexの4種。pydanticのdiscriminated unionで「1 rule = 1 matcher」に制約し、AND/OR複合条件は意図的に排除。複合DSL化するとcueやregoが必要になり「依存5個」という自己規律に反するため。複合ロジックはfirst match winsの複数ルール順序で等価表現可能。

【Bundled rule 2本+fallthrough】画像添付時→multiプロファイル（vision非対応モデルへの画像渡しが最も痛い失敗のため最優先）、code_fence_ratio≥0.3→codingプロファイル（閾値0.3は社内実測で「コード直して」系0.25〜0.45と「使い方教えて」系0.15〜0.30の境界から設定）、どれにも非マッチ→writing（コーダーモデルに日本語文章を書かせると語彙がコード文脈に引っ張られる現象を回避）。

【User overrideはreplace-only】yaml記述時にbundledは丸ごと上書き。prepend/appendモードを用意するとyamlを読んだだけで最終評価順が読めなくなるため見送り。bundled踏襲用テンプレをexamples/providers.auto-custom.yamlとして同梱。

【失敗モードは全て起動時fast-fail】未定義プロファイル参照・未知matcher型・regexコンパイルエラーは全て起動時にfail。リクエスト時の曖昧さをゼロにすることで「なんかたまに変なprofileに行く」現象を排除。fallthroughのみリクエスト時挙動だが、Prometheusカウンターcoderouter_auto_router_fallthrough_totalで監視可能。fallthrough率5%超が「bundled ruleを1本追加する時期」のシグナルとして機能する。

## アイデア

- 「精度よりも解釈可能性」を設計原則に据え、LLM分類器をあえて採用しないという判断—分類根拠がログに確定的に残ることをシステム哲学として優先した点が、監査ログの完全性と同じ発想で応用できる
- code_fence_ratio閾値0.3を社内実測データから決定し、yamlで書き換え可能にする設計—ハードコードせず観測→調整のループを閉じる運用設計として参考になる
- pydanticのmodel_validatorで「exactly one field set」を強制することで、DSL化を防ぎながら将来のmatcher追加に対して後方互換を保つ手法—バリデーション層でアーキテクチャ制約を表現するパターン

## 前提知識

- **LLMルーター** (TODO: 読むべき)
- **Pydantic discriminated union** (TODO: 読むべき)
- **FastAPI middleware** (TODO: 読むべき)
- **Prometheus metrics** (TODO: 読むべき)
- **rule-based分類器** (TODO: 読むべき)

## 関連記事

- /deep_2950 同じOllama + qwen2.5-coderなのに動く/動かないが分かれる6つの構造的原因
- /deep_2951 CodeRouterの内側 — Anthropic⇄OpenAI双方向翻訳とmid-streamセーフなフォールバック設計
- /deep_1420 秘匿環境で使うAI議事録の構成を考える - パイプライン型とLLM完結型の検証
- /deep_2209 書類からのテキスト抽出精度をオープンソースのAIモデルで比較してみた
- /deep_2696 日本語入力システムSumibiの開発 part18: ローカルLLMが閾値を超えたかも

## 原文リンク

[LLMルーターの自動プロファイル選択をrule-basedでどこまでやるか—CodeRouter v1.6 auto_router](https://zenn.dev/zephel01/articles/7614011eef3e76)
