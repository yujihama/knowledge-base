"""
inbox処理スクリプト
Task Scheduler または Claude Code Schedule から定期実行する

処理フロー:
1. inbox.jsonl から未処理エントリを読み込み
2. 各URLのコンテンツを取得
3. Claude Code に要約・分類・タグ付けを依頼
4. YAML frontmatter付き Markdown として保存
5. inbox.jsonl のエントリを処理済みに更新
"""

import json
import logging
import os
import re
import ssl
import subprocess
import sys
import urllib.request
import urllib.error
from datetime import datetime
from difflib import SequenceMatcher
from html.parser import HTMLParser
from pathlib import Path

from dotenv import load_dotenv

load_dotenv(Path(__file__).parent.parent / "bot" / ".env")

# ── Telegram設定 ───────────────────────────────────────
BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN", "")
ALLOWED_USER_IDS = [
    int(uid.strip())
    for uid in os.getenv("ALLOWED_USER_IDS", "").split(",")
    if uid.strip().isdigit()
]

# ── 設定 ──────────────────────────────────────────────
KB_ROOT = Path(os.getenv(
    "KB_ROOT",
    str(Path(__file__).parent.parent / "knowledge-base")
))
INBOX_FILE = KB_ROOT / "inbox" / "inbox.jsonl"
LOG_FILE = Path(__file__).parent.parent / "logs" / "processor.log"
LAST_PROCESSED_FILE = Path(__file__).parent.parent / "logs" / "last_processed.json"
REGISTRY_FILE = Path(__file__).parent.parent / "logs" / "article_registry.json"
MAX_ITEMS_PER_RUN = 100  # 1回の実行で処理する最大件数
FETCH_TIMEOUT = 30      # URLフェッチのタイムアウト(秒)

# カテゴリマッピング
CATEGORIES = {
    "ai-ml": "AI/ML研究（論文、モデル、学習手法、GRPO、RLAIF等）",
    "audit-ai": "監査AI・内部統制・GRC関連",
    "agent-arch": "エージェントアーキテクチャ（LangGraph、MCP、マルチエージェント等）",
    "infra": "インフラ・開発ツール（GPU、Docker、Ollama等）",
    "other": "上記に分類できないもの",
}

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
    """記事レジストリを保存する（アトミック書き込み）"""
    REGISTRY_FILE.parent.mkdir(parents=True, exist_ok=True)
    tmp = REGISTRY_FILE.with_suffix(".tmp")
    tmp.write_text(
        json.dumps(registry, ensure_ascii=False, indent=2), encoding="utf-8"
    )
    os.replace(str(tmp), str(REGISTRY_FILE))


def register_article(registry: dict, title: str, path: str, url: str, category: str) -> int:
    """記事をレジストリに登録し、割り振ったIDを返す"""
    aid = registry["next_id"]
    registry["articles"][str(aid)] = {
        "title": title,
        "path": path,
        "url": url,
        "category": category,
    }
    registry["next_id"] = aid + 1
    return aid


# ── HTMLテキスト抽出（軽量版）──────────────────────────
class TextExtractor(HTMLParser):
    """HTMLからテキストを抽出する簡易パーサー"""

    SKIP_TAGS = {"script", "style", "nav", "footer", "header", "aside"}

    def __init__(self):
        super().__init__()
        self.result = []
        self.skip_depth = 0

    def handle_starttag(self, tag, attrs):
        if tag in self.SKIP_TAGS:
            self.skip_depth += 1

    def handle_endtag(self, tag):
        if tag in self.SKIP_TAGS and self.skip_depth > 0:
            self.skip_depth -= 1

    def handle_data(self, data):
        if self.skip_depth == 0:
            text = data.strip()
            if text:
                self.result.append(text)

    def get_text(self) -> str:
        return "\n".join(self.result)


