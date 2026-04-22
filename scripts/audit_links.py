#!/usr/bin/env python3
"""Audit internal links across all HTML files.
Finds: orphan pages (0 inbound links), low-link pages (<3 inbound), most-linked pages.
"""
from __future__ import annotations
import os, re
from collections import defaultdict
from urllib.parse import urlparse, urljoin

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir))

SKIP_DIRS = {"portal", ".git", "node_modules", "assets"}

def iter_html(root: str):
    for dirpath, dirs, files in os.walk(root):
        dirs[:] = [d for d in dirs if d not in SKIP_DIRS]
        for f in files:
            if f.endswith(".html"):
                yield os.path.join(dirpath, f)

def to_site_path(abs_path: str, root: str) -> str:
    rel = os.path.relpath(abs_path, root).replace("\\", "/")
    return "/" + rel

def resolve_href(href: str, page_path: str, root: str) -> str | None:
    href = href.strip()
    if not href or href.startswith(("mailto:", "tel:", "javascript:", "#", "http", "https")):
        return None
    # absolute site path
    if href.startswith("/"):
        # strip query/fragment
        path = href.split("?")[0].split("#")[0]
        if not path.endswith(".html"):
            if path.endswith("/"):
                path += "index.html"
            else:
                return None
        return path
    # relative path
    page_dir = os.path.dirname(page_path)
    abs_target = os.path.normpath(os.path.join(page_dir, href))
    # back to site path
    try:
        rel = os.path.relpath(abs_target, root).replace("\\", "/")
    except ValueError:
        return None
    path = "/" + rel
    path = path.split("?")[0].split("#")[0]
    if not path.endswith(".html"):
        return None
    return path

def main():
    all_pages: set[str] = set()
    inbound: dict[str, set[str]] = defaultdict(set)
    outbound: dict[str, list[str]] = defaultdict(list)

    href_re = re.compile(r'href=["\']([^"\']+)["\']', re.IGNORECASE)

    for abs_path in iter_html(ROOT):
        page = to_site_path(abs_path, ROOT)
        all_pages.add(page)
        try:
            content = open(abs_path, encoding="utf-8", errors="ignore").read()
        except Exception:
            continue
        for href in href_re.findall(content):
            target = resolve_href(href, abs_path, ROOT)
            if target and target != page:
                inbound[target].add(page)
                outbound[page].append(target)

    # Report
    orphans = [p for p in all_pages if len(inbound[p]) == 0
               and not p.endswith("index.html")
               and "/portal/" not in p
               and p not in ("/404.html", "/offline.html", "/privacy.html", "/terms.html", "/search.html")]

    low_link = [(p, len(inbound[p])) for p in all_pages
                if 0 < len(inbound[p]) < 3
                and "/portal/" not in p]
    low_link.sort(key=lambda x: x[1])

    top_linked = sorted([(p, len(inbound[p])) for p in all_pages], key=lambda x: -x[1])[:20]

    print(f"\n=== LINK AUDIT ({len(all_pages)} pages) ===\n")

    print(f"ORPHANS ({len(orphans)} pages with 0 inbound links):")
    for p in sorted(orphans)[:40]:
        print(f"  {p}")
    if len(orphans) > 40:
        print(f"  ... and {len(orphans)-40} more")

    print(f"\nLOW LINK (<3 inbound) — {len(low_link)} pages:")
    for p, n in low_link[:30]:
        print(f"  {n}  {p}")

    print(f"\nTOP LINKED:")
    for p, n in top_linked:
        print(f"  {n:4d}  {p}")

    # Save report
    report_path = os.path.join(ROOT, "scripts", "link_audit_report.txt")
    with open(report_path, "w", encoding="utf-8") as f:
        f.write(f"Link audit — {len(all_pages)} pages\n\n")
        f.write(f"ORPHANS ({len(orphans)}):\n")
        for p in sorted(orphans):
            f.write(f"  {p}\n")
        f.write(f"\nLOW LINK (<3 inbound):\n")
        for p, n in low_link:
            f.write(f"  {n}  {p}\n")
        f.write(f"\nTOP LINKED:\n")
        for p, n in top_linked:
            f.write(f"  {n:4d}  {p}\n")

    print(f"\nReport saved: scripts/link_audit_report.txt")

if __name__ == "__main__":
    main()
