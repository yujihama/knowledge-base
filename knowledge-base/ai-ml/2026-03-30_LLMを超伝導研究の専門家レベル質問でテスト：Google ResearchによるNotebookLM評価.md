---
title: "LLMを超伝導研究の専門家レベル質問でテスト：Google ResearchによるNotebookLM評価"
url: "https://research.google/blog/testing-llms-on-superconductivity-research-questions/"
date: 2026-03-30
tags: [RAG, NotebookLM, LLM評価, 科学的QA, ソースキュレーション, GPT-4o, Gemini, PNAS]
category: "ai-ml"
memo: "[Google AI Blog] Testing LLMs on superconductivity research questions"
processed_at: "2026-03-30T12:05:41.367124"
---

## 要約

GoogleとCornell大学の共同研究として、PNAS（米国科学アカデミー紀要）に掲載された論文「Expert evaluation of LLM world models: A high-Tc superconductivity case study」の概要。高温超伝導（High-Tc superconductivity）を題材に、6つのLLM（GPT-4o、Perplexity、Claude 3.5、Gemini Advanced Pro 1.5、NotebookLM、カスタムRAGシステム）の専門知識評価を実施した。

【実験設計】高温超伝導の分野に特化した12名の国際専門家が15本の科学レビュー論文を選定し、それらから引用された約3,300件の参考文献を収集。Geminiを用いて実験論文と理論論文を分類し、最終的に1,726件のソース（実験論文＋レビュー論文）をクローズドシステムの知識源として使用。一方、Webアクセス型の4モデルは765本のOA実験論文と1,553本のOA理論論文を含むインターネット全体にアクセス可能。専門家パネルが67問の専門的質問（例：「LSCOにおけるLifshitz転移はどのドーピングレベルで起きるか」「キュプレートの量子臨界点シナリオを支持する証拠は何か」）を作成し、マスクレビュー方式で各モデルを0〜2点の6指標（バランス視点・包括性・簡潔性・エビデンス・画像関連性・定性FB）で採点。

【結果】キュレーション済みデータベースを使用するNotebookLMが総合首位。バランス視点・包括性・エビデンスの各指標でトップまたは上位。2位はカスタムRAGシステム（同一1,726ソース使用）。NotebookLMは簡潔性は最低だが、エビデンス提示は最高。Webアクセス型モデルは情報の網羅性はあるが、品質管理されていないソースから誤情報や偏った視点を含むリスクが高い。

【結論】専門領域においてLLMの回答品質はデータソースの品質管理に強く依存する。閉じたエコシステムの認証済みソースを使うシステムが、オープンウェブアクセス型を上回る。科学的発見を加速するツールとしての信頼性確保には、RAGと専門家によるソースキュレーションの組み合わせが有効。

## アイデア

- 専門家による事前キュレーション済みソース（15本のレビュー論文＋約3,300引用文献）をRAGに与えることで、オープンウェブアクセス型LLMを超える回答精度を達成した点：知識の質は量より品質管理に依存する
- マスクレビュー方式＋6指標（バランス・包括性・簡潔性・エビデンス・画像・定性FB）による専門家評価フレームワーク：LLM-as-judgeではなく人間専門家による評価設計が参考になる
- 67問の専門家設計質問セットとCURIEベンチマークの組み合わせ：特定ドメインでのLLM能力評価方法論として、他分野（監査・法律等）に転用可能なアプローチ
## 関連記事

- /deep_112 知識ベースを自然淘汰するRAG「Darwin RAG」をつくってみた
- /deep_1251 マルチターン医療診断のベンチマーク：保留・誘惑・自己修正（MINT）
- /deep_77 パーソナルヘルスエージェントの解剖：マルチエージェント構造による個人健康支援フレームワーク
- /deep_908 RAGアプリをLLM-as-a-Judgeで強化した事例：Farmer.chatの評価システム構築
- /deep_260 Learn Your Way: 生成AIによる教科書の再構想

## 原文リンク

[LLMを超伝導研究の専門家レベル質問でテスト：Google ResearchによるNotebookLM評価](https://research.google/blog/testing-llms-on-superconductivity-research-questions/)
