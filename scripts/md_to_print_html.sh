#!/usr/bin/env bash
set -euo pipefail
MD_FILE="$1"
OUT_HTML="$2"
TITLE="${3:-Document}"
cat > "$OUT_HTML" <<HTML
<!doctype html>
<html lang="zh-CN">
<head>
  <meta charset="utf-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1" />
  <title>${TITLE}</title>
  <style>
    html, body { font-family: -apple-system, BlinkMacSystemFont, "PingFang SC", "Hiragino Sans GB", "Microsoft YaHei", "Noto Sans CJK SC", Arial, sans-serif; color: #222; }
    body { max-width: 860px; margin: 40px auto; padding: 0 16px; line-height: 1.6; font-size: 16px; }
    h1, h2, h3 { line-height: 1.25; margin: 1.2em 0 0.6em; }
    h1 { font-size: 28px; }
    h2 { font-size: 22px; border-left: 4px solid #3b82f6; padding-left: 10px; }
    h3 { font-size: 18px; }
    ul { padding-left: 24px; }
    li { margin: 4px 0; }
    blockquote { border-left: 4px solid #ddd; padding-left: 12px; color: #555; }
    hr { border: none; border-top: 1px solid #eee; margin: 24px 0; }
    @media print { a[href]:after { content: ""; } }
  </style>
</head>
<body>
<div id="content">
HTML

# naive Markdown to HTML (headings, lists, blockquotes, paragraphs)
awk '
  function esc(s){ gsub("&","&amp;",s); gsub("<","&lt;",s); gsub(">","&gt;",s); return s }
  /^### /{print "<h3>" esc(substr($0,5)) "</h3>"; next}
  /^## /{print "<h2>" esc(substr($0,4)) "</h2>"; next}
  /^# /{print "<h1>" esc(substr($0,3)) "</h1>"; next}
  /^- /{ if (!inlist){ print "<ul>"; inlist=1 } print "<li>" esc(substr($0,3)) "</li>"; next }
  { if(inlist){ print "</ul>"; inlist=0 } }
  /^> /{ print "<blockquote>" esc(substr($0,3)) "</blockquote>"; next }
  /^---$/{ print "<hr/>"; next }
  /^[[:space:]]*$/ { print ""; next }
  { print "<p>" esc($0) "</p>" }
' "$MD_FILE" >> "$OUT_HTML"

cat >> "$OUT_HTML" <<HTML
</div>
</body>
</html>
HTML
echo "Wrote $OUT_HTML"
