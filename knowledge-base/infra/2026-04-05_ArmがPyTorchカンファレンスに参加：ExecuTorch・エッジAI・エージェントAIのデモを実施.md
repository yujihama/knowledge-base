---
title: "ArmがPyTorchカンファレンスに参加：ExecuTorch・エッジAI・エージェントAIのデモを実施"
url: "https://huggingface.co/blog/Arm/arm-at-pytorch-conference"
date: 2026-04-05
tags: [ExecuTorch, PyTorch, vLLM, MixtureOfExperts, エッジAI, Yellow Teaming, Arm, モバイル推論]
category: "infra"
memo: "[HF Blog] Arm will be @ PyTorch Conference, Join Us!"
related: [425, 113, 419, 1611, 1434]
processed_at: "2026-04-05T12:09:52.957385"
---

## 要約

2025年10月22〜23日に開催されるPyTorchカンファレンスに、Armがブース出展・セッション登壇する旨の告知記事。内容はイベント参加の呼びかけが中心であり、新技術の詳細発表ではなく、Armが提供する展示・ワークショップ・ユーザーインタビューの紹介にとどまる。

【ブース展示（Booth P1）】Armブースでは以下のデモが実施された：（1）ニューラルグラフィクスのトレーニング、（2）音声生成・音声認識ワークロードの実行、（3）エージェントAIワークフローの探索。使用技術として、クラウド向けにはvLLMおよびMixture of Experts（MoE）、モバイル・ゲーミング・エッジAI向けにはExecuTorchが採用されている。ExecuTorchはPyTorchのモバイル推論フレームワークであり、2025年8月時点でバージョン0.7がリリースされ「生成AIの大衆化」を目的として開発が進んでいる。

【ワークショップ：AIプロダクト強化セッション】デザイン専門家との1対1ワークショップでは、UX改善に加え「Yellow Teaming」の実践を紹介。Yellow Teamingとは、AIシステムのデプロイ前にリスク・意図しない結果・公平性・透明性・プライバシー・セキュリティ上の問題を事前に特定・評価・軽減するプロアクティブな手法。Red Teaming（攻撃的テスト）の概念を発展させたもので、責任あるAI開発のプロセスとして位置づけられている。

【Voice of the Developer セッション】30分の1対1インタビューセッションで、開発者がAIをクラウド・エッジ・モバイル上でどのように構築・デプロイ・スケールさせているかについての知見を収集。NVIDIA/x86からArmへの移行体験、大規模モデルのプロファイリング・デバッグ、エッジでのLLM安定稼働といった課題が焦点。収集された知見はArm次世代AIツール・SDK・ドキュメントの改善に直接反映される予定。

全体として本記事は技術的な新発表ではなく、イベント参加を促すマーケティング記事。ただし、Armがエッジ・モバイル推論（ExecuTorch）、クラウドLLM推論（vLLM＋MoE）、エージェントAIワークフロー、責任あるAI（Yellow Teaming）を主要訴求軸としていることが確認できる。

## アイデア

- Yellow Teamingという概念：Red Teamingの発展形として、デプロイ前に公平性・透明性・プライバシー・セキュリティリスクを体系的に特定する手法。監査システムの事前リスク評価プロセスと親和性が高い
- ExecuTorch v0.7によるエッジ・モバイルでの生成AI推論：クラウドに依存しないオンデバイス推論基盤として、低レイテンシ・プライバシー保護が求められる用途（監査現場でのオフライン利用など）への応用可能性
- vLLM＋MoEをクラウドArm上で動かすユースケース：NVIDIA GPU前提だったLLMサービングをArm CPUベースのインフラに移行できる可能性を示しており、コスト・消費電力面での代替選択肢として注目
## 関連記事

- /deep_425 Arm & ExecuTorch 0.7：ジェネレーティブAIを大多数のデバイスへ
- /deep_113 金融時系列予測でLightGBM / LSTM / Transformerを比較してみた
- /deep_419 連続バッチ処理（Continuous Batching）をゼロから理解する
- /deep_1611 近接方策最適化（PPO）：方策更新を安定させるクリッピング手法
- /deep_1434 生成AIワークロードの電力プロファイル計測：データセンター全体インフラ計画のための手法

## 原文リンク

[ArmがPyTorchカンファレンスに参加：ExecuTorch・エッジAI・エージェントAIのデモを実施](https://huggingface.co/blog/Arm/arm-at-pytorch-conference)
