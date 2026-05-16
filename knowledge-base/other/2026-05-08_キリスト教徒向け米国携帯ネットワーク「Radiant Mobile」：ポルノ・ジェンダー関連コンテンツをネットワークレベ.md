---
title: "キリスト教徒向け米国携帯ネットワーク「Radiant Mobile」：ポルノ・ジェンダー関連コンテンツをネットワークレベルでブロック"
url: "https://www.technologyreview.com/2026/05/01/1136739/a-new-t-mobile-network-for-christians-aims-to-block-porn-and-gender-related-content/"
date: 2026-05-08
tags: [MVNO, ネットワークレベルブロッキング, コンテンツフィルタリング, Allot, T-Mobile, デジタル検閲, 宗教テック]
category: "other"
related: []
memo: "[MIT Technology Review AI] A new US phone network for Christians aims to block porn and gender-related content"
processed_at: "2026-05-08T21:23:10.863817"
---

## 要約

Radiant Mobileは2026年5月5日にローンチ予定の米国初のMVNO（仮想移動体通信事業者）で、キリスト教徒を対象にT-Mobileの回線を利用した月額30ドルの携帯プランを提供する。技術的な基盤はイスラエルのサイバーセキュリティ企業Allotが提供するネットワークレベルのコンテンツフィルタリングシステムで、100以上のカテゴリにウェブドメインを分類し、該当カテゴリへのアクセスをパケットレベルでブロックする。ポルノコンテンツはデフォルトかつ変更不可でブロックされ、成人ユーザーであっても解除できない。これは米国の携帯プランとして初めてネットワークレベルの恒久的ブロックを実装した事例とされる（Northeastern大学のDavid Choffnes教授が指摘）。LGBTQおよびトランスジェンダー関連コンテンツはAllotの「sexuality」カテゴリとして分類され、デフォルトでブロックされるが成人ユーザーは解除可能。ただし、どのサイトをどのカテゴリに割り当てるかはRadiant MobileのCEO Paul Fisherが主観的に判断する仕組みで、例えばyale.eduはeducationカテゴリだがlgbtq.yale.eduはsexualityカテゴリとして個別ブロック対象となっている。Fisherはファッション業界出身で技術的バックグラウンドを持たない。投資はT-Mobileとの技術仲介役であるCompax Venturesから1,750万ドルを調達しており、NvidiaのVP Roger Bringmannがリード投資家。コンテンツ代替として、Elf Labsから権利取得したシンデレラ等の児童向けキャラクターを用いたAI生成聖書動画ライブラリを提供予定。専門家からはDNS・IPレベルのブロック回避（VPN使用等）が容易であること、またカテゴリ分類の恣意性による誤ブロックリスクが指摘されている。監査AI観点では、コンテンツポリシー実施の透明性・説明責任の欠如、および外部委託フィルタリングシステムへの依存によるガバナンスリスクが示唆される。

## アイデア

- ネットワークレベルのコンテンツブロックはVPNで容易に回避可能であり、技術的実効性よりも『ブランドとしての価値観表明』としての側面が強い可能性
- ドメイン単位のカテゴリ分類という粗粒度なアプローチが誤ブロック（yale.edu全体 vs lgbtq.yale.edu）を生む構造的問題は、AI分類システムの粒度設計における教訓
- コンテンツポリシーの恣意的運用権限を単一の民間事業者が持つ構造は、監査・GRC領域における『誰がルールの番人を監視するか』問題の具体例

## 前提知識

- **MVNO** → /deep_4447 キリスト教徒向け米国携帯ネットワーク「Radiant Mobile」：ポルノ・ジェンダー関連コンテンツをネットワークレベルで強制ブロック
- **DNSブロッキング** (TODO: 読むべき)
- **ディープパケットインスペクション** (TODO: 読むべき)
- **コンテンツフィルタリング** → /deep_4447 キリスト教徒向け米国携帯ネットワーク「Radiant Mobile」：ポルノ・ジェンダー関連コンテンツをネットワークレベルで強制ブロック
- **ネットワーク中立性** (TODO: 読むべき)

## 原文リンク

[キリスト教徒向け米国携帯ネットワーク「Radiant Mobile」：ポルノ・ジェンダー関連コンテンツをネットワークレベルでブロック](https://www.technologyreview.com/2026/05/01/1136739/a-new-t-mobile-network-for-christians-aims-to-block-porn-and-gender-related-content/)
