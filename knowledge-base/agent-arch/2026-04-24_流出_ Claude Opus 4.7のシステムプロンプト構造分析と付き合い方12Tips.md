---
title: "流出? Claude Opus 4.7のシステムプロンプト構造分析と付き合い方12Tips"
url: "https://zenn.dev/orangewk/articles/claude-system-prompt-structure-guide"
date: 2026-04-24
tags: [Claude, システムプロンプト, プロンプトエンジニアリング, memory_system, tool_discovery, CL4R1T4S, LLM対照実験]
category: "agent-arch"
related: [973, 2363, 860, 1483, 108]
memo: "[Zenn LLM] 流出? ClaudeOpus4.7のSystemプロンプト、本人や他LLMに見せてみた — 構造分析 + 付き合い方"
processed_at: "2026-04-24T12:53:39.008945"
---

## 要約

GitHubリポジトリ「elder-plinius/CL4R1T4S」に投稿された「Claude Opus 4.7のシステムプロンプト」とされるテキストを、6モデル（Claude Sonnet 4.6、Claude Opus 4.7 Claude Code上、Claude Opus 4.7 API直叩き、Claude Opus 4.7 Agent SDK経由、Codex/GPT-5.2、Qwen）に読ませた対照実験の構造分析記事。

結論として、逐語レベルの内容（モデル名・日付・実装トリビア）は捏造混入の可能性が高く、Anthropic公式の実行時プロンプトではなく内部ドキュメントの再構成と推定される。一方、構造・方針レベル（階層設計・search_first・著作権ルール・フォーマット規定）は実際の挙動と整合する「本物っぽい」部分を含む。

システムプロンプトの積層構造は「claude_behavior → memory_system → tool_discovery → search_instructions → 安全装置 → 作業環境 → API埋め込み」の順。memory_systemは3層構造で、第1層はセッション開始時に注入されるuserMemoriesタグ、第2層はconversation_search経由で検索する過去会話DB、第3層はmemory_user_editsで直接書き換え可能な編集層。「覚えておいて」と言っただけでは抽出バッチ後にしか第1層に反映されない点が重要。

tool_discoveryはSlack/Gmail/Google Calendarなどの統合ツールをtool_search経由で遅延ロードする設計で、エージェントが自分の能力境界を能動的に探索する構造。著作権のハードリミットは「直接引用15語未満・同一ソース1回限り・歌詞/詩/俳句の完全再現禁止」の3条件。

実用Tips12個の主要点：①「現在の」「最新の」を明示してsearch_firstトリガーを確実に発火させる、②「ドキュメントを作って」vs「書いて」でファイル生成とインライン応答を切り替える、③conversation_searchがキーワード一致のため過去会話参照には固有名詞を含む具体的な表現が必要、④モバイルはデフォルト6〜8文程度に整形されるため「詳しく」と明示が必要、⑤自分固有の作業パターン（著者の「養生パターン」等）をmemory_user_editsに登録することでセッション跨ぎの挙動安定化が可能。

監査エージェント開発への示唆：tool_discoveryの遅延ロード設計はLangGraphのエージェントが自身の能力境界を動的に把握する実装パターンと対応する。memory_systemの3層分離は長期記憶・セッション記憶・即時編集の責務分離設計として参考になる。

## アイデア

- エージェントがtool_searchで自分の能力境界を能動的に探索する設計は、LangGraphでツールを動的に登録・発見する実装パターンと同型であり、能力境界の自己観察を構造的に担保する手法として応用できる
- memory_systemの3層分離（即時注入層・検索層・直接編集層）は、LLMエージェントの記憶管理における責務分離の実装パターンとして、監査エージェントの長期コンテキスト管理設計に直接転用可能
- 同一モデル重みでも環境（システムプロンプト）の差で挙動が大きく変わることを6モデル対照実験で実証した方法論自体が、LLM-as-judgeやエージェント評価における「バリアント制御」の設計参考になる

## 前提知識

- **システムプロンプト** → /deep_62 LLMチャットボットに欠けているもの：目的意識（Purposeful Dialogue）
- **Claude Agent SDK** → /deep_1 Agent SkillにReactアプリを同梱するSkill Appアーキテクチャの実装
- **RAG / conversation_search** (TODO: 読むべき)
- **LLM memory管理** (TODO: 読むべき)
- **tool_use / function calling** (TODO: 読むべき)

## 関連記事

- /deep_973 agency-agentsの144エージェントは「どこまで使えるのか」を本気で調べてみた
- /deep_2363 Claude Max 20xでもトークンが足りない。重度ユーザーが実践する文脈管理と節約の工夫8選
- /deep_860 語彙の地平（Vocabulary Horizon）：LLMペルソナ設計における語彙制限による思考誘導アイデア
- /deep_1483 構文は簡単、意味論は難しい：LLMによるLTL変換の評価
- /deep_108 局所整合から経路全体へ ― 意味の経路積分による生成AI挙動の数理的再解釈

## 原文リンク

[流出? Claude Opus 4.7のシステムプロンプト構造分析と付き合い方12Tips](https://zenn.dev/orangewk/articles/claude-system-prompt-structure-guide)
