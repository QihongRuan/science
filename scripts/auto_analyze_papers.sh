#!/usr/bin/env bash
set -euo pipefail

# Dependencies: pdftotext, rg, awk, sed

ROOT_DIR="$(pwd)"
OUT_DIR="$ROOT_DIR/paper_analysis"
mkdir -p "$OUT_DIR"

echo "Scanning for PDF candidates..." >&2
CANDIDATES=()
while IFS= read -r line; do CANDIDATES+=("$line"); done < <(rg --files -g "**/*.pdf" \
  | rg -vi "(readme|replication|data[-_ ]?(access|availability)|response|permission|agreement|archive|onlineappendix|appendix|fig|figure|graph|plots?|results?|tables?-figures?|programs|matlab|onedrive|icpsr|_README|_READ|da\.pdf)" || true)

is_paper_like() {
  local f="$1"; local head
  head=$(pdftotext -layout "$f" - 2>/dev/null | sed -n '1,300p') || head=""
  echo "$head" | rg -qi "\bAbstract\b" && echo "$head" | rg -qi "\bIntroduction\b"
}

extract_title() {
  local f="$1"; local head
  head=$(pdftotext -layout "$f" - 2>/dev/null | sed -n '1,40p' | tr '\f' '\n')
  # First non-empty line that looks like a title (letters and spaces, not all caps artifacts)
  echo "$head" | sed -n '1,40p' | sed 's/^\s\+//;s/\s\+$//' | awk 'length($0)>5' | head -n 1
}

extract_abstract() {
  local f="$1"
  pdftotext -layout "$f" - 2>/dev/null | awk '
    BEGIN{inabs=0}
    /Abstract/ && inabs==0 {inabs=1; next}
    inabs==1 {print}
    /^[[:space:]]*(JEL:|Keywords:|1[[:space:]]+Introduction)/ {if(inabs==1) exit}
  '
}

list_sections() {
  local f="$1"
  pdftotext -layout "$f" - 2>/dev/null | rg -n "^\s*(([IVX]+\.)|([0-9]+\s+))[A-Z][A-Za-z0-9 ,\-()]{2,}$" | sed 's/^\s\+//'
}

kw_present() {
  local text="$1"; local kw="$2"; echo "$text" | rg -io "$kw" | wc -l | tr -d ' \n'
}

analyze_file() {
  local f="$1"; local rel
  rel="$f"

  echo "Analyzing: $rel" >&2
  local title abs sections intro first200
  title="$(extract_title "$f")"
  abs="$(extract_abstract "$f" | sed 's/\f/ /g')"
  sections="$(list_sections "$f")"
  first200="$(pdftotext -layout "$f" - 2>/dev/null | sed -n '1,200p' | tr '\f' '\n')"
  intro="$(pdftotext -layout "$f" - 2>/dev/null | awk 'BEGIN{inintro=0} /^[[:space:]]*[0-9]+[[:space:]]+Introduction/ {inintro=1; next} {if(inintro) print} /^\s*[0-9]+\s+[A-Z]/{if(inintro) exit}')"

  # Simple metrics
  local abs_words abs_sents abs_avglen nums perc dollar methods diD event iv fe cluster placebo robust policy welfare
  abs_words=$(echo "$abs" | wc -w | tr -d ' ')
  abs_sents=$(echo "$abs" | tr '\n' ' ' | sed 's/\./\.\n/g' | rg -v '^\s*$' | wc -l | tr -d ' ')
  if [ "${abs_sents:-0}" -gt 0 ]; then abs_avglen=$((abs_words/abs_sents)); else abs_avglen=0; fi
  nums=$(echo "$first200" | rg -o "\b[0-9][0-9,\.]*\b" | wc -l | tr -d ' ')
  perc=$(echo "$first200" | rg -o "%" | wc -l | tr -d ' ')
  dollar=$(echo "$first200" | rg -o "\$[0-9]" | wc -l | tr -d ' ')
  methods=$(echo "$first200" | rg -in "difference-?in-?differences|event study|instrument|IV\b|regression discontinuity|RDD|DiD" | sed -n '1,5p')
  diD=$(kw_present "$first200" "difference-?in-?differences|\bDiD\b")
  event=$(kw_present "$first200" "event study")
  iv=$(kw_present "$first200" "instrument|\bIV\b")
  fe=$(kw_present "$first200" "fixed effects|FE")
  cluster=$(kw_present "$first200" "cluster(ed)? standard errors|clustered")
  placebo=$(kw_present "$first200" "placebo")
  robust=$(kw_present "$first200" "robust(ness)?")
  policy=$(kw_present "$first200" "policy|policies|cap-?and-?trade|voucher|MSC|SCC|welfare")
  welfare=$(kw_present "$first200" "welfare|marginal social cost|MSC|SCC")

  local slug out
  slug=$(echo "$rel" | tr '/ ' '__' | tr -cd 'A-Za-z0-9_.-')
  out="$OUT_DIR/${slug%.pdf}.md"
  {
    echo "# $(basename "$rel")"
    echo
    echo "- Path: \"$rel\""
    echo "- Title: ${title:-N/A}"
    echo "- Abstract words: $abs_words; sentences: $abs_sents; avg words/sent: $abs_avglen"
    echo "- Numbers in opening: $nums; percents: $perc; dollar mentions: $dollar"
    echo "- Methods keywords:"
    echo "  - DiD: $diD; Event study: $event; IV: $iv; Fixed effects: $fe; Clustered SEs: $cluster"
    echo "  - Placebo mentions: $placebo; Robust/robustness mentions: $robust"
    echo "- Policy/Welfare cues in opening: $policy (welfare-specific: $welfare)"
    echo
    echo "## Sections detected"
    if [ -n "$sections" ]; then echo '```'; echo "$sections"; echo '```'; else echo "(none detected)"; fi
    echo
    echo "## Abstract (excerpt)"
    if [ -n "$abs" ]; then echo '>'" $(echo "$abs" | tr '\n' ' ' | sed 's/  */ /g' | sed 's/^\s\+//;s/\s\+$//' | cut -c1-800)"; else echo "(no abstract found)"; fi
    echo
    echo "## Intro (first ~120 lines after heading)"
    if [ -n "$intro" ]; then echo '```'; echo "$intro" | sed -n '1,120p'; echo '```'; else echo "(intro not found)"; fi
    echo
    echo "## Methods keywords in opening"
    if [ -n "$methods" ]; then echo '```'; echo "$methods"; echo '```'; else echo "(none detected in opening)"; fi
  } > "$out"
}

count=0
for f in "${CANDIDATES[@]}"; do
  # Skip paths with unusual characters that can confuse tools
  if echo "$f" | rg -q "[?]"; then continue; fi
  if is_paper_like "$f"; then
    analyze_file "$f"
    count=$((count+1))
  fi
done

echo "Wrote $count paper analyses to $OUT_DIR" >&2
