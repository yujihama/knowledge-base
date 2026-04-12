# KB-System 移動手順書
# Downloads → C:\Users\nyham\work\KB_bot

## ※ 設定ファイルの更新は済んでいます（.env, パッチスクリプト）

---

## Step 1: Bot を停止する

タスクマネージャーまたはコマンドプロンプトで、実行中の Telegram Bot を停止してください。

```powershell
taskkill /f /im python.exe
```

（他の Python プロセスが動いていない場合のみ。動いている場合は Bot のウィンドウを Ctrl+C で閉じてください）

---

## Step 2: フォルダを移動する

PowerShell で以下を実行：

```powershell
# venv は移動しても壊れるので除外してコピー
robocopy "C:\Users\nyham\Downloads\kb-system\kb-system" "C:\Users\nyham\work\KB_bot" /E /XD venv __pycache__

# コピー完了を確認
dir "C:\Users\nyham\work\KB_bot"
```

中身が正しくコピーされたことを確認してから、旧フォルダを削除：

```powershell
# 確認後に削除（心配なら後回しでOK）
# rmdir /s /q "C:\Users\nyham\Downloads\kb-system"
```

---

## Step 3: venv を再構築する

```powershell
cd C:\Users\nyham\work\KB_bot
python -m venv venv
.\venv\Scripts\activate
pip install -r bot\requirements.txt
```

---

## Step 4: 動作確認（Bot を手動起動）

```powershell
cd C:\Users\nyham\work\KB_bot
.\venv\Scripts\activate
python bot\telegram_receiver.py
```

Telegram から `/status` を送って応答があれば成功。Ctrl+C で終了。

---

## Step 5: タスクスケジューラを再登録する

**管理者権限**でコマンドプロンプトを開き：

```powershell
cd C:\Users\nyham\work\KB_bot\scripts

# メインのスケジューラ（Bot自動起動 + inbox処理 + 朝ダイジェスト + 週次ダイジェスト）
setup_scheduler_v2.bat

# RSS フェッチャー
setup_rss_scheduler.bat
```

---

## Step 6: 旧タスクスケジューラのエントリを確認

上記の bat ファイルは `/f` オプションで上書き登録するので、
旧パスのエントリは自動的に新しいパスで置き換わります。追加作業は不要です。

---

## 完了チェックリスト

- [ ] Bot が新しい場所から起動できる（Step 4）
- [ ] /status で KB の記事数が正しく表示される
- [ ] タスクスケジューラに KB-System タスクが登録されている
- [ ] 旧 Downloads フォルダを削除（任意、しばらく残しておいてもOK）
