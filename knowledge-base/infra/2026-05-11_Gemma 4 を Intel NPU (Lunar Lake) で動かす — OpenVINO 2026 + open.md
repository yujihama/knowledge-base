---
title: "Gemma 4 を Intel NPU (Lunar Lake) で動かす — OpenVINO 2026 + openvino-genai"
url: "https://zenn.dev/jkudo/articles/ae85d7d099e672"
date: 2026-05-11
tags: [OpenVINO, Intel NPU, Gemma 4, openvino-genai, 量子化 INT4, Lunar Lake, LLMローカル実行, OpenAI互換サーバ, VLMPipeline]
category: "infra"
related: [2696, 2924, 3483, 943, 1530]
memo: "[Zenn LLM] Gemma 4 を Intel NPU (Lunar Lake) で動かす — OpenVINO 2026 + openvino-genai"
processed_at: "2026-05-11T21:32:22.637525"
---

## 要約

Intel Core Ultra 7 258V (Lunar Lake) 搭載機の NPU (AI Boost) 上で Gemma 4 (E2B / E4B) を実用速度で動作させた実機検証レポート。ソフトウェアスタックは OpenVINO 2026.2.0 nightly + openvino-genai + transformers 5.5.0 + optimum-intel の非公式ブランチ (aleksandr-mokrov/gemma4-moe-fixes)。最終的に FastAPI ベースの OpenAI 互換 REST サーバとして仕上げ、OPENAI_BASE_URL を切り替えるだけで既存クライアントから利用可能な構成にしている。

性能ベンチマーク（60 秒持続生成、greedy）では E2B INT4 が NPU 24.9 tok/s・GPU 36.0 tok/s・CPU 12.0 tok/s、E4B INT4 が NPU 12.0 tok/s・GPU 18.5 tok/s・CPU 7.2 tok/s。TPS は全モデルで GPU (Arc 140V iGPU) が最速で、NPU は GPU の 60〜70% 程度。TTFT も GPU が 1 秒未満に対し NPU は 1.5〜2.4 秒と差がある。一方、電力効率（J/token）も GPU が最良で「NPU の方が効率が良い」は本検証では成立しなかった。NPU は絶対電力が 27〜30 W と GPU の 37〜39 W より 8〜10 W 低く、GPU を別作業（ゲーム・配信等）で占有したい場合や純粋なバッテリ重視時の代替として有効。

検証で判明した主な落とし穴は 8 点。①transformers 5.x の Gemma4TextAttention が is_kv_shared_layer (bool) を持つのに対し optimum-intel が kv_shared_layer_index (int) を期待する API 不整合（monkey-patch で対処）。②NPU の chunked decoder が S=1 reshape で全 NaN を出力するバグ（openvino#35222、min_new_tokens=2 で回避）。③Gemma 4 はマルチモーダルアーキテクチャのため LLMPipeline ではなく VLMPipeline が必須。④OpenVINO tokenizer は optimum-cli が出力しないため convert_tokenizer() を別途呼ぶ必要がある。⑤Windows の cp932 環境で日本語入出力時に UnicodeEncodeError（PYTHONUTF8=1 で回避）。⑥公式 OpenVINO IR (gemma-4-E4B-it-int4-ov) が NPU compile 時に「Found 96 duplicated names」で失敗—自前変換ブランチで解決。⑦31B モデルは「NPUW: num_layers.is_static() failed」で NPU 非対応。⑧26B-A4B (MoE) は 32 GB RAM では変換不可（peak 50+ GB）。

NPU チューニングとして CACHE_DIR 指定で初回 285〜365 秒のコンパイルをキャッシュ後 5〜8 秒に短縮、NPUW_LLM_GENERATE_HINT=BEST_PERF で TPS を baseline 9.8 から 18.1 tok/s へ約 85% 向上させることに成功している。監査エージェント開発への示唆として、ローカル LLM をオンデバイス NPU/GPU で稼働させ OpenAI 互換 API として公開するパターンは、機密データを外部送信せずに LLM 推論を完結させる内部監査システムの構成として参考になる。ただし Lunar Lake NPU は E4B INT8 (LM 4.4 GB) で device hang が発生するなど実用メモリ上限が厳しく、大規模モデルは GPU またはクラウドへのフォールバック設計が必要。

## アイデア

- 公式 OpenVINO IR の INT4 量子化グラフに重複ノード名バグが存在し、コミュニティブランチ (gemma4-moe-fixes) の自前変換のみが NPU compile を通過するという『公式が使えない』構造的問題は、ローカル LLM 実行環境の成熟度を測る指標として興味深い
- NPU は絶対電力で GPU より 8〜10 W 低いにもかかわらず TPS が 60〜70% に留まるため J/token 効率では GPU に負けるという逆説—省電力ハードウェアが必ずしも効率的でない点は、エッジ AI 推論の電力設計において重要な示唆
- Gemma 4 がマルチモーダルアーキテクチャ (Gemma4ForConditionalGeneration) のためテキスト専用推論でも VLMPipeline 必須という設計は、モデルアーキテクチャの汎用化がランタイム API の複雑性を増す典型例であり、今後の LLM ローカル実行フレームワーク設計の課題を示している

## 前提知識

- **OpenVINO** → /deep_424 Intel CPU上でVLMを3ステップで動かす方法（OpenVINO + SmolVLM2）
- **INT4量子化** → /deep_425 Arm & ExecuTorch 0.7：ジェネレーティブAIを大多数のデバイスへ
- **NPU推論** (TODO: 読むべき)
- **Gemma 4アーキテクチャ** (TODO: 読むべき)
- **openvino-genai** (TODO: 読むべき)

## 関連記事

- /deep_2696 日本語入力システムSumibiの開発 part18: ローカルLLMが閾値を超えたかも
- /deep_2924 小規模モデルへの行動的傾向の蒸留：3段階にわたる否定的結果
- /deep_3483 Transformers.jsをChromeエクステンションで使う方法：Manifest V3対応アーキテクチャ解説
- /deep_943 Optimum-IntelとOpenVINO GenAIによるモデルの最適化とデプロイ
- /deep_1530 Optimum IntelとOpenVINOでTransformerモデルを高速化する

## 原文リンク

[Gemma 4 を Intel NPU (Lunar Lake) で動かす — OpenVINO 2026 + openvino-genai](https://zenn.dev/jkudo/articles/ae85d7d099e672)
