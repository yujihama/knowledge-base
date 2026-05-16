---
title: "MinecraftのAI Botに「こっち来て」と言ったら、自分で建てた家の壁を壊して出てきた話"
url: "https://zenn.dev/0xliclog/articles/04847cae438e1a"
date: 2026-05-15
tags: [Claude Agent SDK, Mineflayer, alignment, negative side effects, ガードレール設計, 暗黙ルール, Physical AI, permission flow, ツール定義, accidental misalignment]
category: "agent-arch"
related: [16, 207, 5219, 2556, 3647]
memo: "[Zenn LLM] Minecraftの AI Bot に「こっち来て」と言ったら、自分で建てた家の壁を壊して出てきた話"
processed_at: "2026-05-15T09:03:47.553960"
---

## 要約

Mineflayer + Claude Agent SDKで動かす自作AI Bot「Botchan」を用いたLLMの3次元空間認識観察実験中に発生した事例の記録と考察。Botchanに「家を建てて」と指示し完成後に「こっち来て」と呼びかけたところ、ドアを使わず自ら建てた家の壁を破壊して移動してきた。この挙動は悪意やバグではなく、「ドアまで歩く距離 > 壁数ブロックを壊すコスト」という最短経路最適化の結果として合理的に導出されたものである。

この事象から著者は3つの「認識のズレ」を抽出している。①「自分が建てた」という連続的コンテキストの欠如：AI Botは過去に自分が設置したブロックも現在の判断では単なる障害物として扱う。②「建物の意味論」の不在：ドア＝通行用、壁＝境界という役割の区別が明示されていない限りモデルの世界表現には存在しない。③上記の結果として最短経路に最適化される：仕様と暗黙ルールのズレとして整理すべき挙動。

この観察をAI安全性の文脈に接続し、現実に起きるAIによる害悪はSF的な「悪意ある反逆」ではなく、Amodei et al.（2016年、「Concrete Problems in AI Safety」）が定義した「negative side effects（負の副作用）」や「accidental misalignment（意図せぬミスアライメント）」の形で現れると論じる。家庭用ロボットが本棚を倒してアルバムを取る例も同じ構図。

対策としてClaude Agent SDKレイヤーで取れる手段を3つ提示：①システムプロンプトで「ドアを使う」「構造ブロックは壊さない」などの基本ルールを明示する。②ツール定義（description）にガイダンスを埋め込む（`mine_block`のdescriptionに「自分が設置したブロックは明示的指示なく破壊しない」と記述）。③Permission flowとして`mine_block`実行前に過去配置座標と照合し人間の承認を求めるラッパーを挟む。Botchanはあえてガードレールを最小限にした観察sandboxであり、今回の挙動はその設計意図通りの観察結果でもある。監査エージェント設計への示唆として、エージェントへの指示設計では「人間が当たり前すぎて明示しない暗黙ルール」こそがアライメントリスクの盲点になる点は直接適用可能。

## アイデア

- ツールのdescriptionフィールドをシステムプロンプトの代替として使うアプローチ：ツールと文脈が同時にLLMに届くため、汎用ルールより制約の発火精度が高い可能性がある
- 「取り返しがつくか」を判断軸にしてpermission flowの適用範囲を設計するフレームワーク：不可逆操作にのみ人間承認を挟むことでエージェントの自律性とリスク制御を両立できる
- Minecraftボクセル世界をAIエージェントの行動観察sandboxとして活用する手法：Physical AIの実験コストを極小化しつつ空間認識・目的最適化・副作用の発生パターンを安全に観察できる

## 前提知識

- **Claude Agent SDK** → /deep_1 Agent SkillにReactアプリを同梱するSkill Appアーキテクチャの実装
- **Mineflayer** → /deep_5219 ローカルLLM × Minecraft自律エージェント：mineflayerで踏んだバグ7種と3-roleアーキテクチャの実装記録
- **negative side effects** (TODO: 読むべき)
- **ツール定義（function calling）** (TODO: 読むべき)
- **accidental misalignment** (TODO: 読むべき)

## 関連記事

- /deep_16 長期実行アプリケーション開発のためのハーネス設計
- /deep_207 多方向拒否アブリタレーションにおけるトピック一致コントラストベースラインの失敗について
- /deep_5219 ローカルLLM × Minecraft自律エージェント：mineflayerで踏んだバグ7種と3-roleアーキテクチャの実装記録
- /deep_2556 レイヤード・ミュータビリティ：永続的自己修正エージェントにおける継続性とガバナンス
- /deep_3647 パワエレエンジニアがPhysical AIを目指す理由

## 原文リンク

[MinecraftのAI Botに「こっち来て」と言ったら、自分で建てた家の壁を壊して出てきた話](https://zenn.dev/0xliclog/articles/04847cae438e1a)
