"""
既存KB記事の一括改修スクリプト（ステージ1）

処理内容:
1. 「## Yujiの取り組みへの示唆」セクションを削除
2. 「## 監査エージェントへの示唆」セクションを削除
3. タグベースで「## 関連記事」セクションを追加（## 原文リンク の直前に挿入）

使い方:
  python scripts/retrofit_articles.py --dry-run    # 最初の5件だけ表示
  python scripts/retrofit_articles.py              # 全件実行
"""

import argparse
import re
import sys
from pathlib import Path

# process_inbox.py の関数を再利用
sys.path.insert(0, str(Path(__file__).parent))
from process_inbox import (
    KB_ROOT,
    load_kb_index,
    find_related_articles,
    _title_similarity,
)

# 削除対象のセクション見出し
REMOVE_SECTIONS = [
    "## Yujiの取り組みへの示唆",
    "## 監査エージェントへの示唆",
]

# セクション見出しパターン（## で始まる行）
SECTION_RE = re.compile(r"^## .+", re.MULTILINE)


def remove_section(content: str, heading: str) -> str:
    """指定の見出しから次の見出し(または末尾)までを削除"""
    pattern = re.compile(
        rf"(\n?)^{re.escape(heading)}\s*\n(.*?)(?=^## |\Z)",
        re.MULTILINE | re.DOTALL,
    )
    return pattern.sub("", content)


def has_section(content: str, heading: str) -> bool:
    return heading in content


def insert_related_section(content: str, related_lines: str) -> str:
    """## 原文リンク の直前に関連記事セクションを挿入。なければ末尾に追加"""
    marker = "## 原文リンク"
    if marker in content:
        return content.replace(marker, related_lines + "\n" + marker)
    return content.rstrip() + "\n\n" + related_lines + "\n"


def upsert_frontmatter_related(content: str, related_ids: list[int]) -> str:
    """frontmatterにrelated: [id, ...]を追加または更新"""
    related_yaml = ", ".join(str(i) for i in related_ids)
    new_field = f"related: [{related_yaml}]"

    # 既にrelated:行がある場合は上書き
    if re.search(r"^related:\s*\[", content, re.MULTILINE):
        return re.sub(
            r"^related:\s*\[.*?\]",
            new_field,
            content,
            count=1,
            flags=re.MULTILINE,
        )

    # なければ processed_at: の直前に挿入（なければ閉じ---の直前）
    if "processed_at:" in content:
        return content.replace("processed_at:", new_field + "\n" + "processed_at:", 1)

    # fallback: 最初の閉じ---の直前
    return re.sub(r"\n---", f"\n{new_field}\n---", content, count=1)


def parse_tags_from_content(content: str) -> list[str]:
    """frontmatterからタグを抽出"""
    m = re.search(r"^tags:\s*\[([^\]]*)\]", content, re.MULTILINE)
    if not m:
        return []
    return [t.strip().strip('"') for t in m.group(1).split(",") if t.strip()]


def parse_title_from_content(content: str) -> str:
    m = re.search(r'^title:\s*"([^"]*)"', content, re.MULTILINE)
    return m.group(1) if m else ""


def parse_url_from_content(content: str) -> str:
    m = re.search(r'^url:\s*"([^"]*)"', content, re.MULTILINE)
    return m.group(1) if m else ""


def process_file(
    md_path: Path,
    kb_index: list[dict],
    dry_run: bool = False,
) -> dict:
    """1ファイルを処理。変更内容をdictで返す"""
    result = {
        "path": str(md_path.relative_to(KB_ROOT)),
        "removed": [],
        "related_added": False,
        "changed": False,
    }

    content = md_path.read_text(encoding="utf-8")
    original = content

    # 1. セクション削除
    for heading in REMOVE_SECTIONS:
        if has_section(content, heading):
            content = remove_section(content, heading)
            result["removed"].append(heading)

    # 2. 関連記事追加（本文セクション + frontmatterプロパティ）
    tags = parse_tags_from_content(content)
    title = parse_title_from_content(content)
    url = parse_url_from_content(content)
    related: list[dict] = []

    if tags:
        related = find_related_articles(tags, url, title, kb_index, top_k=5)

    if related:
        related_ids = [r["kb_id"] for r in related if r.get("kb_id") is not None]

        # frontmatterに related: [...] を追加/更新
        if related_ids:
            content = upsert_frontmatter_related(content, related_ids)

        # 本文セクションがなければ追加
        if not has_section(content, "## 関連記事"):
            lines = "## 関連記事\n\n"
            for r in related:
                kb_id = r.get("kb_id")
                if kb_id is not None:
                    lines += f"- /deep_{kb_id} {r['title']}\n"
                else:
                    rel_path = "../" + r["path"]
                    lines += f"- [{r['title']}]({rel_path})\n"

            content = insert_related_section(content, lines)

        result["related_added"] = True

    # 変更があれば書き込み
    if content != original:
        result["changed"] = True
        if not dry_run:
            md_path.write_text(content, encoding="utf-8")

    return result


def main():
    parser = argparse.ArgumentParser(description="既存KB記事の一括改修")
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="変更を実際には書き込まず、最初の5件の結果を表示",
    )
    args = parser.parse_args()

    print("KBインデックスを読み込み中...")
    kb_index = load_kb_index()
    print(f"  {len(kb_index)}件のインデックスを読み込みました")

    # 対象ファイル収集
    skip_dirs = {"inbox", "templates", "archive", "weekly-digest", "index", ".obsidian"}
    targets: list[Path] = []
    for md_file in KB_ROOT.rglob("*.md"):
        if any(d in md_file.parts for d in skip_dirs):
            continue
        if md_file.name == "CLAUDE.md":
            continue
        targets.append(md_file)

    targets.sort()
    print(f"対象ファイル: {len(targets)}件")

    if args.dry_run:
        print("\n=== DRY RUN (最初の5件) ===\n")
        targets = targets[:5]

    stats = {"total": 0, "changed": 0, "removed_yuji": 0, "removed_audit": 0, "related": 0}

    for md_path in targets:
        result = process_file(md_path, kb_index, dry_run=args.dry_run)
        stats["total"] += 1

        if result["changed"]:
            stats["changed"] += 1

        for h in result["removed"]:
            if "Yuji" in h:
                stats["removed_yuji"] += 1
            if "監査" in h:
                stats["removed_audit"] += 1

        if result["related_added"]:
            stats["related"] += 1

        if args.dry_run and result["changed"]:
            print(f"--- {result['path']} ---")
            if result["removed"]:
                print(f"  削除: {', '.join(result['removed'])}")
            if result["related_added"]:
                print(f"  関連記事: 追加")
            print()

    # サマリ
    mode = "DRY RUN" if args.dry_run else "DONE"
    print(f"\n=== {mode} ===")
    print(f"処理対象:               {stats['total']}件")
    print(f"変更あり:               {stats['changed']}件")
    print(f"Yujiセクション削除:     {stats['removed_yuji']}件")
    print(f"監査セクション削除:     {stats['removed_audit']}件")
    print(f"関連記事追加:           {stats['related']}件")

    if args.dry_run:
        print(f"\n実行するには: python scripts/retrofit_articles.py")


if __name__ == "__main__":
    main()
