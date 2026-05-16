---
title: "Groq × DPO で「ひらがなだけで答える LLM」をつくる：合成データ生成から学習・評価まで"
url: "https://zenn.dev/quixotiks/articles/98f34bc582ffc9"
date: 2026-04-13
tags: [DPO, Llama3, Unsloth, QLoRA, 合成データ生成, Groq API, TRL, 出力スタイル制御, ファインチューニング]
category: "ai-ml"
related: [335, 265, 1216, 1183, 405]
memo: "[Zenn LLM] Groq × DPO で「ひらがなだけで答える LLM」をつくる - 合成データ生成から学習・評価まで -"
processed_at: "2026-04-13T12:51:06.527283"
---

## 要約

本記事は、Groq API を用いた合成データ生成と DPO（Direct Preference Optimization）による Llama 3 8B の微調整を通じて、「ひらがなのみで回答する LLM」を構築した実践レポートである。

【背景と動機】プロンプトエンジニアリングで「ひらがなだけで答えて」と指示しても漢字・カタカナが混入する問題は、子ども向け教育アプリや日本語学習ツールでは致命的となる。この課題を DPO による出力スタイル制御で解決することが本実験の目的である。

【合成データ生成】Groq API（moonshotai/kimi-k2-instruct-0905）を使い、{system, prompt, chosen, rejected} 形式の DPO 学習データを 4,000 件生成した。chosen はひらがなのみの説明、rejected は漢字かな交じりの通常説明のペアとし、1 回の API 呼び出しで 10 件ずつ JSONL 形式で出力。429 レート制限に対してはエラーメッセージから待機時間をパースして自動リトライし、追記モードで中断・再開を可能にした。生成コストは Groq 無料ティアの範囲内に収まった。

【DPO 学習】ベースモデルは unsloth/llama-3-8b-instruct-bnb-4bit（4bit QLoRA）、フレームワークは Unsloth + TRL 0.22.2（DPOTrainer）を使用。LoRA rank=8、alpha=8、RSLoRA 有効、学習率 5e-6、3 エポック、DPO β=0.1。NVIDIA DGX Spark（GB10, VRAM 122GB）で約 5 時間学習したが、4bit 量子化のため VRAM 24GB 以下の環境でも実行可能。Unsloth により標準の transformers+PEFT 比で約 2 倍の学習速度・60% のメモリ削減を達成。

【学習結果】Step 10 時点で Reward Accuracy 53.8%・Reward Margin 0.027 だったが、Step 100 前後で急速に学習が進み、Step 300 前後で Reward Accuracy 100%・Reward Margin 約 13 に完全収束。最終 Step 1,425 でも安定状態を維持した。学習後のモデルは漢字・カタカナ・句読点を一切含まないひらがなのみの出力を安定して生成する。

【限界と考察】Reward Accuracy が早期に 100% に達した後も Reward Margin が拡大し続ける過学習が確認され、事実正確性の低下が発生した。DPO はスタイルの好みを最適化する手法であり、内容の正確性を直接最適化しないため、「それらしいひらがな列」の生成が事実性より優先される現象が起きる。対策として Early Stopping（Accuracy 100% 達成後 50〜100 ステップで停止）、β 値を 0.1→0.05 に下げること、chosen データへの事実検証パイプライン追加が挙げられている。

【監査エージェント開発への示唆】出力フォーマット・語調・専門用語レベルの厳密な制御が求められる監査レポート生成タスクにおいて、合成データ+DPO による出力スタイル強制は有効なアプローチとなりうる。ただし事実正確性とのトレードオフ管理（chosen データの品質担保・過学習抑制）が実運用の鍵となる。

## アイデア

- プロンプトエンジニアリングでは安定しない出力スタイル制御を DPO で内部表現レベルに埋め込む発想：「ひらがなのみ」という形式制約を chosen/rejected ペアとして定義するだけで、モデルのバイアスを直接書き換えられる
- Groq 無料ティアで 4,000 件の高品質合成データを生成し、GPU 電気代のみで LLM 微調整を完結させるゼロコスト学習パイプライン：商用サービス化前の PoC 検証コストを実質ゼロにできる
- Reward Margin の拡大継続が過学習のシグナルになる点：Accuracy が 100% に達した時点で Early Stopping を設けないと、スタイル適合度が上がる一方で事実正確性が低下するという DPO 固有のトレードオフが顕在化する

## 前提知識

- **DPO** → /deep_111 生成AIのハルシネーションは「誤出力」？ 条件付き分布・真理条件・接地から見る数理的整理
- **LoRA / QLoRA** (TODO: 読むべき)
- **RLHF** → /deep_37 LLMチャットボットに欠けているもの：目的意識（Purposeful Dialogue）
- **Llama 3** → /deep_940 Llama 3.2 リリース：視覚理解とオンデバイス推論を兼ね備えたオープンモデル群
- **Unsloth** → /deep_335 DPO学習におけるバッチサイズと勾配累積がlossに与える影響を検証

## 関連記事

- /deep_335 DPO学習におけるバッチサイズと勾配累積がlossに与える影響を検証
- /deep_265 RapidFire AIによるTRLファインチューニングの最大20倍高速化
- /deep_1216 パーソナルコパイロット：自分専用コーディングアシスタントのトレーニング方法
- /deep_1183 オープンLLMによるConstitutional AI（憲法的AI）の実装
- /deep_405 UnslothとHugging Face Jobsで無料でAIモデルをファインチューニングする方法

## 原文リンク

[Groq × DPO で「ひらがなだけで答える LLM」をつくる：合成データ生成から学習・評価まで](https://zenn.dev/quixotiks/articles/98f34bc582ffc9)
