---
title: "ローカルLLM × Minecraft自律エージェント：mineflayerで踏んだバグ7種と3-roleアーキテクチャの実装記録"
url: "https://zenn.dev/toki_mwc/articles/minecraft-hermes-3role-mineflayer-bugs"
date: 2026-05-11
tags: [mineflayer, LLM-agent, gemma-4, state-machine, llama.cpp, Minecraft, Hermes-agent, 3-role-architecture, 決定論Executor, ReAct]
category: "agent-arch"
related: [1523, 4753, 22, 5000, 4092]
memo: "[Zenn LLM] ローカルLLM｜Minecraft自律｜踏んだバグ7種"
processed_at: "2026-05-11T09:43:02.493647"
---

## 要約

Hermes Agent Creative Hackathon（2026年4月）で構築した3-role構成をMinecraft操作タスクへ移植した際の実装ログ。環境はPaper 1.20.1 build 196、mineflayer 4.25、llama.cpp v8870、gemma-4-E4B-it-Q4_K_M、Windows 11 + WSL2 Ubuntu 24.04。

【アーキテクチャ】Observer・Planner・Executorの3役割に分離。ObserverはmineflayerのチャンクからHP・food・inventory・nearby entitiesをJSONスナップショット化。Plannerはローカルで動くgemma-4-E4B（4.62GiB、RTX 5090で軽負荷）にObserver出力を渡し、{goal, reason, priority}の構造化JSONを800ms以内で返させる。ExecutorはPlannerのgoalを直接実行せず、state machineが現在のinventory・world状態を見て実行すべきactionを確定する。LLMのフラキーさをExecutor層で吸収することで、single-runでspawnからIron Pickaxeまで約290秒での到達を実現した。

【踏んだバグ7種】①Paper 1.20.4とmineflayer 4.25の組み合わせでspawn直後にInvalid move player packetで蹴られる→1.20.1へ降格で解消。②bot.placeBlock()がblockUpdateイベントを待ち続け15秒hangする→bot.lookAt()で向き補正後、Promise.race()で6秒タイムアウトを挟み、配置後にblockAt()で検証する3ステップで成功率1/4→4/4に改善。③bot.entity.positionのx/zがnullになるrace conditionで55回連続chopTreeがヒットしなくなる→ログにposition.toString()を記録し再現時の状態捕捉を必須化。④iron pickaxe craft直前でrawIron単体の判定ロジックの穴によりmineIronOre→smeltの無限ループに入る→ironIngots+rawIronの合算判定とsticks補充分岐をiron tier最優先で追加し35秒で完走。⑤coal miningの優先順位が高すぎてcobble 0のまま60秒タイムアウト×9連発→furnacePlacedチェック前にcobble確保を優先させる順序変更で解消。⑥深層採掘中のcollectBlock()が永続hangする→Promise.race()で12秒タイムアウトとbot.stopDigging()を組み合わせてキャンセル処理。⑦pathfinder停止後のtimeout cleanupが不完全で次タスクのpathfinderが二重起動する→pathfinder停止時に明示的にイベントリスナーを解除。

【知見】LLMをPlannerに限定しExecutorを決定論的state machineに寄せるほど完走率が上がる。tech treeの優先順位は終端（iron pickaxe）から逆算して欠けている素材を埋める「逆順設計」が安全。環境操作型エージェントではLLMの自由度を上げると失敗モードが増える、という制約はVoyagerやGITMがskill DSLで吸収しているトレードオフと同質。監査エージェント開発への示唆：LLMはhigh-levelな判断・ログ生成に専念させ、実際のDB操作やAPI呼び出しはstate machineまたは決定論的ロジックに委ねる分離設計が、エラー耐性と再現性を両立させる現実解となり得る。

## アイデア

- LLMをPlannerに限定し決定論的state machineをExecutorとして分離することで、LLMのフラキーさを吸収しながら完走率を大幅に向上させる「責任配分の逆転」設計が、生成タスク系エージェントとは異なる環境操作型エージェントの現実解であること
- tech treeの優先順位を前向き（素材収集→加工）ではなく終端から逆算して欠けている素材で並べる「逆順設計」により、中間状態の無限ループを構造的に防止できること
- mineflayer/Paperサーバ/ゲーム物理の3層にわたる状態同期の問題（パケット拒否・placeBlock hang・position null・collectBlock hang）は推論性能とは独立して発生し、Promise.race()タイムアウト＋実物検証という防御的実装パターンで体系的に対処できること

## 前提知識

- **mineflayer** (TODO: 読むべき)
- **LLM Planner-Executor分離** (TODO: 読むべき)
- **決定論的state machine** (TODO: 読むべき)
- **llama.cpp** → /deep_940 Llama 3.2 リリース：視覚理解とオンデバイス推論を兼ね備えたオープンモデル群
- **Hermes Agent** → /deep_3000 OpenClaw vs Hermes Agent：2つのオープンソースAIエージェントの設計思想を徹底比較

## 関連記事

- /deep_1523 LogAct: 共有ログによるエージェントの信頼性向上
- /deep_4753 限界ClaudeCodeユーザーがoh-my-claudecodeを調べてみた：マルチエージェント実行フレームワークの全貌
- /deep_22 長期ロボット卓上ゲームにおける内部状態一貫性維持のためのシステム設計
- /deep_5000 自動計画における反事実推論
- /deep_4092 現在のAIエージェントは「発見→応用」ギャップを埋められるか：Minecraftを用いたケーススタディ

## 原文リンク

[ローカルLLM × Minecraft自律エージェント：mineflayerで踏んだバグ7種と3-roleアーキテクチャの実装記録](https://zenn.dev/toki_mwc/articles/minecraft-hermes-3role-mineflayer-bugs)
