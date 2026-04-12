#!/usr/bin/env python3
"""
generate_knowledge_graph.py
===========================
knowledge-base 内の Markdown 記事から frontmatter (tags, category) を抽出し、
pyvis / networkx でインタラクティブなナレッジグラフ (HTML) を生成する。

使い方:
    python scripts/generate_knowledge_graph.py

出力:
    knowledge-base/index/knowledge_graph.html
"""

from __future__ import annotations

import re
import sys
from collections import Counter, defaultdict
from pathlib import Path

try:
    import networkx as nx
    from pyvis.network import Network
except ImportError:
    print("ERROR: pyvis / networkx が必要です。")
    print("  pip install pyvis networkx")
    sys.exit(1)

# ── パス設定 ──────────────────────────────────────────────
KB_ROOT = Path(__file__).resolve().parent.parent / "knowledge-base"
OUTPUT_DIR = KB_ROOT / "index"
OUTPUT_FILE = OUTPUT_DIR / "knowledge_graph.html"

# 除外ディレクトリ
EXCLUDE_DIRS = {"inbox", "index", "weekly-digest"}

# ── タグの正規化 ─────────────────────────────────────────
# 表記揺れを吸収するマッピング（小文字キー → 正規化後の表示名）
NORMALIZE_MAP = {
    "llm": "LLM",
    "rag": "RAG",
    "ai": "AI",
    "ml": "ML",
    "mcp": "MCP",
    "sse": "SSE",
    "claude code": "Claude Code",
    "claude": "Claude",
    "openai": "OpenAI",
    "gpt": "GPT",
    "gemini": "Gemini",
    "react": "React",
    "python": "Python",
    "go": "Go",
    "rust": "Rust",
    "docker": "Docker",
    "kubernetes": "Kubernetes",
    "k8s": "Kubernetes",
    "マルチエージェント": "マルチエージェント",
    "multi-agent": "マルチエージェント",
    "multiagent": "マルチエージェント",
}


def normalize_tag(tag: str) -> str:
    """タグを正規化して返す。"""
    t = tag.strip()
    key = t.lower()
    return NORMALIZE_MAP.get(key, t)


# ── カテゴリの色 ─────────────────────────────────────────
CATEGORY_COLORS = {
    "ai-ml": "#4FC3F7",       # ライトブルー
    "agent-arch": "#AB47BC",   # パープル
    "audit-ai": "#FF7043",     # オレンジ
    "infra": "#66BB6A",        # グリーン
    "other": "#BDBDBD",        # グレー
}


def get_category_color(cat: str) -> str:
    return CATEGORY_COLORS.get(cat, "#90A4AE")


# ── Frontmatter パーサー ──────────────────────────────────
TAG_PATTERN = re.compile(r"tags:\s*\[(.*?)\]", re.DOTALL)
CAT_PATTERN = re.compile(r'category:\s*"?([^"\n]+)"?\s*$', re.MULTILINE)
TITLE_PATTERN = re.compile(r'title:\s*"(.*?)"', re.DOTALL)


def parse_frontmatter(text: str) -> dict | None:
    """YAML frontmatter から title, tags, category を抽出。"""
    if not text.startswith("---"):
        return None
    end = text.find("---", 3)
    if end < 0:
        return None
    fm = text[3:end]

    title_m = TITLE_PATTERN.search(fm)
    title = title_m.group(1) if title_m else None

    tag_m = TAG_PATTERN.search(fm)
    if tag_m:
        raw = tag_m.group(1)
        tags = [normalize_tag(t) for t in raw.split(",") if t.strip()]
    else:
        tags = []

    cat_m = CAT_PATTERN.search(fm)
    category = cat_m.group(1).strip().strip('"') if cat_m else "other"

    return {"title": title, "tags": tags, "category": category}


