---
title: "JAX / Flax で Stable Diffusion を高速推論する方法"
url: "https://huggingface.co/blog/stable_diffusion_jax"
date: 2026-04-11
tags: [JAX, Flax, TPU, StableDiffusion, HuggingFace, Diffusers, bfloat16, pmap, JIT]
category: "infra"
memo: "[HF Blog] 🧨 Stable Diffusion  in JAX / Flax !"
processed_at: "2026-04-11T09:09:48.565012"
---

## 要約

HuggingFaceのDiffusersライブラリ v0.5.1 以降でFlaxがサポートされ、Google TPU上でStable Diffusionの超高速推論が可能になったことを解説したブログ記事。JAXはTPU専用ではないが、各TPUサーバーが8つのTPUアクセラレータを並列動作させる構成と特に相性が良い。

主要な技術的ポイントは以下の通り。

**モデルロードと型精度**: FlaxのパイプラインはFlaxStableDiffusionPipelineを使用し、`from_pretrained`でパイプライン本体とパラメータ辞書を別々に返す（Flaxがステートレスな関数型フレームワークであるため）。TPUはbfloat16をネイティブサポートしており、float32と比べてメモリ効率が高い。

**並列化の仕組み**: 8台のTPUデバイスに対してモデルパラメータを`flax.jax_utils.replicate`で複製し、プロンプトのトークンIDを`shard`で分割する。各デバイスが(1, 77)形状のテンソルを受け取り、8枚の画像を同時生成する。これにより、1枚分の時間で8枚が生成できる。

**JITコンパイルの効果**: `jit=True`を指定することで、JAXコードが効率的な表現にコンパイルされる。初回コンパイルにTPU v2-8で1分以上かかるが、以降の推論（入力が異なっても同形状であれば）は約7秒で完了する。入力形状が変わるとコンパイルがやり直しになるため、一定の形状を維持することが重要。

**乱数管理**: Flaxでは乱数は関数に明示的に渡す設計になっており、`jax.random.PRNGKey`でシードを固定することで分散環境でも完全に再現性が確保される。8デバイスそれぞれに異なるrngを`jax.random.split`で配布することで、各デバイスが異なる画像を生成する。

**出力形状**: 推論結果は(8, 1, 512, 512, 3)のテンソルで返り、reshapeとnumpy_to_pilでPIL画像8枚に変換する。CLIPテキストエンコーダーのトークン長は77固定。

ライセンスはCreativeML OpenRAIL-Mで、出力物の権利はユーザー側にあるが、違法・有害コンテンツ生成の禁止条項がある。

## アイデア

- Flaxのステートレス設計（パラメータとモデル本体の分離）は、マルチデバイス並列化を`replicate`一発で実現できる点で非常にクリーンなアーキテクチャ
- JAXのJITコンパイルは「同形状の入力に対してのみキャッシュが有効」という制約があり、バッチサイズや系列長を動的に変えるシステム設計では注意が必要
- 8デバイスへの乱数の明示的な分割（split）による再現性担保は、分散強化学習（GRPO等）でのロールアウト生成の設計思想と共通しており、デバッグ・実験管理に示唆がある

## Yujiの取り組みへの示唆

直接的な監査AIへの応用は薄いが、JAX/Flaxの並列化パターン（replicate/shard/pmap）はGRPOやRLAIFでの大規模ロールアウト生成を分散TPU/GPU上で実装する際の設計参考になる。特に乱数の明示的管理による再現性確保の思想は、LLM-as-judgeやRLAIFの評価実験で結果の再現性を担保する設計に応用できる。

## 原文リンク

[JAX / Flax で Stable Diffusion を高速推論する方法](https://huggingface.co/blog/stable_diffusion_jax)
