---
title: "Sensible Agent: プロアクティブARエージェントとの非侵襲的インタラクションフレームワーク"
url: "https://research.google/blog/sensible-agent-a-framework-for-unobtrusive-interaction-with-proactive-ar-agents/"
date: 2026-04-04
tags: [AR, proactive-agent, multimodal, VLM, chain-of-thought, few-shot, Android-XR, WebXR, YAMNet, UIST2025, context-aware, gesture-input]
category: "agent-arch"
memo: "[Google AI Blog] Sensible Agent: A framework for unobtrusive interaction with proactive AR agents"
related: [1608, 819, 975, 650, 522]
processed_at: "2026-04-04T12:05:23.818056"
---

## 要約

GoogleのXRチーム（Ruofei Du, Geonsun Lee）がUIST 2025で発表した研究。ARグラスを装着したユーザーに対し、明示的な音声コマンドを必要とせずプロアクティブに支援を提供するエージェントフレームワーク「Sensible Agent」を提案。

【技術構成】システムは4モジュールで構成される。①コンテキストパーサー：VLM（視覚言語モデル）でヘッドセットカメラ映像を解析し、YAMNet（事前学習済み音声イベント分類器）で環境騒音を評価。ユーザーの現在状況（場所・活動）をパース。②プロアクティブクエリジェネレーター：Chain-of-Thought（CoT）推論と6例のfew-shot learningを用いて「何を支援すべきか」を決定。出力はアクション種別（例：Recommend Dish）、クエリ形式（Multi-choice/Binary Choice/Icon）、提示モダリティ（Audio Only/Visual Only/Both）の3要素。③インタラクションモジュール：UIマネージャーが視覚パネルまたはTTS音声で提案を提示。入力モダリティマネージャーがコンテキスト（手の空き状況、騒音レベル）に応じて頭部ジェスチャー・手ジェスチャー・音声コマンド・視線のうち最適な入力手段を有効化。④レスポンスジェネレーター：ユーザーの選択（例：頭を縦に振る）を受け、LLMが自然言語回答を生成しTTSで音声出力。

プロトタイプはAndroid XRおよびWebXR上で動作し、実機のXRヘッドセットで稼働することを確認済み。

【ユーザースタディ】参加者10名が12シナリオ（レストランでのメニュー読み、公共交通機関での移動、スーパーでの買い物、美術館見学、ジム、料理）を体験。Project Astraをモデルにした従来の音声制御ARアシスタントと比較。360°没入動画またはVideo See-Through（VST）ARの2形式で実施。

【結果】NASA Task Load Index（NASA-TLX、100点スケール）による認知負荷がSensible Agentで有意に低下。System Usability Scale（SUS）でも高い使用性を確認。7点Likertスケールでユーザー選好も優位。インタラクション時間も短縮。

特徴的な設計思想は「社会的文脈への適応」：混雑した場所や社会的場面で音声コマンドを強要せず、最小限の視覚・身体的合図で支援を完結させる点にある。

## アイデア

- 「何を支援するか（what）」と「どう提示するか（how）」を独立したモジュールで分離した2段階エージェント設計は、エージェントの行動決定とユーザーへのアウトプット形式選択を疎結合にする汎用的なアーキテクチャパターンとして応用可能
- CoT推論 + 6例few-shotでプロアクティブな行動決定を実現しており、大規模なファインチューニングなしに文脈適応的な行動選択が可能なことを示している
- 入力モダリティをコンテキスト（手の可用性・騒音レベル）に応じて動的に切り替える「入力モダリティマネージャー」の概念は、ユーザーの状態に応じてインタラクション手段を選択するアダプティブUIの参考設計として価値がある
## 関連記事

- /deep_1608 注意機構の集中によるプリファレンス・リダイレクション：コンピュータ操作エージェントへの攻撃
- /deep_819 外科手術動画データセットの拡充手法：VLMの細粒度時空間理解のための SurgSTU-Pipeline
- /deep_975 リモートセンシング向け継続的ビジョン言語学習：ベンチマークと分析（CLeaRS）
- /deep_650 Vision Language Models（より良く、より速く、より強く）- 2025年最新動向
- /deep_522 TimeScope: ビデオ大規模マルチモーダルモデルの長時間動画理解能力を測定するベンチマーク

## 原文リンク

[Sensible Agent: プロアクティブARエージェントとの非侵襲的インタラクションフレームワーク](https://research.google/blog/sensible-agent-a-framework-for-unobtrusive-interaction-with-proactive-ar-agents/)