# ── 記事収集 ──────────────────────────────────────────────
def collect_articles() -> list[dict]:
    """knowledge-base 内の全 .md を走査して記事情報を返す。"""
    articles = []
    for md_file in KB_ROOT.rglob("*.md"):
        # 除外ディレクトリ・CLAUDE.md をスキップ
        rel = md_file.relative_to(KB_ROOT)
        if rel.parts[0] in EXCLUDE_DIRS:
            continue
        if md_file.name == "CLAUDE.md":
            continue

        try:
            content = md_file.read_text(encoding="utf-8")
        except Exception:
            continue

        info = parse_frontmatter(content)
        if not info or not info["title"]:
            continue

        info["path"] = str(md_file)
        articles.append(info)

    return articles


# ── グラフ構築 ────────────────────────────────────────────
def build_graph(articles: list[dict], min_tag_count: int = 2) -> nx.Graph:
    """
    記事ノードとタグノードからなる二部グラフを構築。
    出現回数が min_tag_count 未満のタグは除外してノイズを減らす。
    """
    # タグ出現回数をカウント
    tag_counter: Counter = Counter()
    for a in articles:
        for t in a["tags"]:
            tag_counter[t] += 1

    # 有効タグ（2回以上出現）
    valid_tags = {t for t, c in tag_counter.items() if c >= min_tag_count}

    G = nx.Graph()

    # カテゴリごとの記事数
    cat_counter: Counter = Counter()

    for i, a in enumerate(articles):
        art_id = f"article_{i}"
        # タイトルを30文字に切り詰め
        short_title = a["title"][:30] + ("…" if len(a["title"]) > 30 else "")
        cat = a["category"]
        cat_counter[cat] += 1

        G.add_node(
            art_id,
            label=short_title,
            title=f"📄 {a['title']}\n🏷️ {', '.join(a['tags'])}\n📁 {cat}",
            color=get_category_color(cat),
            size=10,
            node_type="article",
            category=cat,
        )

        for tag in a["tags"]:
            if tag not in valid_tags:
                continue
            tag_id = f"tag_{tag}"
            if tag_id not in G:
                count = tag_counter[tag]
                G.add_node(
                    tag_id,
                    label=tag,
                    title=f"🔖 {tag} ({count} 記事)",
                    color="#FFD54F",   # イエロー
                    size=8 + min(count * 2, 30),  # 出現数に応じてサイズ変更
                    node_type="tag",
                    font={"size": 12, "color": "#333"},
                )
            G.add_edge(art_id, tag_id, color="#E0E0E0", width=0.5)

    print(f"  記事ノード: {len(articles)}")
    print(f"  タグノード (≥{min_tag_count}回出現): {len(valid_tags)}")
    print(f"  エッジ: {G.number_of_edges()}")
    print(f"  カテゴリ分布: {dict(cat_counter.most_common())}")

    return G