def fetch_page_text(url: str, max_len: int = 8000) -> str:
    """URLからページ内容をテキストとして取得"""
    try:
        # Windows環境でSSL証明書エラーを回避
        ssl_ctx = ssl.create_default_context()
        ssl_ctx.check_hostname = False
        ssl_ctx.verify_mode = ssl.CERT_NONE

        req = urllib.request.Request(
            url,
            headers={"User-Agent": "Mozilla/5.0 (KB-System/1.0)"}
        )
        with urllib.request.urlopen(req, timeout=FETCH_TIMEOUT, context=ssl_ctx) as resp:
            html = resp.read().decode("utf-8", errors="replace")

        parser = TextExtractor()
        parser.feed(html)
        text = parser.get_text()

        # 長すぎる場合は切り詰め（Claude Code のトークン節約）
        if len(text) > max_len:
            text = text[:max_len] + "\n\n[...truncated...]"

        return text
    except Exception as e:
        logger.warning(f"Failed to fetch {url}: {e}")
        return f"[ページ取得失敗: {e}]"


# ── arXiv論文の全文取得 ───────────────────────────────
ARXIV_RE = re.compile(
    r"https?://(?:www\.)?arxiv\.org/(?:abs|pdf|html)/(\d+\.\d+(?:v\d+)?)",
    re.IGNORECASE,
)


def detect_arxiv_id(url: str) -> str | None:
    """URLがarxivならpaper IDを返す。.pdf拡張子は除去"""
    m = ARXIV_RE.search(url)
    if not m:
        return None
    return re.sub(r"\.pdf$", "", m.group(1))


def fetch_arxiv_text(paper_id: str) -> str:
    """arxiv論文の本文をHTML版から取得。失敗時はabstractにフォールバック"""
    # HTML版を優先（本文全体が取れる）
    html_url = f"https://arxiv.org/html/{paper_id}"
    text = fetch_page_text(html_url, max_len=30000)
    if text and not text.startswith("[ページ取得失敗") and len(text) > 1000:
        logger.info(f"arxiv HTML版取得成功: {paper_id} ({len(text)}字)")
        return text

    # abstract版にフォールバック
    logger.info(f"arxiv abstract版にフォールバック: {paper_id}")
    abs_url = f"https://arxiv.org/abs/{paper_id}"
    return fetch_page_text(abs_url, max_len=8000)


# ── KB記事インデックス（関連記事・前提知識検索用）─────
FRONTMATTER_RE = re.compile(r"^---\n(.*?)\n---", re.DOTALL)


def parse_frontmatter(path: Path) -> dict | None:
    """記事ファイルの先頭YAML frontmatterを簡易パース"""
    try:
        with open(path, "r", encoding="utf-8") as f:
            content = f.read(2000)
    except OSError:
        return None

    m = FRONTMATTER_RE.search(content)
    if not m:
        return None

    fm_text = m.group(1)
    result: dict = {"tags": []}

    title_m = re.search(r'^title:\s*"([^"]*)"', fm_text, re.MULTILINE)
    if title_m:
        result["title"] = title_m.group(1)

    url_m = re.search(r'^url:\s*"([^"]*)"', fm_text, re.MULTILINE)
    if url_m:
        result["url"] = url_m.group(1)

    tags_m = re.search(r"^tags:\s*\[([^\]]*)\]", fm_text, re.MULTILINE)
    if tags_m:
        result["tags"] = [
            t.strip().strip('"') for t in tags_m.group(1).split(",") if t.strip()
        ]

    category_m = re.search(r'^category:\s*"([^"]*)"', fm_text, re.MULTILINE)
    if category_m:
        result["category"] = category_m.group(1)

    return result


def load_kb_index() -> list[dict]:
    """KB内全記事のfrontmatterをインデックス化。registryからkb_idも紐づける"""
    # registryを先に読んで path→kb_id マップを構築
    registry = load_registry()
    path_to_id: dict[str, int] = {}
    for sid, info in registry.get("articles", {}).items():
        p = info.get("path", "")
        if not p:
            continue
        # registry内のpathは絶対/相対混在の可能性があるので正規化
        try:
            abs_path = Path(p)
            if abs_path.is_absolute():
                rel = str(abs_path.relative_to(KB_ROOT)).replace("\\", "/")
            else:
                rel = p.replace("\\", "/")
            path_to_id[rel] = int(sid)
        except (ValueError, OSError):
            continue

    index: list[dict] = []
    skip_dirs = {"inbox", "templates", "archive"}
    for md_file in KB_ROOT.rglob("*.md"):
        if any(d in md_file.parts for d in skip_dirs):
            continue
        fm = parse_frontmatter(md_file)
        if fm and fm.get("tags"):
            rel_path = str(md_file.relative_to(KB_ROOT)).replace("\\", "/")
            fm["_path"] = rel_path
            fm["_kb_id"] = path_to_id.get(rel_path)
            index.append(fm)
    logger.info(
        f"KBインデックス読み込み: {len(index)}件 (kb_id紐づけ: "
        f"{sum(1 for x in index if x['_kb_id'] is not None)}件)"
    )
    return index


