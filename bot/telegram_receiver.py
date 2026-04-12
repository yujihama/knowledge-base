"""
Telegram Bot - スマホからURLを受信 + ナレッジベースとの対話
GALLERIA (Windows) で常駐実行する

機能:
- URL送信 → inbox に蓄積
- 質問送信 → ナレッジベースを検索して回答
- /deep N → N番目の記事を深掘り
- /search キーワード → ナレッジベース検索
- /status → 状態確認
- /recent → 最近の記事一覧
"""

import json
import logging
import os
import re
import subprocess
import sys
import tempfile
from datetime import datetime, timedelta
from pathlib import Path

from dotenv import load_dotenv
from telegram import Update
from telegram.ext import (
    Application,
    CommandHandler,
    ContextTypes,
    MessageHandler,
    filters,
)

# ── 設定 ──────────────────────────────────────────────
load_dotenv(Path(__file__).parent / ".env")

BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN", "")
ALLOWED_USER_IDS = [
    int(uid.strip())
    for uid in os.getenv("ALLOWED_USER_IDS", "").split(",")
    if uid.strip()
]

KB_ROOT = Path(os.getenv("KB_ROOT", str(Path(__file__).parent.parent)))
INBOX_FILE = KB_ROOT / "inbox" / "inbox.jsonl"
LOG_FILE = Path(__file__).parent.parent / "logs" / "bot.log"
REGISTRY_FILE = Path(__file__).parent.parent / "logs" / "article_registry.json"

# ── ログ設定 ──────────────────────────────────────────
LOG_FILE.parent.mkdir(parents=True, exist_ok=True)
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.FileHandler(LOG_FILE, encoding="utf-8"),
        logging.StreamHandler(sys.stdout),
    ],
)
logger = logging.getLogger(__name__)

# ── ヘルパー ──────────────────────────────────────────
URL_PATTERN = re.compile(r"https?://[^\s<>\"')\]]+", re.IGNORECASE)

# ── 記事レジストリ（通し番号管理）─────────────────────
def load_registry() -> dict:
    """記事レジストリを読み込む"""
    if not REGISTRY_FILE.exists():
        return {"next_id": 1, "articles": {}}
    try:
        return json.loads(REGISTRY_FILE.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, KeyError):
        return {"next_id": 1, "articles": {}}


def save_registry(registry: dict) -> None:
    """記事レジストリを保存する"""
    REGISTRY_FILE.parent.mkdir(parents=True, exist_ok=True)
    tmp = REGISTRY_FILE.with_suffix(".tmp")
    tmp.write_text(
        json.dumps(registry, ensure_ascii=False, indent=2), encoding="utf-8"
    )
    os.replace(str(tmp), str(REGISTRY_FILE))


def init_registry_if_needed() -> None:
    """初回起動時: 既存の全記事をレジストリに登録する"""
    registry = load_registry()
    if registry["articles"]:
        logger.info(f"レジストリ既存: {len(registry['articles'])}件 (next_id={registry['next_id']})")
        return

    logger.info("レジストリ初期化: 既存記事をスキャン中...")
    for md_file in KB_ROOT.rglob("*.md"):
        if md_file.parent.name in ("inbox", "index", "weekly-digest"):
            continue
        if md_file.name == "CLAUDE.md":
            continue
        try:
            content = md_file.read_text(encoding="utf-8")
            meta = {}
            if content.startswith("---"):
                end = content.find("---", 3)
                if end > 0:
                    for line in content[3:end].strip().split("\n"):
                        if ":" in line:
                            key, val = line.split(":", 1)
                            meta[key.strip()] = val.strip().strip('"').strip("'")

            aid = registry["next_id"]
            registry["articles"][str(aid)] = {
                "title": meta.get("title", md_file.stem),
                "path": str(md_file),
                "url": meta.get("url", ""),
                "category": md_file.parent.name,
            }
            registry["next_id"] = aid + 1
        except Exception:
            continue

    save_registry(registry)
    logger.info(f"レジストリ初期化完了: {len(registry['articles'])}件登録")


