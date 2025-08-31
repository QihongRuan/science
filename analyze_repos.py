#!/usr/bin/env python3
"""
Comprehensive analysis of AEA replication packages
Extracts patterns, best practices, and insights from 158 repositories
"""

import os
import json
import glob
from pathlib import Path
from collections import defaultdict, Counter
import re

class AEARepositoryAnalyzer:
    def __init__(self, base_path):
        self.base_path = Path(base_path)
        self.repos = list(self.base_path.glob("*/"))
        self.analysis_results = {
            'total_repos': len(self.repos),
            'structure_patterns': {},
            'documentation': {},
            'programming_languages': {},
            'best_practices': {},
            'common_issues': {},
            'statistical_methods': {},
            'reproducibility_features': {}
        }
    
    def analyze_all(self):
        """Run complete analysis suite"""
        print(f"Analyzing {len(self.repos)} repositories...")
        
        # Initialize counters
        language_files = defaultdict(int)
        readme_quality = []
        folder_structures = []
        master_scripts = []
        data_statements = []
        dependencies_docs = []
        
        for i, repo in enumerate(self.repos, 1):
            if i % 20 == 0:
                print(f"Progress: {i}/{len(self.repos)} repositories analyzed")
            
            repo_analysis = self.analyze_single_repo(repo)
            
            # Aggregate results
            for lang, count in repo_analysis['languages'].items():
                language_files[lang] += count
            
            readme_quality.append(repo_analysis['readme_score'])
            folder_structures.append(repo_analysis['structure_type'])
            
            if repo_analysis['has_master_script']:
                master_scripts.append(repo.name)
            
            if repo_analysis['has_data_statement']:
                data_statements.append(repo.name)
            
            if repo_analysis['has_dependencies']:
                dependencies_docs.append(repo.name)
        
        # Compile final statistics
        self.compile_statistics(language_files, readme_quality, 
                              folder_structures, master_scripts,
                              data_statements, dependencies_docs)
        
        return self.analysis_results
    
    def analyze_single_repo(self, repo_path):
        """Analyze individual repository"""
        analysis = {
            'name': repo_path.name,
            'languages': self.detect_languages(repo_path),
            'structure_type': self.classify_structure(repo_path),
            'readme_score': self.assess_readme(repo_path),
            'has_master_script': self.check_master_script(repo_path),
            'has_data_statement': self.check_data_statement(repo_path),
            'has_dependencies': self.check_dependencies(repo_path),
            'code_organization': self.assess_code_organization(repo_path),
            'statistical_methods': self.detect_statistical_methods(repo_path)
        }
        return analysis
    
    def detect_languages(self, repo_path):
        """Count files by programming language"""
        extensions = {
            '.do': 'Stata',
            '.m': 'MATLAB',
            '.py': 'Python',
            '.R': 'R',
            '.jl': 'Julia',
            '.sas': 'SAS',
            '.cpp': 'C++',
            '.f90': 'Fortran'
        }
        
        counts = defaultdict(int)
        for ext, lang in extensions.items():
            files = list(repo_path.rglob(f"*{ext}"))
            if files:
                counts[lang] = len(files)
        
        return counts
    
    def classify_structure(self, repo_path):
        """Classify repository structure pattern"""
        subdirs = [d.name.lower() for d in repo_path.iterdir() if d.is_dir()]
        
        # Check for standard patterns
        if all(d in subdirs for d in ['data', 'code', 'output']):
            return 'standard_three_folder'
        elif all(d in subdirs for d in ['src', 'data', 'results']):
            return 'src_data_results'
        elif 'replication' in subdirs:
            return 'replication_focused'
        elif all(d in subdirs for d in ['do', 'log', 'data']):
            return 'stata_traditional'
        elif len(subdirs) > 10:
            return 'complex_multi_folder'
        elif len(subdirs) < 3:
            return 'minimal_structure'
        else:
            return 'custom_structure'
    
    def assess_readme(self, repo_path):
        """Score README comprehensiveness"""
        readme_files = list(repo_path.glob("README*"))
        if not readme_files:
            return 0
        
        score = 0
        readme_content = ""
        
        for readme in readme_files:
            try:
                with open(readme, 'r', encoding='utf-8', errors='ignore') as f:
                    readme_content += f.read().lower()
            except:
                continue
        
        # Check for key sections
        key_sections = {
            'requirements': ['requirement', 'dependencies', 'software', 'version'],
            'data': ['data', 'dataset', 'source'],
            'instructions': ['instruction', 'how to', 'steps', 'run', 'execute'],
            'files': ['file', 'structure', 'organization'],
            'output': ['output', 'results', 'tables', 'figures'],
            'authors': ['author', 'contact'],
            'license': ['license', 'copyright'],
            'citation': ['citation', 'cite', 'reference']
        }
        
        for section, keywords in key_sections.items():
            if any(keyword in readme_content for keyword in keywords):
                score += 1
        
        return score
    
    def check_master_script(self, repo_path):
        """Check for master execution script"""
        master_patterns = ['master*', 'main*', 'run*', '_RunAll*', '00_*', '0_*']
        
        for pattern in master_patterns:
            if list(repo_path.glob(pattern)):
                return True
        
        return False
    
    def check_data_statement(self, repo_path):
        """Check for data availability statement"""
        data_files = ['Data_Availability*', 'data_statement*', 'DAS*']
        readme_files = list(repo_path.glob("README*"))
        
        # Check dedicated files
        for pattern in data_files:
            if list(repo_path.glob(pattern)):
                return True
        
        # Check in README
        for readme in readme_files:
            try:
                with open(readme, 'r', encoding='utf-8', errors='ignore') as f:
                    content = f.read().lower()
                    if 'data availability' in content or 'data access' in content:
                        return True
            except:
                continue
        
        return False
    
    def check_dependencies(self, repo_path):
        """Check for dependency documentation"""
        dep_files = ['requirements.txt', 'environment.yml', 'packages.R', 
                    'stata.trk', 'dependencies*', 'packages*']
        
        for pattern in dep_files:
            if list(repo_path.glob(pattern)):
                return True
        
        return False
    
    def assess_code_organization(self, repo_path):
        """Assess code organization quality"""
        code_files = list(repo_path.glob("**/*.do")) + \
                    list(repo_path.glob("**/*.R")) + \
                    list(repo_path.glob("**/*.py")) + \
                    list(repo_path.glob("**/*.m"))
        
        if not code_files:
            return 'no_code'
        
        # Check for numbered files (indicating order)
        numbered = sum(1 for f in code_files if re.match(r'^\d+', f.name))
        
        # Check for modular organization
        unique_dirs = len(set(f.parent for f in code_files))
        
        if numbered > len(code_files) * 0.5:
            return 'numbered_sequential'
        elif unique_dirs > 3:
            return 'modular_organized'
        elif len(code_files) < 5:
            return 'simple_few_files'
        else:
            return 'standard_organization'
    
    def detect_statistical_methods(self, repo_path):
        """Detect statistical methods used"""
        methods = []
        code_files = list(repo_path.glob("**/*.do")) + \
                    list(repo_path.glob("**/*.R")) + \
                    list(repo_path.glob("**/*.py"))
        
        # Keywords for different methods
        method_keywords = {
            'OLS': ['regress', 'lm(', 'ols', 'regression'],
            'IV': ['ivregress', 'ivreg', 'instrument', '2sls', 'tsls'],
            'Panel': ['xtreg', 'plm', 'panel', 'fixed effect', 'random effect'],
            'DID': ['diff-in-diff', 'difference-in-difference', 'did', 'event study'],
            'RDD': ['rdrobust', 'rdd', 'regression discontinuity', 'fuzzy rd'],
            'ML': ['random forest', 'neural', 'lasso', 'ridge', 'elastic net',
                  'machine learning', 'cross-validation', 'sklearn'],
            'Structural': ['gmm', 'maximum likelihood', 'mle', 'structural model'],
            'Time Series': ['arima', 'var', 'vecm', 'cointegration', 'unit root'],
            'Causal': ['causal', 'treatment effect', 'ate', 'att', 'propensity'],
            'Bayesian': ['bayes', 'mcmc', 'prior', 'posterior', 'gibbs']
        }
        
        content = ""
        for f in code_files[:20]:  # Sample first 20 files
            try:
                with open(f, 'r', encoding='utf-8', errors='ignore') as file:
                    content += file.read().lower()
            except:
                continue
        
        for method, keywords in method_keywords.items():
            if any(keyword in content for keyword in keywords):
                methods.append(method)
        
        return methods
    
    def compile_statistics(self, language_files, readme_quality, 
                          folder_structures, master_scripts,
                          data_statements, dependencies_docs):
        """Compile final statistics and insights"""
        
        # Language distribution
        total_files = sum(language_files.values())
        self.analysis_results['programming_languages'] = {
            'distribution': dict(language_files),
            'percentages': {lang: (count/total_files*100) 
                          for lang, count in language_files.items()},
            'dominant': max(language_files, key=language_files.get)
        }
        
        # Documentation quality
        avg_readme_score = sum(readme_quality) / len(readme_quality)
        self.analysis_results['documentation'] = {
            'average_readme_score': avg_readme_score,
            'high_quality_repos': sum(1 for s in readme_quality if s >= 6),
            'poor_documentation': sum(1 for s in readme_quality if s <= 2),
            'has_data_statements': len(data_statements),
            'has_dependencies': len(dependencies_docs)
        }
        
        # Structure patterns
        structure_counts = Counter(folder_structures)
        self.analysis_results['structure_patterns'] = dict(structure_counts)
        
        # Reproducibility features
        self.analysis_results['reproducibility_features'] = {
            'master_scripts': len(master_scripts),
            'percentage_with_master': (len(master_scripts) / len(self.repos) * 100)
        }
        
        # Best practices identification
        self.identify_best_practices(master_scripts, data_statements, 
                                    dependencies_docs, readme_quality)
    
    def identify_best_practices(self, master_scripts, data_statements, 
                               dependencies_docs, readme_quality):
        """Identify repos following best practices"""
        
        # Find repos with high scores across multiple dimensions
        repo_scores = {}
        
        for i, repo in enumerate(self.repos):
            score = 0
            repo_name = repo.name
            
            # Check various quality indicators
            if repo_name in master_scripts:
                score += 2
            if repo_name in data_statements:
                score += 2
            if repo_name in dependencies_docs:
                score += 2
            if i < len(readme_quality) and readme_quality[i] >= 6:
                score += 3
            
            repo_scores[repo_name] = score
        
        # Top 10% repos
        sorted_repos = sorted(repo_scores.items(), key=lambda x: x[1], reverse=True)
        top_10_percent = int(len(sorted_repos) * 0.1)
        
        self.analysis_results['best_practices'] = {
            'top_repositories': sorted_repos[:top_10_percent],
            'common_features': self.extract_common_features(sorted_repos[:top_10_percent])
        }
    
    def extract_common_features(self, top_repos):
        """Extract common features from top repositories"""
        features = []
        
        if not top_repos:
            return features
        
        # Analyze top repos for common patterns
        for repo_name, score in top_repos[:5]:
            repo_path = self.base_path / repo_name
            
            # Check for specific good practices
            if list(repo_path.glob("*master*")):
                features.append("Has master script")
            if list(repo_path.glob("*test*")):
                features.append("Includes tests")
            if list(repo_path.glob("*log*")):
                features.append("Maintains logs")
        
        return list(set(features))
    
    def generate_report(self):
        """Generate comprehensive report"""
        report = []
        report.append("=" * 80)
        report.append("AEA REPLICATION PACKAGES: COMPREHENSIVE ANALYSIS REPORT")
        report.append("=" * 80)
        report.append(f"\nTotal Repositories Analyzed: {self.analysis_results['total_repos']}")
        
        report.append("\n" + "=" * 40)
        report.append("PROGRAMMING LANGUAGE DISTRIBUTION")
        report.append("=" * 40)
        for lang, pct in self.analysis_results['programming_languages']['percentages'].items():
            report.append(f"{lang}: {pct:.1f}%")
        
        report.append("\n" + "=" * 40)
        report.append("DOCUMENTATION QUALITY")
        report.append("=" * 40)
        doc = self.analysis_results['documentation']
        report.append(f"Average README Score: {doc['average_readme_score']:.2f}/8")
        report.append(f"High Quality Documentation: {doc['high_quality_repos']} repos")
        report.append(f"Poor Documentation: {doc['poor_documentation']} repos")
        report.append(f"Has Data Statements: {doc['has_data_statements']} repos")
        report.append(f"Documents Dependencies: {doc['has_dependencies']} repos")
        
        report.append("\n" + "=" * 40)
        report.append("REPOSITORY STRUCTURE PATTERNS")
        report.append("=" * 40)
        for pattern, count in self.analysis_results['structure_patterns'].items():
            report.append(f"{pattern}: {count} repos")
        
        report.append("\n" + "=" * 40)
        report.append("REPRODUCIBILITY FEATURES")
        report.append("=" * 40)
        repro = self.analysis_results['reproducibility_features']
        report.append(f"Has Master Scripts: {repro['master_scripts']} repos ({repro['percentage_with_master']:.1f}%)")
        
        report.append("\n" + "=" * 40)
        report.append("TOP REPOSITORIES (BEST PRACTICES)")
        report.append("=" * 40)
        for repo, score in self.analysis_results['best_practices']['top_repositories'][:10]:
            report.append(f"{repo}: Score {score}/9")
        
        return "\n".join(report)

# Run analysis
if __name__ == "__main__":
    analyzer = AEARepositoryAnalyzer("AEAREP-103-ssh/aea_packages_complete")
    results = analyzer.analyze_all()
    report = analyzer.generate_report()
    
    print("\n" + report)
    
    # Save results
    with open("aea_analysis_results.json", "w") as f:
        json.dump(results, f, indent=2, default=str)
    
    with open("aea_analysis_report.txt", "w") as f:
        f.write(report)
    
    print("\n✅ Analysis complete! Results saved to:")
    print("  - aea_analysis_results.json")
    print("  - aea_analysis_report.txt")