def _title_similarity(a: str, b: str) -> float:
    """タイトル類似度（0.0-1.0）。近似重複の排除に使用"""
    if not a or not b:
        return 0.0
    return SequenceMatcher(None, a[:60], b[:60]).ratio()


def find_related_articles(
    new_tags: list[str],
    new_url: str,
    new_title: str,
    kb_index: list[dict],
    top_k: int = 5,
) -> list[dict]:
    """タグ重複で既存記事をスコアリングし、上位を返す"""
    new_tag_set = {t.lower() for t in new_tags if t}
    if not new_tag_set:
        return []

    scored: list[dict] = []
    for item in kb_index:
        # 同一URL（過去の処理）は除外
        if item.get("url") and item["url"] == new_url:
            continue
        # タイトルが酷似した近似重複を除外
        if _title_similarity(item.get("title", ""), new_title) > 0.75:
            continue

        other_tags = {t.lower() for t in item.get("tags", []) if t}
        overlap = len(new_tag_set & other_tags)
        if overlap == 0:
            continue

        scored.append(
            {
                "path": item["_path"],
                "title": item.get("title", ""),
                "url": item.get("url", ""),
                "kb_id": item.get("_kb_id"),
                "score": overlap,
            }
        )

    scored.sort(key=lambda x: (x["score"], x["title"]), reverse=True)
    return scored[:top_k]


def find_prereq_articles(
    prereqs: list[str], kb_index: list[dict]
) -> list[tuple[str, dict | None]]:
    """前提知識ごとに既存記事を検索。該当なしはNone"""
    result: list[tuple[str, dict | None]] = []
    for concept in prereqs:
        if not concept:
            continue
        concept_lower = concept.lower()
        match: dict | None = None
        for item in kb_index:
            title = item.get("title", "").lower()
            tags = [t.lower() for t in item.get("tags", [])]
            if concept_lower in title or concept_lower in tags:
                match = {
                    "path": item["_path"],
                    "title": item.get("title", ""),
                    "url": item.get("url", ""),
                    "kb_id": item.get("_kb_id"),
                }
                break
        result.append((concept, match))
    return result


# ── Claude Code 呼び出し ──────────────────────────────
def call_claude_code(prompt: str) -> str | None:
    """Claude Code をヘッドレスモードで呼び出し（入出力ともファイル経由）"""
    import tempfile
    tmp_in = None
    tmp_out = None
    try:
        # プロンプトを一時ファイルに書き出し
        with tempfile.NamedTemporaryFile(
            mode="w", suffix=".txt", encoding="utf-8", delete=False
        ) as f:
            f.write(prompt)
            tmp_in = f.name

        # 出力用一時ファイル
        tmp_out = tmp_in + ".out.txt"

        # ファイル経由で入出力（パイプのエンコーディング問題を回避）
        cmd = f'type "{tmp_in}" | claude -p - --model claude-sonnet-4-6 --output-format text > "{tmp_out}" 2>&1'
        result = subprocess.run(
            cmd,
            timeout=300,
            cwd=str(KB_ROOT),
            shell=True,
        )

        # 出力をUTF-8で読み込み
        if os.path.exists(tmp_out):
            output = Path(tmp_out).read_text(encoding="utf-8", errors="replace").strip()
            if result.returncode == 0 and output:
                return output
            else:
                logger.error(f"Claude Code error (rc={result.returncode}): {output[:200]}")
                return None
        else:
            logger.error("Claude Code output file not created")
            return None
    except FileNotFoundError:
        logger.error("Claude Code が見つかりません。PATHを確認してください。")
        return None
    except subprocess.TimeoutExpired:
        logger.error("Claude Code がタイムアウトしました。")
        return None
    finally:
        for p in (tmp_in, tmp_out):
            if p:
                try:
                    os.remove(p)
                except OSError:
                    pass

