---
title: "RAGのfaithfulnessは0.67。それでも3回に1回間違っていた"
url: "https://zenn.dev/elvisyao/articles/ae00088688620b"
date: 2026-06-08
tags: [RAG, faithfulness, context_recall, LLM-as-judge, JQaRA, grounded-but-wrong, リランカー, RAG評価]
category: "ai-ml"
related: [6276, 112, 2563, 7417, 75]
memo: "[Zenn LLM] RAGのfaithfulnessは0.67。それでも3回に1回間違っていた"
processed_at: "2026-06-08T09:02:21.932455"
---

## 要約

著者はJQaRA（JAQKETベースの日本語RAG評価データセット）を用いてオンプレRAGシステムを構築し、生成モデル（qwen3:32b）とは独立した判定モデル（gemma4:31b）で評価した。ハードウェアはRTX 5090単体＋Ollama。

【Act1: リランカーの限界】dense検索にcross-encoderリランカーを追加した結果、P@1は0.8308→0.8440（+1.3pt）と改善したが、Recall@10は0.5738→0.5634（-1.0pt）と低下した。これはリランカーが既存の候補集合を並べ替えるだけであり、dense検索が一度も取得できなかった文書を補完できないことを示す。生成モデルがtop-5やtop-10を参照する構成では、P@1向上よりRecall@10低下が下流品質に悪影響を与えうる。

【Act2: faithfulnessの罠】生成評価100件でfaithfulness=0.6662が得られ、一見許容範囲に見えた。しかし本質的なボトルネックはcontext_recall=0.4062であり、多くのクエリで正答に必要な根拠文書がそもそも検索されていなかった。faithfulnessは「回答が検索コンテキストと整合しているか」を測るのみで、その回答が事実として正しいかは測定しない。誤った文脈を忠実に反映した回答もfaithfulと判定される。

独立した正答性チェック（gold answerとの比較）を実施したところ、100件中33件がfaithfulかつwrong（grounded-but-wrong）であることが判明。faithfulnessゲートのみでは33件の誤回答を素通りさせていた。因果連鎖はcontext_recall低下→根拠なしでも流暢に回答→faithfulだがwrongという構造。

【教訓】本番RAGの評価ゲートとして、①gold answerに対する正答性（grounded-but-wrongを捕捉）、②context_recall（先行指標）、③faithfulness（ハルシネーションガードとして正答性の上に乗せる）、④独立判定モデル（自己選好バイアス排除）の4点を提唱。LLM-as-judgeで生成モデルに自己採点させるとスコア分散がほぼゼロになりやすく、今回の独立判定モデルはfaithfulness spread=0.05（非ゼロ）を示し正常に機能した。recallがボトルネックの場合の正しいレバーはチャンキング・埋め込みモデル・ハイブリッド検索・クエリ拡張であり、リランカーではない。監査AIシステムにおいても、faithfulnessのみを信頼すると自信満々な誤回答を見逃すリスクが高く、正答性とrecallの両方でゲートを張ることが不可欠。

## アイデア

- faithfulness=0.67は一見合格ラインだが、context_recall=0.41という上流の欠損により100件中33件がgrounded-but-wrongになる——faithfulnessは十分条件ではなく必要条件に過ぎないという逆説
- リランカー追加でP@1は上がるがRecall@10は下がる：precisionとrecallのトレードオフを無視してP@1だけで「改善」と判断するのは、生成モデルが実際に読む指標（Recall@k）を見ていないミス
- LLM-as-judgeの自己選好バイアス対策として生成モデルと別モデルを判定に使い、score spreadが非ゼロであることを健全性の証拠とする運用規律

## 前提知識

- **RAG** → /deep_5 Google Research at The Check Up: ヘルスケアAIの最新研究成果と実臨床への展開（2026年）
- **faithfulness / context_recall** (TODO: 読むべき)
- **LLM-as-judge** → /deep_3 Claude Code のAIチームでLLMの品質を自動でチェックする方法
- **cross-encoder リランカー** (TODO: 読むべき)
- **Recall@k / P@k** (TODO: 読むべき)

## 関連記事

- /deep_6276 製造業RAGの本番運用設計：Evals・Observability・Prompt Versioning・Fallback【コード付き】
- /deep_112 知識ベースを自然淘汰するRAG「Darwin RAG」をつくってみた
- /deep_2563 文字通りの要約を超えて：医療SOAPノート評価におけるハルシネーションの再定義
- /deep_7417 ローカルLLMで「PoC止まり」にしない業務AIエージェント ― MCP＋RAG評価まで一気通貫
- /deep_75 テスト時拡散を用いたDeep Researcher（TTD-DR）：反復的ドラフト改善による長文レポート生成

## 原文リンク

[RAGのfaithfulnessは0.67。それでも3回に1回間違っていた](https://zenn.dev/elvisyao/articles/ae00088688620b)
