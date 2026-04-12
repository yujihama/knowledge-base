# KB-System: スマホ → GALLERIA ナレッジベース自動蓄積システム

スマホで見つけた気になるサイトを Telegram Bot 経由で GALLERIA に送り、
Claude Code が自動で要約・分類・タグ付けしてナレッジベースに蓄積するシステム。

## システム構成

```
スマホ (Telegram)
    ↓ URLを送信
GALLERIA (Windows, 常時起動)
    ├── Telegram Bot (常駐) → inbox.jsonl に蓄積
    ├── Task Scheduler (定期実行)
    │   ├── process_inbox.py (毎日 9:00/21:00)
    │   │   └── Claude Code で要約・分類・タグ付け
    │   └── generate_digest.py (毎週月曜 8:00)
    │       └── 週次ダイジェストレポート生成
    └── knowledge-base/
        ├── ai-ml/        # AI/ML研究
        ├── audit-ai/     # 監査AI
        ├── agent-arch/   # エージェントアーキテクチャ
        ├── infra/        # インフラ
        └── weekly-digest/ # 週次レポート
```

## セットアップ手順

### Step 1: Telegram Bot を作成する

1. スマホで Telegram を開く（未インストールなら https://telegram.org/ から）
2. Telegram 内で `@BotFather` を検索してチャットを開く
3. `/newbot` と送信
4. Bot の名前を入力（例: `Yuji KB Bot`）
5. Bot のユーザー名を入力（例: `yuji_kb_bot` ※末尾は `bot` で終わること）
6. 表示される **Bot Token** をメモする（例: `7123456789:AAH...`）
7. 自分の User ID を確認するため `@userinfobot` にメッセージを送る → 表示される数字をメモ

### Step 2: GALLERIA に Python 環境を準備

```powershell
# Python がなければインストール (https://www.python.org/downloads/)
python --version  # 3.10以上を確認

# プロジェクトフォルダに移動
cd C:\Users\<ユーザー名>\kb-system

# 仮想環境を作成（推奨）
python -m venv venv
.\venv\Scripts\activate

# 依存パッケージをインストール
pip install -r bot\requirements.txt
```

### Step 3: 環境変数を設定

```powershell
# .env ファイルを作成
copy bot\.env.example bot\.env
```

`bot\.env` をテキストエディタで開き、以下を記入:

```
TELEGRAM_BOT_TOKEN=7123456789:AAH...  ← Step1で取得したトークン
ALLOWED_USER_IDS=123456789            ← Step1で確認した自分のUser ID
KB_ROOT=C:\Users\<ユーザー名>\kb-system\knowledge-base
```

### Step 4: Bot の動作確認

```powershell
cd C:\Users\<ユーザー名>\kb-system
.\venv\Scripts\activate
python bot\telegram_receiver.py
```

スマホの Telegram で自分の Bot にメッセージを送ってみる:
- `/start` → 使い方が表示される
- `https://example.com テスト` → URL が保存される
- `/status` → inbox の状態が表示される

動作確認できたら `Ctrl+C` で終了。

### Step 5: Claude Code をインストール

```powershell
# Node.js がなければ https://nodejs.org/ からインストール
npm install -g @anthropic-ai/claude-code

# 認証
claude auth login

# 動作確認
claude -p "Hello, respond with OK" --output-format text
```

### Step 6: 処理スクリプトの動作確認

```powershell
# Step 4 で保存したURLを処理してみる
python scripts\process_inbox.py
```

`knowledge-base/` 配下にカテゴリ別の Markdown ファイルが生成されれば成功。

### Step 7: タスクスケジューラに登録

**管理者として** コマンドプロンプトを開き:

```powershell
scripts\setup_scheduler.bat
```

これで以下が自動登録される:
- **Telegram Bot**: ログオン時に自動起動
- **inbox処理**: 毎日 9:00 と 21:00 に実行
- **週次ダイジェスト**: 毎週月曜 8:00 に実行

## 使い方

### URLを保存する

スマホのブラウザで気になるページを見つけたら:
1. 共有ボタンをタップ
2. Telegram を選択
3. 自分の Bot を選んで送信
4. メモを添えたい場合は URL の後にテキストを追加

### ナレッジベースを検索する

Telegram Bot に:
```
/search GRPO
/search 監査エージェント
/recent
/status
```

### 蓄積されたファイルを見る

`knowledge-base/` フォルダを直接開いて Markdown ファイルを閲覧。
VS Code や Obsidian で開くとタグやリンクが活用しやすい。

## ファイル構成

```
kb-system/
├── bot/
│   ├── telegram_receiver.py   # Telegram Bot (常駐)
│   ├── requirements.txt       # Python依存パッケージ
│   ├── .env.example           # 環境変数テンプレート
│   └── .env                   # 環境変数 (自分で作成)
├── scripts/
│   ├── process_inbox.py       # inbox処理 (定期実行)
│   ├── generate_digest.py     # 週次ダイジェスト生成
│   ├── start_bot.bat          # Bot起動バッチ
│   └── setup_scheduler.bat    # タスクスケジューラ登録
├── knowledge-base/
│   ├── CLAUDE.md              # Claude Code用コンテキスト
│   ├── inbox/                 # 未処理URL
│   ├── ai-ml/                 # AI/ML研究
│   ├── audit-ai/              # 監査AI
│   ├── agent-arch/            # エージェントアーキテクチャ
│   ├── infra/                 # インフラ
│   ├── other/                 # その他
│   ├── weekly-digest/         # 週次レポート
│   └── index/                 # ベクトルインデックス (将来)
├── logs/                      # ログファイル
└── README.md                  # このファイル
```

## 今後の拡張

- **ベクトル検索**: RTX 3090 導入後、Ollama + embedding モデルで自然言語検索
- **RSS自動取得**: arXiv, Hugging Face Daily Papers 等を自動収集
- **Claude Code Schedule**: `claude-code-scheduler` プラグインでの管理
- **Obsidian連携**: knowledge-base フォルダを Obsidian Vault として開く