def process_entry(entry: dict, kb_index: list[dict]) -> dict | None:
    """1件のURLエントリを処理。成功時は {"title", "path", "url", "category"} を返す"""
    url = entry["url"]
    memo = entry.get("memo", "")
    logger.info(f"Processing: {url}")

    # 1. ページ内容取得（arXivなら全文を試みる）
    arxiv_id = detect_arxiv_id(url)
    if arxiv_id:
        page_text = fetch_arxiv_text(arxiv_id)
    else:
        page_text = fetch_page_text(url)

    # 2. Claude Code で要約・分類（日本語タイトル・日本語出力）
    categories_desc = "\n".join(
        f"- {k}: {v}" for k, v in CATEGORIES.items()
    )

    prompt = f"""以下のウェブページの内容を分析してください。

【URL】{url}
【ユーザーメモ】{memo or "なし"}

【ページ内容（抜粋）】
{page_text}

以下のJSON形式で回答してください。JSONのみを出力し、他のテキストは含めないでください。

{{
  "title": "日本語のタイトル（原文が英語の場合は翻訳）",
  "summary": "1000字程度の日本語要約。技術的な仕組み・背景・結果を具体的に書く。抽象表現は避け、数値や固有名詞を積極的に使う",
  "category": "以下から1つ選択: {', '.join(CATEGORIES.keys())}",
  "tags": ["タグ1", "タグ2", "タグ3"],
  "ideas": ["技術的または概念として面白い点1", "面白い点2", "面白い点3"],
  "prerequisites": ["この記事を理解するために前提となる技術概念・モデル名・用語を3〜5個。固有名詞（Transformer, PPO, LoRA等）を優先し、1〜4語程度の短い表記で"]
}}

カテゴリの定義:
{categories_desc}"""

    response = call_claude_code(prompt)
    if not response:
        return None

    # 3. JSONパース
    try:
        # ```json ... ``` の囲みを除去
        cleaned = re.sub(r"```json\s*", "", response)
        cleaned = re.sub(r"```\s*$", "", cleaned)
        cleaned = cleaned.strip()
        data = json.loads(cleaned)
    except json.JSONDecodeError:
        logger.error(f"JSON parse failed for {url}. Response: {response[:200]}")
        return None

    # 4. Markdown生成・保存
    category = data.get("category", "other")
    if category not in CATEGORIES:
        category = "other"

    safe_title = re.sub(r'[<>:"/\\|?*]', "_", data.get("title", "untitled"))
    date_str = datetime.now().strftime("%Y-%m-%d")
    filename = f"{date_str}_{safe_title[:60]}.md"

    output_dir = KB_ROOT / category
    output_dir.mkdir(parents=True, exist_ok=True)
    output_path = output_dir / filename

    tags_list = data.get("tags", [])
    tags_yaml = ", ".join(tags_list)
    ideas = "\n".join(
        f"- {t}" for t in data.get("ideas", [])
    )
    prereqs = [p for p in data.get("prerequisites", []) if p]

    # 関連記事・前提知識を検索
    related = find_related_articles(
        tags_list, url, data.get("title", ""), kb_index, top_k=5
    )
    related_ids = [r["kb_id"] for r in related if r.get("kb_id") is not None]
    related_yaml = ", ".join(str(i) for i in related_ids)
    prereq_matches = find_prereq_articles(prereqs, kb_index)

    md_content = f"""---
title: "{data.get('title', 'Untitled')}"
url: "{url}"
date: {date_str}
tags: [{tags_yaml}]
category: "{category}"
related: [{related_yaml}]
memo: "{memo}"
processed_at: "{datetime.now().isoformat()}"
---

## 要約

{data.get('summary', '')}

## アイデア

{ideas}
"""

    if prereq_matches:
        md_content += "\n## 前提知識\n\n"
        for concept, match in prereq_matches:
            if match:
                kb_id = match.get("kb_id")
                if kb_id is not None:
                    # Telegram上で /deep_N はタップ可能になる
                    md_content += (
                        f"- **{concept}** → /deep_{kb_id} {match['title']}\n"
                    )
                else:
                    rel_path = "../" + match["path"]
                    md_content += (
                        f"- **{concept}** → [{match['title']}]({rel_path})\n"
                    )
            else:
                md_content += f"- **{concept}** (TODO: 読むべき)\n"

    if related:
        md_content += "\n## 関連記事\n\n"
        for r in related:
            kb_id = r.get("kb_id")
            if kb_id is not None:
                md_content += f"- /deep_{kb_id} {r['title']}\n"
            else:
                rel_path = "../" + r["path"]
                md_content += f"- [{r['title']}]({rel_path})\n"

    md_content += f"""
## 原文リンク

[{data.get('title', url)}]({url})
"""

    output_path.write_text(md_content, encoding="utf-8")
    logger.info(f"Saved: {output_path}")

    return {
        "title": data.get("title", "Untitled"),
        "path": str(output_path),
        "url": url,
        "category": category,
    }


