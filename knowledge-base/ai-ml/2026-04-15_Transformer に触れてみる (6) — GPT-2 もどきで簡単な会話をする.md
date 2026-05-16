---
title: "Transformer に触れてみる (6) — GPT-2 もどきで簡単な会話をする"
url: "https://zenn.dev/derwind/articles/dwd-transformer06"
date: 2026-04-15
tags: [GPT-2, MiniGPT2, Transformer, Pre-LN, GloVe, 言語モデル, 会話生成, PyTorch, 自己回帰モデル, TinyStories]
category: "ai-ml"
related: [113, 216, 585, 518, 105]
memo: "[Zenn 機械学習] Transformer に触れてみる (6) — GPT-2 もどきで簡単な会話をする"
processed_at: "2026-04-15T12:43:26.920695"
---

## 要約

本記事は、著者が独自実装した MiniGPT2 を拡張し、限定語彙（150語＋特殊記号で計188語）のみを使った英語会話データセットで学習させ、簡単な質疑応答・会話生成を実現した実験記録である。

データセットはGPT-4.1で大量生成した会話例を手作業で調整して構築。会話ペア289個・質疑応答ペア220個からなり、各単語が最低10回登場するよう調整されている。単語埋め込みにはGloVe（2024 Wikipedia+Gigaword 5、50次元）を使用し、意味的近傍がベクトル空間でも近くなるよう設計した。特殊トークン（<PAD>, <BOS>, <EOS>, <UNK>）はGloVeベクトルから最大距離になるよう別途選定している。

モデルアーキテクチャは GPT-1（Post-LN）から GPT-2（Pre-LN）方式に変更した。Post-LNは「Attention → 残差加算 → LayerNorm」の順だが、深いネットワークで勾配が不安定になる問題があった。GPT-2のPre-LNは「LayerNorm → Attention → 残差加算」とすることで学習安定性を改善している。BlockクラスはLayerNorm×2・単頭アテンション・FFN（ReLU活性化、ffn_expansion倍の中間層）で構成される。

SentencePairDatasetでは入力文と応答文を単純に結合してトークン化し、[BOS]+トークン列+[EOS]を構築。入力xと正解yを1トークンずれた形にして自己回帰的に学習する標準的な言語モデル学習手法を採用。最大系列長29トークンでパディング処理を行っている。

生成結果は「how old are you, judy? → i am eight years old.」のように一部は正確に応答できるが、「how old is judy? → mary says this book is for john.」のように意味的に無関係な応答も多く、語彙・データ規模の限界が明確に示されている。関連研究としてGuppyLM（Colab5分学習で会話可能）やTinyStories（arXiv:2305.07759）が紹介されており、本プロジェクトはその後の目的（未公開）に向けた基盤実験という位置付けである。実装コーディングはほぼGemini 2.5 Proに委任している点も特徴的。

## アイデア

- 語彙188語・データ500件程度の極小スケールで会話モデルを構築し、どこまで意味のある応答が可能かを実験的に検証している点—スケール限界の可視化として教育的価値が高い
- Post-LN（GPT-1）からPre-LN（GPT-2）へのアーキテクチャ変更が、小規模モデルでも教師データ記憶精度に影響することを実装レベルで確認している点
- 特殊トークンの埋め込みベクトルをGloVe空間から最大距離になるよう選定するという実用的な工夫—通常はランダム初期化されることが多いが、埋め込み空間の干渉を意識した設計

## 前提知識

- **Transformer** → /deep_99 LLM Architecture Gallery徹底解説：30+モデルの内部構造を4軸で横断比較する
- **GPT-2 / Pre-LN** (TODO: 読むべき)
- **自己回帰言語モデル** (TODO: 読むべき)
- **GloVe埋め込み** (TODO: 読むべき)
- **PyTorch Dataset/DataLoader** (TODO: 読むべき)

## 関連記事

- /deep_113 金融時系列予測でLightGBM / LSTM / Transformerを比較してみた
- /deep_216 金融市場へのLLM応用：価格予測・合成データ・マルチモーダル学習の可能性と限界
- /deep_585 nanoVLMでゼロから実装するKVキャッシュ
- /deep_518 TransformerベースニューラルネットワークのGPU高速化リアルタイム推論最適化
- /deep_105 TransformerでAttention Residualsを観察する

## 原文リンク

[Transformer に触れてみる (6) — GPT-2 もどきで簡単な会話をする](https://zenn.dev/derwind/articles/dwd-transformer06)
