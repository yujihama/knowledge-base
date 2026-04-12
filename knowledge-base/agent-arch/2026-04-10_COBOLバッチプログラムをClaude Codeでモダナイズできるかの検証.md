---
title: "COBOLバッチプログラムをClaude Codeでモダナイズできるかの検証"
url: "https://zenn.dev/solvio/articles/a309c0c6771582"
date: 2026-04-10
tags: [Claude Code, COBOL, モダナイゼーション, Codex, マルチエージェント, パイプライン自動化, LLM-as-judge, バッチ処理]
category: "agent-arch"
memo: "[Zenn LLM] CobolのバッチプログラムをClaude Codeでモダナイズできるかの検証"
related: [3, 1641, 21, 931, 75]
processed_at: "2026-04-10T12:27:59.349931"
---

## 要約

Solvio株式会社による検証記事。Claude CodeとOpenAI Codexを組み合わせた7段階の変換パイプラインを構築し、AWSが公開するメインフレームモダナイゼーション用リポジトリ「AWS CardDemo」に含まれるCOBOLバッチプログラム6本をPythonスクリプトへ変換した結果を報告している。

検証の流れは以下の通り。まずGnuCOBOLをローカルにインストールしてCOBOL実行環境を構築し、顧客情報表示プログラム（CBCUS01C.cbl）を対象にClaude Codeへ変換指示を行ったところ、初回から出力がMD5レベルで完全一致した。

大量ファイルの変換を想定したパイプラインは7ステージで構成される。Stage 1（Claude Code）でCOBOL解析・仕様書生成、Stage 2（Codex）でテストケース設計・テストデータ生成・COBOL実行による正解出力確定、Stage 3（Claude Code）でPython変換、Stage 4（スクリプト）でPython実行、Stage 5（スクリプト）でdiff比較・合否判定、Stage 6（Codex）で変換コードのレビュー、Stage 7（Claude Code）でレポート生成。実装者と評価者を意図的に別モデルに分けることでバイアスを排除する設計が特徴的。

1st versionでは6テストケース中5件がPASS（83.3%）。唯一のFAILはVSAMインデックスファイルが空の場合の挙動差異で、COBOLではOPEN時にFILE STATUS 35（ファイル未存在）でABENDするのに対し、Pythonでは空テキストファイルを正常オープンして0件正常終了してしまうI/Oモデルの根本的な違いが原因。Codexによるレビューがこの差異を検出できており、テストの信頼性が一定担保されていることを確認。

改善版パイプラインではレビュー指摘の自動修正と再実行を追加。最終的にCBCUS01C含む6本のバッチプログラムで全30テストケースの出力完全一致を達成した。Claude.mdやSkills/Hooksを活用してパイプライン全体を自動化しており、人間は最終受け入れのみを担当する構成。定型的なバッチ処理変換においてコーディングエージェントが実用水準に達しているという評価。

## アイデア

- 実装者（Claude Code）と評価者（Codex）を別モデルに分離してバイアスを排除する設計パターンは、LLM-as-judgeの精度向上に直結する汎用的なアーキテクチャ原則として応用できる
- Stage 2でCodexがテストデータを自動生成し、実際のCOBOL実行結果を正解ラベルとして確定する手法は、正解データが存在しないレガシーシステムのテスト自動化に対する実践的な解法
- VSAM vs テキストファイルのI/Oモデル差異のように、言語変換ではセマンティクスの等価性ではなく実行環境の差異がバグの根源になるケースを自動検出できるdiff＋レビューの二重チェック構造
## 関連記事

- /deep_3 Claude Code のAIチームでLLMの品質を自動でチェックする方法
- /deep_1641 限界社会人のための Codex 節約活用術：OpenRouterで無料モデルをサブエージェントに使う
- /deep_21 部分の総和を超えて：マルチモーダルヘイトスピーチ検出における意図変化の解読
- /deep_931 自律走行ポートフォリオ：機関投資家向け資産運用のエージェントアーキテクチャ
- /deep_75 テスト時拡散を用いたDeep Researcher（TTD-DR）：反復的ドラフト改善による長文レポート生成

## 原文リンク

[COBOLバッチプログラムをClaude Codeでモダナイズできるかの検証](https://zenn.dev/solvio/articles/a309c0c6771582)
