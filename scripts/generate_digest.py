"""
週次ダイジェスト生成
毎週月曜朝に Task Scheduler から実行し、
1週間分の蓄積記事をカテゴリ横断で分析・レポート化する
"""

import json
import logging
import os
import subprocess
import sys
from datetime import datetime, timedelta
from pathlib import Path

from dotenv import load_dotenv

load_dotenv(Path(__file__).parent.parent / "bot" / ".env")

KB_ROOT = Path(os.getenv(
    "KB_ROOT",
    str(Path(__file__).parent.parent / "knowledge-base")
))
DIGEST_DIR = KB_ROOT / "weekly-digest"
LOG_FILE = Path(__file__).parent.parent / "logs" / "digest.log"

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


def collect_recent_articles(days: int = 7) -> list[dict]:
    """過去N日間に作成されたMarkdownファイルを収集"""
    cutoff = datetime.now() - timedelta(days=days)
    articles = []

    for md_file in KB_ROOT.rglob("*.md"):
        if md_file.parent.name in ("inbox", "index", "weekly-digest"):
            continue

        try:
            content = md_file.read_text(encoding="utf-8")
            # frontmatterからメタデータを抽出
            meta = {}
            if content.startswith("---"):
                end = content.find("---", 3)
                if end > 0:
                    for line in content[3:end].strip().split("\n"):
                        if ":" in line:
                            key, val = line.split(":", 1)
                            meta[key.strip()] = val.strip().strip('"').strip("'")

            # 日付チェック
            date_str = meta.get("date", "")
            if date_str:
                try:
                    file_date = datetime.strptime(date_str, "%Y-%m-%d")
                    if file_date < cutoff:
                        continue
                except ValueError:
                    pass

            articles.append({
                "path": str(md_file.relative_to(KB_ROOT)),
                "category": md_file.parent.name,
                "title": meta.get("title", md_file.stem),
                "tags": meta.get("tags", ""),
                "url": meta.get("url", ""),
                "content_preview": content[:1500],
            })
        except Exception as e:
            logger.warning(f"Error reading {md_file}: {e}")

    return articles


def generate_digest(articles: list[dict]) -> str | None:
    """Claude Code で週次ダイジェストを生成"""
    if not articles:
        return None

    articles_text = ""
    for a in articles:
        articles_text += (
            f"\n---\n"
            f"カテゴリ: {a['category']}\n"
            f"タイトル: {a['title']}\n"
            f"タグ: {a['tags']}\n"
            f"URL: {a['url']}\n"
            f"内容:\n{a['content_preview']}\n"
        )

    prompt = f"""以下は今週ナレッジベースに蓄積された{len(articles)}件の記事です。
週次ダイジェストレポートを日本語で作成してください。

【記事一覧】
{articles_text}

以下の構成でMarkdownレポートを作成してください:

1. **今週のハイライト**: 最も重要な発見・トレンドを3-5個
2. **カテゴリ別サマリー**: 各カテゴリの記事を簡潔にまとめる
3. **テーマ横断の洞察**: カテゴリを横断して見えるパターンやトレンド
4. **監査エージェント開発への示唆**: プロジェクトに活かせるポイント
5. **来週のウォッチポイント**: 追跡すべきトピック

Markdownのみを出力してください。"""

    try:
        result = subprocess.run(
            ["claude", "-p", prompt, "--output-format", "text"],
            capture_output=True,
            text=True,
            timeout=180,
            cwd=str(KB_ROOT),
            encoding="utf-8",
            errors="replace",
            shell=True,
        )
        if result.returncode == 0:
            return result.stdout.strip()
        else:
            logger.error(f"Claude Code error: {result.stderr}")
            return None
    except Exception as e:
        logger.error(f"Claude Code call failed: {e}")
        return None


def main() -> None:
    logger.info("=== 週次ダイジェスト生成開始 ===")

    articles = collect_recent_articles(days=7)
    logger.info(f"過去7日間の記事: {len(articles)}件")

    if not articles:
        logger.info("記事がありません。スキップ。")
        return

    digest_content = generate_digest(articles)
    if not digest_content:
        logger.error("ダイジェスト生成に失敗しました。")
        return

    # 保存
    DIGEST_DIR.mkdir(parents=True, exist_ok=True)
    today = datetime.now()
    week_start = today - timedelta(days=today.weekday())
    week_end = week_start + timedelta(days=6)
    filename = f"{week_start.strftime('%Y-%m-%d')}_{week_end.strftime('%Y-%m-%d')}_digest.md"

    output_path = DIGEST_DIR / filename
    header = (
        f"---\n"
        f"type: weekly-digest\n"
        f"period: {week_start.strftime('%Y-%m-%d')} ~ {week_end.strftime('%Y-%m-%d')}\n"
        f"generated_at: {today.isoformat()}\n"
        f"article_count: {len(articles)}\n"
        f"---\n\n"
        f"# 週次ダイジェスト ({week_start.strftime('%m/%d')} - {week_end.strftime('%m/%d')})\n\n"
    )

    output_path.write_text(header + digest_content, encoding="utf-8")
    logger.info(f"Saved digest: {output_path}")
    logger.info("=== 週次ダイジェスト生成完了 ===")


if __name__ == "__main__":
    main()