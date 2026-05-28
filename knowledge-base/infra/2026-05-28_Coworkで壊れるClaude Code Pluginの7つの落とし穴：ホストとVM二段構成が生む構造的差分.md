---
title: "Coworkで壊れるClaude Code Pluginの7つの落とし穴：ホストとVM二段構成が生む構造的差分"
url: "https://zenn.dev/storehero/articles/2bc58c12090f72"
date: 2026-05-28
tags: [Claude Code, Claude Desktop, Cowork, Plugin, hooks, WSL, 環境変数, shell展開, VM]
category: "infra"
related: [6679, 5970, 94, 2961, 4228]
memo: "[Zenn LLM] ハーネスエンジニアなら知っておきたい Cowork でぶっ壊れる Claude Code Plugin の罠"
processed_at: "2026-05-28T09:03:19.495539"
---

## 要約

本記事は、Claude Code CLIとCowork（Claude Desktop内蔵のagentic実行モード）でPluginを動作させた際に生じる非対称な挙動を、probe実験に基づいて7パターン整理したものである。検証環境はWindows版Claude Desktop v1.8555.2（Claude Code core v2.1.146-150）。

Coworkの根本的なアーキテクチャは「ホストOS（Windows/macOS）」と「ローカルLinux VM（Ubuntuベース）」の二段構成であり、plugin-level hookはホストOS側のshellで実行され、skill bodyのbash/Bash toolサブプロセスはVM内で実行される。この分断が全落とし穴の根源となる。

【環境変数の消失】CLIではplugin-level hookのenvに`CLAUDE_PLUGIN_ROOT`、`CLAUDE_PLUGIN_DATA`、`CLAUDE_PROJECT_DIR`、`CLAUDE_PLUGIN_OPTION_*`、`CLAUDE_ENV_FILE`等が設定されるが、Coworkではこれらが全て未設定（UNSET）になる。

【hook commandの二重破壊】top-levelのhook commandでは`$VAR`展開が抑止され、`bash -c`でwrapすれば展開は有効になるが、`CLAUDE_PLUGIN_*`系はそもそもenvに存在しないため取得不可。結果として`${CLAUDE_PLUGIN_ROOT}/hooks/log.sh`という記述は`No such file or directory`エラーで失敗する。

【skill bodyのパス化け】skill body内の`${CLAUDE_PLUGIN_ROOT}`は事前置換（Claude Code本体がスキャンして置換）により動作するが、置換後の値はホストOSのパス（例：Windowsなら`C:\...`）になる。VM内からこのパスにアクセスするにはmount経由である必要があり、plugin install dirやfolder connect配下にある場合のみVMからアクセス可能。それ以外のホストパスはVMから見えない。

【filesystemの完全分断】plugin-level hookとBash toolは別のfilesystem namespaceで動作するため、`/tmp/foo.txt`をhook側で書いてもBash tool側からは読めない。`CLAUDE_ENV_FILE`もCoworkでは未設定のため、hook→Bash toolへの環境変数受け渡し手段が存在しない。

【skill frontmatter hookの不発火】CLIでは有効なskill frontmatter hookが、Coworkでは発火が確認できない。`PreToolUse`ブロック自体は書けるが、サイレントに失敗するパターンが存在する。

【SessionStart hookの無音失敗】CLIで正常動作するSessionStart hookが、Coworkでは無音で失敗するケースがある。

対策として、plugin install dirの参照には`find /sessions`経由の別経路を使用すること、変数を使う場合は必ず`bash -c '...'`でwrapすること、bash固有構文（`[[ ]]`等）はPOSIX非互換のため`bash -c`内に閉じ込めることが推奨される。ホスト・VM環境の判別には`hostname`コマンドが使えるとされており、`claude`と返ればVM内、それ以外はホストOS側と判断できる。監査エージェント開発においてClaude CodeをCI/CD的な自動化基盤として利用する場合、このCowork/CLI差分はPlugin設計の早期段階で考慮すべき構造的制約となる。

## アイデア

- 「事前置換」と「envシェル展開」の区別という概念：Claude Code本体が行う文字列スキャン置換と、起動したshellが行うenv展開は別プロセスであり、同じ`${VAR}`記法でも動作する層が異なるという設計上の非自明な差分
- `hostname`コマンドによるホスト/VM環境判別：`claude`固定であればVM内、それ以外はホストOSという単純な判別法で、両環境対応Pluginの分岐軸として使える実用的なイディオム
- 二段構成アーキテクチャが生む構造的落とし穴の体系化：単発バグでなくアーキテクチャ由来の必然的差分として7パターンを整理したprobeベースの調査手法が、他のツール差分調査にも転用できるアプローチ

## 前提知識

- **Claude Code Plugin** → /deep_6679 ハーネスエンジニアが知っておくべき Claude Code Plugin の落とし穴：環境変数・事前置換・sensitive の tier 別挙動
- **shell hook** (TODO: 読むべき)
- **WSL/Linux VM** (TODO: 読むべき)
- **環境変数展開** (TODO: 読むべき)
- **POSIX sh vs bash** (TODO: 読むべき)

## 関連記事

- /deep_6679 ハーネスエンジニアが知っておくべき Claude Code Plugin の落とし穴：環境変数・事前置換・sensitive の tier 別挙動
- /deep_5970 ハーネスは書いて終わりじゃなかった ── 3か月運用して動的に壊れた5つの瞬間
- /deep_94 コーディングエージェントのエンジニアリングに対する考え方
- /deep_2961 【Claude Code】セキュリティに配慮した調査エージェントの作成
- /deep_4228 superpowersを解析して学ぶClaude Codeプラグイン設計

## 原文リンク

[Coworkで壊れるClaude Code Pluginの7つの落とし穴：ホストとVM二段構成が生む構造的差分](https://zenn.dev/storehero/articles/2bc58c12090f72)