def get_article_from_registry(article_id: int) -> dict | None:
    """レジストリからIDで記事を取得し、本文を読み込んで返す"""
    registry = load_registry()
    info = registry["articles"].get(str(article_id))
    if not info:
        return None

    p = Path(info["path"])
    if not p.exists():
        return None

    try:
        content = p.read_text(encoding="utf-8")
        meta = {}
        body = content
        if content.startswith("---"):
            end = content.find("---", 3)
            if end > 0:
                for line in content[3:end].strip().split("\n"):
                    if ":" in line:
                        key, val = line.split(":", 1)
                        meta[key.strip()] = val.strip().strip('"').strip("'")
                body = content[end + 3:].strip()

        return {
            "kb_id": article_id,
            "title": info.get("title", meta.get("title", p.stem)),
            "category": info.get("category", p.parent.name),
            "tags": meta.get("tags", ""),
            "url": info.get("url", meta.get("url", "")),
            "body": body,
            "path": str(p),
        }
    except Exception:
        return None


def build_path_to_id_map() -> dict[str, int]:
    """パス→レジストリID の逆引きマップを構築"""
    registry = load_registry()
    return {v["path"]: int(k) for k, v in registry["articles"].items()}


def extract_urls(text: str) -> list[str]:
    return URL_PATTERN.findall(text)


def save_to_inbox(entry: dict) -> None:
    INBOX_FILE.parent.mkdir(parents=True, exist_ok=True)
    with open(INBOX_FILE, "a", encoding="utf-8") as f:
        f.write(json.dumps(entry, ensure_ascii=False) + "\n")


def is_authorized(user_id: int) -> bool:
    if not ALLOWED_USER_IDS:
        return True
    return user_id in ALLOWED_USER_IDS


def call_claude_code(prompt: str, timeout: int = 120) -> str | None:
    """Claude Code をヘッドレスモードで呼び出し（バイナリ読み取り）"""
    tmp_in = None
    proc = None
    try:
        with tempfile.NamedTemporaryFile(
            mode="w", suffix=".txt", encoding="utf-8", delete=False
        ) as f:
            f.write(prompt)
            tmp_in = f.name

        proc = subprocess.Popen(
            f'type "{tmp_in}" | claude -p - --model claude-sonnet-4-6 --output-format text',
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            shell=True,
            cwd=str(KB_ROOT),
        )
        stdout_bytes, stderr_bytes = proc.communicate(timeout=timeout)
        output = stdout_bytes.decode("utf-8", errors="replace").strip()

        if proc.returncode == 0 and output:
            return output
        else:
            err = stderr_bytes.decode("utf-8", errors="replace").strip()
            logger.error(f"Claude Code error: {err[:200]}")
            return None
    except FileNotFoundError:
        logger.error("Claude Code not found")
        return None
    except subprocess.TimeoutExpired:
        logger.error("Claude Code timeout")
        if proc:
            proc.kill()
        return None
    except Exception as e:
        logger.error(f"Claude Code error: {e}")
        return None
    finally:
        if tmp_in:
            try:
                os.remove(tmp_in)
            except OSError:
                pass