# ── Git自動反映 ──────────────────────────────────────
GIT_REPO_ROOT = Path(__file__).parent.parent


def git_commit_and_push(saved_articles: list[dict]) -> bool:
    """新記事をgit commit & pushする。成功時True"""
    if not saved_articles:
        return False

    try:
        # 新記事ファイルをステージング
        paths_to_add = []
        for article in saved_articles:
            p = Path(article["path"])
            if p.exists():
                paths_to_add.append(str(p.relative_to(GIT_REPO_ROOT)))

        if not paths_to_add:
            logger.info("Git: ステージング対象ファイルなし")
            return False

        for path in paths_to_add:
            subprocess.run(
                ["git", "add", path],
                cwd=str(GIT_REPO_ROOT),
                check=True,
                capture_output=True,
            )

        # レジストリもコミット対象に含める
        registry_rel = str(REGISTRY_FILE.relative_to(GIT_REPO_ROOT))
        subprocess.run(
            ["git", "add", registry_rel],
            cwd=str(GIT_REPO_ROOT),
            check=True,
            capture_output=True,
        )

        # コミット
        date_str = datetime.now().strftime("%Y-%m-%d %H:%M")
        msg = f"Add {len(paths_to_add)} KB article(s) [{date_str}]"
        result = subprocess.run(
            ["git", "commit", "-m", msg],
            cwd=str(GIT_REPO_ROOT),
            capture_output=True,
            text=True,
        )
        if result.returncode != 0:
            logger.warning(f"Git commit failed: {result.stderr.strip()}")
            return False
        logger.info(f"Git commit: {msg}")

        # プッシュ
        result = subprocess.run(
            ["git", "push"],
            cwd=str(GIT_REPO_ROOT),
            capture_output=True,
            text=True,
            timeout=60,
        )
        if result.returncode != 0:
            logger.warning(f"Git push failed: {result.stderr.strip()}")
            return False
        logger.info("Git push 完了")
        return True

    except Exception as e:
        logger.warning(f"Git操作失敗: {e}")
        return False


# ── Telegram通知 ─────────────────────────────────────
def send_telegram_notification(message: str) -> None:
    """処理完了をTelegramで通知する"""
    if not BOT_TOKEN or not ALLOWED_USER_IDS:
        logger.debug("Telegram通知スキップ（トークンまたはユーザーID未設定）")
        return
    ssl_ctx = ssl.create_default_context()
    ssl_ctx.check_hostname = False
    ssl_ctx.verify_mode = ssl.CERT_NONE
    for user_id in ALLOWED_USER_IDS:
        try:
            payload = json.dumps({"chat_id": user_id, "text": message}).encode("utf-8")
            req = urllib.request.Request(
                f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage",
                data=payload,
                headers={"Content-Type": "application/json"},
            )
            with urllib.request.urlopen(req, timeout=10, context=ssl_ctx) as resp:
                if resp.status == 200:
                    logger.info(f"Telegram通知送信完了 → user_id={user_id}")
        except Exception as e:
            logger.warning(f"Telegram通知失敗: {e}")


