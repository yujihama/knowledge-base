---
title: "IntentVLM: 順逆モデリングとVideo-Language Modelsによるオープン語彙意図認識"
url: "https://tldr.takara.ai/p/2604.24002"
date: 2026-05-09
tags: [VLM, 意図認識, forward-inverse modeling, HRI, オープン語彙, ビデオ言語モデル, ハルシネーション抑制, 構造化推論]
category: "ai-ml"
related: [642, 1928, 3913, 21, 3817]
memo: "[HF Daily Papers] IntentVLM: Open-Vocabulary Intention Recognition through Forward-Inverse Modeling with Video-Language Models"
processed_at: "2026-05-09T09:42:27.365532"
---

## 要約

IntentVLMは、ヒューマンロボットインタラクション（HRI）における人間の意図理解を高精度に行うための2段階ビデオ言語フレームワーク。認知科学の「順逆モデリング（forward-inverse modeling）」からインスピレーションを得た設計が特徴。

従来の意図認識システムは、クローズドな語彙セット（固定ラベル）に依存するか、LLM/VLMによる直接推論に頼るため、ハルシネーション（幻覚生成）が問題となっていた。IntentVLMはこれを2段階に分解して対処する。第1段階（Forward Modeling）では、観測された動画・テキスト情報から「ゴール候補」を複数生成する。第2段階（Inverse Modeling）では、生成された候補群の中から構造化推論（structured inference）によって最も整合性の高い意図を選択する。この「生成→選択」パイプラインにより、潜在的推論空間でのハルシネーションを抑制しながら、オープン語彙（任意の自然言語表現）での意図認識を実現する。

モデルはVideo-Language Model（VLM）をバックボーンとして使用し、テキスト・視覚・動画の異種モダリティを統合して解釈する。評価はIntentQAおよびInst-IT Benchの2つのベンチマークで実施され、最大80%の精度を達成。ベースライン比で30ポイント超の改善を示し、人間レベルのパフォーマンスに匹敵した。また、新しいタスクへの学習後も既存の知識を保持する「破滅的忘却なし（without catastrophic forgetting）」という特性も確認されており、継続学習への耐性を持つ点も重要な知見。

監査エージェント開発への示唆としては、意図認識の「候補生成＋構造化選択」という2段階アーキテクチャが、監査エージェントにおける「異常候補列挙→根拠に基づく判定」という推論パターンに応用できる。特に、LLMが直接答えを出すのではなく、まず仮説空間を生成してから絞り込むアプローチは、監査判断の説明可能性・精度向上に有効と考えられる。

## アイデア

- 認知科学の順逆モデリングをVLMアーキテクチャに直接マッピングした点：「前向き（何が起きるか予測）」と「逆向き（何を意図していたか推定）」の分離は、エージェントの説明可能な推論設計に転用できる
- オープン語彙でのゴール候補生成→選択という2段階パイプラインがハルシネーションを30%以上削減した点：単一パスの生成より候補集合からの選択の方が信頼性が高いという実証結果
- 破滅的忘却なしで継続的タスク学習が可能な点：ロボット・エージェントの実運用において、追加ファインチューニングで既存能力を損なわない設計は実用上重要な特性

## 前提知識

- **Video-Language Model (VLM)** (TODO: 読むべき)
- **forward-inverse modeling** (TODO: 読むべき)
- **catastrophic forgetting** → /deep_230 Nested Learning：継続学習のための新しいMLパラダイム
- **open-vocabulary recognition** (TODO: 読むべき)
- **multimodal fusion** (TODO: 読むべき)

## 関連記事

- /deep_642 ConInfer: トレーニング不要なオープン語彙リモートセンシングセグメンテーションのための文脈認識推論
- /deep_1928 隠れた真実を見抜く：フィールド可視化から記号的解析解を推論するVisual-to-Symbolic AI
- /deep_3913 重要なものに重みを：トークン再重み付けによる医療レポート生成のサンプル効率向上
- /deep_21 部分の総和を超えて：マルチモーダルヘイトスピーチ検出における意図変化の解読
- /deep_3817 見た目を超えて：意味的アンカリングによるVision-Language Modelsのセミオティックギャップ計測

## 原文リンク

[IntentVLM: 順逆モデリングとVideo-Language Modelsによるオープン語彙意図認識](https://tldr.takara.ai/p/2604.24002)
