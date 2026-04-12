---
title: "Intel Xeon上でStarCoderを高速化：Q8/Q4量子化とSpeculative Decoding"
url: "https://huggingface.co/blog/intel-starcoder-quantization"
date: 2026-04-09
tags: [量子化, SmoothQuant, Weight-Only-Quantization, Speculative-Decoding, Intel-Xeon, StarCoder, IPEX, INT4, INT8, Optimum-Intel]
category: "infra"
memo: "[HF Blog] Accelerate StarCoder with 🤗 Optimum Intel on Xeon: Q8/Q4 and Speculative Decoding"
processed_at: "2026-04-09T21:06:20.307111"
---

## 要約

本記事は、Hugging Face の Optimum Intel を使用し、Intel 第4世代 Xeon Scalable プロセッサ上でコード生成LLM「StarCoder-15B」を最大7倍以上高速化した取り組みを解説する。

【ベースライン】PyTorch + Intel Extension for PyTorch（IPEX）を用いたBF16精度でのStarCoder-15B推論を基準とする。評価には HumanEval データセット（164問）を使用し、pass@1精度・TTFT（Time To First Token）・TPOT（Time Per Output Token）を計測。

【INT8量子化（SmoothQuant）】アクティベーションの特定チャネルに大きな外れ値が存在するため、通常の静的量子化はLLMに不向き。SmoothQuantは事前スムージングスケーリング係数を重みとアクティベーション両方に適用し外れ値を平滑化。MBPPデータセットでキャリブレーション後にQ8-StarCoderを生成。精度劣化なし（わずかに改善）で、TTFTが約2.19倍、TPOTが約2.20倍の高速化を達成。

【INT4量子化（Weight Only Quantization）】BF16比でモデルサイズを4倍削減するが、演算前に16bitへのデクオンタイズが必要でFLOPS面のオーバーヘッドが生じる。グループサイズ128の非対称RTN量子化によりHumanEvalでの精度を維持しつつ、TPOTで3.35倍の高速化。ただし初期トークン生成（TTFT）は演算オーバーヘッドにより0.84倍に低下。

【ボトルネックの非対称性】最初のトークン生成（プロンプト全体の並列処理）はFLOPS律速のため、演算精度が高いINT8が有利。2トークン目以降の自己回帰生成はメモリ帯域律速のため、モデルサイズが小さいINT4が有利。この非対称性がINT8とINT4の使い分けの根拠となる。

【Speculative Decoding（Assisted Generation）】ドラフトモデル（StarCoderBase-1B）で複数トークンを仮生成し、ターゲットモデル（StarCoder-15B）が一括検証する手法。INT4量子化と組み合わせることでTPOTがさらに向上し、BF16比で合計7倍以上の高速化を実現。Speculative Decodingは出力品質を数学的に保証しつつ（拒否サンプリングにより）スループットを改善する点が特徴。

【環境・ツール】Intel AMX（Advanced Matrix Extensions）が BF16・INT8 GEMM をハードウェアアクセラレーション。Optimum Intel ライブラリ経由で quantization・assisted generation を統合的に利用可能。デモは HuggingFace Spaces 上で第4世代 Xeon で稼働中。

## アイデア

- TTFT（初期トークン）はFLOPS律速、TPOT（後続トークン）はメモリ帯域律速という非対称なボトルネック構造は、ハイブリッド量子化戦略（プリフィルはINT8、デコードはINT4）の設計根拠として汎用的に応用できる
- 1Bのドラフトモデルと15Bのターゲットモデルを組み合わせたSpeculative Decodingは、精度を保ちながらスループットを倍増させる手法であり、エージェントの応答速度改善に直接応用可能
- SmoothQuantのスムージングスケーリングによるアクティベーション外れ値の抑制は、LLM量子化における汎用的な前処理テクニックとして他モデルにも転用できる
## 関連記事

- /deep_1116 🤗 Optimum IntelとfastRAGによるCPU最適化エンベディング
- /deep_988 QuantoとDiffusersによるメモリ効率的なDiffusion Transformerの推論
- /deep_944 LLMを1.58ビットに Fine-tuning: 極限量子化を手軽に実現する方法
- /deep_424 Intel CPU上でVLMを3ステップで動かす方法（OpenVINO + SmolVLM2）
- /deep_834 GCP第5世代XeonにおけるLLMパフォーマンスベンチマーク：C4 vs N2インスタンス比較

## 原文リンク

[Intel Xeon上でStarCoderを高速化：Q8/Q4量子化とSpeculative Decoding](https://huggingface.co/blog/intel-starcoder-quantization)
