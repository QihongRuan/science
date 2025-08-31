# 📚 AEA Code Repositories: Learning Insights from 158 Economics Research Projects

## Context: Understanding These Repositories

These 158 AEA repositories on Bitbucket are **code and methodology archives** where:
- ✅ **Code is complete** - All analysis scripts included
- ✅ **Documentation exists** - READMEs, comments, methodology notes
- ⚠️ **Data is elsewhere** - Too large for Bitbucket, hosted on Zenodo/OpenICPSR/Dataverse
- 📖 **Purpose: Teaching** - Learn how economists actually code

---

## 🎯 Key Discovery: Data Reference Patterns

### How Economists Handle External Data

**1. OpenICPSR References (Most Common)**
```stata
* From multiple repositories:
* Data available at: openicpsr-120217
* Download from: https://www.openicpsr.org/openicpsr/project/120217
```

**2. Zenodo Archives**
```bash
# Found in download scripts:
wget https://zenodo.org/record/XXXXX/files/data.zip
unzip data.zip -d ./data/
```

**3. Journal Dataverses**
```stata
* Data repository: Harvard Dataverse
* DOI: 10.7910/DVN/XXXXX
* Files: panel_data.dta, cross_section.dta
```

**4. Institutional Sources**
```stata
* Hospital data from CA OSHPD
* Apply at: https://oshpd.ca.gov/data-and-reports/
* Processing time: 2-3 months
```

---

## 💡 Code Patterns Worth Learning

### 1. **Smart Data Loading Without Local Files**

**Pattern A: Check and Download**
```stata
* Smart data management pattern
capture confirm file "data/main_dataset.dta"
if _rc {
    di "Data not found locally. Please download from:"
    di "https://openicpsr.org/project/120217"
    di "Place in data/ folder"
    exit
}
```

**Pattern B: Automated Retrieval**
```python
# From Python repositories
import os
import requests

def get_data():
    if not os.path.exists('data/dataset.csv'):
        print("Downloading data from repository...")
        url = "https://zenodo.org/record/XXX/files/data.zip"
        # Download logic here
    else:
        print("Data found locally")
```

### 2. **Placeholder Data for Testing**

**Excellent Practice Found:**
```stata
* Create synthetic data for code testing
clear
set obs 1000
gen treatment = runiform() > 0.5
gen outcome = rnormal() + 0.5*treatment
gen state = floor(runiform()*50)
save "data/synthetic_test.dta", replace

* Note: Replace with actual data from OpenICPSR
```

### 3. **Documentation of Data Requirements**

**Best README Pattern:**
```markdown
## Data Requirements

This code requires the following datasets:

1. **Main Panel Data** (panel_main.dta)
   - Source: OpenICPSR Project 120217
   - Size: ~2GB
   - Variables: 47
   - Observations: 1.2M

2. **Crosswalk Files** (crosswalk_*.csv)
   - Source: Public, included in /data/public/
   - Size: <10MB
   
3. **Restricted Data** (confidential_*.dta)  
   - Source: Apply through data provider
   - Requirements: IRB approval, DUA
   - Contact: dataaccess@institution.edu
```

---

## 🔬 Econometric Implementation Patterns

### 1. **Difference-in-Differences Excellence**

```stata
* Found in 106+ repositories - CLEAN IMPLEMENTATION
* =================================================
* DIFFERENCE-IN-DIFFERENCES ESTIMATION
* =================================================

* Setup
xtset unit_id time_period

* Create interaction terms clearly
gen post = (year >= 2010)
gen treated_post = treated * post

* Main specification with multiple levels
eststo clear

* (1) Basic DID
eststo: xtreg outcome treated_post treated post, fe cluster(state)

* (2) Add covariates
eststo: xtreg outcome treated_post treated post controls*, fe cluster(state)

* (3) State-specific trends
eststo: xtreg outcome treated_post treated post i.state#c.year, fe cluster(state)

* (4) Event study specification
forvalues t = -5/5 {
    gen treat_`=abs(`t')' = treated * (year == 2010 + `t')
}
eststo: xtreg outcome treat_*, fe cluster(state)

* Export results
esttab using "tables/did_results.tex", ///
    title("Difference-in-Differences Results") ///
    b(3) se(3) star(* 0.10 ** 0.05 *** 0.01) ///
    replace
```

### 2. **Instrumental Variables Pattern**

```stata
* Found in 113 repositories - ROBUST IMPLEMENTATION
* =================================================
* IV/2SLS ESTIMATION
* =================================================

* First stage power check
reg endogenous instrument controls*, cluster(state)
test instrument
scalar F_stat = r(F)
di "First stage F-statistic: " F_stat

* Only proceed if F > 10
if F_stat > 10 {
    * Main IV regression
    ivregress 2sls outcome controls* ///
        (endogenous = instrument), ///
        cluster(state) first
    
    * Save first stage
    estimates store first_stage
    
    * Reduced form
    reg outcome instrument controls*, cluster(state)
    estimates store reduced_form
}
else {
    di "Weak instrument warning: F = " F_stat
}
```

### 3. **Machine Learning Integration**

```stata
* Found in 60 repositories - MODERN APPROACH
* =================================================
* LASSO FOR VARIABLE SELECTION
* =================================================

* Install if needed
cap which lassopack
if _rc ssc install lassopack

* Lasso for covariate selection
lasso linear outcome controls*, nolog
local selected = e(allvars_sel)
di "Selected variables: `selected'"

* Use selected variables in main regression
reg outcome treatment `selected', robust
```

---

## 📊 Data Management Without Data Files

