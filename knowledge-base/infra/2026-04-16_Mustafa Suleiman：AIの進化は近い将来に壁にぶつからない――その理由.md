---
title: "Mustafa Suleiman：AIの進化は近い将来に壁にぶつからない――その理由"
url: "https://www.technologyreview.com/2026/04/08/1135398/mustafa-suleyman-ai-future/"
date: 2026-04-16
tags: [compute-scaling, GPU, HBM, NVLink, InfiniBand, Moore's Law, Epoch AI, AI-agent, エネルギー, Microsoft AI]
category: "infra"
related: [404, 518, 828, 408, 488]
memo: "[MIT Technology Review AI] Mustafa Suleyman: AI development won’t hit a wall anytime soon—here’s why"
processed_at: "2026-04-16T12:28:29.875049"
---

## 要約

Microsoft AI CEOのMustafa Suleimanが、AIの進化が「壁に当たる」という懐疑論を否定し、指数的な計算能力の拡大が今後も続く根拠を論じた記事。

2010年から現在にかけて、フロンティアモデルの学習に使われる計算量は約10^14 FLOPSから10^26 FLOPSへと1兆倍増加した。これを支える三つの技術的進展が同時進行している。第一にNvidiaのGPU性能が2020年の312テラFLOPSから現在の2,250テラFLOPSへと6年で7倍以上向上。第二にHBM（High Bandwidth Memory）がスタック構造で帯域幅を大幅に向上させ（HBM3は前世代比3倍）、GPUへのデータ供給がボトルネックにならなくなった。第三にNVLinkやInfiniBandにより数十万GPUをウェアハウス規模で単一の計算エンティティとして結合できるようになった。

これらの相乗効果により、ある言語モデルの学習時間が2020年には8GPU×167分かかっていたものが、現在の等価ハードウェアでは4分未満に短縮。Moore's Lawが予測する5倍に対し実測50倍の改善が達成された。

ソフトウェア面でもEpoch AIの研究によると、固定性能水準に達するために必要な計算量は約8ヶ月ごとに半減しており、従来のMoore's Law（18〜24ヶ月）を大きく上回るペースで効率化が進んでいる。一部モデルの推論コストは年率換算で最大900分の1まで低下した。

将来見通しとして、主要ラボの計算能力は年率約4倍で拡大中であり、2027年には世界のAI関連計算能力がH100換算で1億個相当（3年で10倍）に達する見込み。2028年末までに実効計算能力は今後さらに約1,000倍に達すると予測される。エネルギー問題についても、太陽光発電コストが50年で約100分の1、バッテリーコストが30年で97%減というエネルギー技術の指数的低下によってクリーンなスケーリングへの道筋があるとしている。

Suleimanはこれらを基に、チャットボットから「ほぼ人間レベルのエージェント」への移行が起きると予測。数日間のコード記述、数週間〜数ヶ月規模のプロジェクト実行、交渉・物流管理を自律的にこなすセミオートノマスなAIワーカーチームの実現を展望している。監査エージェント開発の観点からは、長期間の自律タスク実行能力の急速な向上は、監査プロセスの自動化範囲の拡大と複雑なワークフロー管理への応用可能性を示唆する。

## アイデア

- Moore's Law（5倍/6年）を大幅に超える実測50倍の計算効率改善：ハードウェア・メモリ帯域・ネットワーク相互接続の3要素が同時進化したことで従来の予測モデルが機能しなくなっている点
- 「計算量の半減時間が8ヶ月」というEpoch AIの知見：アルゴリズム効率化がハードウェア改善と独立して進行しており、実効スケーリングの加速が二重に生じている点
- エネルギーコストの指数的低下がコンピュート拡大の物理的上限を緩和するという構造：AI計算需要の急増と再エネコスト低下が同時進行するため、エネルギーは絶対的な制約にならないという論点

## 前提知識

- **FLOPs / 計算量スケーリング** (TODO: 読むべき)
- **Moore's Law** → /deep_1763 Mustafa Suleyman: AIの発展は近い将来壁にぶつからない——その理由
- **HBM (High Bandwidth Memory)** (TODO: 読むべき)
- **NVLink / InfiniBand** (TODO: 読むべき)
- **AIエージェント** → /deep_2 AIエージェント自作のための基礎知識 - Google ADK (Go) を使ったエージェント構築

## 関連記事

- /deep_404 Ulyssesシーケンス並列化：100万トークンコンテキストでのLLM学習
- /deep_518 TransformerベースニューラルネットワークのGPU高速化リアルタイム推論最適化
- /deep_828 PyTorchにおけるGPUメモリの可視化と理解
- /deep_408 Google Cloud の GPU 付き Cloud Run で Ollama + ローカル LLM を動かす
- /deep_488 Claude Code × Google Colab 第3弾：PyTorch LSTMで東京の気温7日間予測（GPU使用）

## 原文リンク

[Mustafa Suleiman：AIの進化は近い将来に壁にぶつからない――その理由](https://www.technologyreview.com/2026/04/08/1135398/mustafa-suleyman-ai-future/)
