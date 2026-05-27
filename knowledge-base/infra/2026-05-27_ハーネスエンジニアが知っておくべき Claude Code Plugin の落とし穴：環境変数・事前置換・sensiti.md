---
title: "ハーネスエンジニアが知っておくべき Claude Code Plugin の落とし穴：環境変数・事前置換・sensitive の tier 別挙動"
url: "https://zenn.dev/storehero/articles/20ed4b2e8772b3"
date: 2026-05-27
tags: [Claude Code, Plugin, hooks, SKILL.md, 環境変数, sensitive, ハーネスエンジニア, userConfig]
category: "infra"
related: [4228, 5970, 94, 1045, 5907]
memo: "[Zenn LLM] ハーネスエンジニアなら知っておきたい Claude Code Plugin の落とし穴"
processed_at: "2026-05-27T09:08:19.696964"
---

## 要約

本記事は Claude Code v2.1.146-150 を対象に probe ベースで検証した結果をまとめたもので、plugin 開発で事故率の高い 6 つの論点を解説する。

Plugin のコード実行場所は①plugin-level hook（hooks/hooks.json）、②skill frontmatter hook（SKILL.md の YAML frontmatter）、③Bash tool subprocess（SKILL.md 本文）の 3 層に分かれており、それぞれ別プロセスで起動される。この 3 層で Claude Code 本体から渡される環境変数のセットが非対称であることが最大の落とし穴となる。

【環境変数の tier 別伝播】CLAUDE_PLUGIN_ROOT は①②に設定されるが③には未設定。CLAUDE_PLUGIN_DATA は①のみ。CLAUDE_PLUGIN_OPTION_<KEY>（userConfig 値）は①のみで②③には届かない。CLAUDE_PROJECT_DIR は①②に設定されるが③では未設定。これは再現性のある挙動であり、意図的な設計と推定される。

【${VAR} 事前置換の tier 別 allowlist】Claude Code 本体がコマンド実行前に ${VAR} を置換する「事前置換」と、/bin/sh が実行時に展開する「シェル展開」が混在する。${CLAUDE_PLUGIN_ROOT} は全 tier で置換されるが、${CLAUDE_PLUGIN_DATA} は skill frontmatter hook で validator が reject する。${user_config.KEY} は①と skill body では置換されるが、skill frontmatter hook では literal のまま /bin/sh に渡り「Bad substitution」エラーになる。${CLAUDE_PROJECT_DIR} は①とskill bodyで置換されるが②では literal のまま。

【skill body の置換タイミング】SKILL.md 本文の ${VAR} 置換は skill が invoke されて Claude の context にロードされる瞬間のみ実行される。Read ツールや Grep ツールでファイルとして読んだ場合は literal の ${CLAUDE_PLUGIN_ROOT} がそのまま見える。

【sensitive: true の tier 別挙動】保存先は~/.claude/settings.json から OS keychain または ~/.claude/.credentials.json の pluginSecrets セクションに分離される。plugin-level hook の env には平文で届く（hook 作者を信頼する設計）。skill body では ${user_config.KEY} がブロック文字列（[hidden]等）に置換され、Claude の context に機密値がリークしない設計になっている。

監査エージェント開発への示唆：認証情報や API シークレット等の機密値を扱う処理は必ず plugin-level hook（①）に閉じ込め、skill body や skill frontmatter hook には機密値を渡さない設計原則が重要。環境変数の伝播境界を意識したアーキテクチャ設計は、監査ログの改ざん防止や権限分離の実装パターンと同様の考え方であり、ゼロトラスト的な tier 分離設計の参考になる。

## アイデア

- 環境変数の伝播が 3 層で非対称という設計は「plugin 作者 vs ユーザ」の二層 trust モデルを実装レベルで強制しており、権限分離をアーキテクチャで担保するアプローチとして参考になる
- ${VAR} の事前置換と /bin/sh のシェル展開が混在することで tier ごとに置換可否が変わるという挙動は、Claude Code が独自の template engine を持つことを示しており、LLM ツール呼び出しの前処理レイヤー設計として興味深い
- sensitive: true の値が skill body では Claude の context にリークしない設計（ブロック文字列への置換）は、LLM に機密情報を渡さずに外部システム連携を実現するための実装パターンとして応用可能

## 前提知識

- **Claude Code Plugin** (TODO: 読むべき)
- **hooks.json** (TODO: 読むべき)
- **SKILL.md** → /deep_1045 エイプリルフールに「担当と話せるAIエージェント」を3時間で作った話
- **環境変数伝播** (TODO: 読むべき)
- **/bin/sh シェル展開** (TODO: 読むべき)

## 関連記事

- /deep_4228 superpowersを解析して学ぶClaude Codeプラグイン設計
- /deep_5970 ハーネスは書いて終わりじゃなかった ── 3か月運用して動的に壊れた5つの瞬間
- /deep_94 コーディングエージェントのエンジニアリングに対する考え方
- /deep_1045 エイプリルフールに「担当と話せるAIエージェント」を3時間で作った話
- /deep_5907 ひと月でADRを40本近く書いたら何が変わったか — Claude Code規範運用1ヶ月の失敗録

## 原文リンク

[ハーネスエンジニアが知っておくべき Claude Code Plugin の落とし穴：環境変数・事前置換・sensitive の tier 別挙動](https://zenn.dev/storehero/articles/20ed4b2e8772b3)
