---
title: "簡潔な方が良い：関数呼び出しエージェントにおけるChain-of-Thoughtの非単調な予算効果"
url: "https://tldr.takara.ai/p/2604.02155"
date: 2026-04-09
tags: [Chain-of-Thought, function-calling, CoT budget, FR-CoT, Qwen2.5, LLM agent, function routing, hallucination]
category: "agent-arch"
memo: "[HF Daily Papers] Brief Is Better: Non-Monotonic Chain-of-Thought Budget Effects in Function-Calling Language Agents"
processed_at: "2026-04-09T09:46:20.323883"
---

## 要約

本論文は、関数呼び出し（function-calling）エージェントにおけるChain-of-Thought（CoT）の推論トークン数と精度の関係を体系的に分析した研究。Berkeley Function Calling Leaderboard v3 Multipleベンチマークの200タスクを用い、Qwen2.5-1.5B-Instructモデルに対して0〜512トークンの6段階バジェットを検証した。

中心的な発見は「非単調パターン」の存在。推論なし（d=0）では精度44.0%だが、わずか32トークンの短い推論（brief CoT）で64.0%へと45%相対改善する。一方、256トークンまで延ばすと精度は25.0%にまで低下し、推論なしを下回る（McNemar検定 p<0.001）。

誤りの三分類分析により、このメカニズムが明らかになった。d=0では30.5%のタスクが誤った関数選択（wrong function routing）により失敗する。32トークンのCoTはこれを1.5%まで削減し、事実上「関数ルーティングステップ」として機能する。しかし256トークンでは誤関数選択が28.0%に戻り、さらに18.0%の幻覚関数（hallucinated functions）が発生する。

オラクル分析では、解決可能なタスクの88.6%が最大32推論トークンしか必要とせず、平均27.6トークンで十分であることが判明。より細粒度のスイープでは最適値が8〜16トークンに存在することが示された。

この知見を基に、論文は**Function-Routing CoT（FR-CoT）**を提案。推論フェーズを「Function: [name] / Key args: [...]」という構造化テンプレートに固定し、推論開始時点で有効な関数名へのコミットメントを強制する手法。FR-CoTはd=32の自由形式CoTと統計的に同等の精度を達成しつつ、関数幻覚率を0.0%に削減する構造的信頼性保証を提供する。バジェットチューニング不要でこの保証が得られる点が実用上の強みである。

## アイデア

- 推論トークンが多いほど良いという直感は誤りで、32トークン程度の「短い思考」が最適という非単調性は、エージェント設計における推論量の最適化問題を根本から問い直す知見
- CoTの主な効果が「関数ルーティング（どのツールを呼ぶかの選択）」にあるという分解分析は、マルチツールエージェントのデバッグや改善において誤りの原因を構造的に切り分ける視点を提供する
- FR-CoTのように推論フォーマットを構造化テンプレートに固定することで幻覚を0%にできるという結果は、プロンプトエンジニアリングによる信頼性保証の可能性を示し、ファインチューニング不要な実用的アプローチとして注目に値する
## 関連記事

- /deep_715 Open R1 アップデート #3: OlympicCoderモデルとCodeForces-CoTsデータセットの公開
- /deep_972 論文「Learning to Reason with LLMs」を実運用視点で解説：企業導入で注意すべき5つのリスク
- /deep_861 蒸留モデルとは何か？ - DeepSeek R1の登場から1年で振り返るLLM知識蒸留の仕組みと実力
- /deep_111 生成AIのハルシネーションは「誤出力」？ 条件付き分布・真理条件・接地から見る数理的整理
- /deep_156 推論モデルは思考の連鎖（Chain of Thought）を制御できない——それは良いことだ

## 原文リンク

[簡潔な方が良い：関数呼び出しエージェントにおけるChain-of-Thoughtの非単調な予算効果](https://tldr.takara.ai/p/2604.02155)
