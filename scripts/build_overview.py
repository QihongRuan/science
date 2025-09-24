#!/usr/bin/env python3
"""
Build overview report from per-repo summaries with robust error handling
"""

import json
from pathlib import Path
import re

def safe_extract_score(text, label):
    """Safely extract score from text with error handling"""
    try:
        lines = text.split('\n')
        for line in lines:
            line = line.strip()
            # Handle both "- README score: 1" and "README Score: 5/8" formats
            if line.lower().startswith(f"- {label.lower()}") or line.lower().startswith(label.lower()):
                # Extract score from format like "- README score: 1" or "README Score: 5/8"
                score_match = re.search(r'(\d+)(?:/\d+)?', line)
                if score_match:
                    return int(score_match.group(1))
        return 0
    except:
        return 0

def safe_extract_boolean(text, label):
    """Safely extract boolean from text with error handling"""
    try:
        lines = text.split('\n')
        for line in lines:
            line = line.strip()
            # Handle both "- Master script: True" and "Master Script: True" formats
            if line.lower().startswith(f"- {label.lower()}") or line.lower().startswith(label.lower()):
                return 'true' in line.lower() or 'yes' in line.lower()
        return False
    except:
        return False

def safe_extract_text(text, label):
    """Safely extract text after label with error handling"""
    try:
        lines = text.split('\n')
        for line in lines:
            line = line.strip()
            # Handle both "- Structure: custom_structure" and "Structure: custom_structure" formats
            if line.lower().startswith(f"- {label.lower()}") or line.lower().startswith(label.lower()):
                parts = line.split(':', 1)
                if len(parts) > 1:
                    return parts[1].strip()
        return ""
    except:
        return ""

def calculate_score(entry):
    """Calculate overall score for a repository"""
    score = 0
    score += entry.get('readme_score', 0)
    if entry.get('master_script', False):
        score += 3
    if entry.get('dependencies_documented', False):
        score += 2
    if entry.get('data_statement', False):
        score += 2
    if entry.get('structure') in ['standard_three_folder', 'src_data_results', 'replication_focused', 'modular_organized']:
        score += 2
    return score

def main():
    base_dir = Path(__file__).parent.parent
    reports_dir = base_dir / "reports"
    per_repo_dir = reports_dir / "per_repo"
    
    if not per_repo_dir.exists():
        print(f"Error: {per_repo_dir} does not exist")
        return
    
    entries = []
    
    # Process each markdown file
    for md_file in sorted(per_repo_dir.glob("*.md")):
        repo_name = md_file.stem
        try:
            content = md_file.read_text(encoding='utf-8')
            
            # Extract data with error handling
            entry = {
                'name': repo_name,
                'readme_score': safe_extract_score(content, "README score"),
                'master_script': safe_extract_boolean(content, "Master script"),
                'dependencies_documented': safe_extract_boolean(content, "Dependencies documented"),
                'data_statement': safe_extract_boolean(content, "Data statement"),
                'structure': safe_extract_text(content, "Structure")
            }
            
            entries.append(entry)
            
        except Exception as e:
            print(f"Warning: Could not process {repo_name}: {e}")
            # Add minimal entry to avoid missing data
            entries.append({
                'name': repo_name,
                'readme_score': 0,
                'master_script': False,
                'dependencies_documented': False,
                'data_statement': False,
                'structure': "unknown"
            })
    
    if not entries:
        print("No entries found")
        return
    
    # Calculate scores and sort
    scored_entries = []
    for entry in entries:
        score = calculate_score(entry)
        scored_entries.append((score, entry))
    
    # Sort by score (descending)
    scored_entries.sort(key=lambda x: x[0], reverse=True)
    
    # Get top and bottom 20
    top_20 = scored_entries[:20]
    bottom_20 = scored_entries[-20:]
    
    # Calculate statistics
    total = len(entries)
    avg_readme = sum(entry['readme_score'] for entry in entries) / total
    share_master = sum(1 for entry in entries if entry['master_script']) / total * 100
    share_deps = sum(1 for entry in entries if entry['dependencies_documented']) / total * 100
    share_data = sum(1 for entry in entries if entry['data_statement']) / total * 100
    
    # Generate overview report
    overview_lines = [
        "# Repository Overview Report",
        "",
        f"**Total Analyzed Repositories:** {total}",
        f"**Average README Score:** {avg_readme:.2f}/8",
        f"**Master Script Present:** {share_master:.1f}%",
        f"**Dependencies Documented:** {share_deps:.1f}%",
        f"**Data Availability Statement:** {share_data:.1f}%",
        "",
        "## Top 20 Best-Practice Repositories",
        ""
    ]
    
    for i, (score, entry) in enumerate(top_20, 1):
        overview_lines.append(f"{i}. **{entry['name']}** (Score: {score})")
        overview_lines.append(f"   - README Score: {entry['readme_score']}/8")
        overview_lines.append(f"   - Master Script: {'✓' if entry['master_script'] else '✗'}")
        overview_lines.append(f"   - Dependencies: {'✓' if entry['dependencies_documented'] else '✗'}")
        overview_lines.append(f"   - Data Statement: {'✓' if entry['data_statement'] else '✗'}")
        overview_lines.append("")
    
    overview_lines.extend([
        "## 20 Repositories Needing Most Improvement",
        ""
    ])
    
    for i, (score, entry) in enumerate(bottom_20, 1):
        overview_lines.append(f"{i}. **{entry['name']}** (Score: {score})")
        overview_lines.append(f"   - README Score: {entry['readme_score']}/8")
        overview_lines.append(f"   - Master Script: {'✓' if entry['master_script'] else '✗'}")
        overview_lines.append(f"   - Dependencies: {'✓' if entry['dependencies_documented'] else '✗'}")
        overview_lines.append(f"   - Data Statement: {'✓' if entry['data_statement'] else '✗'}")
        overview_lines.append("")
    
    overview_lines.extend([
        "## Key Insights and Recommendations",
        "",
        "### Most Common Issues:",
        f"- {100-share_master:.1f}% of repositories lack a clear master script",
        f"- {100-share_deps:.1f}% of repositories don't document dependencies",
        f"- {100-share_data:.1f}% of repositories lack data availability statements",
        f"- Average README quality is {avg_readme:.2f}/8, indicating room for improvement",
        "",
        "### Actionable Recommendations:",
        "1. **Add Master Scripts**: Create clear entry points (master.do, run.sh, main.py)",
        "2. **Improve Documentation**: Enhance README files with setup instructions and requirements",
        "3. **Document Dependencies**: Provide requirements.txt, environment.yml, or package lists",
        "4. **Data Statements**: Include clear data availability and access information",
        "5. **Standardize Structure**: Adopt consistent folder organization (data/, code/, output/)",
        "",
        "### Best Practices from Top Repositories:",
        "- Clear, comprehensive README files with step-by-step instructions",
        "- Well-documented dependencies and environment setup",
        "- Modular code organization with logical folder structure",
        "- Data availability statements and access instructions",
        "- Master scripts that orchestrate the entire replication process"
    ])
    
    # Write overview report
    overview_file = reports_dir / "overview.md"
    overview_file.write_text('\n'.join(overview_lines), encoding='utf-8')
    
    print(f"✅ Generated overview report: {overview_file}")
    print(f"📊 Processed {total} repositories")
    print(f"🏆 Top repository: {top_20[0][1]['name']} (Score: {top_20[0][0]})")
    print(f"📈 Average README score: {avg_readme:.2f}/8")

if __name__ == "__main__":
    main()
