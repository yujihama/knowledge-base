---
title: "証明可能なプライバシーを保証するAI利用インサイト取得システム（Google Research）"
url: "https://research.google/blog/toward-provably-private-insights-into-ai-use/"
date: 2026-04-03
tags: [differential-privacy, TEE, federated-analytics, Gemma, confidential-computing, LLM-as-judge, structured-summarization, AMD-SEV-SNP]
category: "ai-ml"
memo: "[Google AI Blog] Toward provably private insights into AI use"
related: [23, 21, 931, 112, 208]
processed_at: "2026-04-03T12:03:22.699856"
---

## 要約

GoogleはPixel端末のRecorderアプリを対象に、ユーザーのGenAI機能利用状況を「証明可能なプライバシー（Provably Private Insights: PPI）」として取得する新システムを発表した。本システムは、差分プライバシー（Differential Privacy: DP）、信頼実行環境（Trusted Execution Environment: TEE）、LLMによる構造化要約（Structured Summarization）を組み合わせた「機密連合分析（Confidential Federated Analytics: CFA）」の上に構築されている。

技術的な仕組みは以下の通り。ユーザーデバイスは分析対象データ（例：Recorderの文字起こしテキスト）をTEE管理の公開鍵で暗号化してアップロードする。TEE内のキーストアは、事前承認された処理ステップにのみ復号鍵を渡す。TEE内ではオープンソースのGemma 3 4Bモデルがデータエキスパートとして動作し、「このトランスクリプトのトピックは何か？」「ユーザーは不満を抱いているか？」といった質問に対して分類ラベルを出力する。その分類結果はDP雑音を付加したヒストグラムとして集計され、集計値のみがGoogleに返される。個々のユーザーデータは一切TEEの外に出ない。

システムの検証可能性を担保するため、プライバシーに関与するすべてのコード（秘密集計アルゴリズム、TEEスタック、LLMプロンプト処理ワークフロー）はオープンソース化・再現可能ビルド対応されており、署名はRekorの改ざん防止ログに公開されている。AMD SEV-SNP CPUを用いたGoogle Project OakのTEEアテステーションにより、サーバー側でこれら以外の処理が実行されていないことを外部機関が検証できる。

Recorderアプリでは、「改善に協力する」設定を有効にしたユーザーのトランスクリプトが対象となり、Gemma 3によるトピック分類（メモ、リマインダー、会議等）のDPヒストグラムが生成される。また、Recorderの要約機能の精度評価にもCFAが活用されており、合成データではなく実ユーザーデータに基づく品質評価がプライバシー保護下で実現されている。コードはGoogle Parfaitリポジトリ上でオープンソース公開済み。

## アイデア

- LLMをTEE内に閉じ込めることで、プロンプト設計の自由度を保ちながらDP保証を維持できる点——プロンプトが変わってもDPは集計アルゴリズムに適用されるため、「どんな質問をしても個人は特定されない」という保証が成立する
- LLM-as-judgeをTEE内で実行することで、実ユーザーデータを用いたモデル品質評価がプライバシー保護下で可能になる——合成データ依存の評価パイプラインの限界を克服する実用的なアーキテクチャ
- コード署名・再現可能ビルド・TEEアテステーションの三層構造により、「何が起きているかを外部が検証できる」という監査可能性（auditability）がシステム設計レベルで組み込まれている
## 関連記事

- /deep_23 音声エージェント評価のための新フレームワーク EVA
- /deep_21 部分の総和を超えて：マルチモーダルヘイトスピーチ検出における意図変化の解読
- /deep_931 自律走行ポートフォリオ：機関投資家向け資産運用のエージェントアーキテクチャ
- /deep_112 知識ベースを自然淘汰するRAG「Darwin RAG」をつくってみた
- /deep_208 差分プライバシーを用いたAIチャットボット利用状況分析フレームワーク「Urania」

## 原文リンク

[証明可能なプライバシーを保証するAI利用インサイト取得システム（Google Research）](https://research.google/blog/toward-provably-private-insights-into-ai-use/)
