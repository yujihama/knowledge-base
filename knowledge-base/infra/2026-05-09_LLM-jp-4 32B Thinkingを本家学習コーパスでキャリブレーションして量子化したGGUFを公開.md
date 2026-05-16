---
title: "LLM-jp-4 32B Thinkingを本家学習コーパスでキャリブレーションして量子化したGGUFを公開"
url: "https://zenn.dev/suzumura_lab/articles/0a1bdb04ec87ca"
date: 2026-05-09
tags: [GGUF, 量子化, imatrix, llama.cpp, LLM-jp, MoE, Q4_K_M, llm-jp-corpus-v4, ローカルLLM, 思考連鎖]
category: "infra"
related: [3653, 3909, 4331, 2862, 4332]
memo: "[Zenn LLM] LLM-jp-4 32B Thinking を本家学習コーパスでキャリブレーションして量子化したGGUFを公開しました"
processed_at: "2026-05-09T12:48:19.014126"
---

## 要約

東京大学鈴村研究室のインフラエンジニアが、LLM-jpプロジェクトの llm-jp-4-32b-a3b-thinking（総32B・アクティブ3BのMoE構成、思考連鎖出力対応）をQ4_K_Mに量子化したGGUFをHugging Faceで公開した。最大の特徴は、imatrix（importance matrix）のキャリブレーションに、当該モデル自身の事前学習コーパスである llm-jp-corpus-v4 を直接使用している点である。imatrixは「学習分布に近いテキストを通すほど重要度を正確に反映する」性質があり、汎用Webコーパスや英語Wikipediaではなく訓練同源コーパスを使うことで、低ビット量子化後でも日本語性能（特に学術ドメイン）が劣化しにくい量子化を実現した。採用したコーパスミックスは ja_wiki（25%）・ja_cc（30%）・ja_kaken（科研費抄録、15%）・en_wiki（15%）・code_stack（15%）の5種で、研究者ユースケースを意識して学術日本語コーパス（ja_kaken）を15%含めている点が工夫点。公開リポジトリには Q4_K_M GGUF本体のほか、imatrix.dat・corpus_subsets.yaml・fetch_corpus.py・build_calibration.py を同梱しており、リポジトリをgit cloneするだけで同一キャリブレーションテキストを手元で再生成可能な設計になっている。使い方は3段階に整理されている：①huggingface-cliでQ4_K_M GGUFをダウンロードし llama-server でOpenAI互換サーバを起動（--jinjaフラグ必須。これがないと思考連鎖の reasoning_content 分離が機能しない）、②fetch_corpus.py + build_calibration.py でキャリブレーションテキストを自前生成、③同梱の imatrix.dat とf16シャード（3分割、合計約60GB）を llama-quantize --imatrix に渡してQ5_K_MやQ3_K_M等別ビット幅へ再量子化（マージ不要）。量子化時は --output-tensor-type Q8_0 オプションで出力射影層をQ8_0固定することで、思考連鎖系モデルの長文プロンプト下でのargmax安定性を確保している。llama.cppはbrew install一発で導入可能でありMac/Docker/CUDA各環境に対応。監査エージェント開発への示唆として、コーパスとモデルが両方公開されているオープンソースLLMでは、訓練分布と同源データでimatrixを作ることで、量子化コストを抑えつつドメイン特化性能を維持できる。内部監査・GRCドメイン向けに類似のアプローチ（監査報告書・基準文書でimatrixをキャリブレーション）を取れば、ローカルLLMの実用精度を高める可能性がある。

## アイデア

- 訓練分布と同源のコーパスでimatrixをキャリブレーションする手法は、汎用コーパス使用時より低ビット量子化での性能劣化を抑えられる可能性があり、ドメイン特化モデルの量子化戦略として応用できる
- 科研費抄録（ja_kaken）を15%含めた学術ドメイン寄りのコーパスミックスにより、研究・専門職ユースケース向けの日本語精度を優先した量子化設計が可能なことを実証している
- f16シャードとimatrix.datを公開することで、ユーザーがllama-quantizeを1回叩くだけで任意ビット幅への再量子化が完結する再利用可能なパイプライン設計が、ローカルLLM配布の新しいベストプラクティスになりうる

## 前提知識

- **GGUF / llama.cpp** (TODO: 読むべき)
- **imatrix（importance matrix）** (TODO: 読むべき)
- **量子化（Q4_K_M / K-quant）** (TODO: 読むべき)
- **MoE（Mixture of Experts）** (TODO: 読むべき)
- **思考連鎖（Chain-of-Thought）** (TODO: 読むべき)

## 関連記事

- /deep_3653 システムダイナミクスAIアシスタントのベンチマーク：クラウドLLM対ローカルLLMによるCLD抽出・議論タスク評価
- /deep_3909 llama.cppの設定で8GBの性能が5倍変わる — 主要オプションの最適値を出した
- /deep_4331 RTX 4060 8GB でどこまで動く？ Qwen3 サイズ別 VRAM 境界線を探る
- /deep_2862 Qwen3-235B-A22B を OpenCode と Ollama でローカル運用する超初心者向けガイド
- /deep_4332 ローカルLLM 6モデルサイズ別比較：gemma3 / qwen3 / gpt-oss をOllamaで実測

## 原文リンク

[LLM-jp-4 32B Thinkingを本家学習コーパスでキャリブレーションして量子化したGGUFを公開](https://zenn.dev/suzumura_lab/articles/0a1bdb04ec87ca)
