---
title: "異なるLLMによるコードレビューでSelf-Enhancementバイアスを軽減する"
url: "https://zenn.dev/beingish/articles/4c0d999411ecee"
date: 2026-05-09
tags: [LLM-as-a-Judge, Self-Enhancement, Claude Code, Gemini CLI, コードレビュー, バイアス軽減, Vertex AI, Skill]
category: "agent-arch"
related: [1741, 2824, 3242, 1429, 2953]
memo: "[Zenn LLM] 異なる LLM によるコードレビューでバイアスを軽減する"
processed_at: "2026-05-09T12:47:46.499921"
---

## 要約

LLMをコードレビュアーとして利用する際、LLM-as-a-Judgeで観測されるバイアスが問題となる。arxiv:2410.02736が示す12種類のバイアス（Position、Verbosity、Self-Enhancement等）のうち、現在でも対処が必要なのはPositionとSelf-Enhancementの2つ。特にSelf-Enhancementは「自分が生成したコードを同一モデルでレビューさせると指摘が甘くなる」という問題で、同一ファミリーのモデル間（例：Claude CodeでコードをGenerateしてCode Reviewでレビュー）でも発現する。Anthropicのbloom調査が報告するSelf-preferential biasがその根本原因であり、Self-Enhancementはその一表出形態と位置付けられる。

対処法として本記事が提案するのは「コード生成モデルとは別ファミリーのモデルでレビューする」というアプローチ。著者はClaude Codeで開発し、Gemini CLIでレビューする構成を採用。Claude CodeのSkill機能を使い、`/review-gemini`コマンド一発でGemini CLIにレビューを委譲するSkillを実装している。

Skillの実装は`~/.claude/skills/review-gemini/SKILL.md`に記述。`disable-model-invocation: true`を設定してClaude自身の推論を介さずGemini CLIに直接渡す。コマンドは`gemini --allowed-tools "run_shell_command(git)" -p "<プロンプト>"`で、mainブランチとの全差分（コミット済み・ステージ済み・未コミット・untracked全て）をレビュー対象とする。出力はClaudeが一切要約・編集せずそのまま表示する点が重要（Claudeによる解釈介入を避けるため）。

認証はVertex AI経由（Google Cloud ADC）で行い、APIトークンをローカルに置くリスクを回避。モデルはgemini-2.5-flashを使用（2.5-proはsycophancyバイアスが多いため非推奨）。レビュープロンプトは重大度（Critical/Major/Minor）・ファイル名・行番号・観点別セクションを含むフォーマットを指定し、意図的に良い判断がされた箇所も「破壊しないための記録」として列挙させる。

監査エージェント開発への示唆：LLM-as-a-Judgeを評価パイプラインに組み込む際、Self-Enhancementバイアスを避けるために生成モデルと評価モデルを別ファミリーにする設計原則は、コードレビューに限らずLangGraphベースの評価ノード設計にも直接適用できる。

## アイデア

- Self-Enhancementバイアスは同一モデルだけでなく同一ファミリー間でも発現するため、OpenAI→Anthropic、Anthropic→Googleのようにベンダーを跨ぐ構成が必要という知見
- disable-model-invocation: trueによりClaudeの推論を完全にバイパスし、外部CLIツールへの純粋なオーケストレーターとしてSkillを機能させる設計パターン
- 「修正時に誤って壊さないよう、意図的に良い判断がされている箇所を保護目的で列挙する」というレビュープロンプト設計は、コード品質の退行防止に有効な観点

## 前提知識

- **LLM-as-a-Judge** → /deep_908 RAGアプリをLLM-as-a-Judgeで強化した事例：Farmer.chatの評価システム構築
- **Self-Enhancement bias** (TODO: 読むべき)
- **Claude Code Skills** → /deep_1473 Claude Code Skillsは作って終わりじゃない — 事後ログで改善サイクルを回す
- **Gemini CLI** (TODO: 読むべき)
- **Application Default Credentials** (TODO: 読むべき)

## 関連記事

- /deep_1741 プロンプトを毎日書いていたら、コードレビューの書き方が変わった
- /deep_2824 プロンプトの再現性をAIに自動チューニングさせる方法 〜 暗黙知を排除する
- /deep_3242 AIにコードを書かせ続けた結果起こった悲劇：ガバナンス崩壊と立て直し記録
- /deep_1429 非エンジニアがKaggleで3999チーム中1257位になった話
- /deep_2953 長門有希ペルソナがClaude Codeのトークン消費を削減する：キャラクター指定vsルールベース圧縮の比較検証

## 原文リンク

[異なるLLMによるコードレビューでSelf-Enhancementバイアスを軽減する](https://zenn.dev/beingish/articles/4c0d999411ecee)
