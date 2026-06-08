---
title: "faithfulness spread が 0.000 になった話 — 自己採点RAG evalの実態と対処"
url: "https://zenn.dev/elvisyao/articles/5e9b935e7f1f09"
date: 2026-06-08
tags: [RAG, faithfulness, self-enhancement-bias, Ollama, qwen3, gemma4, LLM-as-judge, eval, spread]
category: "ai-ml"
related: [7417, 2257, 2691, 6484, 7786]
memo: "[Zenn LLM] faithfulness spread が 0.000 になった話 — 自己採点RAG evalの実態と対処"
processed_at: "2026-06-08T21:07:08.731027"
---

## 要約

RAG評価における自己採点（self-evaluation）の根本的な欠陥を実測データで示した記事。生成モデルと同一モデルを判定に用いた場合、faithfulness spreadが文字通り0.0000になる現象を報告している。

実験設定はJQaRAデータセットを用いた100クエリのRAG評価。生成モデルはqwen3:32b（Qwen/アリババ）を使用。自己採点条件ではqwenファミリーの同一モデルを判定に、独立評判条件ではgemma4:31b（Gemma/グーグル）を判定に使用した。

結果の比較：自己採点ではfaithfulness mean=0.7751・spread=0.0000・grounded-but-wrong=48/100だったのに対し、独立評判（gemma4:31b）ではmean=0.6662・spread=0.0500・grounded-but-wrong=33/100だった。

spread=0.0000の意味は深刻で、判定モデルがクエリごとの回答品質を実際には区別せず、全クエリに同一のfaithfulness分布を返していたことを示す。つまり「判定モデルが回答を読まずに承認印を押し続けていた」状態だ。これはself-enhancement biasと呼ばれる既知の現象で、モデルが自分のフレーズを認識して高く評価する傾向であり、モデル能力が高いほど強く発現する。

水増しfaithfulnessの連鎖効果も重要：faithfulと判定されるプールが広がるほどgrounded-but-wrongの機会も増え、自己採点では独立評判が「faithfulでない」と正しく弾くべき回答まで「grounded」と数えてしまう。これが48件vs33件の差の原因だ。

独立判定モデル構築の3原則として著者は挙げる：①別ファミリーでの分離（単に別チェックポイントではなく別学習系譜）、②gold answerへのアンカー（主観タスクと違い参照回答があればバイアスの余地が縮む）、③on-premでの2パスアーキテクチャ（RTX 5090 32GB環境でqwen3:32bとgemma4:31bは同時常駐できないため、全生成→VRAMアンロード→全判定の順序が必要）。

監査エージェント開発への示唆：RAG品質評価を自動化する際に自己採点パイプラインを採用すると、評価指標が実態を大幅に過大評価する。監査判断の根拠となるRAGシステムの品質保証には、異なるモデルファミリーによる独立評判と、人手ラベルとのサンプル突き合わせ（推奨30〜50件）が必要条件となる。

## アイデア

- spread=0.0000という単一指標が判定モデルの崩壊（追認印モード）を即座に検出するサニティゲートとして機能する点：meanだけ見ていると気づけない
- 自己採点biasがfaithfulnessの偽陽性→grounded-but-wrongの偽陽性という連鎖を生む構造：1つの水増しが下流の別指標を汚染するメカニズム
- on-prem環境でのVRAM制約が2パスアーキテクチャを強制する運用実態：クラウドAPIでは見えないコストとトレードオフがローカルLLM評価基盤に存在する

## 前提知識

- **RAG** → /deep_5 Google Research at The Check Up: ヘルスケアAIの最新研究成果と実臨床への展開（2026年）
- **faithfulness評価** (TODO: 読むべき)
- **LLM-as-judge** → /deep_3 Claude Code のAIチームでLLMの品質を自動でチェックする方法
- **self-enhancement bias** (TODO: 読むべき)
- **Ollama** → /deep_52 SyGra Studio 紹介：合成データ生成のビジュアル・インタラクティブ環境

## 関連記事

- /deep_7417 ローカルLLMで「PoC止まり」にしない業務AIエージェント ― MCP＋RAG評価まで一気通貫
- /deep_2257 ローカルLLM + RAGでSlay the Spire 2の攻略アドバイザーを作った話：OpenWebUI実践記録
- /deep_2691 カンニング用AIをアップグレードしようとしたら、RAGの限界にぶつかった話
- /deep_6484 prompt / context / agent / harness: ボトルネック移動で読むLLM engineeringの系譜とその先
- /deep_7786 RAGのfaithfulnessは0.67。それでも3回に1回間違っていた

## 原文リンク

[faithfulness spread が 0.000 になった話 — 自己採点RAG evalの実態と対処](https://zenn.dev/elvisyao/articles/5e9b935e7f1f09)
