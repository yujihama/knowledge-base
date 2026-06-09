---
title: "harness-starter-kitは魔法ではない — エラーを早く表に出すためのフレームワーク"
url: "https://zenn.dev/yuuaan/articles/0cc85801f42f4e"
date: 2026-06-09
tags: [harness-starter-kit, AGENTS.md, failure-memory, coding-agent, CI/CD, dogfooding, decision-record, Next.js, Django, TypeScript]
category: "agent-arch"
related: [4752, 3947, 6415, 90, 4618]
memo: "[Zenn LLM] 3. harness-starter-kitは魔法ではない。エラーを早く表に出すためのもの"
processed_at: "2026-06-09T21:06:06.730432"
---

## 要約

harness-starter-kitは、AIコーディングエージェント（Cursor/Claude Code/Codex等）が作業するリポジトリに、AGENTS.md・decision docs・failure docs・検査スクリプト・CI設定を組み込むためのスターターキット。著者は韓国出身のジュニア開発者で、DjangoプロジェクトとNext.jsプロジェクト（today-bus）の2つのdogfood repoで実運用を続けている。

当初の期待は「harnessを入れればエージェントのミスが明確に減る」だったが、実際には「エラーを早く発見・記録・再検査できる場所を作る」ことが主な価値だと認識を改めた。エージェントは境界条件の見落とし・不適切な実装・生成ファイルの誤編集など依然としてミスをする。

Django dogfood repoでは、scripts/check_harness.pyがdocs drift check・structure check・encoding hygiene check・manage.py test等を実行し、GitHub Actionsにも接続している。またlocal kit referenceとstarterkit最新版の差分（refresh gap）が問題となり、.harness/source.jsonと/harness updateコマンドでバージョン追跡する仕組みを設けた。

Next.js dogfood（today-bus）ではTAGO公共交通API・TMAP・OpenRouteService等の外部APIを多数使用。npm run check:harness（lint→test:planner→typecheck→build→check-harness.mjs）が失敗した事例では、Next.js devサーバーが生成した.next/dev/types/validator.tsの古い型ファイルをtscが読み込んでしまう問題が発生。対処として「next typegen && tsc --noEmit --incremental false」に変更し、failure recordをdocs/failures/0005-next-dev-validator-typecheck-artifact.md、decision recordをdocs/decisions/0017-refresh-next-generated-types-before-typecheck.mdとして記録。同様にTAGO APIパラメータの大文字小文字（nodeId→nodeid）の不一致問題も、failure noteだけでなくplanner/provider testに接続することで再発防止を図った。

live API smoke checkはcredentials・network・quota・provider uptimeに依存するため、normal gateには入れずfocused/manualのままにすべきと判断。deterministic local checkのみをnormal gateに含める設計が重要な知見として挙げられる。

Harness Doctorスコアは「repo内にdurable evidenceがあるか（agent instructions/local checks/decision records/failure records等）」を示すharness health signalであり、「エージェントが同じバグを繰り返しにくくなったか」というagent effectivenessとは別物と明確に区別する。後者の証明にはtask outcome recordsや実タスクデータの蓄積が必要。著者はこのフレームワークを「installer」ではなく「ルール発見→リポジトリに記録→検査化→失敗記録→検出手段への接続→次のupdate/refreshで改善」というメンテナンスループとして位置づけている。監査エージェント開発への示唆：failure memoryをdetection/preventionに接続するアプローチは、監査ルールの違反検出チェックを再利用可能な形で蓄積するパターンに直接応用できる。

## アイデア

- failure noteを「何が起きたか」の記録に留めず、具体的なtest/fixture/smoke checkと接続させることで初めてdurable preventionになるという設計思想
- Harness health（repo構造の完備度）とAgent effectiveness（実タスクでのミス再発率）を明確に分離し、Doctorスコアの過信を戒める指標分離の考え方
- live API check（credentials/network依存）とdeterministic local check（再現可能）をnormal gateとfocused/manualに分離するCI設計パターン

## 前提知識

- **AGENTS.md** → /deep_8 LLMに「マジカルバナナ」式連想想起を実装したら会話が変わった
- **CI/CD gate** (TODO: 読むべき)
- **ADR（Architecture Decision Record）** (TODO: 読むべき)
- **smoke test** (TODO: 読むべき)
- **TypeScript tsc** (TODO: 読むべき)

## 関連記事

- /deep_4752 ハーネスは書いて終わりではない: Self-Evolving Agentの設計
- /deep_3947 pi-mono：完成品AIコーディングツールではなく、自作エージェント基盤として見ると強い
- /deep_6415 Gemma 4搭載の小説執筆AIエージェント【NovelPilot】
- /deep_90 CoDD（整合性駆動開発）活用ガイド #1: spec.md → 設計書 → コードの全ステップ解説
- /deep_4618 AIで爆速Mermaid図生成！ローカル動作のデスクトップアプリ「DiagramBuilder」を作った

## 原文リンク

[harness-starter-kitは魔法ではない — エラーを早く表に出すためのフレームワーク](https://zenn.dev/yuuaan/articles/0cc85801f42f4e)
