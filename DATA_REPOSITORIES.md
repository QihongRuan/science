# Data Repositories Reference

This document describes the large data repositories that are stored locally but not included in this Git repository due to size constraints.

## Repository Contents

### AEAREP-103-ssh/ (14GB)
- **Description**: Complete SSH-accessible AEA replication packages
- **Size**: 14GB
- **Contents**: 
  - Full AEA replication packages with code and data
  - Analysis results and extracted insights
  - PDF proof files and documentation
- **Status**: Local clone, not pushed to GitHub due to size
- **Access**: Available in local development environment

### aea_replication_packages/ (152KB)
- **Description**: Lightweight replication package references
- **Size**: 152KB  
- **Contents**:
  - 10.1257-aer.104.12.4231-lv39/ - AER paper replication
  - AEAREP-103/ - Core analysis repository
- **Status**: Contains nested git repositories
- **Access**: Submodules of larger research datasets

## Data Access Notes

These repositories contain:
1. **Proprietary research data** - May have access restrictions
2. **Large binary files** - Not suitable for standard git repositories
3. **Nested git structures** - Require special handling as submodules
4. **Analysis outputs** - Generated from source data processing

## Recommendations

For full data access:
1. Contact repository maintainer for specific datasets
2. Use analysis scripts in `/scripts/` directory to regenerate results
3. Reference extracted insights in markdown documentation files
4. Consider using Git LFS for large file management in future

## Generated Analysis Files

The following files in this repository contain extracted insights from these data repositories:
- `AER_REMARKABLE_FINDINGS.md`
- `COMPREHENSIVE_INSIGHTS_REPORT.md`
- `CRITICAL_INSIGHTS.md`
- `aea_analysis_results.json`
- `aea_analysis_report.txt`