def search_knowledge_base(query: str, max_results: int = 10) -> list[dict]:
    """ナレッジベースを検索してマッチする記事を返す"""
    results = []
    query_lower = query.lower()
    keywords = query_lower.split()

    for md_file in KB_ROOT.rglob("*.md"):
        if md_file.parent.name in ("inbox", "index"):
            continue
        if md_file.name == "CLAUDE.md":
            continue

        try:
            content = md_file.read_text(encoding="utf-8")
            content_lower = content.lower()

            # 全キーワードが含まれるかスコア計算
            score = sum(1 for kw in keywords if kw in content_lower)
            if score == 0:
                continue

            # frontmatter解析
            meta = {}
            body = content
            if content.startswith("---"):
                end = content.find("---", 3)
                if end > 0:
                    for line in content[3:end].strip().split("\n"):
                        if ":" in line:
                            key, val = line.split(":", 1)
                            meta[key.strip()] = val.strip().strip('"').strip("'")
                    body = content[end + 3:].strip()

            results.append({
                "title": meta.get("title", md_file.stem),
                "category": md_file.parent.name,
                "tags": meta.get("tags", ""),
                "url": meta.get("url", ""),
                "body": body,
                "path": str(md_file),
                "score": score,
            })
        except Exception:
            continue

    results.sort(key=lambda x: x["score"], reverse=True)
    return results[:max_results]


def get_recent_articles(days: int = 7, limit: int = 10) -> list[dict]:
    """直近N日の記事を取得"""
    cutoff = datetime.now() - timedelta(days=days)
    articles = []

    for md_file in KB_ROOT.rglob("*.md"):
        if md_file.parent.name in ("inbox", "index", "weekly-digest"):
            continue
        if md_file.name == "CLAUDE.md":
            continue

        try:
            content = md_file.read_text(encoding="utf-8")
            meta = {}
            body = content
            if content.startswith("---"):
                end = content.find("---", 3)
                if end > 0:
                    for line in content[3:end].strip().split("\n"):
                        if ":" in line:
                            key, val = line.split(":", 1)
                            meta[key.strip()] = val.strip().strip('"').strip("'")
                    body = content[end + 3:].strip()

            date_str = meta.get("date", "")
            if date_str:
                try:
                    if datetime.strptime(date_str, "%Y-%m-%d") < cutoff:
                        continue
                except ValueError:
                    pass

            articles.append({
                "title": meta.get("title", md_file.stem),
                "category": md_file.parent.name,
                "tags": meta.get("tags", ""),
                "url": meta.get("url", ""),
                "body": body,
                "path": str(md_file),
                "date": date_str,
            })
        except Exception:
            continue

    articles.sort(key=lambda x: x.get("date", ""), reverse=True)
    return articles[:limit]


# ── ハンドラー ────────────────────────────────────────
async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    msg = (
        "こんにちは！ KBナレッジBotです 📚\n\n"
        "【URLを保存】\n"
        "URLを送信 → 自動で要約・分類して蓄積\n\n"
        "【質問する】\n"
        "URLを含まないメッセージ → ナレッジベースから回答\n"
        "例: 「コンテキストリセットについて教えて」\n\n"
        "【コマンド】\n"
        "/recent - 最近の記事一覧\n"
        "/search キーワード - 記事を検索\n"
        "/deep 番号 - 記事を深掘り\n"
        "/ask 質問 - KB全体に質問\n"
        "/status - 状態確認\n"
    )
    await update.message.reply_text(msg)


async def status_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if not is_authorized(update.effective_user.id):
        return

    # inbox
    inbox_total = 0
    inbox_unprocessed = 0
    if INBOX_FILE.exists():
        with open(INBOX_FILE, "r", encoding="utf-8") as f:
            for line in f:
                inbox_total += 1
                if not json.loads(line.strip()).get("processed", False):
                    inbox_unprocessed += 1

    # カテゴリ別
    categories = {}
    for folder in KB_ROOT.iterdir():
        if folder.is_dir() and folder.name not in ("inbox", "index", "weekly-digest", "logs"):
            md_count = len(list(folder.glob("*.md")))
            if md_count > 0:
                categories[folder.name] = md_count

    total_articles = sum(categories.values())
    cat_text = "\n".join(f"  {name}: {count}件" for name, count in sorted(categories.items()))

    await update.message.reply_text(
        f"📊 KB状態\n\n"
        f"蓄積記事: {total_articles}件\n"
        f"未処理inbox: {inbox_unprocessed}件\n\n"
        f"【カテゴリ別】\n{cat_text}"
    )


