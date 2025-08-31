#!/usr/bin/env python3
"""
Analyze econometric and statistical methods used in AEA replication packages
"""

import os
import re
from pathlib import Path
from collections import Counter, defaultdict

class EconometricAnalyzer:
    def __init__(self, base_path):
        self.base_path = Path(base_path)
        self.methods_found = defaultdict(list)
        self.stata_commands = {
            'OLS': ['regress ', 'reg ', 'areg '],
            'Panel': ['xtreg', 'xtset', 'xtlogit', 'xtprobit', 'xttobit', 'xtivreg'],
            'IV/2SLS': ['ivregress', 'ivreg2', 'xtivreg', '2sls'],
            'Probit/Logit': ['probit', 'logit', 'mlogit', 'ologit', 'oprobit'],
            'Tobit': ['tobit', 'xttobit'],
            'DID': ['diff', 'did_', 'event_study', 'twfe'],
            'RDD': ['rdrobust', 'rddensity', 'rdplot'],
            'Matching': ['psmatch', 'nnmatch', 'teffects'],
            'Quantile': ['qreg', 'xtqreg', 'quantile'],
            'GMM': ['gmm', 'xtabond', 'xtdpdsys'],
            'Time Series': ['arima', 'var', 'vec', 'dfuller', 'dfgls'],
            'Survival': ['stcox', 'streg', 'stset'],
            'Structural': ['ml model', 'nlsur', 'nl '],
            'Bootstrap': ['bootstrap', 'boottest'],
            'Clustering': ['cluster', 'vce(cluster'],
            'Fixed Effects': [' fe ', 'absorb(', 'reghdfe'],
            'Random Effects': [' re ', 'mixed', 'xtmixed'],
            'Synthetic Control': ['synth', 'synth_runner'],
            'Machine Learning': ['lasso', 'elasticnet', 'randomforest']
        }
        
        self.r_methods = {
            'OLS': ['lm(', 'glm('],
            'Panel': ['plm', 'pdata.frame', 'fixest'],
            'IV': ['ivreg', 'tsls'],
            'Causal': ['did', 'rdrobust', 'synthdid'],
            'ML': ['randomForest', 'glmnet', 'xgboost', 'caret'],
            'Bayesian': ['brm', 'stan', 'MCMCpack'],
            'Time Series': ['arima', 'VAR', 'forecast']
        }
        
        self.python_methods = {
            'OLS': ['OLS', 'sm.OLS', 'LinearRegression'],
            'Panel': ['PanelOLS', 'RandomEffects', 'FixedEffect'],
            'ML': ['sklearn', 'RandomForest', 'XGBoost', 'tensorflow', 'pytorch'],
            'Causal': ['DoWhy', 'CausalML', 'EconML'],
            'Time Series': ['ARIMA', 'VAR', 'statsmodels.tsa']
        }
    
    def analyze_all_repos(self):
        """Analyze all repositories for econometric methods"""
        print("Analyzing econometric methods across repositories...")
        
        stata_methods = Counter()
        r_methods = Counter()
        python_methods = Counter()
        
        repos = list(self.base_path.glob("*/"))
        
        for i, repo in enumerate(repos, 1):
            if i % 20 == 0:
                print(f"Progress: {i}/{len(repos)} repositories")
            
            # Analyze Stata files
            for do_file in repo.rglob("*.do"):
                content = self.read_file(do_file)
                for method, patterns in self.stata_commands.items():
                    if any(pattern in content.lower() for pattern in patterns):
                        stata_methods[method] += 1
                        self.methods_found[method].append(repo.name)
            
            # Analyze R files
            for r_file in repo.rglob("*.R"):
                content = self.read_file(r_file)
                for method, patterns in self.r_methods.items():
                    if any(pattern in content for pattern in patterns):
                        r_methods[method] += 1
            
            # Analyze Python files
            for py_file in repo.rglob("*.py"):
                content = self.read_file(py_file)
                for method, patterns in self.python_methods.items():
                    if any(pattern in content for pattern in patterns):
                        python_methods[method] += 1
        
        return {
            'stata': stata_methods,
            'r': r_methods,
            'python': python_methods
        }
    
    def read_file(self, filepath):
        """Read file content safely"""
        try:
            with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
                return f.read()
        except:
            return ""
    
    def analyze_robustness_checks(self):
        """Look for robustness check patterns"""
        robustness_patterns = {
            'alternative_specifications': ['robust', 'alternative', 'specification'],
            'sensitivity_analysis': ['sensitivity', 'sens_'],
            'placebo_tests': ['placebo', 'falsification'],
            'bootstrap': ['bootstrap', 'boot'],
            'jackknife': ['jackknife', 'jknife'],
            'cross_validation': ['crossval', 'cv', 'kfold'],
            'heterogeneity': ['heterogen', 'subgroup', 'subsample'],
            'winsorize': ['winsor', 'trim', 'outlier']
        }
        
        robustness_counts = Counter()
        
        for repo in self.base_path.glob("*/"):
            for do_file in repo.rglob("*.do"):
                content = self.read_file(do_file).lower()
                for check_type, patterns in robustness_patterns.items():
                    if any(pattern in content for pattern in patterns):
                        robustness_counts[check_type] += 1
        
        return robustness_counts
    
    def analyze_data_cleaning(self):
        """Analyze data cleaning practices"""
        cleaning_patterns = {
            'missing_values': ['missing', 'impute', 'drop if', 'keep if'],
            'outliers': ['outlier', 'winsor', 'trim', 'percentile'],
            'duplicates': ['duplicates', 'unique', 'distinct'],
            'merging': ['merge', 'append', 'joinby'],
            'reshaping': ['reshape', 'transpose', 'wide', 'long'],
            'recoding': ['recode', 'replace', 'generate', 'egen']
        }
        
        cleaning_counts = Counter()
        
        for repo in self.base_path.glob("*/"):
            for do_file in repo.rglob("*.do"):
                content = self.read_file(do_file).lower()
                for practice, patterns in cleaning_patterns.items():
                    if any(pattern in content for pattern in patterns):
                        cleaning_counts[practice] += 1
        
        return cleaning_counts
    
    def identify_advanced_techniques(self):
        """Identify use of advanced/modern techniques"""
        advanced = {
            'machine_learning': [],
            'causal_inference': [],
            'structural_models': [],
            'bayesian': [],
            'text_analysis': [],
            'network_analysis': []
        }
        
        ml_keywords = ['lasso', 'ridge', 'elastic', 'random forest', 'xgboost', 
                       'neural', 'deep learning', 'cross-validation']
        causal_keywords = ['rdd', 'regression discontinuity', 'synthetic control',
                          'did', 'difference-in-difference', 'instrumental variable',
                          'propensity score', 'matching']
        structural_keywords = ['structural model', 'gmm', 'maximum likelihood',
                             'simulated method', 'indirect inference']
        bayesian_keywords = ['bayes', 'mcmc', 'prior', 'posterior', 'stan', 'gibbs']
        
        for repo in self.base_path.glob("*/"):
            all_code = ""
            for ext in ['*.do', '*.R', '*.py', '*.m']:
                for file in repo.glob(f"**/{ext}"):
                    all_code += self.read_file(file).lower()
            
            if any(kw in all_code for kw in ml_keywords):
                advanced['machine_learning'].append(repo.name)
            if any(kw in all_code for kw in causal_keywords):
                advanced['causal_inference'].append(repo.name)
            if any(kw in all_code for kw in structural_keywords):
                advanced['structural_models'].append(repo.name)
            if any(kw in all_code for kw in bayesian_keywords):
                advanced['bayesian'].append(repo.name)
            if 'nltk' in all_code or 'spacy' in all_code or 'text mining' in all_code:
                advanced['text_analysis'].append(repo.name)
            if 'networkx' in all_code or 'igraph' in all_code or 'network' in all_code:
                advanced['network_analysis'].append(repo.name)
        
        return advanced
    
    def generate_report(self, methods_data, robustness_data, cleaning_data, advanced_data):
        """Generate comprehensive econometric analysis report"""
        report = []
        report.append("=" * 80)
        report.append("ECONOMETRIC METHODS ANALYSIS REPORT")
        report.append("=" * 80)
        
        # Stata methods
        report.append("\n### STATA ECONOMETRIC METHODS ###")
        for method, count in sorted(methods_data['stata'].items(), 
                                   key=lambda x: x[1], reverse=True):
            report.append(f"{method}: {count} repositories")
        
        # R methods
        if methods_data['r']:
            report.append("\n### R STATISTICAL METHODS ###")
            for method, count in sorted(methods_data['r'].items(), 
                                       key=lambda x: x[1], reverse=True):
                report.append(f"{method}: {count} repositories")
        
        # Python methods
        if methods_data['python']:
            report.append("\n### PYTHON/ML METHODS ###")
            for method, count in sorted(methods_data['python'].items(), 
                                       key=lambda x: x[1], reverse=True):
                report.append(f"{method}: {count} repositories")
        
        # Robustness checks
        report.append("\n### ROBUSTNESS CHECKS ###")
        for check, count in sorted(robustness_data.items(), 
                                  key=lambda x: x[1], reverse=True):
            report.append(f"{check}: {count} repositories")
        
        # Data cleaning
        report.append("\n### DATA CLEANING PRACTICES ###")
        for practice, count in sorted(cleaning_data.items(), 
                                     key=lambda x: x[1], reverse=True):
            report.append(f"{practice}: {count} repositories")
        
        # Advanced techniques
        report.append("\n### ADVANCED TECHNIQUES ###")
        for technique, repos in advanced_data.items():
            if repos:
                report.append(f"{technique}: {len(repos)} repositories")
                report.append(f"  Examples: {', '.join(repos[:3])}")
        
        return "\n".join(report)

# Run analysis
if __name__ == "__main__":
    analyzer = EconometricAnalyzer("AEAREP-103-ssh/aea_packages_complete")
    
    print("Starting econometric analysis...")
    methods = analyzer.analyze_all_repos()
    
    print("\nAnalyzing robustness checks...")
    robustness = analyzer.analyze_robustness_checks()
    
    print("Analyzing data cleaning practices...")
    cleaning = analyzer.analyze_data_cleaning()
    
    print("Identifying advanced techniques...")
    advanced = analyzer.identify_advanced_techniques()
    
    report = analyzer.generate_report(methods, robustness, cleaning, advanced)
    
    print("\n" + report)
    
    # Save report
    with open("econometric_methods_report.txt", "w") as f:
        f.write(report)
    
    print("\n✅ Econometric analysis complete!")
    print("Report saved to: econometric_methods_report.txt")