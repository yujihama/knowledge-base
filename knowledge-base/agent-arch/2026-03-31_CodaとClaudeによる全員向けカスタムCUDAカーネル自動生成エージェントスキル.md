---
title: "CodaとClaudeによる全員向けカスタムCUDAカーネル自動生成エージェントスキル"
url: "https://huggingface.co/blog/custom-cuda-kernels-agent-skills"
date: 2026-03-31
tags: [CUDA, エージェントスキル, Claude Code, Codex, HuggingFace, kernels, PyTorch, diffusers, transformers, H100, カーネル最適化, RMSNorm]
category: "agent-arch"
memo: "[HF Blog] Custom Kernels for All from Codex and Claude"
processed_at: "2026-03-31T21:09:01.054341"
---

## 要約

HuggingFaceは、コーディングエージェント（Claude Code、Codex等）がプロダクション品質のCUDAカーネルを自動生成できるようにする「エージェントスキル」を開発・公開した。このスキルは`kernels`ライブラリに同梱されており、`kernels skills add cuda-kernels --claude`の1コマンドで`.claude/skills/cuda-kernels/`に展開され、Claude CodeやCursorが自動的に読み込む。

スキルの構成は約550トークンのSKILL.md（構造化ガイドライン）に加え、GPU最適化ガイド（H100/A100/T4別）、diffusers・transformers統合パターン、カーネルテンプレート（BF16/FP16/FP32対応）、ベンチマークスクリプト、トラブルシューティングドキュメントで構成される。エージェントはこれを読み込むことで、アーキテクチャ固有のメモリアクセスパターン、ベクトル化戦略、warpシャッフルリダクション、PyTorchバインディング生成、build.toml設定まで自律的に実施できる。

実証として2つのターゲットに適用した。①diffusersのLTX-Video（動画生成パイプライン）向けにRMSNorm、RoPE 3D、GEGLU、AdaLNカーネルをH100 80GB HBM3上でBF16精度で生成。孤立RMSNormベンチマークでは平均1.88倍高速化（帯域効率34.7%）を達成。エンドツーエンドの49フレーム・30ステップ動画生成では、最適化カーネル＋torch.compileで1.43倍高速化（ベースライン比）。②transformersのQwen3-8B向けにRMSNormカーネルを生成し、中規模シーケンス長で最大2.16倍の高速化を実現（大規模シーケンスではFlashAttentionのボトルネックが支配的となり効果は限定的）。

生成されるプロジェクト構成は`kernel_src/`（.cuファイル）、`torch-ext/`（PyTorch C++バインディング）、ベンチマークスクリプト、build.toml、setup.py等の完全なプロジェクト形式。HuggingFace Kernel Hubとの統合により、生成したカーネルをコミュニティに配布・再利用する仕組みも提供されている。エージェントスキルとして「ドメイン知識をパッケージ化してオンデマンドでコンテキストに注入する」パターンの具体的な実装例であり、LLMトレーニングスキルなど既存の同パターンと一貫した設計思想に基づく。

## アイデア

- 「ドメイン知識をスキルファイルとしてパッケージ化し、エージェントのコンテキストにオンデマンド注入する」設計パターンは、CUDA以外の専門領域（会計基準、監査手順、法規制等）にも転用可能な汎用アーキテクチャ
- エージェントが生成したコードを即座にベンチマーク・バリデーションするループ（生成→ビルド→計測→改善）をスキル内に組み込むことで、LLMの出力品質を数値で担保する手法
- 約550トークンの構造化ガイドライン＋参照ドキュメント群という「小さなコアプロンプト＋グレップ可能な詳細ドキュメント」の構成は、長大なシステムプロンプトより検索効率が高く、エージェントの情報アクセスパターンに最適化されている

## Yujiの取り組みへの示唆

エージェントスキルとして「専門ドメイン知識をコンテキスト注入可能な構造化ドキュメント群にパッケージ化する」パターンは、監査エージェント開発に直接応用できる。監査基準（IIA基準、J-SOX要件、リスク評価フレームワーク等）をスキルファイルとして整備し、LangGraphエージェントのノードがオンデマンドで読み込む設計にすることで、汎用LLMを監査専門エージェントに変換できる。550トークンのSKILL.mdに主要指示を集約し、詳細をgrep可能なmdファイルに分散させる構成は、Pydanticによる型安全なツール定義と組み合わせることで、監査エージェントの信頼性向上に寄与する。

## 原文リンク

[CodaとClaudeによる全員向けカスタムCUDAカーネル自動生成エージェントスキル](https://huggingface.co/blog/custom-cuda-kernels-agent-skills)
