---
title: "LLM-as-a-Judgeを作る前にやるべき5つのエラー分析手順（Hamel Husain流）"
url: "https://zenn.dev/lappy/articles/8fa754cdf9af6c"
date: 2026-05-11
tags: [LLM-as-a-Judge, エラー分析, 評価設計, Open Coding, Axial Coding, Hamel Husain, LLM評価, grounded-theory, few-shot, Cohen's kappa]
category: "ai-ml"
related: [2012, 1068, 4664, 888, 100]
memo: "[Zenn LLM] LLM-as-a-Judgeを作る前にやるべき5つのエラー分析手順（Hamel Husain流）"
processed_at: "2026-05-11T09:06:07.333779"
---

## 要約

元AirbnbデータサイエンティストのHamel Husainが提唱する「LLM評価はエラー分析が最重要」という方法論をZennユーザーが5つの論点に整理した記事。

核心的な主張は「LLM-as-a-Judgeを先に作ると失敗する」という逆張りの順序論。helpfulness scoreのような汎用メトリクスはプロダクト固有の壊れ方を検出できない。具体例として不動産AIアシスタント「Nurture Boss」のケースが挙げられており、「バスルームのconnected/disconnected誤答」はhelpfulness scoreでPASSとなり、「SMS返信にMarkdownを使う誤り」はconciseness scoreでPASSとなる。いずれも汎用Judgeでは捕捉不能であることを示している。

Hamel流のエラー分析手順は社会学のグラウンデッド・セオリーを借用した2段階構造を取る。第1段階のOpen Coding（自由記述）では対話ログ1件ずつに自由なメモを書く。第2段階のAxial Coding（分類整理）では類似メモを束ねて「Missing User Education（40%）」「Authentication/Access Issues（30%）」「Poor Context Handling（20%）」「Inadequate Error Messages（10%）」のような名前付きカテゴリへ昇格させる。この比率分布が初めて「次に手を入れるべき場所」をデータで決める根拠となる。

レビュー件数の目安はHamel氏の発言によれば、30件から始めて新しい失敗パターンが出なくなるまで継続、最終目標は100件以上。1時間で100件を読むと約40〜50件のエラーが検出される感覚値も示されている。エラーがほぼ出ない場合は「品質が高い」ではなく「評価が緩い」サインと解釈する。

役割分担として「エラー分析はPMが所有すべき、エンジニアではない」と明言。ドメインを判断できる1人を「benevolent dictator（優しい独裁者）」として指名し、最終判断を集約することを推奨。

Judge実装はエラー分析完了後に限定的に導入。Honeycombの自然言語クエリ評価Judgeを例に、出力形式はbinary（good/bad）のJSONに固定し、数値スコア（1〜5）は「Judge間で揺れる」として明確に否定。Few-shotにはエラー分析で収集した人間ラベル済み実例を使用。Judge校正には100件以上の人間ラベルとのCohen's kappaを用いる。

合格率は70%前後が健全で、100%はJudgeが甘いサインとして設計し直しのきっかけとする。Judgeの合格率はプロダクト品質ではなくJudge難易度の指標と位置づける点が重要。

監査エージェント開発への示唆：監査基準の解釈はドメイン専門家（公認会計士・内部監査人）が行うべきであり、LLM-as-a-Judgeを先に設計すると「一般的な正確性」しか測れず、内部統制固有の要件（証跡の完全性、リスク分類の正確性等）を取り逃す。Open/Axial Codingのアプローチは監査ログのエラー分類にも直接適用可能。

## アイデア

- Judge設計より先に人間が対話ログを読むという「逆順設計」は、評価基準の空振りを防ぐ。汎用メトリクス（helpfulness score）はプロダクト固有の失敗（SMS中のMarkdown、不動産用語の誤認識）を検出できないという具体的な反例が説得力を持つ
- 社会学のグラウンデッド・セオリー（Open Coding → Axial Coding）をLLM評価に転用する発想が独特。エラーカテゴリを比率表として可視化することで、プロンプト改善の優先順位をデータドリブンに決定できる
- Judgeの出力をbinary（good/bad）に固定し、critiqeを必ず文章で付けさせる設計により、critique文章がそのまま次のfew-shot例として再利用でき、Judge精度が運用とともに自己強化する仕組みになっている

## 前提知識

- **LLM-as-a-Judge** → /deep_908 RAGアプリをLLM-as-a-Judgeで強化した事例：Farmer.chatの評価システム構築
- **few-shot prompting** → /deep_514 レビューから要件へ：LLMは人間のようなユーザーストーリーを生成できるか？
- **Cohen's kappa** → /deep_2012 生成AIで「将来対応スキル」を評価する：GoogleのVantage研究実験
- **グラウンデッド・セオリー** (TODO: 読むべき)
- **binary classification** (TODO: 読むべき)

## 関連記事

- /deep_2012 生成AIで「将来対応スキル」を評価する：GoogleのVantage研究実験
- /deep_1068 構造化生成によるプロンプト一貫性の改善
- /deep_4664 大規模言語モデルにおける文化配慮型機械翻訳：ベンチマークと調査
- /deep_888 RIFT: ルーブリック失敗モード分類体系と自動診断
- /deep_100 LLM評価はギャンブルだった — promptstatsで始める統計的評価

## 原文リンク

[LLM-as-a-Judgeを作る前にやるべき5つのエラー分析手順（Hamel Husain流）](https://zenn.dev/lappy/articles/8fa754cdf9af6c)
