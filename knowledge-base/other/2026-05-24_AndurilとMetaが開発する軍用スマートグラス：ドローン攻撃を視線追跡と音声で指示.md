---
title: "AndurilとMetaが開発する軍用スマートグラス：ドローン攻撃を視線追跡と音声で指示"
url: "https://www.technologyreview.com/2026/05/18/1137412/inside-anduril-and-metas-quest-to-make-smart-glasses-for-warfare/"
date: 2026-05-24
tags: [AR headset, LLM on device, drone command, Anduril Lattice, Gemini, Llama, Claude, eye tracking, military AI, edge inference]
category: "other"
related: [3097, 868, 3096, 5165, 286]
memo: "[MIT Technology Review AI] Inside Anduril and Meta’s quest to make smart glasses for warfare"
processed_at: "2026-05-24T21:06:34.070374"
---

## 要約

防衛テック企業AndurilはMetaと共同で、米陸軍向けの拡張現実（AR）ヘッドセットを2つの形態でプロトタイプ開発中。1つ目は米陸軍の「Soldier Born Mission Command（SBMC）」プログラム向けで、2025年にAndurilが1億5900万ドルのプロトタイプ契約を獲得したもの。既存のヘルメットに取り付ける形式で、Meta製のディスプレイとウェーブガイドを使用する。2つ目はAnduril自費開発の「EagleEye」で、ARヘッドセットをヘルメット本体に統合した設計。陸軍が採用しなければ外国軍への販売も視野に入れる。

両システムの中核はAndurilのソフトウェア「Lattice」で、2026年3月に陸軍が200億ドルを投じてインフラ全体との統合を発表済み。グラス上のUIは、コンパス表示から周辺ドローンの位置、AIによるトラック等の目標認識まで、状況に応じた情報を視野にオーバーレイする。兵士は自然言語で指示を入力し、Google Gemini・Meta Llama・Anthropic Claudeのいずれかを使ったLLMが音声をLatticeへのコマンドに変換する。さらに、音声を使わず視線追跡と軽いタップ操作でドローンの偵察・攻撃指示を完結させる設計も検討されており、「人間を武器システムとして最適化する」というビジョンを掲げる。

デジタルナイトビジョンには生成AIと従来MLを組み合わせた新技術を採用し、これまで課題だった応答速度と画質を改善したとする。一方で課題も多く、粉塵・爆発・煙への耐久性、100ポンド超の装備に加わる重量増加、5G非依存でのローカルAI推論など、実戦環境での要件は厳しい。陸軍が量産に移行するのは早くても2028年見込み（選定があれば）。前任のMicrosoftは220億ドルの契約が実現性の問題でキャンセルされた経緯があり、ハードルは高い。RAND上級研究員Jonathan Wongは「情報過多を減らすどころか増やすリスク」を指摘しており、実際の有用性の検証には数年の野外テストが必要と述べる。

## アイデア

- 視線追跡＋音声＋LLMを組み合わせたマルチモーダルな人間–エージェントインターフェースの実装事例：エージェントが多段タスク（偵察→目標発見→攻撃推薦）を自律的にこなし、人間は承認のみを行うHuman-in-the-loopアーキテクチャとして注目に値する
- LLMをエッジデバイス上でローカル推論させる必要性：5G非依存でGemini/Llama/Claudeを端末単体で動かす設計は、ローカルLLMインフラ構築の実践的なユースケースを示している
- 「人間を武器システムとして最適化する」という発想は、監査エージェント開発における『監査人をエージェントオーケストレーターとして最適化する』設計思想と構造的に類似しており、情報提示・判断支援・承認フローの設計に参考になる

## 前提知識

- **LLM on-device推論** (TODO: 読むべき)
- **Human-in-the-loop** → /deep_24 1対1を超えて：動的な人間とAIのグループ会話のオーサリング・シミュレーション・テスト
- **マルチモーダルUI** → /deep_1362 AIが中小ネット販売業者の商品企画・製造元調達を変革——AlibbaのAccioが月間1000万ユーザー突破
- **Anduril Lattice** (TODO: 読むべき)
- **AR waveguide** (TODO: 読むべき)

## 関連記事

- /deep_3097 個人的AIを使った小説の執筆フロー
- /deep_868 エージェント型エキスパートシステムにおける構造化LLMルーティングのランタイム負荷配分：完全要因計画クロスバックエンド手法
- /deep_3096 そのAIアプリはテストされているか：LLMアプリの自動テスト実践論
- /deep_5165 RFPを貼るだけでAWSアーキテクチャ設計書が出てくるSaaSを個人開発した
- /deep_286 Anthropicダダ漏れ、Sora白旗、Meta迷走 — AI速報 2026-03-30

## 原文リンク

[AndurilとMetaが開発する軍用スマートグラス：ドローン攻撃を視線追跡と音声で指示](https://www.technologyreview.com/2026/05/18/1137412/inside-anduril-and-metas-quest-to-make-smart-glasses-for-warfare/)
