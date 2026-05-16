---
title: "Apple Intelligence Foundation Models、思ったより使える／使えない（個人開発での本格活用）"
url: "https://zenn.dev/sawasige/articles/seekthea-apple-intelligence"
date: 2026-05-10
tags: [Foundation Models, Apple Intelligence, オンデバイスLLM, Swift, @Generable, NLEmbedding, ハイブリッドLLM設計, 構造化出力, Refusal, iOS 26]
category: "infra"
related: [4189, 868, 797, 2285, 3630]
memo: "[Zenn LLM] Apple Intelligence の Foundation Models、思ったより使える / 使えない（個人開発で本気使い）"
processed_at: "2026-05-10T12:50:04.104763"
---

## 要約

個人開発のRSSリーダーアプリ「Seekthea」でAppleのFoundation Models framework（オンデバイスLLM）をフル活用した実践レポート。Foundation ModelsはiOS 26 / macOS 26以降に同梱される約3BパラメータのSwift APIで、iPhone 15 Pro以降・M1以降のデバイスで動作し、追加ダウンロード不要・完全無料で利用できる。

Seektheaでは記事の要約・カテゴリ分類・キーワード抽出・興味学習用翻訳をすべてオンデバイスで処理。クラウドLLMと比較した主な優位点は3点：①コストゼロ（大量呼び出しでも無課金）、②プライバシー保護（ユーザーの読書データが外部に出ない）、③低レイテンシ（カテゴリ分類で実測0.2〜0.3秒）。

一方で限界も明確。3Bモデルゆえ複雑な推論・長文生成はGPT/Claude/Geminiに劣る。日本語の自然さは「読める」レベル止まりで、ハルシネーションも発生する。また安全フィルタが超保守的で、軍事・政治・検閲関連ニュースは批判的立場の記事でも`GenerationError.refusal`で拒否される。

構造化出力は`@Generable`アノテーションを付与したSwift structを渡すだけで型安全なレスポンスが得られる点が強み。JSONパースエラーに悩まされるクラウドLLMのStructured Outputsより実装が簡潔。

実装上のハマりどころとして2段階のハルシネーション問題が紹介されている。①カテゴリ名の表記ゆれ（「テクノロジー」→「テック」「Technology」等）はアルファベット1文字で回答させることで解決。②プロンプト内のカテゴリ説明文をAIが記事本文のキーワードと誤認する問題は、プロンプトをセクション分離し「カテゴリ参考の語ではなく記事本文から」と明示することで改善。

意味類似度計算にはApple Intelligenceではなく`Natural Language framework`の`NLEmbedding`（iOS 13から提供の事前学習済み埋め込み）を採用。マイクロ秒オーダーで処理でき、LLMへの毎回問い合わせを避けている。「LLMはLLMが得意な仕事、ベクトル類似度は軽量API」という棲み分けが実践的。

監査エージェント開発への示唆：大量のドキュメントを処理する監査システムでも、単純な分類・抽出タスクはオンデバイスLLMで完結させ、複雑な推論のみクラウドLLMに委譲するハイブリッド設計が有効。ただし現時点ではiOS/macOSアプリに限定され、サーバーサイドでの活用はできない。

## アイデア

- @GenerableアノテーションによるSwiftネイティブの型安全構造化出力は、JSONパース不要でLLMレスポンスをstructに直接マッピングできる設計であり、クラウドLLMのStructured Outputsより実装コストが低い
- LLMとNLEmbeddingの役割分担（抽出はLLM・類似度計算はベクトルAPI）により、処理速度をマイクロ秒オーダーに保ちながら意味的検索を実現するアーキテクチャパターンは他システムにも応用可能
- カテゴリ分類の回答を自由文ではなくアルファベット1文字の閉じた選択肢に限定する手法は、3Bクラスの小型LLMでの出力安定化に有効な実践的プロンプト設計

## 前提知識

- **Foundation Models** → /deep_791 ウェルビーイングに根ざしたAIのポジティブビジョンが必要である
- **オンデバイスLLM** → /deep_995 SmolLM - 高速かつ高性能な小規模言語モデルファミリー
- **Structured Outputs** → /deep_392 OllamaでローカルLLM：導入から最新エコシステムまでを解説（2026年版）
- **NLEmbedding** (TODO: 読むべき)
- **ハルシネーション対策** → /deep_10 LLMクローラーを制御する『AIO』基本マニュアル：llms.txtとllms-full.txtの実装

## 関連記事

- /deep_4189 機能を増やさずに品質を上げた話 — デジタルAIペット（仮称）Phase 2.5 Polish
- /deep_868 エージェント型エキスパートシステムにおける構造化LLMルーティングのランタイム負荷配分：完全要因計画クロスバックエンド手法
- /deep_797 エージェント型エキスパートシステムにおける構造化LLMルーティングのランタイム負荷配分：フルファクトリアル・クロスバックエンド手法
- /deep_2285 ウェルビーイングに根ざした、AIのポジティブなビジョンが必要だ
- /deep_3630 ウェルビーイングに根ざしたAIの肯定的ビジョンが必要だ

## 原文リンク

[Apple Intelligence Foundation Models、思ったより使える／使えない（個人開発での本格活用）](https://zenn.dev/sawasige/articles/seekthea-apple-intelligence)
