"""telegram_receiver.py に last_processed.json フォールバックを追加"""
import sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

path = r'C:\Users\nyham\Downloads\kb-system\kb-system\bot\telegram_receiver.py'
with open(path, 'r', encoding='utf-8') as f:
    content = f.read()

changes = 0

# PATCH1: LAST_PROCESSED_FILE 定数を追加（KB_ROOT 定義の直後）
old1 = 'KB_ROOT = Path(os.getenv("KB_ROOT", str(Path(__file__).parent.parent)))\nINBOX_FILE'
new1 = ('KB_ROOT = Path(os.getenv("KB_ROOT", str(Path(__file__).parent.parent)))\n'
        'LAST_PROCESSED_FILE = KB_ROOT / "logs" / "last_processed.json"\n'
        'INBOX_FILE')
if 'LAST_PROCESSED_FILE' in content:
    print('PATCH1 skip (already exists)')
elif old1 in content:
    content = content.replace(old1, new1)
    print('PATCH1 OK')
    changes += 1
else:
    print('PATCH1 NOT FOUND')

# PATCH2: load_last_processed_to_cache() 関数を追加（deep_n_command の直前）
old2 = 'async def deep_n_command('
new2 = '''def load_last_processed_to_cache() -> None:
    """last_processed.json からキャッシュを復元する（/deep_N フォールバック用）"""
    global recent_articles_cache
    if not LAST_PROCESSED_FILE.exists():
        return
    try:
        import json as _json
        data = _json.loads(LAST_PROCESSED_FILE.read_text(encoding="utf-8"))
        recent_articles_cache.clear()
        for i, item in enumerate(data, 1):
            p = Path(item["path"])
            if not p.exists():
                continue
            text = p.read_text(encoding="utf-8")
            meta = {}
            body = text
            if text.startswith("---"):
                end = text.find("---", 3)
                if end > 0:
                    for line in text[3:end].strip().split("\\n"):
                        if ":" in line:
                            k, v = line.split(":", 1)
                            meta[k.strip()] = v.strip().strip('"').strip("'")
                    body = text[end + 3:].strip()
            recent_articles_cache[i] = {
                "title": item.get("title", meta.get("title", p.stem)),
                "category": item.get("category", p.parent.name),
                "tags": meta.get("tags", ""),
                "url": item.get("url", meta.get("url", "")),
                "body": body,
                "path": str(p),
            }
        logger.info(f"last_processed.json から {len(recent_articles_cache)} 件をキャッシュに復元")
    except Exception as e:
        logger.warning(f"last_processed.json 読み込み失敗: {e}")


async def deep_n_command('''

if 'load_last_processed_to_cache' in content:
    print('PATCH2 skip (already exists)')
elif old2 in content:
    content = content.replace(old2, new2)
    print('PATCH2 OK')
    changes += 1
else:
    print('PATCH2 NOT FOUND')

# PATCH3: deep_command でキャッシュミス時にフォールバック
old3 = '''    article = recent_articles_cache.get(num)
    if not article:
        await update.message.reply_text(
            "その番号の記事がありません。先に /recent か /search を実行してください。"
        )
        return'''
new3 = '''    article = recent_articles_cache.get(num)
    if not article:
        # last_processed.json からフォールバック読み込み
        load_last_processed_to_cache()
        article = recent_articles_cache.get(num)
    if not article:
        await update.message.reply_text(
            "その番号の記事がありません。先に /recent か /search を実行してください。"
        )
        return'''
if 'load_last_processed_to_cache()' in content and 'フォールバック読み込み' in content:
    print('PATCH3 skip (already exists)')
elif old3 in content:
    content = content.replace(old3, new3)
    print('PATCH3 OK')
    changes += 1
else:
    print('PATCH3 NOT FOUND - checking...')
    idx = content.find('recent_articles_cache.get(num)')
    print(repr(content[idx-10:idx+300]))

if changes > 0:
    with open(path, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f'File written ({changes} patches applied)')
else:
    print('No changes made')
