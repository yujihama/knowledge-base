---
title: "ニューロンは原始演算子を夢見るか？ Wake-Sleep圧縮がSchankのイベント意味論を再発見する"
url: "https://arxiv.org/abs/2603.25975"
date: 2026-04-05
tags: [DreamCoder, wake-sleep学習, 最小記述長, MDL, 概念依存理論, シンボルグラウンディング, プログラム合成, イベント意味論, ATOMICグラフ, 知識表現]
category: "ai-ml"
memo: "[arXiv cs.AI+cs.LG] Do Neurons Dream of Primitive Operators? Wake-Sleep Compression Rediscovers Schank's Event Semantics"
processed_at: "2026-04-05T09:09:25.586088"
---

## 要約

本論文は、1970年代にRoger Schankが提唱した「概念依存理論（Conceptual Dependency Theory）」の中核をなすイベント原始演算子群（ATRANS: 所有権移転、PTRANS: 物理的移動、MTRANS: 情報転送、INGESTなど）が、人手でのルール設計なしに圧縮圧力だけから自動的に再発見できるかを検証した研究である。

手法として、プログラム合成フレームワーク「DreamCoder」のwake-sleepライブラリ学習を、イベントの状態変換（世界の「before/after」ペア）に適用する。覚醒フェーズ（wake）では各イベントを説明する演算子の組み合わせを探索し、睡眠フェーズ（sleep）では最小記述長（MDL: Minimum Description Length）原理に基づき再頻出パターンを新たな演算子として抽象化する。出発点は4つの汎用原始演算子のみであり、ドメイン知識は一切与えない。

実験は2段階で行われた。①合成データ：システムが発見した演算子はSchankの手動設計原始演算子と直接対応し（MOVE_PROP_has → ATRANS、CHANGE_location → PTRANS、SET_knows → MTRANS等）、ベイズMDLスコアはSchankの4%以内に収束しながら100%のイベントを説明（Schankの手動系は81%）。さらに複合演算子（「mail」= ATRANS + PTRANS）も自律的に構成された。②ATOMICコモンセンス知識グラフの実世界データ：Schankの原始演算子では自然言語イベントのわずか10%しか説明できないのに対し、発見されたライブラリは100%を説明。支配的な演算子は物理行動ではなく精神・感情状態変化（CHANGE_wants: 20%、CHANGE_feels: 18%、CHANGE_is: 18%）であり、これらはSchankの元の体系には存在しない。

この結果は、（1）イベント原始演算子が人手設計なしに圧縮圧力から導出可能であること、（2）Schankの核心的原始演算子が情報理論的に正当化されること、（3）現実的イベント空間では精神・感情演算子が物理演算子より支配的であることを初めて実証的に示す。symbol groundingとneural compressionの橋渡しとなる結果といえる。

## アイデア

- 圧縮原理（MDL）だけで1970年代に人手設計された意味論的原始演算子を再発見できたことは、LLMの内部表現がシンボリックな意味構造を暗黙的に保持している可能性を示唆する独立した証拠となる
- 現実世界のイベントではSCHANKが想定した物理演算子ではなくCHANGE_wants/feels/isなど精神・感情演算子が支配的（合計56%）であり、行動予測やエージェント設計における状態表現のモデル化を再考させる知見
- wake-sleepによるライブラリ成長は「少数の汎用原始演算子 → 圧縮を通じた専門演算子の自律的獲得」という経路を示し、エージェントがツールやスキルを自己組織化する仕組みのプロトタイプとして参照できる
## 関連記事

- /deep_242 単純性バイアスの圧縮理論的解釈
- /deep_306 シンプリシティバイアスの圧縮理論的解釈
- /deep_1646 AIの「理解」をハードウェアが縛る理由 —— TPUでは蜂の嗅覚は実装できない

## 原文リンク

[ニューロンは原始演算子を夢見るか？ Wake-Sleep圧縮がSchankのイベント意味論を再発見する](https://arxiv.org/abs/2603.25975)
