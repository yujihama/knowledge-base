"""process_inbox.py の通知ブロックを更新するパッチスクリプト"""
import re, sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

path = r'C:\Users\nyham\Downloads\kb-system\kb-system\scripts\process_inbox.py'
with open(path, 'r', encoding='utf-8') as f:
    content = f.read()

changes = 0

# PATCH1: saved_titles: list[str] = [] -> saved_articles: list[dict] = []
if 'saved_titles: list[str] = []' in content:
    content = content.replace('saved_titles: list[str] = []', 'saved_articles: list[dict] = []')
    print('PATCH1 OK')
    changes += 1
else:
    print('PATCH1 skip')

# PATCH2: saved_titles.append(memo[:60]) -> saved_articles.append(result)
old2 = '''                success_count += 1
                # 通知用にタイトルを記録（memoからフィード名とタイトルを取得）
                memo = entry.get("memo", "") or entry.get("url", "")
                saved_titles.append(memo[:60])'''
new2 = '''                success_count += 1
                saved_articles.append(result)'''
if old2 in content:
    content = content.replace(old2, new2)
    print('PATCH2 OK')
    changes += 1
else:
    print('PATCH2 skip')

# PATCH3: 通知末尾ブロック全体を置換
old3 = '''    logger.info(f"=== 処理完了: {success_count}/{len(to_process)}件成功 ===")

    # Telegram通知（処理件数が1件以上の場合のみ）
    if success_count > 0:
        remaining = len(unprocessed) - len(to_process)
        msg = f"✅ inbox処理完了 {success_count}/{len(to_process)}件"
        if remaining > 0:
            msg += f"（残り{remaining}件）"
        msg += "\\n"
        for title in saved_titles:
            msg += f"\\n・{title}"
        send_telegram_notification(msg)'''

new3 = '''    logger.info(f"=== 処理完了: {success_count}/{len(to_process)}件成功 ===")

    # last_processed.json に書き出し（/deep_N ボットコマンド用）
    if saved_articles:
        try:
            LAST_PROCESSED_FILE.write_text(
                json.dumps(saved_articles, ensure_ascii=False, indent=2),
                encoding="utf-8"
            )
            logger.info(f"last_processed.json 更新: {len(saved_articles)}件")
        except Exception as e:
            logger.warning(f"last_processed.json 書き込み失敗: {e}")

    # Telegram通知（処理件数が1件以上の場合のみ）
    if success_count > 0:
        remaining = len(unprocessed) - len(to_process)
        msg = f"✅ inbox処理完了 {success_count}/{len(to_process)}件"
        if remaining > 0:
            msg += f"（残り{remaining}件）"
        msg += "\\n"
        for i, article in enumerate(saved_articles, 1):
            title = article["title"][:45]
            msg += f"\\n・{title} /deep_{i}"
        send_telegram_notification(msg)'''

if old3 in content:
    content = content.replace(old3, new3)
    print('PATCH3 OK')
    changes += 1
else:
    print('PATCH3 NOT FOUND')
    # デバッグ: 部分一致確認
    idx = content.find('Telegram通知（処理件数')
    if idx >= 0:
        print('Partial match at:', idx)
        print(repr(content[idx-50:idx+300]))

if changes > 0:
    with open(path, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f'File written ({changes} patches applied)')
else:
    print('No changes made')
