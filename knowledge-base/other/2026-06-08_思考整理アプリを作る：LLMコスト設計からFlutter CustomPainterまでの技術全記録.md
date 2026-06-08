---
title: "思考整理アプリを作る：LLMコスト設計からFlutter CustomPainterまでの技術全記録"
url: "https://zenn.dev/uray/articles/0e854dacd21744"
date: 2026-06-08
tags: [Claude Haiku 4.5, Prompt Caching, tool_use, Flutter, CustomPainter, Pydantic, LLMコスト設計, 構造化出力, LOD, 個人開発]
category: "other"
related: [797, 4189, 4036, 4475, 7375]
memo: "[Zenn LLM] 思考整理アプリを作る：LLMコスト設計からFlutter CustomPainterまでの技術全記録"
processed_at: "2026-06-08T09:08:47.791867"
---

## 要約

「やることが多すぎて寝つけない」という課題を解決するモバイルアプリ「BubbleClear」の個人開発記録。頭の中にあることを3〜5分で吐き出すと、Claude Haiku 4.5が各テーマの重みと感情スコアを分析し、バブルマップとして可視化する。ターゲットは複数プロジェクトを掛け持つナレッジワーカー（30〜45歳）。

【LLMコスト設計】機能実装前に原価モデルを確定する方針を採用。1セッションあたり入力1,500トークン・出力800トークンを想定し、Haiku 4.5の単価（$1.00/$5.00 per Mtoken）で計算すると約¥0.82/セッション。ヘビーユーザーが月30回使用しても月¥24.6、Standardプラン¥380の6.5%に収まる。Claude Sonnet 4系では1セッション¥4〜12となり原価率30〜90%に跳ね上がるため却下。GPT-4o miniも検討したが、データ非保持ポリシーの明示的保証とtool_useのスキーマ遵守率でHaikuを選定。

【Prompt Caching】約1,200トークンのシステムプロンプトをephemeral（TTL 5分）キャッシュ対象に設定。キャッシュヒット時は入力1,500トークンのうち1,200トークン分の課金が省略され、1セッション¥0.82→¥0.66〜0.73（12〜18%削減）。ただしAPI キー単位の管理のため、複数ユーザーのリクエストが時間的に集中する規模にならないと恩恵は限定的。β期間はヒット率を計測してから1時間TTLへの移行を判断する方針。

【構造化出力設計】JSON modeではなくtool_use＋tool_choice強制でスキーマ準拠率を向上。label/weight/domain/time_horizon/urgency/emotion/summaryの7フィールドを定義し、tool_use通過後もPydanticで再バリデーション。3段階フォールバックを実装：1回目失敗→同スキーマで再試行→2回目失敗→label＋weightのみの簡易スキーマでフォールバック。バブル描画に最低限必要な2フィールドが取得できれば体験を維持できる設計。

【Flutter CustomPainter】30〜50個のバブルを60fps描画するためにCustomPainter（Skia/Impellerエンジン直接操作）を採用。React NativeのJavaScriptブリッジ経由描画では60fps維持が困難な場面があるため。LOD（Level of Detail）を4段階実装：実効半径4px未満→描画スキップ、14px未満→単色フラット、24px未満→テキスト非表示、24px以上→フルレンダリング。Paintオブジェクトの再生成を避けるため、半径差0.5px以下でのキャッシュ更新スキップも実装。破裂演出はsin関数の小数部を利用した決定論的疑似乱数（sin-hash）で「毎回ランダムに見えるが同じバブルは同じ弾け方をする」挙動を実現。

【アーキテクチャ】バックエンドはFastAPI（Python）、Cloudflare Workers移行に備えてLLM呼び出し層をLLM_PROVIDER環境変数で切り替え可能に抽象化。認証はSupabase Auth（Magic Link）でPostgreSQL統合・RLS一体化。各技術選定をADR（Architecture Decision Record）としてdocs/adr/に記録し、棄却理由と変更理由を残す運用を採用。

監査エージェント開発への示唆：LLMの出力を信頼しない設計思想（tool_use強制＋Pydantic再バリデーション＋3段階フォールバック）は、監査証跡の確実な取得が求められるエージェントシステムに直接応用可能。コスト試算を先行させてからモデル選定する手順も、監査システムの商用展開時に参考になる。

## アイデア

- 機能実装前にLLM原価モデルを確定し、モデル選定・プラン設計・損益分岐点（有料ユーザー3〜4名）まで一貫して試算してから開発を開始するアプローチ
- sin関数の小数部を利用した決定論的疑似乱数（sin-hash）により、同じバブルは常に同じ破裂パターンを示しつつ、バブルごとに異なるエフェクトを実現する手法
- tool_use強制＋Pydantic再バリデーション＋3段階フォールバック（7フィールド→7フィールド再試行→2フィールド簡易）という多層防御でLLMの確率的挙動に対応する設計パターン

## 前提知識

- **Claude Prompt Caching** (TODO: 読むべき)
- **Function Calling / tool_use** (TODO: 読むべき)
- **Pydantic** → /deep_52 SyGra Studio 紹介：合成データ生成のビジュアル・インタラクティブ環境
- **Flutter CustomPainter** (TODO: 読むべき)
- **LLMトークン課金モデル** (TODO: 読むべき)

## 関連記事

- /deep_797 エージェント型エキスパートシステムにおける構造化LLMルーティングのランタイム負荷配分：フルファクトリアル・クロスバックエンド手法
- /deep_4189 機能を増やさずに品質を上げた話 — デジタルAIペット（仮称）Phase 2.5 Polish
- /deep_4036 未経験者がVRAM 16GBでAIキャラの台本生成を動かすまで(第4回) ── 「きみ」を消したら、品質も消えた話
- /deep_4475 採点基準v2改訂で「直感力9点」が認定された——LLM個人アセスメントプロンプト設計の実践記録
- /deep_7375 学生が個人開発でLightGBM競馬予想アプリを運用してわかったこと

## 原文リンク

[思考整理アプリを作る：LLMコスト設計からFlutter CustomPainterまでの技術全記録](https://zenn.dev/uray/articles/0e854dacd21744)
