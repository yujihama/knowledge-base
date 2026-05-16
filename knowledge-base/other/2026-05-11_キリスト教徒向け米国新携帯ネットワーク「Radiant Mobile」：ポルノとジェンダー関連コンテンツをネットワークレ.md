---
title: "キリスト教徒向け米国新携帯ネットワーク「Radiant Mobile」：ポルノとジェンダー関連コンテンツをネットワークレベルでブロック"
url: "https://www.technologyreview.com/2026/05/01/1136739/a-new-t-mobile-network-for-christians-aims-to-block-porn-and-gender-related-content/"
date: 2026-05-11
tags: [MVNO, コンテンツフィルタリング, ネットワークレベルブロック, Allot, T-Mobile, デジタル検閲, プラットフォームガバナンス]
category: "other"
related: []
memo: "[MIT Technology Review AI] A new US phone network for Christians aims to block porn and gender-related content"
processed_at: "2026-05-11T21:44:22.113181"
---

## 要約

Radiant Mobileは2026年5月5日ローンチ予定のMVNO（仮想移動体通信事業者）で、T-Mobileの帯域を借りてキリスト教徒向けに特化した携帯プランを月額30ドルで提供する。技術基盤はイスラエルのサイバーセキュリティ企業Allotが提供するネットワークレベルのコンテンツフィルタリングで、100以上のカテゴリにウェブドメインを分類し、対象カテゴリのサイトへのアクセスを遮断する。ポルノは成人ユーザーでも解除不可のデフォルトブロック対象となっており、米国の携帯キャリアとして初めてこうした解除不能なネットワークレベルブロックを実装した事例とされる。ジェンダー・トランスジェンダー関連コンテンツはAllotの「sexuality」カテゴリに該当するとして、デフォルトでブロックされるが成人アカウントオーナーは設定変更が可能。ブロック範囲の決定はRadiant創業者のPaul Fisherが主観的に行う部分が大きく、例えばYale大学のlgbtq.yale.eduをsexualityカテゴリに分類してブロックする一方、yale.edu本体は現時点では許可しているが、メインページにLGBTQコンテンツが増えれば全体をブロックすると明言している。Northeasternのコンピュータサイエンス教授David Choffnesは、ネットワークレベルのブロック自体は珍しくないが、米国の携帯プランで成人でも解除できないブロックを実装するのは前例がないと指摘する。投資面ではCompax Venturesから1750万ドルの資金調達を受けており、NvidiaのVP Roger Bringmannが主要投資家。コンテンツ空白を埋めるため、AI生成の聖書動画や、Elf Labsから権利取得したシンデレラ・ティンカーベル等のキャラクターを用いた宗教的コンテンツライブラリを提供予定。監査AI・内部統制の観点からは、コンテンツポリシー執行をネットワークインフラレイヤーに組み込む手法は、企業内のDLP（データ損失防止）やアクセス制御の設計思想と類似しており、誰が何を「許可」か「禁止」かを定義する主体の透明性・説明責任が問われる点で示唆がある。

## アイデア

- ネットワークレベルのコンテンツブロックを商業携帯プランに組み込む手法は、企業内ゼロトラストネットワークやDNSフィルタリング（例: Cisco Umbrella）の民間コンシューマー向け応用として技術的に興味深い
- ドメイン単位のカテゴリ分類では同一ドメイン内のサブドメインや動的コンテンツへの対応が限界であり、yale.eduとlgbtq.yale.eduを別扱いする事例はDNS/URLフィルタリングの粒度問題を具体的に示している
- コンテンツポリシーの定義権限を民間事業者に委ねる構造は、監査分野における内部統制設計（誰がルールを決め、誰がそれを執行し、誰が監査するか）の独立性原則と直接対比できる

## 前提知識

- **MVNO（仮想移動体通信事業者）** (TODO: 読むべき)
- **DNSフィルタリング** (TODO: 読むべき)
- **ネットワークレベルDPI（Deep Packet Inspection）** (TODO: 読むべき)
- **コンテンツカテゴリ分類** (TODO: 読むべき)
- **プラットフォームガバナンス** → /deep_4832 米国初：キリスト教徒向け携帯ネットワーク「Radiant Mobile」がネットワークレベルでポルノ・LGBT関連コンテンツをブロック

## 原文リンク

[キリスト教徒向け米国新携帯ネットワーク「Radiant Mobile」：ポルノとジェンダー関連コンテンツをネットワークレベルでブロック](https://www.technologyreview.com/2026/05/01/1136739/a-new-t-mobile-network-for-christians-aims-to-block-porn-and-gender-related-content/)
