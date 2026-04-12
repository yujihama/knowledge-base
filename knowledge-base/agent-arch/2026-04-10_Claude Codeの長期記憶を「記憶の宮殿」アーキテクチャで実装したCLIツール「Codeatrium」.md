---
title: "Claude Codeの長期記憶を「記憶の宮殿」アーキテクチャで実装したCLIツール「Codeatrium」"
url: "https://zenn.dev/senna/articles/f746b9ad67d14d"
date: 2026-04-10
tags: [Claude Code, 長期記憶, 記憶の宮殿, Structured Distillation, ハイブリッド検索, BM25, HNSW, RRF, tree-sitter, multilingual-e5-small, SessionStartHook, palace object]
category: "agent-arch"
memo: "[Zenn LLM] Claude Codeの長期記憶を「記憶の宮殿」で実装した話"
processed_at: "2026-04-10T09:34:20.484028"
---

## 要約

コーディングエージェント（Claude Code）に長期記憶を与えるCLIツール「Codeatrium」の設計と実装を解説した記事。arXiv:2603.13017「Structured Distillation for Personalized Agent Memory」を基盤とし、古典的な記憶術「記憶の宮殿」をAIエージェントの記憶構造に応用している。

【アーキテクチャ概要】Claude Codeの会話履歴（~/.claude/projects/以下のJSONL）をStopHookをトリガーに非同期でDBへ保存。SessionStartHookで会話をpalace objectと呼ぶ構造化データに蒸留する。palace objectは「exchange_core（一文要約、埋め込み対象）」「specific_context（パラメータ等の具体値）」「rooms（記憶の宮殿メタファーによる概念分類）」「symbols（tree-sitterで抽出した関数名・クラス名）」「verbatim_ref（原文への参照ポインタ）」の5フィールドで構成される。

【検索方式】会話原文に対するBM25キーワード検索と、palace objectのexchange_coreに対するHNSW（ベクトル検索）を組み合わせるハイブリッド検索を採用。論文の107構成×201クエリの評価でBM25単独は全構成で有意に劣化（|d|=0.031–0.756）、最良構成はCross BM25(V)+HNSW(D)でMRR 0.759。融合アルゴリズムにはRRF（Reciprocal Rank Fusion）を採用。CombMNZを採用しない理由として、ベクトル検索が常に何らかの結果を返す（偽陽性問題）ためhit_count乗算が不当なスコアブーストを生むことを指摘。RRFはスコア絶対値でなく順位のみで融合するため、スケール正規化不要かつ偽陽性の影響を受けない。

【埋め込みモデル】multilingual-e5-small（384次元）を採用。日英バイリンガル対応・CPU動作・軽量（コールドスタート約7秒）の課題をUnixソケットサーバーでモデルを常駐させることで解決し、2回目以降のレイテンシを0.2秒未満に抑制。アイドル10分で自動停止。

【コスト】蒸留1件あたり平均750〜1,000 tokens（200〜999文字帯）、Proプランでセッションリミットの約1.7%。Structured output（claude -p --output-format json）とユーザー語彙保持指示でLLM出力のブレを抑制。50文字以下の短い交換はインデックス段階で除外。

【コンテキスト注入】CLAUDE.mdにはマーカー付き最小限ルールのみ埋め込み、具体的なコマンド使い方はSessionStart Hookのloci primeがstdoutへ出力してコンテキストウィンドウに動的注入。ツール変更時もCLAUDE.md更新不要。

## アイデア

- 会話原文とその蒸留オブジェクトを別レイヤーに分離し、BM25はVerbatim・HNSWはDistilledに適用するクロスレイヤー構成が検索精度を最大化する（MRR 0.759）という実証的知見
- RRFをCombMNZより優先する理由が明確：ベクトル検索の「ヒットしない件数ゼロ」という特性がCombMNZのhit_count乗算と相性が悪く、偽陽性が高スコアを得る構造的問題を回避できる
- palace objectのsymbolsフィールドにtree-sitterで抽出したコードシンボルを保持することで「コード→過去会話」の逆引き検索を実現し、設計意図・実装背景の想起を可能にする

## Yujiの取り組みへの示唆

監査エージェント開発においてLangGraphの複数セッションにまたがる設計意図・判断根拠の保持は重要課題であり、palace objectの構造化蒸留＋ハイブリッド検索は監査エージェントの会話履歴管理に直接応用可能。特にPydanticによるStructured outputとの親和性が高く、蒸留データ構造をPydanticモデルで定義することで型安全な記憶管理が実現できる。またRRFによるハイブリッド融合はRAGシステムの検索精度向上にも転用でき、監査エビデンスや規程文書の検索基盤として活用できる観点で参考になる。

## 原文リンク

[Claude Codeの長期記憶を「記憶の宮殿」アーキテクチャで実装したCLIツール「Codeatrium」](https://zenn.dev/senna/articles/f746b9ad67d14d)
