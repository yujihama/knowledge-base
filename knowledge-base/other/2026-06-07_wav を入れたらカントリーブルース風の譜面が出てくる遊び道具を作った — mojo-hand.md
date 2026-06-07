---
title: "wav を入れたらカントリーブルース風の譜面が出てくる遊び道具を作った — mojo-hand"
url: "https://zenn.dev/logicia32/articles/2026-06-06-mojo-hand-blues-tab"
date: 2026-06-07
tags: [LilyPond, librosa, Travis picking, ブルーススケール, 動的計画法, OpenRouter, pyfluidsynth, 音楽生成]
category: "other"
related: [1641, 7411, 7336, 4670, 349]
memo: "[Zenn LLM] wav を入れたらカントリーブルース風の譜面が出てくる遊び道具を作った — mojo-hand"
processed_at: "2026-06-07T09:08:40.930030"
---

## 要約

mojo-hand は、wav ファイルを入力としてカントリーブルース風の Travis picking 譜面（PDF）とギター音色の wav を出力するコマンドラインツール。パイプラインは「採譜 → Travis picking 化 → ブルース化 → 量子化 → 楽譜・音源生成」の5段構成で、オプションで LLM polish を追加できる。

採譜には librosa の pyin（単声ピッチトラッキング）を使用。当初 Spotify の basic-pitch（多声採譜）を採用予定だったが、TensorFlow が Python 3.12 で要求バージョン（< 2.15.1）を満たせず断念。Travis picking 化では親指でベース（E/A/D弦）、他の指でメロディ（G/B/e弦）を分担させ、numpy で alt bass パターンを生成する。ブルース化は --bluesness パラメータ（0〜100）で強度を連続調整でき、40以上でブルーススケール（1 ♭3 4 ♭5 5 ♭7）へのスナップ、60以上で swing 化（triplet feel）、80以上で12-bar I-IV-V 進行への寄せ、100で全効果が重なる。運指決定は動的計画法（Viterbi アルゴリズム）で fret 移動コストを最小化し、同時刻の fret 差が5を超えた場合はポストプロセスで弦を置き直す。楽譜は LilyPond ソースを自前生成して PDF 化し、音源は pyfluidsynth + FluidR3 SoundFont で MIDI → wav 変換する。

LLM の役割分担が設計の核心。中間ファイル events.json（小節情報・bpm等）を LLM に渡し、「phrase_breaks_beats」「swing_ratio」「key」「time_signature」の4項目のみを構造化 JSON で返させる。音符そのものは LLM に触らせない。LLM が壊れた JSON を返した場合や API キー未設定の場合は空 dict にフォールバックして algorithmic only モードで完結する。OpenRouter 経由で小さめのモデルを利用し、1曲あたりのコストは数千分の1ドル程度。

開発中のハマりどころとして、LilyPond の \relative モードと絶対ピッチ生成のミスマッチで音符が数オクターブ上に飛ぶ問題（absolute mode 切替で解決）、量子化なしでは32分音符だらけになる問題（8分音符グリッドへのスナップ追加で改善）、bass と melody の DP が独立していたため物理的に届かない運指が発生した問題（fret span 5超えでの弦置き直し処理で対応）などがあった。現時点の制限として、採譜は単声のみ、拍子は4/4固定、キー検出は頻度ヒューリスティック。パブリックドメインの童謡3曲（ふるさと・さくらさくら・蛍の光）を同梱している。

## アイデア

- アルゴリズム（DP）と LLM の役割を明確に分離し、LLM は音符ではなく「キー・フレーズ区切り・swing比」といった音楽的メタ判断のみを担当させる設計は、LLM の出力を構造化 JSON に限定してフォールバックを保証する堅牢なアーキテクチャパターンとして応用範囲が広い
- --bluesness 0〜100 という連続パラメータで音楽スタイルの変換強度を段階的に制御する発想は、生成AIの出力トーンや専門性レベルの調整インタフェース設計に転用できる
- bass と melody で独立した Viterbi アルゴリズムを走らせた後、物理制約（指の届く範囲）をポストプロセスで補正するアプローチは、マルチエージェントの出力を後段で整合性チェックする設計に類似しており、監査エージェントの判断整合性検証にも参考になる

## 前提知識

- **librosa / pyin** (TODO: 読むべき)
- **LilyPond** (TODO: 読むべき)
- **Viterbi アルゴリズム** (TODO: 読むべき)
- **Travis picking** (TODO: 読むべき)
- **12-bar ブルース進行** (TODO: 読むべき)

## 関連記事

- /deep_1641 限界社会人のための Codex 節約活用術：OpenRouterで無料モデルをサブエージェントに使う
- /deep_7411 中国のAIモデルを実用目線で整理する（2026年6月）
- /deep_7336 【実録】同じ指示を2回出した日、AIがGCPを7万円分焼き尽くした話（OpenClaw転換劇 Vol.2）
- /deep_4670 SymphonyGen: 制御可能なハーモニースケルトンによる3D階層型オーケストラ生成
- /deep_349 Pythonでノイズ除去あり・なしを比較する ― 音声分類の精度はどう変わるか

## 原文リンク

[wav を入れたらカントリーブルース風の譜面が出てくる遊び道具を作った — mojo-hand](https://zenn.dev/logicia32/articles/2026-06-06-mojo-hand-blues-tab)
