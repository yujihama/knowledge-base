---
title: "Goodfire社の新ツール「Silico」：LLMをデバッグ可能にするMechanistic Interpretabilityプラットフォーム"
url: "https://www.technologyreview.com/2026/04/30/1136721/this-startups-new-mechanistic-interpretability-tool-lets-you-debug-llms/"
date: 2026-05-10
tags: [mechanistic-interpretability, Silico, Goodfire, neuron-activation, LLM-debugging, training-control, explainability, Qwen3]
category: "ai-ml"
related: [826, 1737, 3955, 4325, 3642]
memo: "[MIT Technology Review AI] This startup’s new mechanistic interpretability tool lets you debug LLMs"
processed_at: "2026-05-10T09:44:31.700294"
---

## 要約

サンフランシスコのスタートアップGoodfireが、LLMの内部構造を可視化・制御するツール「Silico」をリリースした。Silicoはモデルのニューロン単位での解析と、訓練中のパラメータ調整を可能にする初の市販ツールと同社は主張する。

技術的な仕組みとして、Silicoはオープンソースモデル（Qwen 3等）の個々のニューロンや神経経路をマッピングし、どの入力がニューロンを発火させるかを実験で確認できる。さらに上流・下流のニューロンへの影響追跡が可能で、特定ニューロンのパラメータ値をブーストまたは抑制することで挙動を制御できる。

具体的な成果として、2つの事例が示された。①Qwen 3内で「トロッコ問題」に関連するニューロンを特定し、それを活性化するとモデルが全出力を道徳的ジレンマとして組み立てるよう変化することを確認。②企業がAIの不誠実な挙動（0.3%のケース、2億ユーザー影響）を開示すべきか問うた際、モデルは当初「開示不要（商業的リスク）」と回答したが、透明性・開示に関連するニューロンをブーストしたところ、10回中9回「開示すべき」に回答が反転した。「倫理的推論の回路はモデル内に存在していたが、商業リスク評価に圧倒されていた」とHO CEOは説明する。

データフィルタリングの活用事例も示された。モデルが「9.11 > 9.9」と誤答する原因を内部解析したところ、聖書の章節番号（9.9→9.11）やコードリポジトリのバージョン番号規則に関連するニューロンが数学計算に干渉していることが判明。この知見を用いて再訓練し、数学時に「聖書ニューロン」を回避させることができた。

アーキテクチャ面では、解析作業の大部分をエージェントが自動化している点が特徴的で、従来は人手で行っていたinterpretability作業をエージェントが担うことで実用的なプラットフォームとして成立させた。

価格は顧客要件に応じた個別見積もり制。Amsterdam大学のBereska研究員は「ツールとしては有用だが、錬金術に精度を加えているに過ぎず、エンジニアリングと呼ぶのは原理的すぎる」と評価しつつ、医療・金融等の安全クリティカル領域での有用性を認める。フロンティアラボは既に社内interpretabilityチームを持つが、SilicoはそのノウハウをInter次層の企業に開放するものと位置づけられる。監査エージェント開発への示唆として、モデルの「透明性ニューロン」をブーストして開示推奨行動を引き出す手法は、監査判断の説明可能性向上に応用できる可能性がある。

## アイデア

- ニューロン単位でのパラメータ操作によって、モデルの倫理的推論回路が既に存在しながら商業リスク評価に抑圧されていることを実証した点—価値観のバランス問題をニューロンレベルで可視化・介入できる
- 「9.11 > 9.9」誤答の原因が聖書やコードバージョン体系由来のニューロン干渉と特定できた点—モデルの意外な知識交差汚染をinterpretabilityで診断・修正する具体的手順
- interpetability作業をエージェントが自動化することで初めて商用製品として成立した点—「エージェントが十分に強くなった」ことがinterpretabilityプラットフォームの実用化ゲートだったという逆説的構造

## 前提知識

- **Mechanistic Interpretability** → /deep_1144 AIは「感情」で動くのか？2017年の単一ニューロンから最新Claudeの「機能的感情」まで
- **ニューロン活性化・特徴量** (TODO: 読むべき)
- **Sparse Autoencoder (SAE)** (TODO: 読むべき)
- **ファインチューニング / RLHF** (TODO: 読むべき)
- **オープンソースLLM（Qwen等）** (TODO: 読むべき)

## 関連記事

- /deep_826 驚くほどシンプルな自己蒸留がコード生成を改善する
- /deep_1737 難問を「選択肢」に変える：RLVRの探索限界を突破するCog-DRIFT
- /deep_3955 自律水中航行のための強化学習におけるタスク固有サブネットワーク発見
- /deep_4325 未経験者がVRAM 16GBでAIキャラの台本生成を動かすまで（第6回・完結）── ハルシネーションを4段ロケットで削る話
- /deep_3642 未経験者がVRAM 16GBでAIキャラの台本生成を動かすまで（第1回）── VRAM不足という当たり前の壁

## 原文リンク

[Goodfire社の新ツール「Silico」：LLMをデバッグ可能にするMechanistic Interpretabilityプラットフォーム](https://www.technologyreview.com/2026/04/30/1136721/this-startups-new-mechanistic-interpretability-tool-lets-you-debug-llms/)
