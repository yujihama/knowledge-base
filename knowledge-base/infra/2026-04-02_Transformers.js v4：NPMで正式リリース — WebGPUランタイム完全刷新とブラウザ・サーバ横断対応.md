---
title: "Transformers.js v4：NPMで正式リリース — WebGPUランタイム完全刷新とブラウザ・サーバ横断対応"
url: "https://huggingface.co/blog/transformersjs-v4"
date: 2026-04-02
tags: [Transformers.js, WebGPU, ONNX Runtime, JavaScript, NPM, MoE, Mamba, エッジAI推論, esbuild, ModelRegistry]
category: "infra"
memo: "[HF Blog] Transformers.js v4 Preview: Now Available on NPM!"
related: [152, 641, 1102, 1159, 650]
processed_at: "2026-04-02T09:07:09.271148"
---

## 要約

Transformers.js v4が2026年2月9日にNPMで正式リリースされた。2025年3月から約1年の開発期間を経た本バージョンの最大の変更点は、WebGPUランタイムをC++で完全書き直ししたことである。ONNXランタイムチームと共同でテストされたこの新ランタイムは、ブラウザ・Node.js・Bun・Denoを横断して同一コードで動作し、WebGPUによるハードウェアアクセラレーションをサーバサイドJavaScript環境でも利用可能にした。

パフォーマンス面では、`com.microsoft.MultiHeadAttention`オペレータの採用によりBERT系埋め込みモデルで約4倍の高速化を達成。`com.microsoft.GroupQueryAttention`、`com.microsoft.MatMulNBits`、`com.microsoft.QMoE`等のONNX Runtime Contrib Operatorを活用し、LLMの推論を最適化している。

ビルドシステムはWebpackからesbuildへ移行し、ビルド時間が2秒から200ミリ秒（10倍高速化）に短縮。デフォルトエクスポートの`transformers.web.js`はバンドルサイズが53%削減された。

リポジトリ構造はpnpmワークスペースを用いたモノレポに移行。v3では8000行超の単一ファイルだった`models.js`をモジュール分割し、保守性を大幅に向上させた。

新規対応モデルとしてGPT-OSS、Chatterbox、GraniteMoeHybrid、LFM2-MoE、HunYuanDenseV1、Olmo3、FalconH1等を追加。アーキテクチャレベルではMamba（状態空間モデル）、Multi-head Latent Attention（MLA）、Mixture of Experts（MoE）をサポート。これらすべてWebGPU対応済み。

新API`ModelRegistry`はプロダクション向けで、`get_pipeline_files`でロード前にファイル一覧取得、`get_file_metadata`でファイルサイズ確認、`is_pipeline_cached`でキャッシュ状態確認、`get_available_dtypes`で利用可能な精度型（fp32/fp16/q4/q4f16等）照会が可能。`env.useWasmCache`でWASMランタイムキャッシュ、`env.fetch`でカスタムfetch実装（認証ヘッダ付与等）にも対応する。

## アイデア

- WebGPUランタイムをC++で再実装することで、ブラウザ・Node・Bun・Deno間の推論コード共通化が実現した点 — 環境差異の吸収をランタイム層に押し込む設計思想
- ONNX Runtime Contrib Operatorを積極活用してBERT系で4倍高速化を達成した点 — 標準オペレータではなく拡張オペレータを使いこなすことがパフォーマンスの鍵
- `ModelRegistry`によるロード前の資産検査API — ダウンロードサイズ計算・キャッシュ確認・精度型照会をパイプライン実行前に行える設計はプロダクション運用で実用的
## 関連記事

- /deep_152 トークンを流し続けろ：16のオープンソースRLライブラリから学ぶ非同期学習アーキテクチャ
- /deep_641 トレーニング不要なエキスパート言語モデルの動的アップサイクリング
- /deep_1102 WebGPUディスパッチオーバーヘッドのLLM推論への影響：4社GPU・3バックエンド・3ブラウザ横断的な特性分析
- /deep_1159 WebGPUのLLM推論におけるディスパッチオーバーヘッドの特性評価：4社のGPUベンダー・3つのバックエンド・3つのブラウザにわたる比較
- /deep_650 Vision Language Models（より良く、より速く、より強く）- 2025年最新動向

## 原文リンク

[Transformers.js v4：NPMで正式リリース — WebGPUランタイム完全刷新とブラウザ・サーバ横断対応](https://huggingface.co/blog/transformersjs-v4)
