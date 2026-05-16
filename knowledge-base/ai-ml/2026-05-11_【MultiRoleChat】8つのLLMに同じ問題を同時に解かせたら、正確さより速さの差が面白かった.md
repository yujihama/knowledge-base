---
title: "【MultiRoleChat】8つのLLMに同じ問題を同時に解かせたら、正確さより速さの差が面白かった"
url: "https://zenn.dev/tsukitsukiss/articles/multirolechat-llm-parallel-quiz-benchmark"
date: 2026-05-11
tags: [LLMベンチマーク, 並列推論, 応答速度, Groq, MultiRoleChat, gpt-5.4, claude-opus-4-6, gemini, レイテンシ比較]
category: "ai-ml"
related: [3898, 2920, 5034, 112, 178]
memo: "[Zenn LLM] 【MultiRoleChat】8つのLLMに同じ問題を同時に解かせたら、正確さより速さの差が面白かった"
processed_at: "2026-05-11T09:39:34.380773"
---

## 要約

自作ツール「MultiRoleChat.py」を使い、8つのLLMに対して同一条件・同一問題・並列実行でクイズベンチマーク（19問）を実施した実験レポート。参加モデルはChatGPT(gpt-5.4)、Gemini(gemini-3.1-pro-preview)、Claude(claude-opus-4-6)、Groq経由のgpt-oss-120bとgpt-oss-20b、Mistral(mistral-large-2512)、Together(Llama-3.3-70B-Instruct-Turbo)、Grok(grok-4-1-fast)の8体。正解率では5体が19問中19問で満点（100%）、Groq-20bとMistralが94.7%、Llamaが89.5%という結果になった。ただし問題が公式過去問であるため、記憶の再現か理解かは区別できないとの注記あり。最大の知見は応答速度の差にある。Groq-20bが平均0.62秒で最速、Groq-120bが0.73秒と続き、GroqのカスタムAIインフラ（OpenAI互換高速推論）の優位性が明確に示された。一方で「fast」を名乗るgrok-4-1-fastは平均9.17秒で7位、Geminiは10.07秒で最下位と、命名やブランドとレイテンシが一致しないケースが浮き彫りになった。誤答が発生した問題は知識問題ではなく「問題文の状況設定を正確に読み取り適切な手法を選ぶ」系の問題であり、軽量モデルや特定プロバイダーで文脈読解力の差が現れた可能性がある。Googleは特定問題でQ6=15秒、Q17=29秒という突出した遅延を示し、問題の複雑さや文字数によってレイテンシが変動しやすい傾向が観察された。総合順位は正解率優先・同率時は速度で決定する方式で、Groq-120bが精度100%・速度0.73秒で総合1位。ツールはGitHubで公開されており、`quiz multiline continuous`コマンドで複数行問題を連続投入し、全モデルへの並列リクエスト→応答順表示→ログ自動保存（Markdown形式）というフローで動作する。監査エージェント開発への示唆としては、精度が横並びになる問題難易度帯では推論インフラのレイテンシが実運用上の差別化要因になる点が参考になる。特にリアルタイム性が求められる監査補助ユースケースではGroq等の高速推論インフラの採用が有効と考えられる。

## アイデア

- 精度が横並びになる難易度帯では応答速度が唯一の差別化要因になるという逆説的な知見：ベンチマーク設計において難易度キャリブレーションが重要
- 「fast」命名モデルのAPIレイテンシが最下位クラスだった事実：モデル名のマーケティング用語と実測インフラ性能の乖離を定量的に示した点
- 誤答パターンが知識問題ではなく文脈読解・状況判断問題に集中していた観察：LLMの能力評価においてfactual recallと文脈推論の分離が評価設計上必要

## 前提知識

- **LLM API** → /deep_409 Hugging Face SpacesにGGUFモデルをデプロイして無料LLM APIを構築する方法
- **並列処理** → /deep_2817 AIマルチセッション運営で気づいた7つの原則 — 3日間で270万行を消して見えた景色
- **推論レイテンシ** (TODO: 読むべき)
- **OpenAI互換エンドポイント** (TODO: 読むべき)
- **ベンチマーク設計** → /deep_2829 ChatGPTが自信満々に嘘をつく「本当の理由」— OpenAI論文「Why Language Models Hallucinate」解説

## 関連記事

- /deep_3898 階層型記憶3層設計 — LLMの「忘れる」問題を設計で解く
- /deep_2920 見て・指して・磨く：視覚フィードバックを用いたGUI接地のマルチターンアプローチ
- /deep_5034 自己同一性を前提としない体系「顕現論（Aletheics）」をLLMに与えて哲学談義すると面白い
- /deep_112 知識ベースを自然淘汰するRAG「Darwin RAG」をつくってみた
- /deep_178 小モデル、大きな成果：分解アプローチによる優れたインテント抽出

## 原文リンク

[【MultiRoleChat】8つのLLMに同じ問題を同時に解かせたら、正確さより速さの差が面白かった](https://zenn.dev/tsukitsukiss/articles/multirolechat-llm-parallel-quiz-benchmark)
