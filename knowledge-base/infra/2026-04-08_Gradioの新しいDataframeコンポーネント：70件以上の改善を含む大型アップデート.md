---
title: "Gradioの新しいDataframeコンポーネント：70件以上の改善を含む大型アップデート"
url: "https://huggingface.co/blog/gradio-dataframe-upgrade"
date: 2026-04-08
tags: [Gradio, gr.Dataframe, Python, UI, データ可視化, ダッシュボード, インタラクティブUI]
category: "infra"
memo: "[HF Blog] Introducing Gradio's new Dataframe!"
processed_at: "2026-04-08T09:13:53.382336"
---

## 要約

GradioのDataframeコンポーネント（gr.Dataframe）が大規模アップデートを受け、2025年3月24日にリリースされた。過去6週間で70件以上のIssue（バグ修正・機能追加）をクローズした。主な新機能は以下の通り。

①マルチセル選択：複数セルを一括選択し、コピーや削除が可能になった。②行番号表示とカラム固定：`show_row_numbers`パラメータで行番号列を追加でき、`pinned_columns`パラメータで横スクロール時に特定列を固定表示できる。③コピーボタンとフルスクリーンボタン：`show_copy_button=True`でセル値をCSV形式でコピー、`show_fullscreen_button=True`でフルスクリーン表示が可能。④スクロールトップボタン：大量データ表示時に先頭への素早い移動が可能。⑤アクセシビリティ向上とスタイリング強化：キーボードナビゲーションの改善と、`styler`パラメータによる外観カスタマイズが可能。⑥行・列選択イベント：セレクトイベントで行全体のデータを取得できるようになり、インタラクティブな操作が容易になった。⑦静的カラム指定：`static_columns`パラメータで編集不可の列を指定できる。⑧検索機能：`show_search='search'`でデータ内をキーワード検索可能。⑨フィルタリング機能：`show_search='filter'`でデータを絞り込み表示できる。⑩セル選択の挙動改善：より直感的なセル選択操作を実現。

利用するには`pip install --upgrade gradio`で最新バージョンに更新するだけでよい。公式ドキュメントにサンプルコードが掲載されており、Irish Wildlife（アイルランドの野生動物）データを例にした実装例が示されている。今後もアクセシビリティ・パフォーマンス・インテグレーションの改善が継続予定。

## アイデア

- show_search='filter'とshow_search='search'を切り替えるだけで検索・絞り込みの両方に対応できる設計は、パラメータの直交性が高く、シンプルなAPIで多様なユースケースをカバーする好例
- pinned_columns＋show_row_numbersの組み合わせは、横に広い監査ログや評価結果テーブルの視認性を大幅に改善できる実用的な機能
- static_columnsパラメータによる編集可否の列単位制御は、インタラクティブデモで入力を受け付けるべき列と読み取り専用列を明確に分けられる点で、UIの意図を明示する設計パターンとして参考になる

## Yujiの取り組みへの示唆

監査エージェントの評価結果やLLM-as-judgeのスコアリング結果をGradioのDataframeで可視化する際、show_search='filter'による絞り込みやpinned_columnsによるキー列固定が実用的に使える。LangGraphパイプラインのデバッグ用ダッシュボードやエージェント評価UIをGradioで構築する場合、static_columnsで入力列と出力列を分けることでUXを明確化できる。ただしコアの研究領域（GRPO、RLAIF、Agent Architecture）とは直接関係しないため、ツールとしての参考情報にとどまる。

## 原文リンク

[Gradioの新しいDataframeコンポーネント：70件以上の改善を含む大型アップデート](https://huggingface.co/blog/gradio-dataframe-upgrade)
