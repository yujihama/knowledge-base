---
title: "オンデバイスVLM（画像入力LLM）のレシピ：VLMKitによるiOS実装"
url: "https://zenn.dev/mlboydaisuke/articles/vlmkit-on-device-recipes"
date: 2026-06-06
tags: [VLM, オンデバイスAI, iOS, Swift, Qwen3-VL, SmolVLM2, ARKit, LiDAR, CoreML, ハルシネーション対策, プライバシー保護AI]
category: "infra"
related: [1928, 7303, 2421, 1257, 424]
memo: "[Zenn LLM] オンデバイスVLM (画像入力LLM) のレシピ"
processed_at: "2026-06-06T21:18:02.216973"
---

## 要約

VLMKit は、iPhone/iPad 上でオンデバイス動作する Vision Language Model（VLM）をSwiftから数行で利用できるオープンソースライブラリ（MIT ライセンス）。モデルは Hugging Face から初回起動時にダウンロードされ、Qwen3-VL-4B（約3GB、精度とサイズのバランス）、Qwen3-VL-8B（約6GB、16GB iPad/M系Mac向け）、SmolVLM2-500M（約1GB、8GB iPhone向け軽量モデル）の3種から選択できる。

VLM は画像の自由記述説明には強い一方、オブジェクトの正確な個数カウント（3個程度まで）や画像内の正確な位置返答が苦手という制約がある。VLMKit はこの弱点を Apple 純正フレームワークと組み合わせることで補完する設計を採用している。具体的には Vision（顔検出・OCR・物体検出）、ARKit（空間リアルタイム認識）、LiDAR（iPhone Pro搭載、距離の実測）、CoreML（オンデバイスAI推論）との連携により、VLM 単体では不可能なユースケースを実現する。

提供されるレシピは以下の通り。①書類QA：機械銘板・領収書・契約書等から「ラベル: 値」形式のデータを全抽出し、自由文質問に対して答えと逐語的根拠文をセットで返す（ハルシネーション対策）。②物体ハイライト：画像キャプション生成と同時に、「黒い犬」「赤いボール」等の各物体が写真のどの領域に存在するかをハイライト表示。③群衆個別説明：Apple Vision で全人物を検出→一人ずつ切り出してVLMに個別質問するパイプライン。④レシートCSV変換：Excel/Numbers に直接貼れる形式で出力。⑤名刺→連絡先保存：項目ごとの構造化抽出でiOS連絡先アプリに直接登録。⑥3D物体計測：ARKit＋LiDAR で幅・高さ・奥行き・体積を実寸計測し、VLMの説明を3次元空間に重畳表示。

オンデバイス化の主な動機はデータプライバシー。顧客契約書をOpenAIに送信できない、患者の薬写真をGoogleに送れない、経費レシートを社外サーバーにアップできないといった業務上の制約を、「データもAIもスマホ内で完結」することで解決する。監査・内部統制の観点では、証憑（領収書・契約書・銘板）のオフライン構造化抽出パイプラインとして直接転用可能であり、根拠文の逐語引用機能はエビデンス管理の証跡性確保にも有効。Swift Package Manager で1行追加するだけで導入でき、Mac CLI でも `swift run vlmkit-cli docqa plate.jpg --ask "型番は?"` の形で実機なしに試せる。

## アイデア

- VLMの弱点（カウント・位置特定）をApple純正フレームワーク（Vision/ARKit/LiDAR）で補完するハイブリッドアーキテクチャは、監査エージェントにおける証憑解析パイプラインの設計パターンとして応用可能
- 回答に逐語的根拠文を必須とするRAG的アプローチにより、ハルシネーションを構造的に抑制している点は、LLM-as-judgeや監査エビデンス管理への転用価値が高い
- SmolVLM2-500Mの約1GBという軽量モデルが8GB iPhoneで動作する事実は、エッジデバイスでの推論コスト最適化（モデル選択基準）を実務的に示している

## 前提知識

- **Vision Language Model (VLM)** (TODO: 読むべき)
- **CoreML** → /deep_7303 YoloV5をCoreMLに変換し、デコードレイヤーとNMSを追加してiOSで使う方法
- **ARKit/LiDAR** (TODO: 読むべき)
- **Qwen3-VL** → /deep_2732 長期マルチモーダル深層検索エージェント：LMM-Searcherの提案
- **ハルシネーション** → /deep_28 IBMとUC BerkeleyがIT-BenchとMASTを使ってエンタープライズエージェントの失敗原因を診断

## 関連記事

- /deep_1928 隠れた真実を見抜く：フィールド可視化から記号的解析解を推論するVisual-to-Symbolic AI
- /deep_7303 YoloV5をCoreMLに変換し、デコードレイヤーとNMSを追加してiOSで使う方法
- /deep_2421 Sentence Transformersによるマルチモーダル埋め込み・リランカーモデルのトレーニングとファインチューニング
- /deep_1257 Saliency-R1: 顕著性マップ整合報酬によるVLMの解釈可能性と忠実性の強化
- /deep_424 Intel CPU上でVLMを3ステップで動かす方法（OpenVINO + SmolVLM2）

## 原文リンク

[オンデバイスVLM（画像入力LLM）のレシピ：VLMKitによるiOS実装](https://zenn.dev/mlboydaisuke/articles/vlmkit-on-device-recipes)