async def recent_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if not is_authorized(update.effective_user.id):
        return

    articles = get_recent_articles(days=7, limit=10)
    if not articles:
        await update.message.reply_text("直近7日間の記事はありません。")
        return

    path_to_id = build_path_to_id_map()

    msgs = ["📋 最近の記事（7日間）\n"]
    for a in articles:
        kb_id = path_to_id.get(a["path"], "?")
        msgs.append(f"#{kb_id} [{a['category']}] {a['title']}\n   /deep_{kb_id}")

    msgs.append("\n深掘りしたい記事があれば /deep 番号 で")
    await update.message.reply_text("\n".join(msgs))


async def search_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if not is_authorized(update.effective_user.id):
        return

    query = " ".join(context.args) if context.args else ""
    if not query:
        await update.message.reply_text("使い方: /search キーワード")
        return

    results = search_knowledge_base(query)
    if not results:
        await update.message.reply_text(f"「{query}」に一致する記事はありません。")
        return

    path_to_id = build_path_to_id_map()

    msgs = [f"🔍 「{query}」の検索結果: {len(results)}件\n"]
    for r in results:
        kb_id = path_to_id.get(r["path"], "?")
        msgs.append(f"#{kb_id} [{r['category']}] {r['title']}\n   /deep_{kb_id}")

    msgs.append("\n深掘りしたい記事があれば /deep 番号 で")
    await update.message.reply_text("\n".join(msgs))


async def deep_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """記事を深掘り: 詳細表示 + 質問受付"""
    if not is_authorized(update.effective_user.id):
        return

    if not context.args:
        await update.message.reply_text("使い方: /deep 番号")
        return

    try:
        num = int(context.args[0])
    except ValueError:
        await update.message.reply_text("番号を指定してください。例: /deep 1")
        return

    # レジストリから記事を取得（通し番号で一意に特定）
    article = get_article_from_registry(num)
    if not article:
        await update.message.reply_text(
            f"#{num} の記事が見つかりません。\n"
            f"/recent や /search で番号を確認してください。"
        )
        return

    # 記事の全文を表示
    body = article["body"]
    if len(body) > 3500:
        body = body[:3500] + "\n\n[...続きあり]"

    msg = (
        f"📖 #{num} {article['title']}\n"
        f"カテゴリ: {article['category']}\n"
        f"タグ: {article['tags']}\n\n"
        f"{body}\n\n"
        f"🔗 {article.get('url', '')}\n\n"
        f"この記事について質問があれば、そのまま送ってください。"
    )

    # 現在深掘り中の記事をユーザーコンテキストに保存
    context.user_data["current_article"] = article
    await update.message.reply_text(msg)


async def ask_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """ナレッジベース全体に質問"""
    if not is_authorized(update.effective_user.id):
        return

    question = " ".join(context.args) if context.args else ""
    if not question:
        await update.message.reply_text("使い方: /ask 質問内容")
        return

    await update.message.reply_text("🔍 ナレッジベースを検索中...")

    # 関連記事を検索
    results = search_knowledge_base(question, max_results=5)

    if not results:
        await update.message.reply_text(
            "関連する記事が見つかりませんでした。\n"
            "別のキーワードで試すか、URLを送って情報を蓄積してください。"
        )
        return

    # 関連記事をコンテキストにしてClaude Codeに質問
    context_text = ""
    for i, r in enumerate(results, 1):
        body_preview = r["body"][:1500]
        context_text += (
            f"\n--- 記事{i}: {r['title']} ---\n"
            f"カテゴリ: {r['category']}\n"
            f"{body_preview}\n"
        )

    prompt = f"""あなたはパーソナルナレッジベースのアシスタントです。
以下のナレッジベースの記事を参考に、質問に日本語で回答してください。

【質問】
{question}

【参考記事】
{context_text}

回答のルール:
- 参考記事の内容に基づいて具体的に回答する
- 記事に無い情報は「ナレッジベースにはこの情報はありません」と伝える
- 関連する記事のタイトルを参照として挙げる
- Telegramで読みやすいよう簡潔に（500字以内目安）"""

    answer = call_claude_code(prompt)
    if answer:
        # 参照した記事を末尾に
        refs = "\n".join(f"  - {r['title']}" for r in results[:3])
        await update.message.reply_text(f"{answer}\n\n📚 参照記事:\n{refs}")
    else:
        await update.message.reply_text("回答の生成に失敗しました。もう一度試してください。")

