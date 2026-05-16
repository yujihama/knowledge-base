---
title: "64GB RAM & Podman と格闘しながら専用 ChatGPT を立てた話"
url: "https://zenn.dev/yuito2742/articles/ece5a866d7c161"
date: 2026-05-05
tags: [Ollama, Open WebUI, Podman, Caddy, CPU推論, MoE, Qwen3.6, GLM-4.7-Flash, AlmaLinux, systemd, iptables, 量子化, Q4_K_M, セルフホスト]
category: "infra"
related: [1116, 3642, 2691, 2558, 125]
memo: "[Zenn LLM] 64GB の RAM & Podman と格闘しながら専用 ChatGPT を立てた話"
processed_at: "2026-05-05T12:26:09.227889"
---

## 要約

i9-13900 + 64GB RAM のCPU専用マシン上に、Ollama + Open WebUI + Caddy を組み合わせたセルフホスト LLM サーバを構築した実践記録。OS は AlmaLinux 10.1、コンテナランタイムは rootful Podman 5.6.0、リバースプロキシは Caddy 2.11.2。常駐モデルは Qwen3.6 35B-A3B (Q4_K_M, 約24GB) と GLM-4.7-Flash (Q4_K_M, 約18GB) の2本立てで、KV cache (Q8量子化 + Flash Attention) 込みで合計約54〜56GBに収まる設計。CPU推論での選定基準は「アクティブパラメータが小さいMoEモデル」で、Qwen3.6はアクティブ3B、GLM-4.7-Flashも実効3Bとなる。Ollamaのsystemd overrideでOLLAMA_MAX_LOADED_MODELS=2、OLLAMA_KEEP_ALIVE=24h、OLLAMA_FLASH_ATTENTION=1、OLLAMA_KV_CACHE_TYPE=q8_0を設定し、2モデル同時常駐と低メモリ消費を両立。Open WebUIはrootful Podman + network_mode: hostで動かし、bridge絡みのネットワーク問題を回避してOllamaへ127.0.0.1:11434で直接アクセス。systemdラッパーでollama.serviceへの依存関係を定義し自動起動を実現。セキュリティ面ではfirewalldをiptablesに置き換え、Ollama APIポート(11434)を外部からDROPしLAN(192.168.0.0/16)経由のみSUBNETチェインで許可。Caddyはホストで直接動かし、tls internalで自己署名証明書を自動発行してHTTPS化。ハマりポイントとして、OllamaがUser=rootで起動しモデルが/root/.ollamaに保存される問題、rootless Podmanのuid/gidマッピングによるボリューム権限エラー、コンテナからollamaへのhostアドレス解決の違い（rootlessはhost.containers.internalでDockerとは異なる）、iptables反映時のSSH切断リスクへの対応（5分後ロールバック保険）、GLMのrepeat_penalty=1.0固定（1.1以上で出力破綻）とQwenのpresence_penalty=1.5（thinking mode繰り返し防止）など実運用上の細かな設定の落とし穴が詳述されている。推論速度はi9-13900 + Q4_K_Mで10〜15 t/sが目安。監査エージェント開発への示唆として、GPU調達前のプロトタイピング環境としてMoE量子化モデル + CPU推論の組み合わせは現実的な選択肢であり、LangGraphやPydanticベースのエージェント処理をローカルLLMでテストする際の構成参考になる。

## アイデア

- CPUのみで30B級MoEモデルを2本同時常駐させるメモリ設計：アクティブパラメータ3BのMoEモデル × Q4_K_M量子化 + KV cacheのQ8量子化を組み合わせることで、64GB RAMに収める計算が成立する点
- rootful Podman + network_mode: hostによるネットワーク単純化：rootless特有のuid/gidマッピング問題とbridge経由のDNS解決の複雑さを一括回避する実用的判断
- iptables反映時の5分後自動ロールバック保険：SSHが切断された場合の詰み防止として、sleep 300 && iptables-restore をバックグラウンドで走らせておき、確認後にkillするパターン

## 前提知識

- **Ollama** → /deep_52 SyGra Studio 紹介：合成データ生成のビジュアル・インタラクティブ環境
- **Podman** → /deep_2820 PodmanのコンテナLinuxでNVIDIA GPU(Geforce RTX)を使ったローカルLLM環境を構築してみた
- **MoEモデル** (TODO: 読むべき)
- **量子化 (GGUF/Q4_K_M)** (TODO: 読むべき)
- **systemd** (TODO: 読むべき)

## 関連記事

- /deep_1116 🤗 Optimum IntelとfastRAGによるCPU最適化エンベディング
- /deep_3642 未経験者がVRAM 16GBでAIキャラの台本生成を動かすまで（第1回）── VRAM不足という当たり前の壁
- /deep_2691 カンニング用AIをアップグレードしようとしたら、RAGの限界にぶつかった話
- /deep_2558 オンデバイスストリーミングASRの限界に挑む：低レイテンシ推論向け高精度コンパクト英語モデル
- /deep_125 SliderQuant: LLM向け高精度ポストトレーニング量子化フレームワーク

## 原文リンク

[64GB RAM & Podman と格闘しながら専用 ChatGPT を立てた話](https://zenn.dev/yuito2742/articles/ece5a866d7c161)
