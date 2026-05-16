---
title: "キリスト教徒向け新携帯ネットワーク「Radiant Mobile」：ネットワークレベルでポルノ・LGBTコンテンツをブロック"
url: "https://www.technologyreview.com/2026/05/01/1136739/a-new-t-mobile-network-for-christians-aims-to-block-porn-and-gender-related-content/"
date: 2026-05-10
tags: [MVNO, コンテンツフィルタリング, Allot, T-Mobile, ネットワークレベルブロッキング, デジタル検閲, 宗教テック]
category: "other"
related: []
memo: "[MIT Technology Review AI] A new US phone network for Christians aims to block porn and gender-related content"
processed_at: "2026-05-10T21:05:36.763017"
---

## 要約

米国で2026年5月5日にローンチ予定のMVNO（仮想移動体通信事業者）「Radiant Mobile」は、キリスト教徒をターゲットとした携帯電話プランを提供する。同社はT-Mobileの回線をCompaxDigitalを介して利用し、月額30ドルのプランを展開する。最大の特徴は、イスラエルのサイバーセキュリティ企業Allotの技術を用いたネットワークレベルのコンテンツブロッキングにある。ポルノコンテンツは成人ユーザーを含む全アカウントで無効化不可能なブロックが適用される。これは米国の携帯キャリアとして初のケースとされ、ノースイースタン大学のサイバーセキュリティ研究者David Choffnesはこの点を特記している。LGBTおよびトランスジェンダー関連コンテンツについては「sexuality」カテゴリとして分類され、デフォルトでブロックされるが、成人アカウント保有者は解除可能。Allotは100以上のカテゴリ（暴力、マルウェア、ゲーム、セクト等）にウェブドメインを分類し、カテゴリ単位でフィルタリングを行う。この方式の問題点は、分類の粒度が粗くサブドメイン単位での対応が限定的であること。例として、yale.eduはeducationカテゴリで許可されているが、lgbtq.yale.eduは別ドメインとしてsexualityカテゴリでブロックされる。創業者のPaul Fisherはファッション業界出身で元スーパーモデルエージェントであり、Ryan ReynoldsがMint Mobileで構築したブランド型携帯事業モデルに着想を得た。資金はCompax VenturesからNvidia副社長Roger Bringmannを主要投資家として1750万ドルを調達。コンテンツ空白を埋めるため、AI生成聖書動画やElf Labsから権利を取得したシンデレラ・ティンカーベル等のキャラクターを活用した宗教コンテンツライブラリを提供予定。監査AI開発への示唆としては、コンテンツポリシーの分類・執行をネットワーク層で自動化するアーキテクチャは、企業内のデータガバナンスやアクセス制御ポリシーの自動執行と類似した構造を持つ点が参考になる。

## アイデア

- ネットワーク層でのドメインカテゴリ分類による強制ポリシー執行は、企業のゼロトラストネットワーク設計や監査システムのアクセス制御モデルと構造的に類似しており、コンプライアンス自動執行の参考になる
- Allotのような100以上カテゴリのドメイン分類エンジンは、RAGシステムにおけるコンテンツ安全フィルターや検索結果の事前スクリーニングに応用可能な技術基盤
- サブドメイン単位の分類限界（yale.edu vs lgbtq.yale.edu）は、粗粒度分類システムの誤分類リスクを示しており、LLM-as-judgeによる細粒度判定の補完的価値を示唆している

## 前提知識

- **MVNO** → /deep_4535 キリスト教徒向け米国携帯ネットワーク「Radiant Mobile」：ポルノとLGBT関連コンテンツをネットワーク層でブロック
- **DNSフィルタリング** (TODO: 読むべき)
- **ネットワークレベルブロッキング** → /deep_4498 キリスト教徒向け米国携帯ネットワーク「Radiant Mobile」：ポルノ・ジェンダー関連コンテンツをネットワークレベルでブロック
- **コンテンツカテゴリ分類** (TODO: 読むべき)
- **ゼロトラストネットワーク** (TODO: 読むべき)

## 原文リンク

[キリスト教徒向け新携帯ネットワーク「Radiant Mobile」：ネットワークレベルでポルノ・LGBTコンテンツをブロック](https://www.technologyreview.com/2026/05/01/1136739/a-new-t-mobile-network-for-christians-aims-to-block-porn-and-gender-related-content/)
