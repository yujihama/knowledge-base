---
title: "Neural Super Sampling（NSS）：ArmによるモバイルGPU向けAIアップスケーリング技術"
url: "https://huggingface.co/blog/Arm/neural-super-sampling"
date: 2026-04-06
tags: [Neural Super Sampling, 超解像, モバイルGPU, Arm, Neural Accelerator, リアルタイム推論, Unreal Engine, Vulkan, テンポラルアップスケーリング, HuggingFace]
category: "ai-ml"
memo: "[HF Blog] Neural Super Sampling is here!"
processed_at: "2026-04-06T21:05:44.573178"
---

## 要約

Neural Super Sampling（NSS）はArmが開発したリアルタイム・テンポラル・スーパーサンプリング向けのパラメータ予測モデルで、モバイルGPUのNeural Accelerator（NX）上での実行に最適化されている。低解像度の時系列入力フレームから高品質な高解像度フレームを再構成することで、GPUの計算コストを削減しながら高解像度レンダリングを実現する。

Enchanted Castleデモでは、540pでレンダリングしたフレームを1080pにアップスケールする処理を持続性能セットアップ下で4msで完了し、GPU負荷を50%削減することに成功している。NSSはモバイルゲーム、XR（拡張現実）、その他の電力制約のあるグラフィクス用途を主なターゲットとしている。

実装面では、Unreal Engine向けに2つのプラグインが提供されている。「NSS Plugin for Unreal® Engine」と「Unreal® NNE Plugin for ML extensions for Vulkan」である。開発者はこれらを通じてNSSをリアルタイムアプリケーションに統合できる。

学習データとしては「Neural Graphics Dataset」が公開されており、参照画像・画像シーケンスにモーション・深度などのデータが付属している。現バージョンはNSSモデル開発フローのデモ用として限定的なデータセットを含むにとどまるが、今後「Neural Graphics Model Gym」としてキャプチャ・変換ツールを含む包括的なデータセットが提供予定とされている。

モデルはHugging Faceで公開されており、開発者がすぐに実験を開始できる状態となっている。技術的な背景として、Arm Neural Technology上でのNeural Accelerator活用により、従来のGPUシェーダーベースのアップスケーリング（TAA、DLSSのモバイル版相当）に比べて電力効率の高い推論を実現する点が特徴である。

## アイデア

- 540p→1080pを4msで処理するリアルタイム超解像モデルの設計：時系列フレーム間の差分（モーション・深度情報）をパラメータ予測に活用することで、単一フレーム超解像より高品質な結果を低コストで実現している点
- Neural Accelerator（NX）専用最適化：汎用GPUシェーダーではなく、モバイルSoC内の専用ML推論ユニットにオフロードすることでGPU負荷を50%削減する設計思想は、エッジデバイスでのAI推論最適化の好例
- Neural Graphics Model Gymによるデータ収集・再学習パイプラインの公開予定：ゲームエンジンからの合成データ（モーション・深度・カラー）を用いたモデル学習フローは、ドメイン特化型AIモデルの継続的改善サイクルとして参考になる構成

## 原文リンク

[Neural Super Sampling（NSS）：ArmによるモバイルGPU向けAIアップスケーリング技術](https://huggingface.co/blog/Arm/neural-super-sampling)
