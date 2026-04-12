---
title: "モデルからエージェントへ：Responses APIへのコンピュータ環境の統合"
url: "https://openai.com/index/equip-responses-api-computer-environment"
date: 2026-03-31
tags: [Responses API, computer-use, OpenAI, browser-automation, RPA, tool-use, sandbox, GUI-agent]
category: "agent-arch"
memo: "[OpenAI Blog] From model to agent: Equipping the Responses API with a computer environment"
related: [1608, 389, 440, 387, 77]
processed_at: "2026-03-31T09:08:19.801454"
---

## 要約

OpenAIはResponses APIに「computer-use-preview」ツールを追加し、LLMがブラウザやデスクトップ環境を直接操作できるエージェント機能を提供開始した。このツールはモデルにスクリーンショットの取得・クリック・キー入力・スクロールといたOSレベルの操作を可能にし、従来のfunction callingによるAPI連携では対応できなかった「UIしか持たないシステム」へのアクセスを実現する。技術的には、モデルがスクリーンショットを受け取り、次に行うべき操作（座標指定クリック、テキスト入力等）をJSON形式で返し、開発者側のサンドボックス環境でその操作を実行してから次のスクリーンショットをモデルに返すというループ構造をとる。Responses APIのstreamingと組み合わせることで、長時間タスクの途中状態をリアルタイムに取得できる。対象モデルはcomputer-use-previewと呼ばれる専用スナップショットで、GPT-4o系ではなくClaude-computer-useに近いアーキテクチャを持つとされる。セキュリティ上の注意点として、モデルが操作するサンドボックスは開発者側で用意する必要があり、OpenAIはサンドボックス環境自体は提供しない。BrowserBaseやE2Bなどのサードパーティサンドボックスとの統合例が公式ドキュメントで紹介されている。利用料金はinput/output tokenに加え、computer callの回数に応じた追加コストが発生する。従来のWebブラウジングツール（web_search）と異なり、任意のWebサイトやローカルアプリを人間と同様に操作できる点が最大の差別化要素であり、RPA（Robotic Process Automation）の代替としての活用が期待される。ただし現時点ではpreviewステータスであり、レイテンシや精度面での本番利用には課題が残る。

## アイデア

- LLMがスクリーンショット→操作指示→実行→スクリーンショットのループでGUI操作を行う構造は、LangGraphのノード間状態遷移と親和性が高く、computer_use_nodeを1ノードとして組み込めるアーキテクチャが成立する
- APIを持たない既存の業務システム（ERP、監査ツール等）へのアクセス手段として、function callingではなくcomputer-useを使うことで統合コストを大幅に削減できる可能性がある
- Anthropicのcomputer-useとOpenAIのcomputer-use-previewが競合したことで、GUI操作エージェントがAPIの標準機能として定着しつつあり、エージェントアーキテクチャの設計においてGUI操作レイヤーを考慮する必要性が高まっている
## 関連記事

- /deep_1608 注意機構の集中によるプリファレンス・リダイレクション：コンピュータ操作エージェントへの攻撃
- /deep_389 国防総省、AI企業が機密データでモデルをトレーニングする計画を検討中
- /deep_440 労働者への報酬インサイト提供：OpenAIの取り組み
- /deep_387 ペンタゴン、AI企業による機密データでの学習を計画――米国防省高官が明かす
- /deep_77 パーソナルヘルスエージェントの解剖：マルチエージェント構造による個人健康支援フレームワーク

## 原文リンク

[モデルからエージェントへ：Responses APIへのコンピュータ環境の統合](https://openai.com/index/equip-responses-api-computer-environment)
