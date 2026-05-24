---
title: "Agent開発における「No disclaimer by design」という考え方"
url: "https://zenn.dev/mofuteq/articles/12cfb91a86b347"
date: 2026-05-24
tags: [Agent Runtime, No disclaimer by design, verdict, verification questions, State Machine, 判断境界, abstain, human review handoff, contract-question-agent]
category: "agent-arch"
related: [6273, 6124]
memo: "[Zenn LLM] Agent開発における、No disclaimer by designという考え方"
processed_at: "2026-05-24T09:05:33.318534"
---

## 要約

Agent Runtimeを開発する中で、AIの出力末尾に添付される免責文（disclaimer）の本質的な問題を考察した記事。著者は自作Agentの画面に「AIは間違うかもしれません」という注意書きがあることに気づき、それを静かに削除した経緯から、このコンセプトを提唱している。

免責文が存在する理由を分析すると、単に「AIの精度が低い」という技術的説明ではなく、人間がAIに対して設定した「判断境界」の表明であることがわかる。車や鍬などの従来ツールとは異なり、AIは「文章で理由を述べ、判断らしいものを言葉で返す」ため、人間は「この出力は判断ではない」「最終判断は人間が行う」という線引きを必要とする。つまりdisclaimerは性能の注意書きであると同時に、主体性の帰属に関する宣言でもある。

問題は、Agent Runtime設計の観点からdisclaimerを「最後に貼るだけ」では不十分な点にある。Agentが実質的にverdict（判断）を返した後に「これは助言ではありません」と付記するのは、設計の順序が逆である。本来必要なのは、runtimeレベルで境界を持つことだ。具体的には：scope外のクエリを入口で止める、evidenceが薄ければabstainする、verdict方向に進みそうな場合はrubricで制御する、human reviewが必要な場合は明示的にhandoffする、といった仕組みをworkflow側で実装することを指す。

contract-question-agentの実例では、この思想が明確に示される。契約条項を読ませる際に「この契約は締結すべきです」というverdictを返させるのではなく、「この条項の対象範囲はどこか」「片務的な義務になっていないか」「終了後も残る義務はあるか」といったverification questionsを返させる設計にする。AgentはFrames（判断材料）を返し、Verdicts（判断）は人間に委ねる。この設計であれば、末尾に大きなdisclaimerを貼る必要性が自然と減少する。

「No disclaimer by design」とはdisclaimerを一切書かないことではなく、免責文に頼らなくても境界が保たれるruntimeを設計すること。Agent RuntimeはAIの振る舞いを制御するだけでなく、「人間がどこから判断を引き受けるのか」を示すinterfaceでもある。監査AI開発においても、リスク評価や契約レビューでAgentがverdictを返すのではなく、verification questionsやevidence frameを返す設計が判断責任の所在を明確化する上で重要な示唆を持つ。

## アイデア

- disclaimerは精度の注意書きではなく「判断主体の帰属を宣言する行為」という再解釈——AIが言語で判断らしいものを返すという特性が、従来ツールにはなかった主体性の曖昧さを生む
- Frames not verdicts という設計原則——AgentにVerdict（判断）ではなくVerification questions（確認すべき問い）を返させることで、runtime側に境界を持たせdisclaimerへの依存を構造的に減らす
- Agent RuntimeはAI制御システムであると同時に「human-AI間の判断境界を定義するinterface」という視点——system→humanの線引きとhuman→AIの線引きが双方向に存在するという設計思想

## 前提知識

- **Agent Runtime** → /deep_6124 Google I/O 2026のAI発表をAIエンジニア・研究視点で読む
- **State Machine / guard** (TODO: 読むべき)
- **LLM出力制御** → /deep_4036 未経験者がVRAM 16GBでAIキャラの台本生成を動かすまで(第4回) ── 「きみ」を消したら、品質も消えた話
- **Human-in-the-loop** → /deep_24 1対1を超えて：動的な人間とAIのグループ会話のオーサリング・シミュレーション・テスト
- **Abstain / Rubric** (TODO: 読むべき)

## 関連記事

- /deep_6273 Vector DBを外したら、RAGではなくAgent Runtimeが残った
- /deep_6124 Google I/O 2026のAI発表をAIエンジニア・研究視点で読む

## 原文リンク

[Agent開発における「No disclaimer by design」という考え方](https://zenn.dev/mofuteq/articles/12cfb91a86b347)
