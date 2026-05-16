---
title: "コンパニオンAIの「黙る」をデフォルトとして設計した話：Asterelの抑制系アーキテクチャ"
url: "https://zenn.dev/haru0416/articles/companion-ai-silence-default"
date: 2026-05-15
tags: [コンパニオンAI, 沈黙設計, Rust, proactiveモジュール, trust_level, AutonomyLevel, 抑制アーキテクチャ, 決定論的ルール]
category: "agent-arch"
related: [5495, 5471, 1936, 4912, 4627]
memo: "[Zenn LLM] コンパニオンAIの「黙る」を、default として設計した話"
processed_at: "2026-05-15T09:02:22.706665"
---

## 要約

コンパニオンAIランタイム「Asterel」（pre-1.0、Rust実装）において、AIの自発発話を抑制する「沈黙をデフォルトとする設計」を実装した記録。

多くのAIプロダクトはエンゲージメント時間・ターン数・再訪率などKPIが「話す方向」に寄っており、チャットUIも無応答をエラーとして扱う。LLM自体も「質問されたら答える」コーパスで訓練されているため、自然な状態では発話方向にドリフトする。これに対しAsterelは、発話判定をLLMではなくRust側の決定論的ルールで切ることで、LLM呼び出し前に発話するかどうかを決定する構造を採用している。

proactiveモジュールは「観察→トリガー判定→policyフィルタ→prompt候補化」の4ステップで動作する。トリガー条件はツール信頼性低下・感情下降傾向・状況認識×進行中プロジェクト・自己改善フォールバックの4種。policyフィルタ（`filter_by_policy`関数）では、trust_level < 0.6（TRUST_GATE）なら空のVecを即返し、autonomyがReadOnlyなら同様に空返し、Supervisedならば種別をSuggestionのみに絞り、最後に`.take(1)`で1ターン1件に制限する。これにより「trust × autonomy × 種別 × 数」の4段ゲートが構成される。

抑制の仕組みは3層に分かれる。①defer：reflectで「伝えるべき」と判定された内容を`follow_up_queue`に永続保存し（上限MAX_PENDING_FOLLOW_UPS=20件、超過分は古い順に破棄）、次セッションの適切タイミングで`[Pending Follow-ups]`ブロックとしてpromptに投入。②throttle：`.take(1)`による1ターン1件制限。③hold back：発話候補生成前の段階でaffect topology・stance integrity verifier・forgetモジュールが分散してローカルに判定し、「表に出さない」を累積する。

意図的にやらないと決めた設計方針として、「相槌で時間を埋めない」「感情検出を毎回言語化しない」「proactive判定をLLMに委ねない」「会話量でtrustを稼がせない」が明示されており、これらがKPIや技術的引力に対する能動的な対抗手段として位置づけられている。

監査エージェント開発への示唆：エージェントが自発的に介入するかどうかを事前の決定論的ルールでゲートする設計は、監査ワークフローにおける「エージェントが不必要に割り込まない」制御にも応用できる。trust_levelのような信頼スコアによる発話許可ゲートは、エージェントの権限管理（AutonomyLevel相当）と組み合わせることでReActエージェントの過剰介入を抑制する機構として参考になる。

## アイデア

- 発話判定をLLM出力後ではなくLLM呼び出し前に決定論的ルールで行う「pre-LLM gate」設計により、LLMの自然な発話ドリフトを根本から防ぐアプローチ
- trust × autonomy × 種別 × 数の4段ゲートによる多層フィルタリング構造：単一のon/offではなく、信頼スコア・モード・発話種別・頻度を独立した軸として組み合わせる設計
- 「黙る」機構を単一モジュールに集中させず、affect topology・stance integrity・forgetモジュールに分散配置することで、各機構の文脈を保ちながら累積的に抑制を実現する分散hold back設計

## 前提知識

- **LLMプロンプト設計** → /deep_4901 アコーディオンパターン：巨大な単一LLMプロンプトをやめた理由と2段階分割アーキテクチャ
- **ReActエージェント** → /deep_4188 ReActエージェントが本当に必要な業務はどれか：4象限による業務AI設計の腑分け
- **コンパニオンAI** → /deep_5471 コンパニオンAIに「共感したまま判断軸を手放さない」を実装する話
- **Rust非同期処理** (TODO: 読むべき)
- **affect/感情モデリング** (TODO: 読むべき)

## 関連記事

- /deep_5495 コンパニオンAIの記憶を、普通のRAGじゃない設計にした話
- /deep_5471 コンパニオンAIに「共感したまま判断軸を手放さない」を実装する話
- /deep_1936 🤗 APIユーザー向けTransformer推論を100倍高速化した方法
- /deep_4912 論文から再実装してわかったHNSW近傍探索の本当の難所 — pgvectorの中身を理解する
- /deep_4627 化学データをDuckDBで扱えるようにする自作拡張機能「ducksmiles」を作った

## 原文リンク

[コンパニオンAIの「黙る」をデフォルトとして設計した話：Asterelの抑制系アーキテクチャ](https://zenn.dev/haru0416/articles/companion-ai-silence-default)
