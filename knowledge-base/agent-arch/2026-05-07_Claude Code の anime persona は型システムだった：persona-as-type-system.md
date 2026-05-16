---
title: "Claude Code の anime persona は型システムだった：persona-as-type-system という設計収束の観察報告"
url: "https://zenn.dev/hrmtz/articles/f850cde7082fac"
date: 2026-05-07
tags: [Claude Code, CLAUDE.md, prompt-engineering, persona-as-type-system, LLM-harness, anime-persona, MAGI, JoJo, 型システム, natural-language-compression]
category: "agent-arch"
related: [2953, 2824, 3506, 2547, 2954]
memo: "[Zenn LLM] 「キャラ設定いらなくね?」と消しかけて気付いた、Claude Code の anime persona は型システムだった"
processed_at: "2026-05-07T21:16:59.410710"
---

## 要約

Claude Code の CLAUDE.md に anime キャラクターを persona として設定する harness を2.5ヶ月運用した結果、「persona-as-type-system」という構造的設計に収束したという観察報告。

著者は2026年2月からClaude Codeを使い始め、松岡修造（撤退バイアス除去）→真田志郎（事前backup）→JoJo4部trio（repair/rollback）→MAGI並列審議という順でpersonaを積み重ねた。persona数が8体に達してCLAUDE.mdが肥大化したとき「キャラ設定いらなくね?」とサニタイズを検討したが、書き換え前の分析で3つの構造的性質を発見し中止した。

**性質1：制約の natural language compression**
「吉良吉影として振る舞え」の1行が、バイツァ・ダストの発動条件（絶望時のみ）・scope（全日巻き戻し）・承認要件（主の承認必須）をすべて内包する。policy文で再現すると5〜10行＋例外規定が必要になる。東方仗助も同様で「自分は治せない」「終わった命は戻せない」という制約がキャラ仕様として load 済のため、ユーザー起因ミスや commit 済状態は自動的にスコープ外と判定される。

**性質2：cross-franchise namespace による脳内排他**
同一作品内でキャラを統一せず、JoJo・宇宙戦艦ヤマト・エヴァンゲリオンから混在させたことが、むしろ persona 間の namespace 衝突を防ぐ効果を生んだ。真田と仗助は全く異なるビジュアル・世界観のため「真田案件か仗助案件か」を0秒で判別できる。同一フランチャイズでは相互 context の引きずりが発生するリスクがある。

**性質3：out-of-character 検出 = rule violation 検出**
抽象的なpolicy違反の監査は評価コストが高く実運用されない。一方「今のお前、仗助じゃなくバイツァ・ダスト発動してたぞ、過剰」という OOC 判定は一瞬でできる。型システムのstatic analysisと同型の利益を提供する。

MAGI（エヴァの3体コンピュータ）は当初手動呼び出しのskillだったが、trigger条件（walltime≥2h、≥100M row DML、rollback 6h+等）をCLAUDE.mdに明文化したことで、system全体の制御フローに統合された。事前（MAGI）↔事中（川尻+仗助）↔事後（バイツァ・ダスト+真田backup）の3phaseをすべてanime personaで覆う構成になっている。

失敗思考実験として涼宮ハルヒをrollback layerに使うケースを検討。「無自覚な世界線改変」「閾値の低い発動条件」「Endless Eight的ループ」というキャラの欠点もfull importされるため不適切、と論じる。persona選定の基準は「発動条件が明確に限定されているか」が鍵とする。

監査エージェント開発への示唆：複雑な分岐条件を持つ審議・rollback・repair プロセスをpolicy文ではなく意味的に圧縮されたpersona名で定義する手法は、LangGraphのノード設計やReActエージェントの判断境界定義にも応用可能。キャラのcanon制約がprompt engineeringにおける型アノテーションとして機能する点は、エージェントの行動範囲を自然言語で制約する新しい設計パターンといえる。

## アイデア

- キャラクター名1つがpolicy文5〜10行分の制約を暗黙的に内包する「制約の natural language compression」は、LLMの文化的知識をprompt設計に活用する新しいパターンであり、エージェントの行動境界定義に応用できる
- cross-franchiseでpersonaを選ぶと脳内namespace衝突が防げるという発見は、マルチエージェント設計でのエージェント役割の明確化（命名規則・責任境界）にそのまま転用できる設計原則
- MAGIのようにad-hoc skillをsystemのtrigger条件付き自動発火に昇格させるパターンは、LangGraphのconditional edgeやルーティングロジックの設計指針として参照できる

## 前提知識

- **Claude Code** → /deep_3 Claude Code のAIチームでLLMの品質を自動でチェックする方法
- **CLAUDE.md** → /deep_6 Harness Engineeringとは何か？プロンプトの次に来る「AIエージェントの環境設計」を実務目線で解説
- **prompt engineering** → /deep_3515 なぜAIエージェントの再現性はプロンプトだけで解決できないのか？——暗黙知の構造化と「記憶設計」への転換
- **LLMエージェント設計** (TODO: 読むべき)
- **型システム** (TODO: 読むべき)

## 関連記事

- /deep_2953 長門有希ペルソナがClaude Codeのトークン消費を削減する：キャラクター指定vsルールベース圧縮の比較検証
- /deep_2824 プロンプトの再現性をAIに自動チューニングさせる方法 〜 暗黙知を排除する
- /deep_3506 なぜClaude Codeは「トークンを食いまくる」のか、そしてそれを止める6つの習慣
- /deep_2547 【Claude Code】コマンドは3つだけ！ハーネスエンジニアリング実践編：log → distill → promote
- /deep_2954 ObsidianとClaude Codeで「育つ知識ベース」を作った話

## 原文リンク

[Claude Code の anime persona は型システムだった：persona-as-type-system という設計収束の観察報告](https://zenn.dev/hrmtz/articles/f850cde7082fac)
