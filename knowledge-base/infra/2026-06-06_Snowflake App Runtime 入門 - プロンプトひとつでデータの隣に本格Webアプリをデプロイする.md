---
title: "Snowflake App Runtime 入門 - プロンプトひとつでデータの隣に本格Webアプリをデプロイする"
url: "https://zenn.dev/snowflakejp/articles/9e5b8fa393ccd8"
date: 2026-06-06
tags: [Snowflake, App Runtime, Next.js, SPCS, CoCo, Cortex Code, snowflake-apps, Owner's Rights, Caller's Rights, snow CLI]
category: "infra"
related: [6295, 1263, 3648, 6562, 1793]
memo: "[Zenn LLM] Snowflake App Runtime 入門 - プロンプトひとつでデータの隣に本格Webアプリをデプロイする！"
processed_at: "2026-06-06T09:07:18.609778"
---

## 要約

Snowflake Summit 2026で発表された「Snowflake App Runtime」は、Next.jsなどのフルスタックWebアプリをSnowflakeのデータ基盤の内側に直接デプロイできるPlatform-as-a-Serviceである。Snowpark Container Services（SPCS）上のAPPLICATION SERVICEという専用オブジェクトとして稼働し、従来のCREATE SERVICE（ユーザー定義spec）とは異なり、バージョン管理されたパッケージからデプロイされる点が特徴。Public Preview（Trialアカウントを除く全アカウントで利用可能）の現時点ではNode.js/Next.jsをサポートし、PythonサポートはRoadmap上にある。

最大の特徴は「データをコピーしない」アーキテクチャ。Snowflake内のデータに直接アクセスするため、ガバナンスが崩れない。認証はSnowflake SSOが自動適用され、コードを書く必要がない。公開URLは`https://<id>-<org>-<account>-<region>.snowflakecomputing.app/`形式で自動発行される。

AIコーディングエージェント「CoCo（Cortex Code）」に同梱の`snowflake-apps`スキルを使うと、プロンプト一つで雛形生成からデプロイまで一気通貫で実行される。スキルはNext.js 16 + React 19 + snowflake-sdkのテンプレート、Snowflake接続ヘルパー`lib/snowflake.ts`、デプロイ設定`snowflake.yml`/`app.yml`を自動生成する。データアクセスは`querySnowflake()`関数一つで行え、権限モードとして「Owner's Rights（アプリ所有者の権限で全ユーザーが同一データを参照）」と「Caller's Rights（ログインユーザー本人の権限で行レベルセキュリティが機能）」を`callersRights: true`オプション一行で切り替えられる。

デプロイは`snow app deploy`コマンドで「アップロード→リモートビルド→デプロイ」を一括実行。`snowflake.yml`の`type: snowflake-app`フィールドでNative App Frameworkと自動区別される。著者は架空ECサービス「Glacier Style」の売上ダッシュボードを実際に構築し、KPIカード・フィルタ・グラフを含むNext.jsアプリを本番デプロイまで検証した。

Streamlit in Snowflake（Python・フロントエンド不要・データ探索向け）、Native App Framework（アカウント間配布・Marketplace向け）との棲み分けも明示されており、「凝ったUI・業務フロー」が必要な社内Webアプリには App Runtimeが最適とされる。監査エージェント開発への示唆としては、Snowflake内の監査ログや統制データに直接アクセスしつつ、データ移動なしでレビュー用Webアプリを構築できる点が挙げられる。権限モードの切り替えにより、監査役と被監査部門で見えるデータを行レベルで分離する実装も容易である。

## アイデア

- データをコピーせずアプリをデータの隣にデプロイする設計により、ガバナンスとリアルタイム性を両立できる点は、監査エージェントのデータアクセス層設計に直接応用できる
- Owner's Rights / Caller's Rights を1行のオプションで切り替えられる権限モデルは、マルチテナント型監査ツールで被監査部門ごとにデータ可視範囲を制御する際のパターンとして参考になる
- AIエージェント（CoCo）にスキル（snowflake-apps）を同梱し、プロンプトからインフラデプロイまでを一気通貫で自動化する設計は、エージェントにドメイン固有のワークフローをスキルとして持たせるアーキテクチャパターンの実例である

## 前提知識

- **Snowpark Container Services** (TODO: 読むべき)
- **Next.js / React** (TODO: 読むべき)
- **SQL権限モデル（Owner's/Caller's Rights）** (TODO: 読むべき)
- **snow CLI** (TODO: 読むべき)
- **Native App Framework** (TODO: 読むべき)

## 関連記事

- /deep_6295 自己収縮曲線を用いた制約付きオンライン凸最適化の改良保証
- /deep_1263 物体検出リーダーボード：評価指標とその落とし穴の解説
- /deep_3648 機械学習論文を毎日自動収集してAIで日本語解説するサイトを作った（MLinfo）
- /deep_6562 llms.txtのURLを1行渡したら、AIが仕様をたどりながらウェブアプリを作ってくれた話
- /deep_1793 YOLOv8とRT-DETRの比較：COCO val 2017における速度・精度のトレードオフ

## 原文リンク

[Snowflake App Runtime 入門 - プロンプトひとつでデータの隣に本格Webアプリをデプロイする](https://zenn.dev/snowflakejp/articles/9e5b8fa393ccd8)
