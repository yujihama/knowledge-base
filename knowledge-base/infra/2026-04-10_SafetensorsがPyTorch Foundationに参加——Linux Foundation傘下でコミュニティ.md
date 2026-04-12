---
title: "SafetensorsがPyTorch Foundationに参加——Linux Foundation傘下でコミュニティガバナンスへ移行"
url: "https://huggingface.co/blog/safetensors-joins-pytorch-foundation"
date: 2026-04-10
tags: [Safetensors, PyTorch Foundation, Linux Foundation, モデルシリアライズ, ゼロコピーロード, 量子化, FP8, GPTQ, AWQ, Tensor Parallel]
category: "infra"
memo: "[HF Blog] Safetensors is Joining the PyTorch Foundation"
processed_at: "2026-04-10T09:41:11.957344"
---

## 要約

Hugging Faceが開発したモデル重みの保存フォーマット「Safetensors」が、2026年4月8日付けでPyTorch Foundationにホストプロジェクトとして参加した。同Foundationには既にDeepSpeed、Ray、vLLM、PyTorch本体などが参加しており、Safetensorsはこれらと並ぶ形でLinux Foundation傘下のベンダーニュートラルなガバナンス体制に移行する。

Safetensorsが誕生した背景には、pickle形式の危険性がある。従来のPyTorchモデル保存に使われていたpickle形式は任意コードを実行できるため、オープンなモデル共有が普及した現在ではマルウェアリスクが深刻だった。Safetensorsはこれを解決するため、JSONヘッダー（上限100MB）でテンソルのメタデータを記述し、その後ろに生のテンソルデータを配置するシンプルな構造を採用している。ゼロコピーロード（ディスクからテンソルを直接メモリマップ）とレイジーロード（チェックポイント全体をデシリアライズせずに特定の重みだけ読み込む）により、大規模モデルの効率的な扱いを実現している。現在Hugging Face Hub上の数万モデルがこのフォーマットを採用しており、事実上のデファクトスタンダードとなっている。

ガバナンス面では、商標・リポジトリ・ガバナンス文書（GOVERNANCE.md、MAINTAINERS.md）がLinux Foundationに移管された。HFのコアメンテナー2名（LucとDaniel）はTechnical Steering Committeeに残り、日常的な開発をリードし続ける。ユーザー視点では破壊的変更は一切なく、既存のAPIおよびHubインテグレーションはそのまま維持される。

今後のロードマップとして、(1) PyTorchコアのシリアライズシステムとしてSafetensorsを採用する取り組み、(2) CUDA・ROCm等のアクセラレータへの直接ロードを実現するデバイスアウェアなload/save API、(3) Tensor Parallel・Pipeline Parallel向けのファーストクラスAPI（各ランクやパイプラインステージが必要な重みのみロード可能に）、(4) FP8・GPTQ・AWQなどのブロック量子化フォーマットやサブバイト整数型のサポート正式化——が挙げられている。これらの課題をPyTorch Foundation内の他プロジェクト（vLLM、Ray等）と協調して解決できる体制が整った点が今回の移管の最大の意義といえる。

## アイデア

- JSONヘッダー＋生バイナリのシンプルな二層構造が、pickle形式の任意コード実行リスクを根本から排除している点——フォーマット設計でセキュリティを担保するアプローチは監査ツール設計にも応用できる発想
- レイジーロードによりチェックポイント全体を展開せず特定の重みのみ読み込める仕組みは、大規模モデルのTensor Parallel/Pipeline Parallel推論における帯域・メモリ効率に直結する実用上の優位点
- 商標とガバナンスをLinux Foundation（単一企業ではなく）に移管することで、長期的な中立性とエコシステム全体の信頼を確保するオープンソースプロジェクトの持続可能な運営モデルとして参考になる
## 関連記事

- /deep_988 QuantoとDiffusersによるメモリ効率的なDiffusion Transformerの推論
- /deep_524 NVIDIA NIMでHugging Face上の10万以上のLLMを高速デプロイ
- /deep_1266 🤗 Transformersでネイティブサポートされる量子化スキームの概要
- /deep_1116 🤗 Optimum IntelとfastRAGによるCPU最適化エンベディング
- /deep_1528 補償ベースLLM量子化における残差誤差の再考

## 原文リンク

[SafetensorsがPyTorch Foundationに参加——Linux Foundation傘下でコミュニティガバナンスへ移行](https://huggingface.co/blog/safetensors-joins-pytorch-foundation)
