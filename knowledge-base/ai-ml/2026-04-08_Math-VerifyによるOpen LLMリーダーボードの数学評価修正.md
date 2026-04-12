---
title: "Math-VerifyによるOpen LLMリーダーボードの数学評価修正"
url: "https://huggingface.co/blog/math_verify_leaderboard"
date: 2026-04-08
tags: [evaluation, benchmark, MATH-Hard, SymPy, Math-Verify, Open-LLM-Leaderboard, LLM評価, Qwen, DeepSeek, AceMath]
category: "ai-ml"
memo: "[HF Blog] Fixing Open LLM Leaderboard with Math-Verify"
processed_at: "2026-04-08T09:47:18.055266"
---

## 要約

HuggingFaceのOpen LLM Leaderboardで使用されていた数学評価（MATH-Hard）に重大な問題があり、Math-Verifyという新しいパーサーで全3,751モデルを再評価した。MATH-Hardタスクは、Hendrycks MATHデータセットの難易度Level 5の1,324問題を5-shotで評価するもの。従来の評価パイプラインはMinerva-Math論文の形式に従った回答を要求し、SymPyで数式解析後にgold answerと比較していた。問題は3段階で発生していた。第一に、モデルが規定フォーマット（'Final answer is [ANSWER]. I hope it is correct.'）に従わず、\boxed{}記法やその他の表現で答えを提示した場合、正解であっても抽出失敗（None）と判定された。第二に、SymPyでのLaTeX→数式変換時に、集合（union）、区間記法、行列、パーセント表記等が正しく解析できなかった。第三に、比較段階で小数丸め（1/3 vs 0.333...）、数値評価（sqrt(1/2)*7 vs sqrt(0.5)*7）、変数代入（k=1 vs 1）、行列同値、集合比較がサポートされておらず、正解が不正解と判定された。Math-Verifyはこれらすべての問題を修正し、コード3行の変更で導入可能。再評価の結果、全体平均で61問多く正解（+4.66ポイント）となった。特にAlgebra（+8.27）とPrealgebra（+6.93）サブセットの改善が顕著で、一部モデルでは+90ポイントに達した。モデルファミリー別では、Qwenモデルがスコア2倍以上、DeepSeekモデルが約3倍の改善（\boxed{}記法が抽出不能だったため）。Top20の順位が大幅に変動し、NvidiaのAceMathモデルがMATH-Hardで首位を獲得、Qwen派生モデルがその直下を占めた。評価システムの実装バグがベンチマーク順位に与える影響の大きさを示す事例。

## アイデア

- 評価パーサーの実装バグが数学ベンチマーク順位を最大3倍変動させる可能性があり、ベンチマーク結果の信頼性はモデル能力だけでなく評価インフラの品質に強く依存する
- \boxed{}、区間記法、行列、集合など数学的表現の多様性を扱うには、正規表現やSymPy単独では不十分で、専用パーサーが必要というアーキテクチャ上の教訓
- コード3行の変更で全評価結果が覆るという事実は、評価パイプラインのテスト・検証の重要性を示しており、CI/CDに評価システムの単体テストを組み込む必要性を示唆する

## Yujiの取り組みへの示唆

監査エージェントでLLM-as-judgeを活用する際、評価パーサーの実装品質が最終判定の正確性に直接影響する点は重要な示唆。構造化出力（JSON、数式、法令条文番号等）の抽出で同様の問題が発生しうるため、Math-Verifyのような専用バリデーターの設計パターンが参考になる。Pydanticでの出力スキーマ検証と組み合わせ、エージェントの回答抽出ロジックを堅牢化する際の設計指針として活用できる。

## 原文リンク

[Math-VerifyによるOpen LLMリーダーボードの数学評価修正](https://huggingface.co/blog/math_verify_leaderboard)
