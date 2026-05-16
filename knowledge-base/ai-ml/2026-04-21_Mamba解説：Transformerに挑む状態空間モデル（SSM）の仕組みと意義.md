---
title: "Mamba解説：Transformerに挑む状態空間モデル（SSM）の仕組みと意義"
url: "https://thegradient.pub/mamba-explained/"
date: 2026-04-21
tags: [Mamba, SSM, 状態空間モデル, Selective SSM, 線形計算量, 長文脈, Transformer代替, Zero-Order Hold, Parallel Associative Scan, S4]
category: "ai-ml"
related: [1837, 222, 833, 255, 1975]
memo: "[The Gradient] Mamba Explained"
processed_at: "2026-04-21T12:30:07.621655"
---

## 要約

MambaはAlbert GuとTri Daoが開発した状態空間モデル（SSM）ベースのシーケンスモデルで、TransformerのAttentionが抱える二次計算量ボトルネックを解消することを目的としている。Transformerでは全トークン間のペアワイズ通信によりトレーニング時O(n²)、推論時O(n)の計算量が生じ、KVキャッシュのO(n)メモリも問題となる。Mambaはこれを線形計算量（O(n)）で処理し、最大100万トークンの長いコンテキストに対応しながら、Transformerと同等以上の性能を実現する。推論速度はTransformerの最大5倍とされる。

技術的核心は連続時間の微分方程式 h'(t)=Ah(t)+Bx(t)、y(t)=Ch(t)+Dx(t) で表されるSSMで、離散化（Zero-Order Hold法）により差分方程式に変換して実装される。従来のSSM（S4等）はA・B・C行列が入力に依存しない（Linear Time-Invariant）であったため、「選択的なフィルタリング」ができず、無関係な情報を切り捨てられない問題があった。

Mambaの革新点は「選択的状態空間モデル（Selective SSM / S6）」の導入で、B・C・∆パラメータを入力xの関数とすることで、コンテキストに応じて何を記憶し何を忘れるかを動的に制御できるようにした点にある。例えば「ロブスターの話をしている文章でオスかメスかを答えよ」という課題では、性別に関する情報を選択的に保持する必要があり、LTIでは対応不可能だがMambaは可能となる。

ただし選択性の導入により並列スキャンが単純には使えなくなるため、Mambaはハードウェアを意識した「Parallel Associative Scan」と「Kernel Fusion」でGPU上での高速化を実現している（FlashAttentionと同様のアプローチ）。モデルアーキテクチャとしては、MLP内にSSMを組み込んだMambaブロックをスタックする構造で、Transformerブロックに相当する。

Mamba-3BはThe Pileデータセットにおいて同サイズのTransformerを上回り、2倍のサイズのTransformerと同等の性能を示した。一方、弱点として「In-Context Learning（ICL）」や「2〜5ショット学習」ではTransformerに劣るとされ、コンプレッション型モデルゆえに全情報を固定サイズの状態に詰め込む必要がある点が制約となる。解釈可能性の観点では、Transformerの注意マップのような直感的な可視化ツールが存在せず研究が難しいとされる。監査エージェント開発への示唆としては、長大な監査ログや規程文書を低コストで処理するバックボーンとしての活用可能性があり、特に数百万トークン規模の文書全体を一度に処理するユースケースに適している。

## アイデア

- 入力依存パラメータ（B・C・∆をxの関数にする）という単純な変更が『選択性』を生み出し、LTIとSelectiveの差がそのまま『記憶と忘却の制御能力』の有無につながる点が概念的に鮮明
- 状態hを『過去の圧縮』と定義することで、Transformerのアテンションが行う『全過去への直接アクセス』vs Mambaの『圧縮された要約への参照』という根本的なトレードオフが見えてくる——ICLでの劣位はこの圧縮コストの直接的な現れ
- ハードウェア制約（GPUのSRAM/HBM階層）に合わせてアルゴリズムを再設計するアプローチ（Kernel Fusion + Recomputation）はFlashAttentionと同系統の発想で、アーキテクチャ革新とシステム最適化が不可分であることを示す好例

## 前提知識

- **Transformer / Attention機構** (TODO: 読むべき)
- **KVキャッシュ** → /deep_106 TurboQuant: 極限圧縮によるAI効率の再定義
- **RNN / 隠れ状態** (TODO: 読むべき)
- **FlashAttention** → /deep_221 Differential Transformer V2：カスタムカーネル不要・推論高速化を実現した差分注意機構の改良版
- **状態空間モデル（S4）** (TODO: 読むべき)

## 関連記事

- /deep_1837 UNDO Flip-Flop：状態空間モデルにおける可逆的意味状態管理の制御プローブ
- /deep_222 Falcon-H1-Arabic: ハイブリッドMamba-Transformerアーキテクチャによるアラビア語AI最前線
- /deep_833 Falcon 3 ファミリー：10B以下の高性能オープンモデル群の紹介
- /deep_255 Apriel-H1: 効率的な推論モデル蒸留の意外なカギ
- /deep_1975 WUTDet: 密集した小物体を含む10万スケールの船舶検出データセットとベンチマーク

## 原文リンク

[Mamba解説：Transformerに挑む状態空間モデル（SSM）の仕組みと意義](https://thegradient.pub/mamba-explained/)
