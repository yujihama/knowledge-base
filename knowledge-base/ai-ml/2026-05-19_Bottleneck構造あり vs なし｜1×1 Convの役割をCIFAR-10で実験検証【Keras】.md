---
title: "Bottleneck構造あり vs なし｜1×1 Convの役割をCIFAR-10で実験検証【Keras】"
url: "https://zenn.dev/wasurenamemo/articles/63b6e37224b715"
date: 2026-05-19
tags: [CNN, Bottleneck, ResNet, 1x1Conv, Keras, CIFAR-10, BasicBlock, パラメータ効率]
category: "ai-ml"
related: [4049, 2656, 5652, 5039, 3911]
memo: "[Zenn 機械学習] Bottleneck構造あり vs なし｜1×1 Convの役割をCIFAR-10で実験検証【Keras】"
processed_at: "2026-05-19T21:02:15.711456"
---

## 要約

ResNet50などの深いCNNで採用されるBottleneck Block（1×1 Conv → 3×3 Conv → 1×1 Conv）とBasicBlock（3×3 Conv → 3×3 Conv）をKeras + CIFAR-10で比較検証した実験記事。Bottleneckの1×1 Convはチャンネル数を1/4（64→16）に圧縮してから3×3 Convに通し、その後元のチャンネル数に復元するという役割を持つ。パラメータ数は理論上BasicBlockの約17分の1になる（チャンネル数64の場合: BasicBlock 73,728 vs Bottleneck 4,352）。実験条件はCIFAR-10、30エポック、Adam最適化、バッチサイズ64、スキップ接続なし、ブロック数2という浅い構成。結果はBasicBlock（test accuracy 77.85%、パラメータ数398,474、学習時間195.8秒）がBottleneck（67.84%、51,114、154.8秒）を約10ポイント上回った。パラメータ数はBottleneckが約1/8、学習時間は41秒短縮されたものの、精度面では大幅な劣後となった。敗因はチャンネル圧縮による情報ロスで、ブロック数が2つしかない浅い構成では圧縮が表現力の低下に直結した。Bottleneckは「少ないパラメータで深さを稼ぐ」技術であり、ResNet50（50層以上）のような深いネットワークでパラメータ爆発を防ぐために設計されている。ResNet18/34ではBasicBlockが採用されているのも同じ理由。今回の実験では、スキップ接続（Residual Connection）なしという条件であり、スキップ接続ありではBottleneckの圧縮による精度低下を補完できる可能性がある点も示唆されている。実務的な示唆として、モデル設計時にBottleneckを使う場合は50層以上の深いネットワーク前提かつスキップ接続との組み合わせが必要条件となる。

## アイデア

- Bottleneckはパラメータ削減効果（約1/8）は明確だが、浅いネットワークでは情報圧縮が精度低下に直結するというトレードオフが実験で定量化されている
- スキップ接続（Residual Connection）なしという条件設定により、ブロック構造単体の効果を純粋に分離できている点が実験設計として巧妙
- ResNet18/34がBasicBlock、ResNet50以降がBottleneckという設計選択の根拠が、深さとパラメータ効率のトレードオフとして明確に説明されている

## 前提知識

- **ResNet** → /deep_324 消費者向けUWBレーダーによる心拍数計測：転移学習アプローチ
- **CNN** → /deep_109 機械学習入門講義メモ：ゼロから作るDeep Learningをベースに
- **Residual Connection** (TODO: 読むべき)
- **Batch Normalization** → /deep_3286 ZC-Swish：エッジ・マイクロバッチ環境向けBN非依存深層ネットワークの安定化
- **1×1 Convolution** (TODO: 読むべき)

## 関連記事

- /deep_4049 Conv2Dのkernel_sizeを3×3・5×5・1×1で比較したら1×1が壊滅した話【Keras×CIFAR-10】
- /deep_2656 KerasのMaxPooling pool_sizeを変えたら予想外の結果になった話【GAP vs Flatten で挙動が逆転】
- /deep_5652 GlobalAveragePooling vs GlobalMaxPooling、シードなしで比較したら誤った結論を出しかけた話【Keras・CIFAR-10】
- /deep_5039 Data Augmentationを重ねすぎると精度が下がる？CIFAR-10で5パターンを比較実験
- /deep_3911 Conv2DのpaddingをsameとvalidにしたらGAPが差を消した話【Keras×CIFAR-10】

## 原文リンク

[Bottleneck構造あり vs なし｜1×1 Convの役割をCIFAR-10で実験検証【Keras】](https://zenn.dev/wasurenamemo/articles/63b6e37224b715)
