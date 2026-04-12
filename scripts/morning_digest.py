"""
朝のダイジェスト生成 → Telegram送信
Task Scheduler で毎朝7:30に実行

処理:
1. 前日に蓄積された記事を収集
2. Claude Code でダイジェスト生成
3. Telegram Bot 経由で送信
"""

import json
import logging
import os
import subprocess
import sys
import tempfile
import urllib.request
import urllib.parse
import ssl
from datetime import datetime, timedelta
from pathlib import Path

from dotenv import load_dotenv

load_dotenv(Path(__file__).parent.parent / "bot" / ".env")

BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN", "")
CHAT_ID = os.getenv("ALLOWED_USER_IDS", "").split(",")[0].strip()
KB_ROOT = Path(os.getenv("KB_ROOT", str(Path(__file__).parent.parent)))
LOG_FILE = Path(__file__).parent.parent / "logs" / "morning_digest.log"

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


def send_telegram(text: str, parse_mode: str = "Markdown") -> bool:
    """Telegram にメッセージを送信"""
    if not BOT_TOKEN or not CHAT_ID:
        logger.error("BOT_TOKEN or CHAT_ID not set")
        return False

    # 長いメッセージは分割（Telegram上限: 4096文字）
    chunks = []
    while len(text) > 4000:
        split_pos = text.rfind("\n", 0, 4000)
        if split_pos == -1:
            split_pos = 4000
        chunks.append(text[:split_pos])
        text = text[split_pos:]
    chunks.append(text)

    for chunk in chunks:
        try:
            data = urllib.parse.urlencode({
                "chat_id": CHAT_ID,
                "text": chunk,
                "parse_mode": parse_mode,
            }).encode("utf-8")

            url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
            ssl_ctx = ssl.create_default_context()
            ssl_ctx.check_hostname = False
            ssl_ctx.verify_mode = ssl.CERT_NONE
            req = urllib.request.Request(url, data=data)
            urllib.request.urlopen(req, timeout=30, context=ssl_ctx)
        except Exception as e:
            logger.error(f"Telegram send failed: {e}")
            # Markdown パースエラーの場合、プレーンテキストで再試行
            if parse_mode == "Markdown":
                return send_telegram(chunk, parse_mode="")
            return False
    return True


def collect_recent_articles(days: int = 1) -> list[dict]:
    """直近N日に処理された記事を収集"""
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

            # processed_at で新しさ判定
            processed_at = meta.get("processed_at", "")
            if processed_at:
                try:
                    proc_date = datetime.fromisoformat(processed_at)
                    if proc_date < cutoff:
                        continue
                except ValueError:
                    pass

            articles.append({
                "title": meta.get("title", md_file.stem),
                "category": md_file.parent.name,
                "tags": meta.get("tags", ""),
                "url": meta.get("url", ""),
                "body": body[:2000],
                "path": str(md_file),
            })
        except Exception as e:
            logger.warning(f"Error reading {md_file}: {e}")

    return articles


def call_claude_code(prompt: str) -> str | None:
    """Claude Code をヘッドレスモードで呼び出し"""
    tmp_in = None
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
        stdout_bytes, stderr_bytes = proc.communicate(timeout=120)
        output = stdout_bytes.decode("utf-8", errors="replace").strip()

        if proc.returncode == 0 and output:
            return output
        else:
            err = stderr_bytes.decode("utf-8", errors="replace").strip()
            logger.error(f"Claude Code error: {err[:200]}")
            return None
    except Exception as e:
        logger.error(f"Claude Code call failed: {e}")
        return None
    finally:
        if tmp_in:
            try:
                os.remove(tmp_in)
            except OSError:
                pass


def generate_morning_digest(articles: list[dict]) -> str:
    """朝のダイジェストを生成"""
    if not articles:
        return None

    articles_text = ""
    for i, a in enumerate(articles, 1):
        articles_text += (
            f"\n--- 記事{i} ---\n"
            f"タイトル: {a['title']}\n"
            f"カテゴリ: {a['category']}\n"
            f"タグ: {a['tags']}\n"
            f"URL: {a['url']}\n"
            f"内容:\n{a['body'][:1000]}\n"
        )

    prompt = f"""以下は昨日ナレッジベースに追加された{len(articles)}件の記事です。
朝の通勤時にスマホで読む簡潔なダイジェストを作成してください。

【記事一覧】
{articles_text}

以下のフォーマットで出力してください（Telegram用、Markdown形式）:

*おはようございます ☀️ 昨日のKBダイジェスト*
（日付）・{len(articles)}件の新規記事

📌 *注目トピック*
最も重要な1-2件について、3行程度で要点を説明

📋 *全記事一覧*
各記事について1行で:
・[カテゴリ] タイトル - 一言コメント

🔍 *深掘りおすすめ*
特に深く読む価値のある記事を1件選び、その理由を2行で

💡 *監査エージェントへの示唆*
プロジェクトに関連するポイントがあれば1-2行で

最後に「気になる記事があれば番号を送ってください」と添えてください。
Telegramで読みやすいよう簡潔にしてください。"""

    return call_claude_code(prompt)


def main() -> None:
    logger.info("=== 朝のダイジェスト生成開始 ===")

    # 直近24時間の記事を収集（記事がなければ2日に広げる）
    articles = collect_recent_articles(days=1)
    if not articles:
        articles = collect_recent_articles(days=2)

    if not articles:
        logger.info("新規記事なし。スキップ。")
        send_telegram("☀️ おはようございます\n\n昨日の新規記事はありませんでした。\n気になるURLがあればいつでも送ってください！")
        return

    logger.info(f"対象記事: {len(articles)}件")

    # ダイジェスト生成
    digest = generate_morning_digest(articles)
    if not digest:
        logger.error("ダイジェスト生成に失敗")
        send_telegram("⚠️ 今朝のダイジェスト生成に失敗しました。手動で確認してください。")
        return

    # Telegram送信
    if send_telegram(digest):
        logger.info("ダイジェスト送信完了")
    else:
        logger.error("ダイジェスト送信失敗")

    logger.info("=== 朝のダイジェスト完了 ===")


if __name__ == "__main__":
    main()
