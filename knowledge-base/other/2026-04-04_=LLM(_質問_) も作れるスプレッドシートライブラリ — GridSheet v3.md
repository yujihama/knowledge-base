---
title: "=LLM("質問") も作れるスプレッドシートライブラリ — GridSheet v3"
url: "https://zenn.dev/righ/articles/d6d1440e1dbe1a"
date: 2026-04-04
tags: [GridSheet, スプレッドシートUI, React, TypeScript, 非同期関数, LLM連携, Spilling, ツリーシェイキング]
category: "other"
memo: "[Zenn LLM] =LLM("質問") も作れるスプレッドシートライブラリ — GridSheet v3"
processed_at: "2026-04-04T21:13:11.361936"
---

## 要約

GridSheet v3 は React/Vue/Svelte/Preact 対応のスプレッドシートUIライブラリのメジャーアップデート。最大の追加機能は async/await のファーストクラスサポートで、セルの数式からLLMや外部APIを直接呼び出せる設計になっている。

非同期関数は BaseFunctionAsync を継承し main() を async にするだけで実装できる。結果は「関数名＋引数のcyrb53ハッシュ」をキーとしてセルごとにキャッシュされ、ttlMilliseconds で有効期限を設定可能。同じ引数で複数セルが同時に呼んだ場合は useInflight 機能により Promise を共有し、APIコールを1回に抑える。依存セル（例: =AVERAGE(A1:A2) でA1,A2が非同期）は解決まで自動的に Pending 状態になり、解決後に依存グラフに沿ってカスケード再計算が走る。

Spilling 機能との組み合わせにより、1回のAPIコールで複数カラムに値を展開できる。GitHub APIの例では、1リポジトリのStars・Forks・Issues・Size・Subscribersを1式で5列に展開。3行×6列=18セルのデータを3回のAPIコールで取得できる。

BaseFunction クラスも強化され、defs（型定義）を記述するだけで引数の数チェック・型チェック・1x1行列の自動展開・パーセント文字列変換などが自動化される。v2 では各関数で手動バリデーションが必要だったが、v3 では main() に純粋なロジックだけを書けばよい。

標準関数（SUM, VLOOKUP等）は @gridsheet/functions として独立パッケージに分離され、カテゴリ別サブパス（./math, ./statistics, ./text, ./lookup, ./time, ./logical, ./information）からツリーシェイキング対応でインポートできる。

v2 で別々だった Renderer・Parser・Labeler・Policy が v3 では Policy クラスに統合され、セルの描画・シリアライズ・数式評価時変換・ドロップダウン選択肢を1オブジェクトで定義できるようになった。

## アイデア

- セル数式からLLMを呼ぶ =LLM("質問") パターン：スプレッドシートUIをLLMオーケストレーションのフロントエンドとして使える設計で、ノーコードに近い形でLLM処理パイプラインを構築できる
- インフライト共有＋TTLキャッシュによるAPI呼び出し最適化：引数ハッシュベースのキャッシュと Promise 共有で、大量セルが同一クエリを参照しても実APIコールを最小化する仕組みは、RAGやエージェントのコスト管理に応用できる設計思想
- Spilling＋非同期の組み合わせ：1式で複数列に値を展開するパターンは、エージェントが複数属性を一括返却する場面（監査証跡の多項目評価など）のUI表現として参考になる
## 関連記事

- /deep_1480 推論とデュアルメモリの共同最適化による自己学習型診断エージェント（SEA）
- /deep_1247 ハーネスエンジニアリングとは何か：プロンプト→コンテキスト→ハーネスへ至るAIエージェント設計の変遷
- /deep_76 ディープリサーチの構築：State of the Artを達成するまでの技術的知見
- /deep_1307 Transformers.jsでMLパワードWebゲームを作る方法
- /deep_13 SkillにアプリケーションをAgent-App共生モデルとして組み込む実装

## 原文リンク

[=LLM("質問") も作れるスプレッドシートライブラリ — GridSheet v3](https://zenn.dev/righ/articles/d6d1440e1dbe1a)
