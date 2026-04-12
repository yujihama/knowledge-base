"""
RSS巡回スクリプト
rss_feeds.json に登録されたフィードを巡回し、新着記事を inbox.jsonl に追記する。

重複排除: knowledge-base/inbox/seen_guids.txt で管理（URL/GUIDを1行ずつ保存）。
流量制御: フィードごとに max_items で1回あたりの最大取得件数を制限。

実行タイミング（Windowsタスクスケジューラ推奨）:
  setup_rss_scheduler.bat で 6時間ごとに自動登録される。
"""

import feedparser
import json
import logging
import os
import ssl
import sys
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

from dotenv import load_dotenv

load_dotenv(Path(__file__).parent.parent / "bot" / ".env")

# ── 設定 ──────────────────────────────────────────────
KB_ROOT = Path(os.getenv(
    "KB_ROOT",
    str(Path(__file__).parent.parent / "knowledge-base")
))
INBOX_FILE    = KB_ROOT / "inbox" / "inbox.jsonl"
SEEN_FILE     = KB_ROOT / "inbox" / "seen_guids.txt"
FEEDS_CONFIG  = Path(__file__).parent / "rss_feeds.json"
LOG_FILE      = Path(__file__).parent.parent / "logs" / "rss_fetcher.log"

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


# ── 重複排除 ──────────────────────────────────────────
def load_seen_guids() -> set[str]:
    """既取得のGUID/URLセットを読み込む"""
    if not SEEN_FILE.exists():
        return set()
    with open(SEEN_FILE, "r", encoding="utf-8") as f:
        return {line.strip() for line in f if line.strip()}


def save_seen_guids(guids: set[str]) -> None:
    """GUIDセットをファイルに書き出す（追記ではなく全件上書き）"""
    SEEN_FILE.parent.mkdir(parents=True, exist_ok=True)
    with open(SEEN_FILE, "w", encoding="utf-8") as f:
        for g in sorted(guids):
            f.write(g + "\n")

def make_guid(entry) -> str:
    """エントリの一意キーを決定する（id > link の優先順）"""
    return getattr(entry, "id", None) or getattr(entry, "link", "") or ""


# ── SSL回避ハンドラ（Windows環境でのSSL証明書エラー対策）──────
def _make_ssl_handler():
    ssl_ctx = ssl.create_default_context()
    ssl_ctx.check_hostname = False
    ssl_ctx.verify_mode = ssl.CERT_NONE
    return urllib.request.HTTPSHandler(context=ssl_ctx)


# ── フィード取得 ──────────────────────────────────────
def fetch_feed(feed_cfg: dict, seen_guids: set[str]) -> list[dict]:
    """
    1フィードを取得し、新着エントリをinbox形式のdictリストで返す。
    seen_guids は更新しない（呼び出し元で管理）。
    """
    name      = feed_cfg["name"]
    url       = feed_cfg["url"]
    max_items = feed_cfg.get("max_items", 10)

    logger.info(f"Fetching: {name} ({url})")
    try:
        parsed = feedparser.parse(
            url,
            agent="Mozilla/5.0 (KB-System RSS Fetcher/1.0)",
            handlers=[_make_ssl_handler()],
        )
    except Exception as e:
        logger.error(f"[{name}] feedparser error: {e}")
        return []

    if parsed.bozo and not parsed.entries:
        logger.warning(f"[{name}] Feed parse error: {parsed.bozo_exception}")
        return []

    logger.info(f"[{name}] {len(parsed.entries)} entries in feed")

    new_entries = []
    for entry in parsed.entries:
        guid = make_guid(entry)
        if not guid:
            logger.debug(f"[{name}] skipping entry with no guid/link")
            continue
        if guid in seen_guids:
            continue

        article_url   = getattr(entry, "link", guid)
        article_title = getattr(entry, "title", "")

        # memoにフィード名とタイトルを入れてClaudeへのヒントにする
        memo = f"[{name}] {article_title}".strip()

        new_entries.append({
            "url":          article_url,
            "memo":         memo,
            "received_at":  datetime.now(timezone.utc).isoformat(),
            "user_id":      0,
            "user_name":    "rss_fetcher",
            "source":       "rss",
            "feed_name":    name,
            "processed":    False,
            "error_count":  0,
        })

        if len(new_entries) >= max_items:
            logger.info(f"[{name}] max_items={max_items} reached, stopping")
            break

    logger.info(f"[{name}] {len(new_entries)} new entries")
    return new_entries


# ── inbox追記 ─────────────────────────────────────────
def append_to_inbox(entries: list[dict]) -> None:
    """新着エントリをinbox.jsonlに追記する"""
    INBOX_FILE.parent.mkdir(parents=True, exist_ok=True)
    with open(INBOX_FILE, "a", encoding="utf-8") as f:
        for entry in entries:
            f.write(json.dumps(entry, ensure_ascii=False) + "\n")


# ── メイン処理 ────────────────────────────────────────
def main() -> None:
    logger.info("=== RSS巡回開始 ===")

    if not FEEDS_CONFIG.exists():
        logger.error(f"フィード設定ファイルが見つかりません: {FEEDS_CONFIG}")
        sys.exit(1)

    with open(FEEDS_CONFIG, "r", encoding="utf-8") as f:
        config = json.load(f)

    feeds = [feed for feed in config.get("feeds", []) if feed.get("enabled", True)]
    logger.info(f"対象フィード数: {len(feeds)}")

    seen_guids = load_seen_guids()
    logger.info(f"既取得GUID数: {len(seen_guids)}")

    total_new = 0
    for feed_cfg in feeds:
        new_entries = fetch_feed(feed_cfg, seen_guids)
        if new_entries:
            append_to_inbox(new_entries)
            for entry in new_entries:
                guid = entry["url"]
                seen_guids.add(guid)
            total_new += len(new_entries)

    save_seen_guids(seen_guids)
    logger.info(f"=== RSS巡回完了: 新着 {total_new} 件を inbox に追加 ===")


if __name__ == "__main__":
    main()
