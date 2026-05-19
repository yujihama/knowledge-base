---
title: "AndurilとMetaが進める軍事用スマートグラス：視線追跡とLLMによるドローン制御"
url: "https://www.technologyreview.com/2026/05/18/1137412/inside-anduril-and-metas-quest-to-make-smart-glasses-for-warfare/"
date: 2026-05-19
tags: [Anduril, Meta, AR headset, LLM, eye tracking, Lattice, drone control, on-device inference, military AI, SBMC]
category: "other"
related: [445, 459, 467, 478, 991]
memo: "[MIT Technology Review AI] Inside Anduril and Meta’s quest to make smart glasses for warfare"
processed_at: "2026-05-19T21:23:38.775247"
---

## 要約

防衛テック企業AndurilとMetaが、米陸軍向け拡張現実（AR）ヘッドセットの共同開発を進めている。米陸軍の「Soldier Born Mission Command（SBMC）」プログラムの下、Andurilは1億5900万ドルのプロトタイプ契約を獲得。このシステムは既存のヘルメットに装着する形式で、視野にコンパス・地図・ドローン位置・AIによる標的認識などの情報を重ね合わせて表示する。兵士は自然言語で音声命令を入力し、LLM（Google Gemini、Meta Llama、Anthropic Claudeを検証中）がそれをソフトウェアコマンドに変換する。さらに視線追跡と軽微なタップ操作による非音声インターフェースも開発中。コア統合ソフトウェアはAndurilのLatticeで、米陸軍は2025年3月にLatticeをインフラ全体に統合するため200億ドルの支出を発表している。Andurilはもう一つの自己資金プロジェクト「EagleEye」も並行開発しており、こちらはヘルメット一体型の設計。軍が採用しない場合は外国軍への販売も検討している。両システムの本格量産開始は早くとも2028年以降の見込み。技術課題としては、爆発・粉塵・煙などの過酷環境での動作、バッテリー持続時間と重量の制約（兵士はすでに45kg超の装備を携行）、5G非依存のオンデバイス推論が挙げられる。デジタル暗視システムにはGenerative AIと従来型MLを組み合わせた手法を採用。Metaがディスプレイおよびウェーブガイドを担当し、サプライチェーンは中国企業不使用の連邦規定に従い再構築された。RAND上席研究員Jonathan Wongは、情報過多の問題と注意帯域幅の限界を指摘しており、実戦での有用性確認には数年の現場テストが必要とする。競合としてRivet（1億9500万ドル契約）やイスラエルElbit（1億2000万ドル契約）も同プログラムに参加している。監査エージェント開発への示唆：LLMが自然言語を構造化コマンドに変換しマルチステップタスク（偵察→標的候補提示→承認フロー）を実行するパターンは、監査エージェントにおける調査指示→証拠収集→リスク判定→承認ワークフローの設計に直接応用可能。

## アイデア

- 視線追跡＋音声＋タップの複合インターフェースで認知負荷を最小化しつつマルチステップタスクを実行する設計は、エージェントUIの新しいパラダイムとなりうる
- LLMが自然言語→ソフトウェアコマンドに変換し、承認チェーンを経てアクションを実行するパターンは、HiL（Human-in-the-Loop）エージェントの典型実装として参考になる
- 5G非依存のオンデバイス推論要件は、エッジAIとモデル圧縮（量子化・蒸留）の実用限界を示す好事例であり、ローカルLLMインフラ構築の設計指針として活用できる

## 前提知識

- **RAG** → /deep_5 Google Research at The Check Up: ヘルスケアAIの最新研究成果と実臨床への展開（2026年）
- **LLM inference** (TODO: 読むべき)
- **computer vision** → /deep_757 AIを活用したストリートビュー画像からの最低床高抽出とMLによる補完を用いた物件レベルの洪水リスク評価（テキサス州全域）
- **Human-in-the-Loop** → /deep_24 1対1を超えて：動的な人間とAIのグループ会話のオーサリング・シミュレーション・テスト
- **on-device ML** (TODO: 読むべき)

## 関連記事

- /deep_445 OpenAIの技術がイランへの軍事作戦でどのように活用される可能性があるか
- /deep_459 OpenAIの技術がイランへの軍事作戦でどのように活用されうるか
- /deep_467 OpenAIの技術がイランとの紛争でどう活用される可能性があるか
- /deep_478 OpenAIの技術がイランとの戦争でどのように使われる可能性があるか
- /deep_991 Llama 3.1 リリース — 405B・70B・8Bの多言語対応・128Kコンテキスト版

## 原文リンク

[AndurilとMetaが進める軍事用スマートグラス：視線追跡とLLMによるドローン制御](https://www.technologyreview.com/2026/05/18/1137412/inside-anduril-and-metas-quest-to-make-smart-glasses-for-warfare/)
