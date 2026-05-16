---
title: "キリスト教徒向け米国携帯ネットワーク「Radiant Mobile」：ポルノ・ジェンダー関連コンテンツをネットワーク層でブロック"
url: "https://www.technologyreview.com/2026/05/01/1136739/a-new-t-mobile-network-for-christians-aims-to-block-porn-and-gender-related-content/"
date: 2026-05-10
tags: [MVNO, ネットワーク層ブロッキング, コンテンツフィルタリング, Allot, T-Mobile, インターネット検閲, キリスト教テック]
category: "other"
related: []
memo: "[MIT Technology Review AI] A new US phone network for Christians aims to block porn and gender-related content"
processed_at: "2026-05-10T12:34:51.791028"
---

## 要約

Radiant Mobileは2026年5月5日に米国でサービス開始予定のMVNO（仮想移動体通信事業者）で、キリスト教徒をターゲットにした携帯プランを提供する。月額30ドルで、T-Mobileの回線を借り受けて運営される。技術基盤としてイスラエルのサイバーセキュリティ企業Allotを採用し、100以上のカテゴリにウェブドメインを分類してネットワーク層でのブロッキングを実施する。ポルノコンテンツはアカウントオーナーであっても解除不可能な形でブロックされ、これは米国の携帯プランとしては初のケースとされる。LGBTQやトランスジェンダー関連コンテンツは「sexuality」カテゴリに分類されデフォルト有効だが成人アカウントによる解除が可能。運営者のPaul Fisherは元ファッション業界のエージェントで、Naomi Campbellらスーパーモデルを担当していた経歴を持ち、深夜の宗教的啓示を受けてこのビジネスを発案したと語っている。投資はCompax VenturesのCEOから1,750万ドルを調達しており、NvidiaのVPであるRoger Bringmannがリード投資家兼サイレントパートナーを務める。ブロックされたコンテンツの代替として、AI生成の聖書動画や、Elf Labsから権利取得したシンデレラ・ティンカーベル等のキャラクターを使った宗教的コンテンツライブラリへのアクセスを提供予定。Northeastern大学のDavid Choffnesはネットワーク層ブロッキング自体は新しくないが、成人が解除できない米国携帯プランは前例がないと指摘する。技術的課題として、Allotのカテゴリ分類が粗く主観的で、例えばyale.eduはeducationとして許可されているがlgbtq.yale.eduはsexualityとしてブロックされるなど、ドメイン単位の判断に恣意性が伴う。Fisherはニュースサイトがジェンダー関連コンテンツを多く掲載し始めた場合、サイト全体をブロックする可能性も示唆している。ネットセキュリティの専門家からは、このモデルが権威主義的政府によるインターネット検閲と同一の技術的手法であり、表現の自由やアクセス権の観点から懸念が呈されている。

## アイデア

- ネットワーク層での不可逆ブロッキングという設計思想：アプリベースのブロッカー（Covenant Eyes等）と異なりOSレベルで回避不能にする手法は、企業ネットワークや政府検閲で使われてきた技術の民間消費者向け転用であり、プラットフォームガバナンスの新しい形態を示している
- ドメイン分類の粗粒度問題：yale.eduとlgbtq.yale.eduを別ドメインとして扱うAllotの分類システムは、サブドメイン・パス単位でのコンテンツ判断ができず、オーナーによる主観的なカテゴリ付けが必然的に生じる構造的限界を露呈している
- 宗教コミュニティを収益化チャネルとするMVNOモデル：教会への売上シェア還元という仕組みはRyan ReynoldsのMint Mobile（T-Mobileが13億ドルで買収）のブランドMVNO戦略を宗教コミュニティに応用したものであり、特定価値観を共有するコホートへのニッチMVNO展開の先例となりうる

## 前提知識

- **MVNO** → /deep_4535 キリスト教徒向け米国携帯ネットワーク「Radiant Mobile」：ポルノとLGBT関連コンテンツをネットワーク層でブロック
- **DNSブロッキング** (TODO: 読むべき)
- **ディープパケットインスペクション（DPI）** (TODO: 読むべき)
- **コンテンツフィルタリング** → /deep_4498 キリスト教徒向け米国携帯ネットワーク「Radiant Mobile」：ポルノ・ジェンダー関連コンテンツをネットワークレベルでブロック
- **ドメイン分類** → /deep_4595 キリスト教徒向け米国携帯ネットワーク「Radiant Mobile」：ネットワークレベルでポルノ・ジェンダー関連コンテンツをブロック

## 原文リンク

[キリスト教徒向け米国携帯ネットワーク「Radiant Mobile」：ポルノ・ジェンダー関連コンテンツをネットワーク層でブロック](https://www.technologyreview.com/2026/05/01/1136739/a-new-t-mobile-network-for-christians-aims-to-block-porn-and-gender-related-content/)