async def deep_n_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """タップ可能な /deep_N コマンドを処理"""
    if not is_authorized(update.effective_user.id):
        return
    text = update.message.text or ""
    match = re.match(r"^/deep_(\d+)", text)
    if match:
        context.args = [match.group(1)]
        await deep_command(update, context)

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """通常メッセージ: URL → 保存 / テキスト → 質問として処理"""
    if not is_authorized(update.effective_user.id):
        await update.message.reply_text("このBotを使う権限がありません。")
        return

    text = update.message.text or ""

    urls = extract_urls(text)

    if urls:
        # === URL保存モード ===
        memo = text
        for url in urls:
            memo = memo.replace(url, "").strip()

        for url in urls:
            entry = {
                "url": url,
                "memo": memo if memo else "",
                "received_at": datetime.now().isoformat(),
                "user_id": update.effective_user.id,
                "user_name": update.effective_user.first_name,
                "processed": False,
            }
            save_to_inbox(entry)
            logger.info(f"Saved URL: {url}")

        reply = f"✅ {len(urls)}件のURLを保存しました！\n"
        for url in urls:
            reply += f"  {url}\n"
        if memo:
            reply += f"  メモ: {memo}\n"
        reply += "\n次回の処理サイクルで自動要約されます。"
        await update.message.reply_text(reply)

    else:
        # === 質問モード ===
        current_article = context.user_data.get("current_article")

        if current_article:
            # 深掘り中の記事がある場合、その記事について回答
            await update.message.reply_text("🤔 考え中...")

            prompt = f"""あなたはナレッジベースアシスタントです。
以下の記事について質問されています。日本語で簡潔に回答してください。

【記事タイトル】{current_article['title']}
【記事内容】
{current_article['body'][:3000]}

【質問】
{text}

回答のルール:
- 記事の内容に基づいて具体的に回答
- 記事に含まれない情報は推測せず正直に伝える
- Telegramで読みやすいよう簡潔に（400字以内目安）
- 監査エージェント開発への応用可能性があれば言及"""

            answer = call_claude_code(prompt)
            if answer:
                await update.message.reply_text(
                    f"{answer}\n\n"
                    f"💬 引き続き質問できます。別の記事を見るには /recent か /search を使ってください。"
                )
            else:
                await update.message.reply_text("回答生成に失敗しました。もう一度試してください。")
        else:
            # ナレッジベース全体に対する質問として処理
            context.args = text.split()
            await ask_command(update, context)


# ── メイン ────────────────────────────────────────────
def main() -> None:
    if not BOT_TOKEN:
        logger.error("TELEGRAM_BOT_TOKEN not set")
        sys.exit(1)

    logger.info("KB Bot starting...")
    logger.info(f"KB_ROOT: {KB_ROOT}")

    # 既存記事をレジストリに登録（初回のみ実行）
    init_registry_if_needed()

    app = Application.builder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start_command))
    app.add_handler(CommandHandler("status", status_command))
    app.add_handler(CommandHandler("recent", recent_command))
    app.add_handler(CommandHandler("search", search_command))
    app.add_handler(CommandHandler("deep", deep_command))
    app.add_handler(CommandHandler("ask", ask_command))
    app.add_handler(MessageHandler(filters.COMMAND, deep_n_command))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    logger.info("Bot ready. Waiting for messages...")
    app.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == "__main__":
    main()