# ── メイン処理 ────────────────────────────────────────
def main() -> None:
    logger.info("=== inbox処理開始 ===")

    if not INBOX_FILE.exists():
        logger.info("inbox.jsonl が存在しません。処理なし。")
        return

    # inbox読み込み
    with open(INBOX_FILE, "r", encoding="utf-8") as f:
        lines = f.readlines()

    entries = []
    for i, line in enumerate(lines):
        line = line.strip()
        if not line:
            continue
        try:
            entry = json.loads(line)
            entry["_line_index"] = i
            entries.append(entry)
        except json.JSONDecodeError:
            logger.warning(f"Invalid JSON at line {i}: {line[:100]}")

    # 未処理のみ抽出
    unprocessed = [e for e in entries if not e.get("processed", False)]
    logger.info(f"未処理: {len(unprocessed)}件 / 全体: {len(entries)}件")

    if not unprocessed:
        logger.info("未処理エントリなし。終了。")
        return

    # 処理実行
    to_process = unprocessed[:MAX_ITEMS_PER_RUN]
    success_count = 0
    saved_articles: list[dict] = []

    # KBインデックスを一度だけロード（関連記事・前提知識検索用）
    kb_index = load_kb_index()

    for entry in to_process:
        try:
            result = process_entry(entry, kb_index)
            if result:
                entry["processed"] = True
                entry["processed_at"] = datetime.now().isoformat()
                success_count += 1
                saved_articles.append(result)
            else:
                entry["error_count"] = entry.get("error_count", 0) + 1
                if entry["error_count"] >= 3:
                    entry["processed"] = True
                    entry["status"] = "failed"
                    logger.warning(f"Marking as failed after 3 attempts: {entry['url']}")
        except Exception as e:
            logger.error(f"Error processing {entry.get('url')}: {e}")
            entry["error_count"] = entry.get("error_count", 0) + 1

    # inbox.jsonl を更新（処理済みフラグを反映）
    entry_map = {e["_line_index"]: e for e in entries}
    updated_lines = []
    for i, line in enumerate(lines):
        if i in entry_map:
            e = {k: v for k, v in entry_map[i].items() if k != "_line_index"}
            updated_lines.append(json.dumps(e, ensure_ascii=False) + "\n")
        else:
            updated_lines.append(line if line.endswith("\n") else line + "\n")

    with open(INBOX_FILE, "w", encoding="utf-8") as f:
        f.writelines(updated_lines)

    logger.info(f"=== 処理完了: {success_count}/{len(to_process)}件成功 ===")

    # レジストリに登録（通し番号を割り振り）
    if saved_articles:
        try:
            registry = load_registry()
            for article in saved_articles:
                article["kb_id"] = register_article(
                    registry,
                    article["title"],
                    article["path"],
                    article["url"],
                    article["category"],
                )
            save_registry(registry)
            logger.info(f"レジストリ更新: {len(saved_articles)}件登録 (next_id={registry['next_id']})")
        except Exception as e:
            logger.warning(f"レジストリ更新失敗: {e}")

    # Git commit & push
    if saved_articles:
        git_ok = git_commit_and_push(saved_articles)
        if git_ok:
            logger.info("Git: リモートに反映完了")
        else:
            logger.warning("Git: リモート反映に失敗（ローカル保存は完了済み）")

    # last_processed.json に書き出し（後方互換）
    if saved_articles:
        try:
            LAST_PROCESSED_FILE.write_text(
                json.dumps(saved_articles, ensure_ascii=False, indent=2),
                encoding="utf-8"
            )
        except Exception as e:
            logger.warning(f"last_processed.json 書き込み失敗: {e}")

    # Telegram通知（処理件数が1件以上の場合のみ、通し番号で表示）
    if success_count > 0:
        remaining = len(unprocessed) - len(to_process)
        msg = f"✅ inbox処理完了 {success_count}/{len(to_process)}件"
        if remaining > 0:
            msg += f"（残り{remaining}件）"
        msg += "\n"
        for article in saved_articles:
            title = article["title"][:45]
            kb_id = article.get("kb_id", "?")
            msg += f"\n・{title} /deep_{kb_id}"
        send_telegram_notification(msg)


if __name__ == "__main__":
    main()