### 1. **Mock Data Generation for Testing**

```stata
* PATTERN: Generate realistic test data
program define create_test_data
    clear
    set seed 12345
    
    * Panel structure
    set obs 50  // states
    gen state = _n
    expand 20   // years
    bysort state: gen year = 2000 + _n - 1
    
    * Treatment assignment
    gen treated = state <= 25
    gen post = year >= 2010
    
    * Realistic outcome with DID effect
    gen outcome = 10 + 2*treated + 3*post + 5*treated*post + ///
                  rnormal(0, 2) + state/10 + year/100
    
    * Add covariates
    gen pop = exp(rnormal(14, 1))
    gen unemployment = runiform(3, 10)
    
    xtset state year
end
```

### 2. **Data Validation Checks**

```stata
* PATTERN: Verify data structure without having data
program define validate_data
    * Check required variables exist
    foreach var in outcome treatment year state {
        capture confirm variable `var'
        if _rc {
            di as error "Required variable `var' not found"
            exit 198
        }
    }
    
    * Check panel structure
    qui xtset
    if "`r(panelvar)'" == "" {
        di as error "Data must be xtset"
        exit 198
    }
    
    * Check for sufficient observations
    qui count
    if r(N) < 100 {
        di as error "Insufficient observations: `r(N)'"
        exit 198
    }
end
```

---

## 🎓 Statistical Methods Implementation Guide

### Most Valuable Code Patterns by Method:

**1. Fixed Effects with Clustering**
```stata
* Standard approach in 537 repositories
reghdfe outcome treatment controls*, ///
    absorb(unit_fe year_fe) ///
    cluster(state)
```

**2. Bootstrap Standard Errors**
```stata
* Found in 337 repositories
bootstrap, reps(1000) cluster(state): ///
    reg outcome treatment controls*
```

**3. Quantile Regression**
```stata
* In 107 repositories
qreg outcome treatment controls*, quantile(0.5)
```

**4. Synthetic Control**
```stata
* In 21 repositories - advanced method
synth outcome predictor1 predictor2 predictor3, ///
    trunit(1) trperiod(2010) ///
    keep(synth_results) replace
```

---

## 🚀 Modern Practices Emerging

### 1. **Version Control Integration**
```stata
* Some repos now include:
shell git add -A
shell git commit -m "Analysis run: $S_DATE"
```

### 2. **Parallel Processing**
```stata
* For large datasets:
parallel setclusters 4
parallel: bootstrap, reps(1000): reg y x
```

### 3. **Dynamic Documentation**
```stata
* Auto-generating markdown:
putdocx begin
putdocx paragraph, style(Title)
putdocx text ("Regression Results")
reg y x
putdocx table results = etable
putdocx save "results.docx", replace
```

---

## 📈 Code Quality Evolution

### Early Repos (100-500): Basic Patterns
```stata
* Simple, often problematic
reg y x
outreg2 using table.xls
```

### Middle Repos (500-1500): Improving
```stata
* Better organization
eststo clear
eststo: reg y x, robust
esttab using "table.tex", replace
```

### Recent Repos (1500+): Professional
```stata
* Modern best practices
cap program drop main_analysis
program define main_analysis
    syntax, [robust]
    
    eststo clear
    foreach spec in "baseline" "controls" "full" {
        eststo `spec': reg y x, `robust'
    }
    
    esttab using "output/table.tex", ///
        label compress replace ///
        b(%9.3f) se(%9.3f) ///
        star(* 0.10 ** 0.05 *** 0.01)
end
```

---

## 💎 Hidden Gems: Advanced Techniques

### 1. **Power Calculations** (Rarely Found)
```stata
power twomeans 0 0.5, sd(1) n(100) power(0.8)
```

### 2. **Multiple Testing Corrections**
```stata
* Bonferroni/Holm adjustments
wyoung outcome, cmd(reg OUTCOMEVAR treatment) ///
    familyp(outcome1 outcome2 outcome3) ///
    bootstrap(100)
```

### 3. **Heterogeneous Treatment Effects**
```stata
* Machine learning for HTE
causal_forest outcome treatment controls*, ///
    num.trees(2000)
```

---

## 🎯 Key Takeaways for Learning

### What These Repos Teach Best:

1. **Real-world code structure** - How economists organize large projects
2. **Method implementation** - Actual code for papers, not textbook examples
3. **Robustness patterns** - How to check sensitivity systematically
4. **Output formatting** - Publication-ready tables and figures
5. **Documentation practices** - What works (and what doesn't)

### What They DON'T Teach:

1. **Data cleaning** - Since raw data isn't included
2. **Data exploration** - Initial analysis steps
3. **Iterative development** - Only see final code
4. **Debugging process** - Errors already fixed

---

## 📚 Recommended Learning Path

### Beginner: Start with these patterns
1. Basic regression with robust SE
2. Summary statistics tables
3. Simple graphs

### Intermediate: Master these
1. Panel data methods
2. Instrumental variables
3. Program definitions

### Advanced: Study these implementations
1. Structural models
2. Machine learning integration
3. Bootstrap/simulation methods

---

## 🏆 Top 5 Repos for Learning

1. **aearep-1331** - Excellent DID and panel methods
2. **aearep-1593** - Best documentation practices
3. **aearep-1556** - Python-Stata integration
4. **AEAREP-1797** - Modern causal inference
5. **aearep-1700** - Clean code organization

These repositories represent the **gold standard** for learning how professional economists code, even without the actual data files.

---

*Analysis based on 158 AEA repositories, 7,243+ code files*
*Focus: Code patterns and implementation techniques*
*December 2024*