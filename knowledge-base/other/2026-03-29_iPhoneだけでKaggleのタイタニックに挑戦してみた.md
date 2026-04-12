---
title: "iPhoneだけでKaggleのタイタニックに挑戦してみた"
url: "https://zenn.dev/hakoniwa_ai/articles/4fe52468a15eed"
date: 2026-03-29
tags: [Kaggle, TinyML, オフラインML, iOS, ニューラルネットワーク, ランダムフォレスト]
category: "other"
memo: "[Zenn 機械学習] iPhoneだけでKaggleのタイタニックに挑戦してみた"
processed_at: "2026-03-29T22:19:45.368707"
---

## 要約

自作iOSアプリ「Hakoniwa AI」を使い、PCやPythonを一切使わずiPhoneのみでKaggleのタイタニックコンペに参加した記録。アプリは完全オフライン動作で、ニューラルネットワークとランダムフォレストに対応し、CSVの読み込み・前処理・学習・提出ファイル生成までをスマホ上で完結させる。損失のリアルタイム可視化やTinyMLエクスポート機能（C++/Rust/Python/Dart）も備える。最終スコアは0.77751。MITライセンスのオープンソースとして公開されており、環境構築不要で機械学習を体験できる入門ツールとして位置づけられている。

## 要点

- PCレス・完全オフラインでニューラルネットワーク学習からKaggle提出まで完結するiOSアプリ「Hakoniwa AI」を自作
- TinyMLエクスポート機能でC++/Rust/Python/Dartへの変換が可能であり、エッジデプロイへの応用余地がある
- タイタニックデータセットで0.77751を達成し、スマホ単体でのML実験環境としての実用性を実証

## 関連記事

- /deep_568 天文学から占星術へ：機械学習による星座ベース性格予測の幻想を検証する
- /deep_633 天文学から占星術へ：機械学習による星座ベースの性格予測という幻想の検証
- /deep_974 変な機械学習アプリを作ってしまった【第1回：動機とredditで玉砕した話】
- /deep_1429 非エンジニアがKaggleで3999チーム中1257位になった話
- /deep_122 ML学習記録 #1 — 初めてのKaggleコンペ（Store Sales時系列予測）でやったこと

## 原文リンク

[iPhoneだけでKaggleのタイタニックに挑戦してみた](https://zenn.dev/hakoniwa_ai/articles/4fe52468a15eed)
