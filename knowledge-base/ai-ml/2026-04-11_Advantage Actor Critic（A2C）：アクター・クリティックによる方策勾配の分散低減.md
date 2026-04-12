---
title: "Advantage Actor Critic（A2C）：アクター・クリティックによる方策勾配の分散低減"
url: "https://huggingface.co/blog/deep-rl-a2c"
date: 2026-04-11
tags: [A2C, Actor-Critic, Policy-Gradient, 強化学習, REINFORCE, Advantage関数, TD誤差, Stable-Baselines3, PyBullet]
category: "ai-ml"
memo: "[HF Blog] Advantage Actor Critic (A2C)"
processed_at: "2026-04-11T21:29:51.043731"
---

## 要約

本記事はHugging Faceの深層強化学習コース Unit 7 として公開されたA2C（Advantage Actor Critic）の解説記事。

【背景：REINFORCEの問題点】
Policy-Gradient法の基本アルゴリズムであるREINFORCEは、モンテカルロサンプリングで収益R(τ)を推定するため不偏性は高いが、エピソード全体を使うため分散が大きい。同一の開始状態から環境の確率性・方策の確率性によって異なる収益が得られるため、勾配推定が不安定になり、学習に大量のサンプルが必要になる。分散を下げるにはバッチサイズを増やす方法があるが、サンプル効率が著しく低下する。

【Actor-Critic の仕組み】
Actor-Critic法はPolicy-Based手法とValue-Based手法を組み合わせたハイブリッドアーキテクチャ。2つのニューラルネットワークを学習する：(1) Actor：方策 π_θ(s,a) を学習し行動を決定、(2) Critic：行動価値関数 q̂_w(s,a) を学習し行動の良さを評価。各タイムステップtで状態S_tをActorとCriticに入力→ActorがA_tを出力→CriticがQ値を計算→ActorはQ値でパラメータ更新→環境からS_{t+1}とR_{t+1}を取得→Criticもパラメータ更新、というオンライン学習ループを回す。モンテカルロ推定（エピソード完了待ち）ではなくTD誤差を使うため、ステップ単位で学習できる。

【A2C：Advantage関数による改善】
Actorの更新基準をQ値からAdvantage関数 A(s,a) = Q(s,a) - V(s) に切り替えたものがA2C。Advantage関数は「その状態の平均的な行動に比べて、この行動がどれだけ良いか」を表す相対的指標。A(s,a)>0なら勾配を正方向に押し上げ、A(s,a)<0なら逆方向に押し下げる。Q(s,a)とV(s)の2つを別々に学習するのはコストが高いが、TD誤差 δ = R_{t+1} + γV(S_{t+1}) - V(S_t) がAdvantage関数の良い推定量として使えるため、V(s)のみを学習するCriticで実装可能。

【実装・実験】
Stable-Baselines3とPyBulletを用いて、二足歩行ロボット（BipedalWalker）とスパイダーロボットの歩行タスクでA2Cを学習する実践例を紹介。Hugging Face Hubへのモデルアップロード・共有フローも含まれる。

## アイデア

- Advantage関数 A(s,a) = Q(s,a) - V(s) はベースライン減算による分散低減の一般原理の具体例であり、TD誤差による近似実装がコスト削減のキー
- Actor（方策）とCritic（価値関数）が互いにフィードバックし合うことで、モンテカルロ法のエピソード完了待ちなしにオンライン学習が可能になる構造
- RLAIFやGRPOとの接点：GRPOはグループ相対的な報酬でAdvantageを推定する手法であり、A2Cの Advantage 概念との比較から報酬スケーリング設計の直感が得やすい

## Yujiの取り組みへの示唆

監査エージェントの強化学習ファインチューニング（GRPO/RLAIF）を検討する際、A2CのAdvantage関数概念は報酬設計と勾配安定化の基礎として直接参照できる。GRPOがグループ内相対報酬でAdvantageを近似する設計を理解するうえで、A2CのTD誤差ベースAdvantage推定との対比が有益。またActor（行動決定）とCritic（評価）の分離構造は、LangGraphにおける「実行エージェント」と「判定エージェント」を役割分離するマルチエージェント設計に対して概念的な参照軸となる。

## 原文リンク

[Advantage Actor Critic（A2C）：アクター・クリティックによる方策勾配の分散低減](https://huggingface.co/blog/deep-rl-a2c)
