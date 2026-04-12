---
title: "Waypoint-1: Overworldによるリアルタイムインタラクティブ映像拡散モデル"
url: "https://huggingface.co/blog/waypoint-1"
date: 2026-04-03
tags: [video-diffusion, diffusion-forcing, self-forcing, DMD, world-model, rectified-flow, autoregressive-generation, real-time-inference, KV-cache, torch-compile]
category: "ai-ml"
memo: "[HF Blog] Introducing Waypoint-1: Real-time interactive video diffusion from Overworld"
processed_at: "2026-04-03T09:07:57.456690"
---

## 要約

Waypoint-1はOverworldが開発したリアルタイムインタラクティブ映像拡散モデルで、テキスト・マウス・キーボードによる制御を可能にする。バックボーンはフレーム因果整流フロートランスフォーマー（frame-causal rectified flow transformer）で、1万時間のビデオゲーム映像にコントロール入力とテキストキャプションを付与したデータセットで学習されている。潜在空間（latent）モデルであり、圧縮済みフレームを対象に訓練される。

既存のワールドモデルが事前学習済みビデオモデルをファインチューニングするアプローチを採るのに対し、Waypoint-1はインタラクティブ体験を最初から目的として設計されている。既存モデルでは数フレームごとにカメラを動かすだけで深刻なレイテンシが生じるが、Waypoint-1はマウスによる自由なカメラ操作とフルキーボード入力をゼロレイテンシで実現し、各フレームがコントロール入力を即時コンテキストとして生成される。

学習手法はdiffusion forcingを基盤とし、過去フレームを条件に未来フレームのノイズ除去を学習する因果アテンションマスクを使用。各フレームは個別にランダムノイズが付加され、推論時は1フレームずつ逐次生成するオートリグレッシブなストリーミングが可能。ただしdiffusion forcingではフレームごとの推論時にミスマッチが発生しエラーが蓄積する問題があるため、self-forcingによるポストトレーニングを実施。Self-forcingはDMD（Distribution Matching Distillation）経由で適用され、1パスCFGと少ステップのデノイジングという副次的メリットも得られる。

推論ライブラリWorldEngineはPure Pythonで実装された高性能インタラクティブワールドモデルストリーミング基盤。RTX 5090上でWaypoint-1-Small（2.3Bパラメータ）を動作させた際、毎秒約30,000トークンパス（1フレーム256トークン）を達成し、4ステップで30FPS、2ステップで60FPSを実現。最適化技術としてAdaLN特徴キャッシング、静的ローリングKVキャッシュ＋Flex Attention、QKV投影の行列積融合（matmul fusion）、torch.compile（fullgraph=True, mode=max-autotune）を組み合わせている。モデルの重みはHugging Face Hubで公開されており、コンシューマーハードウェア上でもシームレスな体験が可能とされている。

## アイデア

- diffusion forcingとself-forcingの組み合わせ：ランダムノイズ学習（diffusion forcing）だけでは推論時のフレームごとのロールアウトとミスマッチが生じエラーが蓄積するが、self-forcing＋DMDでそのギャップを埋め、少ステップ生成と1パスCFGを実現している点が設計上の重要な工夫
- AdaLN特徴キャッシングによる推論最適化：プロンプト条件付けとタイムステップが変わらない間はAdaLN条件付け投影をキャッシュして再利用することで、繰り返し計算を排除し高スループットを達成している
- インタラクティブ性を最初から設計に組み込む重要性：既存ワールドモデルの「ファインチューニングで制御を後付け」ではなく、コントロール入力を学習当初からアーキテクチャに統合することで、ゼロレイテンシかつフルキーボード対応を実現している

## 原文リンク

[Waypoint-1: Overworldによるリアルタイムインタラクティブ映像拡散モデル](https://huggingface.co/blog/waypoint-1)
