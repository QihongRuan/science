#!/usr/bin/env python3
import re
from pathlib import Path

SRC_DIR = Path('pdf_text')
OUT = Path('AER_WRITING_PATTERNS.md')

def clean_lines(text: str):
    lines = [ln.rstrip() for ln in text.splitlines()]
    # Drop leading empty lines and page markers like '\fPage X of Y'
    cleaned = []
    for ln in lines:
        if ln.startswith('\x0c'):
            ln = ln.lstrip('\x0c')
        cleaned.append(ln)
    return cleaned

def extract_sections(lines):
    # Title: first non-empty line, avoid obvious admin headers
    title = ''
    authors = ''
    abstract = ''
    jel = ''
    keywords = ''

    # Heuristics windows
    non_empty = [ln for ln in lines if ln.strip()]
    if non_empty:
        title = non_empty[0].strip()

    # Authors: lines until blank after title, skip email-only lines
    idx_title = next((i for i,l in enumerate(lines) if l.strip()), None)
    if idx_title is not None:
        i = idx_title + 1
        auth_lines = []
        while i < len(lines) and lines[i].strip():
            s = lines[i].strip()
            if '@' in s or s.lower().startswith(('journal:', 'manuscript id', 'american economic review')):
                i += 1
                continue
            auth_lines.append(s)
            i += 1
        # Compress to one line
        authors = ', '.join([re.sub(r'\s{2,}', ' ', a) for a in auth_lines])

    # Abstract: from a line starting with 'Abstract' to next blank
    abs_start = next((i for i,l in enumerate(lines) if re.match(r'^\s*abstract\b', l.strip(), re.I)), None)
    if abs_start is not None:
        i = abs_start
        # Remove the 'Abstract' label
        first = re.sub(r'^\s*abstract\b[:\s-]*', '', lines[i], flags=re.I).strip()
        buf = [first] if first else []
        i += 1
        while i < len(lines) and lines[i].strip():
            buf.append(lines[i].strip())
            # Stop if we bump into JEL/Keywords headings
            if re.search(r'\bJEL\b', lines[i], re.I) or re.search(r'\bKeywords?\b', lines[i], re.I):
                break
            i += 1
        abstract = ' '.join(buf)

    # JEL codes: line containing JEL
    for ln in lines[:200]:  # first pages likely contain it
        m = re.search(r'\bJEL\b[\s:;-]*([A-Z0-9,\s]+)', ln, re.I)
        if m:
            jel = m.group(1).strip()
            break

    # Keywords line
    for ln in lines[:200]:
        m = re.search(r'\bKeywords?\b[\s:;-]*(.*)$', ln, re.I)
        if m:
            keywords = m.group(1).strip()
            break

    # Truncate long fields for readability
    def trunc(s, n=800):
        return (s[:n] + '…') if len(s) > n else s

    return {
        'title': trunc(title, 200),
        'authors': trunc(authors, 300),
        'abstract': trunc(abstract, 1200),
        'jel': trunc(jel, 120),
        'keywords': trunc(keywords, 240),
    }

def main():
    entries = []
    for p in sorted(SRC_DIR.glob('*.txt')):
        try:
            text = p.read_text(errors='ignore')
        except Exception:
            continue
        lines = clean_lines(text)
        meta = extract_sections(lines)
        # Skip if no meaningful text
        if not any(meta.values()):
            continue
        entries.append((p, meta))

    out = []
    out.append('# AER Writing Patterns Summary')
    out.append('')
    out.append(f'- Sources parsed: {len(entries)} PDFs (from proofs/manuscripts)')
    out.append('- Common fields: Title, Authors (heuristic), Abstract, JEL, Keywords')
    out.append('')
    out.append('## Per-Paper Extracts')
    out.append('')
    for p, m in entries:
        out.append(f'### {m["title"] or p.name}')
        out.append(f'- Source: `{p}`')
        if m['authors']:
            out.append(f'- Authors: {m["authors"]}')
        if m['jel']:
            out.append(f'- JEL: {m["jel"]}')
        if m['keywords']:
            out.append(f'- Keywords: {m["keywords"]}')
        if m['abstract']:
            out.append('- Abstract:')
            out.append(f'  {m["abstract"]}')
        out.append('')

    # Aggregate patterns (very light heuristics)
    total_with_jel = sum(1 for _,m in entries if m['jel'])
    total_with_abs = sum(1 for _,m in entries if m['abstract'])
    total_with_kw = sum(1 for _,m in entries if m['keywords'])
    out.append('## Aggregate Patterns')
    out.append(f'- With JEL codes: {total_with_jel}/{len(entries)}')
    out.append(f'- With Abstract extracted: {total_with_abs}/{len(entries)}')
    out.append(f'- With Keywords: {total_with_kw}/{len(entries)}')
    out.append('')
    out.append('## Notable Style Traits (from sample)')
    out.append('- Concise abstracts quantify main effect sizes and uncertainty.')
    out.append('- Early placement of JEL codes and sometimes Keywords.')
    out.append('- Formal tone with contribution and identification foregrounded.')
    out.append('- Disclosures/IRB statements appear prominently in proofs.')
    out.append('- Standard structure: Abstract → Intro → Context/Model → Data → Results → Robustness → Conclusion.')

    OUT.write_text('\n'.join(out))

if __name__ == '__main__':
    main()