# ── HTML 生成 ─────────────────────────────────────────────
def generate_html(G: nx.Graph, output_path: Path) -> None:
    """pyvis で HTML ファイルを生成。"""
    net = Network(
        height="100vh",
        width="100%",
        bgcolor="#1a1a2e",
        font_color="white",
        directed=False,
        notebook=False,
        cdn_resources="in_line",   # オフラインでも動作するよう JS を埋め込む
    )

    # 物理シミュレーション設定
    net.set_options("""
    {
      "physics": {
        "forceAtlas2Based": {
          "gravitationalConstant": -80,
          "centralGravity": 0.01,
          "springLength": 120,
          "springConstant": 0.04,
          "damping": 0.5
        },
        "solver": "forceAtlas2Based",
        "stabilization": {
          "enabled": true,
          "iterations": 200
        }
      },
      "interaction": {
        "hover": true,
        "tooltipDelay": 100,
        "navigationButtons": true,
        "keyboard": true
      },
      "nodes": {
        "borderWidth": 1,
        "borderWidthSelected": 3,
        "font": {
          "size": 10,
          "face": "sans-serif"
        }
      },
      "edges": {
        "smooth": {
          "type": "continuous",
          "forceDirection": "none"
        }
      }
    }
    """)

    net.from_nx(G)

    # 凡例をHTMLに直接追加
    output_path.parent.mkdir(parents=True, exist_ok=True)
    net.save_graph(str(output_path))

    # 凡例 + 検索UI を注入
    html = output_path.read_text(encoding="utf-8")

    legend_html = """
    <div id="legend" style="
        position: fixed; top: 10px; left: 10px; z-index: 1000;
        background: rgba(26,26,46,0.92); border: 1px solid #444;
        border-radius: 8px; padding: 14px 18px; color: #fff;
        font-family: sans-serif; font-size: 13px; line-height: 1.8;
        backdrop-filter: blur(6px);
    ">
        <div style="font-weight:bold; margin-bottom:6px; font-size:15px;">
            📊 KB ナレッジグラフ
        </div>
        <div><span style="color:#FFD54F;">⬤</span> タグ</div>
        <div><span style="color:#4FC3F7;">⬤</span> ai-ml</div>
        <div><span style="color:#AB47BC;">⬤</span> agent-arch</div>
        <div><span style="color:#FF7043;">⬤</span> audit-ai</div>
        <div><span style="color:#66BB6A;">⬤</span> infra</div>
        <div><span style="color:#BDBDBD;">⬤</span> other</div>
        <hr style="border-color:#555; margin:8px 0;">
        <input id="searchBox" type="text" placeholder="🔍 タグ or タイトルで検索"
            style="width:180px; padding:5px 8px; border-radius:4px; border:1px solid #666;
                   background:#2a2a4e; color:#fff; font-size:12px;"
            oninput="searchGraph(this.value)">
    </div>

    <script>
    function searchGraph(query) {
        if (!query) {
            // リセット: 全ノード表示
            network.body.data.nodes.update(
                network.body.data.nodes.getIds().map(id => ({id, hidden: false, opacity: 1}))
            );
            network.body.data.edges.update(
                network.body.data.edges.getIds().map(id => ({id, hidden: false}))
            );
            return;
        }
        const q = query.toLowerCase();
        const nodes = network.body.data.nodes;
        const edges = network.body.data.edges;
        const matchIds = new Set();

        // ノード検索
        nodes.getIds().forEach(id => {
            const node = nodes.get(id);
            const label = (node.label || '').toLowerCase();
            const title = (node.title || '').toLowerCase();
            if (label.includes(q) || title.includes(q)) {
                matchIds.add(id);
            }
        });

        // マッチしたノードの隣接ノードも表示
        const visibleIds = new Set(matchIds);
        edges.getIds().forEach(eid => {
            const e = edges.get(eid);
            if (matchIds.has(e.from)) visibleIds.add(e.to);
            if (matchIds.has(e.to)) visibleIds.add(e.from);
        });

        nodes.update(nodes.getIds().map(id => ({
            id,
            hidden: !visibleIds.has(id),
            opacity: matchIds.has(id) ? 1.0 : 0.3
        })));
        edges.update(edges.getIds().map(eid => {
            const e = edges.get(eid);
            return {id: eid, hidden: !(visibleIds.has(e.from) && visibleIds.has(e.to))};
        }));
    }
    </script>
    """

    html = html.replace("</body>", legend_html + "\n</body>")
    output_path.write_text(html, encoding="utf-8")


# ── メイン ────────────────────────────────────────────────
def main():
    print("=== KB ナレッジグラフ生成 ===")
    print(f"KB_ROOT: {KB_ROOT}")

    articles = collect_articles()
    print(f"\n記事収集完了: {len(articles)} 件")

    if not articles:
        print("記事が見つかりませんでした。")
        sys.exit(1)

    G = build_graph(articles, min_tag_count=2)
    print(f"\nグラフ生成中 → {OUTPUT_FILE}")
    generate_html(G, OUTPUT_FILE)

    print(f"\n✅ 完了: {OUTPUT_FILE}")
    print(f"   ブラウザで開いてください: file:///{OUTPUT_FILE}")


if __name__ == "__main__":
    main()
