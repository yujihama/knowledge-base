---
title: "MLIR入門 — AI推論最適化の仕組みを低レベルから理解する（vec_add Lowering体験）"
url: "https://zenn.dev/ux_xu/articles/mlir-intro-vec-add-lowering"
date: 2026-05-23
tags: [MLIR, LLVM, コンパイラ最適化, AI推論, Lowering, linalg dialect, bufferize, SIMD, progressive lowering, mlir-opt]
category: "infra"
related: [2326, 5797, 4720]
memo: "[Zenn 機械学習] MLIR 入門 — AI推論最適化の仕組みを低レベルから理解する（vec_add Lowering 体験）"
processed_at: "2026-05-23T09:10:15.259551"
---

## 要約

MLIR（Multi-Level Intermediate Representation）はLLVM上に構築されたコンパイラ基盤で、TensorFlow XLA・IREE・torch-mlirなどのAI推論ランタイムに採用されている。本記事では、ベクトル加算（vec_add）を題材に、高レベルのテンソル演算表現から低レベルのLLVM IRまでの段階的変換（progressive lowering）を手を動かして追う。

変換の流れは以下の5段階：①`linalg` dialect（テンソル演算）→ ②bufferizeによって`memref`（明示的メモリバッファ、64バイトアライメントのalloc付き）→ ③`convert-linalg-to-loops`で`scf.for`（構造化ループ、インデックス0〜1024、step 1）→ ④`convert-scf-to-cf`で`cf.br`/`cf.cond_br`による基本ブロック制御（^bb1がヘッダ、^bb2がボディ、^bb3が脱出）→ ⑤`llvm` dialect（`!llvm.ptr`、`llvm.fadd`、`llvm.icmp`等）→ `mlir-translate`でLLVM IRへ。

MLIRの設計思想「1段階で1つの抽象だけを落とす」により、各変換パスの責務が明確に分離される。この分離こそが最適化の挿し込み口を生む：linalg段階ではループタイリング（`linalg.tiling`）やフュージョンが適用でき、scf段階では`scf.parallel`による並列化やunrollが可能で、llvm dialect段階ではSIMD命令へのベクトル化マッピングを行う。

生成されたLLVM IRはスカラーループ状態（`phi`命令でカウンタ管理、`icmp slt`で終端判定、`fadd`で1要素ずつ加算）であり、SIMD化はこの先の`opt`コマンドによるvectorizeパスが担う。動作確認はLLVM/MLIR 17.0.6で行っている。

監査エージェント開発への示唆：LangGraphによる多段エージェントパイプラインはMLIRのprogressive loweringと構造的に類似しており、「各ノードが1つの責務のみを担い、段階的に処理を具体化する」という設計原則は監査ワークフローの分解にも応用できる。推論速度がモデル構造だけでなくコンパイラパイプラインに依存することを理解することで、ローカルLLM推論基盤（Ollama等）のボトルネック分析の解像度が上がる。

## アイデア

- 「1段階で1抽象だけを落とす」progressive loweringの原則は、LangGraphの多段エージェント設計と構造的に同型であり、各ノードの責務分離に応用できる
- `tensor`型（値セマンティクス・副作用なし）をbufferizeで`memref`へ変換する分離設計は、高レベルAPIと低レベルメモリ管理を疎結合にする手法として汎用的
- 同じ演算でも挿し込むパスの順序・位置によって最適化結果が変わるため、コンパイラパイプライン自体がハイパーパラメータとして機能する

## 前提知識

- **LLVM IR** (TODO: 読むべき)
- **コンパイラ中間表現** (TODO: 読むべき)
- **SIMD命令** (TODO: 読むべき)
- **テンソル演算** (TODO: 読むべき)
- **メモリバッファ管理** (TODO: 読むべき)

## 関連記事

- /deep_2326 VFA：グローバル最大値の事前計算によるFlash Attentionのベクトル演算削減
- /deep_5797 MCPサーバーをRustではなく400行の純粋なC++20で書いた理由 〜巨大コード解析における密結合美学〜
- /deep_4720 AutoSP: コンパイラベースのシーケンス並列化によるロングコンテキストLLM学習の自動最適化

## 原文リンク

[MLIR入門 — AI推論最適化の仕組みを低レベルから理解する（vec_add Lowering体験）](https://zenn.dev/ux_xu/articles/mlir-intro-vec-add-lowering)
