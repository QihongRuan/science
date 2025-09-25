#!/usr/bin/env python3
"""
Comprehensive analysis of economic research content in AEA replication packages
"""

import os
import re
import json
from pathlib import Path
from collections import defaultdict, Counter
import pandas as pd

class EconomicContentAnalyzer:
    def __init__(self, base_dir):
        self.base_dir = Path(base_dir)
        self.results = {
            'economic_topics': defaultdict(int),
            'policy_areas': defaultdict(int),
            'data_sources': defaultdict(int),
            'research_questions': defaultdict(int),
            'methodological_approaches': defaultdict(int),
            'geographic_focus': defaultdict(int),
            'time_periods': defaultdict(int),
            'sample_sizes': defaultdict(int),
            'key_findings': [],
            'repo_details': {}
        }
        
        # Economic topic keywords
        self.economic_topics = {
            'macroeconomic': ['gdp', 'inflation', 'unemployment', 'monetary policy', 'fiscal policy', 
                            'business cycle', 'recession', 'growth', 'productivity', 'interest rate'],
            'labor': ['wage', 'employment', 'labor market', 'human capital', 'education', 
                     'training', 'job search', 'unemployment', 'labor supply', 'labor demand'],
            'development': ['poverty', 'inequality', 'development', 'aid', 'microfinance', 
                          'infrastructure', 'health', 'nutrition', 'sanitation', 'education'],
            'trade': ['trade', 'export', 'import', 'tariff', 'trade policy', 'exchange rate', 
                     'balance of payments', 'fdi', 'foreign investment', 'globalization'],
            'finance': ['banking', 'financial markets', 'credit', 'lending', 'risk', 
                       'portfolio', 'asset pricing', 'financial crisis', 'regulation'],
            'environment': ['climate', 'pollution', 'carbon', 'renewable', 'energy', 
                          'environmental policy', 'sustainability', 'green'],
            'health': ['health', 'medical', 'healthcare', 'insurance', 'mortality', 
                      'morbidity', 'treatment', 'hospital', 'doctor'],
            'education': ['school', 'student', 'teacher', 'test score', 'college', 
                         'university', 'learning', 'achievement', 'dropout'],
            'urban': ['city', 'urban', 'rural', 'migration', 'housing', 'transportation', 
                     'infrastructure', 'spatial', 'agglomeration'],
            'behavioral': ['behavior', 'preference', 'choice', 'decision', 'bias', 
                          'nudge', 'experiment', 'survey', 'attitude']
        }
        
        # Policy areas
        self.policy_areas = {
            'education_policy': ['education policy', 'school choice', 'voucher', 'charter school', 
                               'teacher quality', 'curriculum', 'testing'],
            'health_policy': ['health policy', 'medicare', 'medicaid', 'health insurance', 
                            'public health', 'vaccination', 'prevention'],
            'labor_policy': ['minimum wage', 'labor regulation', 'unemployment insurance', 
                           'job training', 'workplace safety', 'union'],
            'trade_policy': ['trade agreement', 'tariff', 'quota', 'trade war', 'wto', 
                           'free trade', 'protectionism'],
            'monetary_policy': ['monetary policy', 'interest rate', 'quantitative easing', 
                              'inflation targeting', 'central bank', 'federal reserve'],
            'fiscal_policy': ['fiscal policy', 'tax', 'government spending', 'deficit', 
                            'debt', 'stimulus', 'austerity'],
            'environmental_policy': ['environmental policy', 'carbon tax', 'cap and trade', 
                                   'renewable energy', 'emissions', 'clean air'],
            'social_policy': ['welfare', 'social security', 'pension', 'childcare', 
                            'family policy', 'social assistance']
        }
        
        # Data sources
        self.data_sources = {
            'survey': ['survey', 'census', 'household', 'individual', 'panel', 'longitudinal'],
            'administrative': ['administrative', 'government', 'official', 'registry', 'records'],
            'experimental': ['experiment', 'randomized', 'treatment', 'control', 'rct'],
            'financial': ['financial', 'stock', 'bond', 'market', 'trading', 'price'],
            'trade': ['trade', 'export', 'import', 'customs', 'bilateral'],
            'satellite': ['satellite', 'night lights', 'remote sensing', 'imagery'],
            'text': ['text', 'news', 'speech', 'document', 'narrative', 'sentiment']
        }

    def analyze_repo(self, repo_path):
        """Analyze a single repository for economic content"""
        repo_name = repo_path.name
        repo_info = {
            'name': repo_name,
            'economic_topics': set(),
            'policy_areas': set(),
            'data_sources': set(),
            'methods': set(),
            'geographic_focus': set(),
            'time_period': None,
            'sample_size': None,
            'key_findings': []
        }
        
        # Search through all files in the repository
        for file_path in repo_path.rglob('*'):
            if file_path.is_file() and file_path.suffix in ['.do', '.py', '.R', '.md', '.txt', '.pdf']:
                try:
                    content = file_path.read_text(encoding='utf-8', errors='ignore').lower()
                    self._analyze_content(content, repo_info, file_path)
                except:
                    continue
        
        return repo_info

    def _analyze_content(self, content, repo_info, file_path):
        """Analyze content for economic indicators"""
        
        # Economic topics
        for topic, keywords in self.economic_topics.items():
            for keyword in keywords:
                if keyword in content:
                    repo_info['economic_topics'].add(topic)
                    self.results['economic_topics'][topic] += 1
        
        # Policy areas
        for policy, keywords in self.policy_areas.items():
            for keyword in keywords:
                if keyword in content:
                    repo_info['policy_areas'].add(policy)
                    self.results['policy_areas'][policy] += 1
        
        # Data sources
        for source, keywords in self.data_sources.items():
            for keyword in keywords:
                if keyword in content:
                    repo_info['data_sources'].add(source)
                    self.results['data_sources'][source] += 1
        
        # Geographic focus
        countries = ['usa', 'united states', 'china', 'india', 'brazil', 'mexico', 'germany', 
                    'france', 'uk', 'japan', 'korea', 'canada', 'australia', 'africa', 'europe', 
                    'asia', 'latin america', 'developing', 'developed']
        for country in countries:
            if country in content:
                repo_info['geographic_focus'].add(country)
                self.results['geographic_focus'][country] += 1
        
        # Time periods
        time_patterns = [
            r'19\d{2}',  # 1900s
            r'20\d{2}',  # 2000s
            r'period.*(\d{4})',  # period mentions
            r'from.*(\d{4}).*to.*(\d{4})',  # date ranges
        ]
        for pattern in time_patterns:
            matches = re.findall(pattern, content)
            if matches:
                repo_info['time_period'] = matches[0] if isinstance(matches[0], str) else matches[0][0]
                break
        
        # Sample sizes
        sample_patterns = [
            r'sample.*?(\d+(?:,\d{3})*)',
            r'n\s*=\s*(\d+(?:,\d{3})*)',
            r'observations.*?(\d+(?:,\d{3})*)',
            r'(\d+(?:,\d{3})*)\s*observations'
        ]
        for pattern in sample_patterns:
            matches = re.findall(pattern, content)
            if matches:
                try:
                    size = int(matches[0].replace(',', ''))
                    if 100 <= size <= 10000000:  # Reasonable sample size range
                        repo_info['sample_size'] = size
                        break
                except:
                    continue
        
        # Methodological approaches
        methods = ['ols', 'iv', '2sls', 'did', 'rdd', 'matching', 'bootstrap', 'bayesian', 
                  'machine learning', 'ml', 'random forest', 'neural network', 'panel', 
                  'fixed effects', 'random effects', 'gmm', 'structural', 'calibration']
        for method in methods:
            if method in content:
                repo_info['methods'].add(method)
                self.results['methodological_approaches'][method] += 1

    def analyze_all_repos(self):
        """Analyze all repositories"""
        print("Starting comprehensive economic content analysis...")
        
        repo_dirs = []
        for pattern in ['aearep-*', 'AEAREP-*', 'training-*', 'TRAINING-*']:
            repo_dirs.extend(self.base_dir.glob(pattern))
        
        print(f"Found {len(repo_dirs)} repositories to analyze")
        
        for i, repo_path in enumerate(repo_dirs):
            if repo_path.is_dir():
                print(f"Analyzing {i+1}/{len(repo_dirs)}: {repo_path.name}")
                repo_info = self.analyze_repo(repo_path)
                self.results['repo_details'][repo_path.name] = repo_info
                
                # Extract key findings from README or main files
                self._extract_key_findings(repo_path, repo_info)
        
        print("Analysis complete!")

    def _extract_key_findings(self, repo_path, repo_info):
        """Extract key findings from repository files"""
        key_files = ['README.md', 'README.txt', 'REPLICATION.md', 'main.do', 'master.do']
        
        for file_name in key_files:
            file_path = repo_path / file_name
            if file_path.exists():
                try:
                    content = file_path.read_text(encoding='utf-8', errors='ignore')
                    # Look for key findings patterns
                    findings = re.findall(r'(?:finding|result|conclusion).*?[.!]', content, re.IGNORECASE)
                    if findings:
                        repo_info['key_findings'].extend(findings[:3])  # Top 3 findings
                        break
                except:
                    continue

    def generate_report(self):
        """Generate comprehensive economic content report"""
        report = []
        report.append("=" * 80)
        report.append("COMPREHENSIVE ECONOMIC RESEARCH CONTENT ANALYSIS")
        report.append("=" * 80)
        report.append(f"Total Repositories Analyzed: {len(self.results['repo_details'])}")
        report.append("")
        
        # Economic Topics
        report.append("ECONOMIC RESEARCH TOPICS")
        report.append("-" * 40)
        for topic, count in sorted(self.results['economic_topics'].items(), key=lambda x: x[1], reverse=True):
            percentage = (count / len(self.results['repo_details'])) * 100
            report.append(f"{topic}: {count} repos ({percentage:.1f}%)")
        report.append("")
        
        # Policy Areas
        report.append("POLICY RESEARCH AREAS")
        report.append("-" * 40)
        for policy, count in sorted(self.results['policy_areas'].items(), key=lambda x: x[1], reverse=True):
            percentage = (count / len(self.results['repo_details'])) * 100
            report.append(f"{policy}: {count} repos ({percentage:.1f}%)")
        report.append("")
        
        # Data Sources
        report.append("DATA SOURCES")
        report.append("-" * 40)
        for source, count in sorted(self.results['data_sources'].items(), key=lambda x: x[1], reverse=True):
            percentage = (count / len(self.results['repo_details'])) * 100
            report.append(f"{source}: {count} repos ({percentage:.1f}%)")
        report.append("")
        
        # Geographic Focus
        report.append("GEOGRAPHIC FOCUS")
        report.append("-" * 40)
        for geo, count in sorted(self.results['geographic_focus'].items(), key=lambda x: x[1], reverse=True)[:15]:
            percentage = (count / len(self.results['repo_details'])) * 100
            report.append(f"{geo}: {count} repos ({percentage:.1f}%)")
        report.append("")
        
        # Methodological Approaches
        report.append("METHODOLOGICAL APPROACHES")
        report.append("-" * 40)
        for method, count in sorted(self.results['methodological_approaches'].items(), key=lambda x: x[1], reverse=True)[:20]:
            percentage = (count / len(self.results['repo_details'])) * 100
            report.append(f"{method}: {count} repos ({percentage:.1f}%)")
        report.append("")
        
        # Sample Size Distribution
        sample_sizes = [info['sample_size'] for info in self.results['repo_details'].values() if info['sample_size']]
        if sample_sizes:
            report.append("SAMPLE SIZE DISTRIBUTION")
            report.append("-" * 40)
            size_ranges = {
                'Small (<1K)': sum(1 for s in sample_sizes if s < 1000),
                'Medium (1K-10K)': sum(1 for s in sample_sizes if 1000 <= s < 10000),
                'Large (10K-100K)': sum(1 for s in sample_sizes if 10000 <= s < 100000),
                'Very Large (>100K)': sum(1 for s in sample_sizes if s >= 100000)
            }
            for range_name, count in size_ranges.items():
                percentage = (count / len(sample_sizes)) * 100
                report.append(f"{range_name}: {count} repos ({percentage:.1f}%)")
            report.append("")
        
        # Top Repositories by Topic Coverage
        report.append("TOP REPOSITORIES BY TOPIC COVERAGE")
        report.append("-" * 40)
        topic_coverage = []
        for repo_name, info in self.results['repo_details'].items():
            coverage = len(info['economic_topics']) + len(info['policy_areas']) + len(info['data_sources'])
            topic_coverage.append((repo_name, coverage, info))
        
        topic_coverage.sort(key=lambda x: x[1], reverse=True)
        for repo_name, coverage, info in topic_coverage[:10]:
            topics = ', '.join(list(info['economic_topics'])[:3])
            report.append(f"{repo_name}: {coverage} topics ({topics})")
        report.append("")
        
        return '\n'.join(report)

    def save_results(self):
        """Save results to files"""
        # Save detailed results as JSON
        with open(self.base_dir / 'economic_content_analysis.json', 'w') as f:
            json.dump(self.results, f, indent=2, default=str)
        
        # Save summary report
        report = self.generate_report()
        with open(self.base_dir / 'economic_content_report.txt', 'w') as f:
            f.write(report)
        
        print(f"Results saved to economic_content_analysis.json and economic_content_report.txt")

def main():
    base_dir = Path(__file__).parent.parent
    analyzer = EconomicContentAnalyzer(base_dir)
    analyzer.analyze_all_repos()
    analyzer.save_results()

if __name__ == "__main__":
    main()
