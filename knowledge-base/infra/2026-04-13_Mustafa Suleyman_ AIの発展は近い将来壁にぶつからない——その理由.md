---
title: "Mustafa Suleyman: AIの発展は近い将来壁にぶつからない——その理由"
url: "https://www.technologyreview.com/2026/04/08/1135398/mustafa-suleyman-ai-future/"
date: 2026-04-13
tags: [GPU, HBM3, NVLink, InfiniBand, Maia200, compute-scaling, Moore's Law, Epoch AI, エージェント移行, エネルギー]
category: "infra"
related: [404, 518, 828, 408, 488]
memo: "[MIT Technology Review AI] Mustafa Suleyman: AI development won’t hit a wall anytime soon—here’s why"
processed_at: "2026-04-13T12:38:12.144307"
---

## 要約

Microsoft AI CEOのMustafa Suleimanが、AIの計算能力が指数関数的に拡大し続ける理由を技術的根拠とともに論じた論考。2010年から現在までの間に、フロンティアモデルの学習に使われる計算量は約10¹⁴ FLOPsから10²⁶ FLOPsへと1兆倍増加した。Suleimanはこの背景として三つの収束を挙げる。第一にチップの高速化：NvidiaのGPUは2020年の312テラFLOPsから現在の2,250テラFLOPsへと6年間で7倍超に向上し、MicrosoftのMaia 200チップは従来ハードウェア比で30%のコスト効率改善を達成。第二にメモリ帯域幅の向上：HBM3（High Bandwidth Memory）の垂直積層技術により帯域幅を3倍にし、GPUの待機時間を解消。第三にクラスタ規模の拡大：NVLinkやInfiniBandにより数十万GPUをウェアハウス規模の単一計算エンティティとして接続可能になった。これらの相乗効果として、言語モデルの学習時間が2020年の8GPU×167分から現在の同等ハードウェアで4分未満に短縮。Moore's Lawが5倍の改善を予測する期間に実際は50倍を達成している。ソフトウェア側でもEpoch AIの研究によれば、一定性能達成に必要な計算量が約8ヶ月ごとに半減するペースで効率化が進み、一部モデルの推論コストは年率換算で最大900分の1まで低下した。今後の予測として、フロンティアモデルの学習計算量は年率5倍ペースで成長しており、2027年までにグローバルなAI関連計算能力がH100換算1億基（現在比10倍）に達する見込み。2028年末までに実効計算量がさらに約1,000倍になるとSuleimanは推計する。エネルギー問題については、太陽光発電コストが50年で100分の1、バッテリー価格が30年で97%低下という別の指数関数的トレンドが相殺する可能性を示唆。この計算能力の爆発的増大が意味するのは、単純な質問応答チャットボットから「数日間コードを書き続け、数週間〜数ヶ月単位のプロジェクトを実行し、交渉・調整・実行を行う」半自律エージェントへの移行であり、認知労働を基盤とするすべての産業の変革を予告する。監査エージェント開発への示唆として、エージェントが週〜月単位の長期タスクを自律実行できる計算基盤が2028年前後に整うという視点は、LangGraphベースの監査エージェントのロードマップ設計において、現在の単タスク完結型設計から長期マルチステップ設計への移行時期を見極める根拠となりうる。

## アイデア

- ソフトウェア効率化（8ヶ月ごとに必要計算量が半減）がハードウェアのMoore's Law（18〜24ヶ月で2倍）を大幅に上回るペースで進行しており、コスト低下の主因がハードではなくソフト側にシフトしている点
- NVLink/InfiniBandによる数十万GPU統合という『クラスタ規模』の次元が、チップ単体性能向上とは独立した第三の指数関数的スケーリング軸として機能している構造
- AIの電力需要増大と再生可能エネルギーコスト低下という二つの指数関数が同時進行しており、エネルギー制約がボトルネックにならない『クリーンスケーリング』経路が現実的になりつつある点

## 前提知識

- **FLOPs（浮動小数点演算）** (TODO: 読むべき)
- **Moore's Law** (TODO: 読むべき)
- **HBM（High Bandwidth Memory）** (TODO: 読むべき)
- **NVLink / InfiniBand** (TODO: 読むべき)
- **フロンティアモデルのスケーリング則** (TODO: 読むべき)

## 関連記事

- /deep_404 Ulyssesシーケンス並列化：100万トークンコンテキストでのLLM学習
- /deep_518 TransformerベースニューラルネットワークのGPU高速化リアルタイム推論最適化
- /deep_828 PyTorchにおけるGPUメモリの可視化と理解
- /deep_408 Google Cloud の GPU 付き Cloud Run で Ollama + ローカル LLM を動かす
- /deep_488 Claude Code × Google Colab 第3弾：PyTorch LSTMで東京の気温7日間予測（GPU使用）

## 原文リンク

[Mustafa Suleyman: AIの発展は近い将来壁にぶつからない——その理由](https://www.technologyreview.com/2026/04/08/1135398/mustafa-suleyman-ai-future/)
