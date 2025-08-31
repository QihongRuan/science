# AERI-2020-0401.R3_Proof_hi.pdf

- Path: "AEAREP-103-ssh/aea_packages_complete/AEAREP-1601/AERI-2020-0401.R3_Proof_hi.pdf"
- Title:                Optimal Lockdown in a Commuting Network
- Abstract words: 202; sentences: 17; avg words/sent: 11
- Numbers in opening: 105; percents: 8; dollar mentions: 0
- Methods keywords: DiD:1 Event:0 IV:0 FE:14 Cluster:0 Placebo:0 Robust:0
- Policy/Welfare cues in opening: 7 (welfare-specific: 0)

## Sections detected
```
72:1       Introduction
186:2     Model
390:               3        Data and Parametrization
631:4     Optimal Spatial Lockdowns
727:5    Conclusion
```

## Abstract (excerpt)
>  We study optimal dynamic lockdowns against Covid-19 within a commuting network. Our framework integrates canonical spatial epidemiology and trade models, and is applied to cities with varying initial viral spread: Seoul, Daegu and NYC-Metro. Spatial lockdowns achieve substantially smaller income losses than uniform lockdowns. In NYM and Daegu—with large initial shocks—the optimal lockdown restricts inflows to central districts before gradual relax- ation, while in Seoul it imposes low temporal but large spatial variation. Actual commuting reductions were too weak in central locations in Daegu and NYM, and too strong across Seoul. JEL Classification: R38, R4, C6 ∗ E-mail : pfajgelb@princeton.edu, ak2796@columbia.edu, wookunkim@smu.edu, cristiano.mantovani@upf.edu, es- chaal@crei.cat. We th

## Intro (first ~120 lines after heading)
```
    Commuting networks are the backbone of cities, allowing interactions that are vital for economic
growth. On a typical day, Manhattan receives as many commuters as its residents–about 1.6 million
people. Two months after the onset of Covid-19, NYC metro commute flows were 48% below pre-
pandemic levels. Weighing the economic costs against the benefits of stopping Covid-19, was this
reduction too large or not large enough? To fight a highly infectious disease without a vaccine,
public authorities must decide if and how to curtail movements across locations connected via
commuting and trade.1 How should lockdown policies be set across locations and time?
    In this paper we establish an efficient benchmark against which to measure the losses from
uncoordinated or spatially uniform lockdown efforts. We study optimal dynamic lockdowns to fight
pandemics in a commuting network using a framework that integrates standard spatial epidemiology
and trade models.2 In the model, a disease spreads through interactions of commuters at the
workplace. Lockdown policies directly reduce the real income of workers who stay at home and
increase shopping costs, and indirectly impact other locations through shifts in expenditures.3
In reality, policies that close specific businesses preclude commutes along particular routes. Our
planning problem determines the fraction of each origin-destination commuting flow allowed to
operate at each point in time to minimize the economic costs and the loss of lives. We also
implement optimal lockdowns by origin or destination that resemble less flexible closures (e.g.,
lockdowns by neighborhood).
    We apply the model using real-time commuting data across districts in two South Korean cities,
Seoul and Daegu, and cellphone mobility data across counties in the NYC Metro area (NYM).
We compare optimal pandemic-fighting strategies across intensities of the initial virus shock and
contrast them with the observed commuting responses. We analyze Korean cities because Korea
has tested for Covid-19 at greater intensities than most countries, making the timeline of their case
data more reliable.4 Seoul is the largest city in Korea and experienced a relatively small caseload,
while Daegu (Korea’s fourth-largest city) experienced the country’s largest shock. We study NYM
because of its economic importance and rapid spread.
    We compute the optimal lockdown given the Covid-19 spread when lockdown policies were an-
nounced. The model matches pre-pandemic commuting flows and wages across locations (Korean
districts and NYM counties). We estimate the transmission rate using data on the spatial distribu-

    1
      Lockdowns were announced fairly uniformly across bordering U.S. states, with a mean difference of 4 days,
although there has been variation in county-level policies. For example, New York, New Jersey, and Connecticut
imposed almost simultaneous lockdown in March 2020, while Illinois did so more two weeks before Missouri (Raifman
et al., 2020).
    2
      The spatial SIR model we formulate is closely related to the multi-city epidemic model in Arino and Van den
Driessche (2003), in which the disease is transmitted from infected residents of location i to susceptible residents of
location j when they meet in location k. The trade model follows Anderson and Van Wincoop (2003).
    3
      Caliendo et al. (2018) and Monte et al. (2018) study diffusion of local shocks across and within cities in related
gravity models.
    4
      Korea had performed 0.878 tests per thousand people at the time of its 1000th patient compared to 0.086 in the
U.S. Stock (2020), Manski and Molinari (2020), Korolev (2020), and Atkeson (2020a) discuss challenges arising from
infrequent testing.


                                                           1
Page 3 of 42




               tion of new cases and commuting flows over time. We use geocoded credit card expenditure data
               from Seoul to estimate the impact of lockdown on the travel costs of shopping.
                  Our first results show that in NYM and Daegu—where the virus initially spread very quickly—
               locations with high virus-diffusion potential are subject to a strict initial lockdown, eliminating up
               to 70% of pre-pandemic inflows, which is partially relaxed over 3 to 6 months. In NYM, many
               locations are locked down early, but only the top-3 central locations (Manhattan, Brooklyn, and
               Bronx) remain closed for a long time in expectation that a vaccine arrives. In contrast, in Seoul—
               where the initial spread of Covid-19 was much smaller—the planner initially locks down only a few
               locations of relatively high centrality. As the virus spreads, the lockdown intensifies and retains
               considerable spatial variation.
                  Our main result reveals large benefits from spatial targeting. Specifically, we find substantially
               lower real-income losses from spatial targeting compared to an optimal but spatially uniform lock-
               down. Given the actual case count by April 30, spatial targeting would have led to 20%, 32%, and
               58% lower economic costs in Daegu, Seoul, and NYM, respectively, than the optimal uniform lock-
               down. We find that optimal lockdowns by destination of commuting flows are almost as efficient as
               the fully flexible benchmark, suggesting that spatially targeted business lockdowns may be enough
               to reap the benefits of spatial targeting.
                  Finally, we compare the optimal benchmark with the observed commuting reductions resulting
               from government action and commuters’ precautionary behavior. On average across locations,
               commuting declines reached troughs of 79%, 36%, and 79% below pre-pandemic levels in Daegu,
               Seoul, and NYM before modestly reverting upward. In NYM and Daegu, these city-level declines
               are not far from the optimal benchmark. However, the most central (peripheral) locations exhibited
               a weaker (stronger) reduction in commuting than what would have been optimal. Across Seoul,
               the actual commuting reductions were too strong compared to the optimal. As a result, across all
               three cities, the real income losses could have been much smaller through optimal spatial targeting.
                  Studies of optimal epidemic control in economic models include Goldman and Lightwood (2002)
               and Rowthorn and Toxvaerd (2012) and, in the context of Covid-19, Atkeson (2020b), Alvarez et al.
               (2020), Jones et al. (2020), Piguillem and Shi (2020), Rowthorn (2020), and Rowthorn and Toxvaerd
               (2020), among others. Acemoglu et al. (2020), Baqaee et al. (2020), and Glover et al. (2020) among
               others study lockdown with heterogeneous agents.
                  Adda (2016) demonstrates that diseases spread through transportation networks exploiting
               variation from public-transport strikes in France, and Viboud et al. (2006) show that work-related
               flows correlate with influenza’s regional spread in the United States. For Covid-19, Tian et al.
               (2020) argue that the Wuhan lockdown and suspending public transport delayed the spread across
               China, Fang et al. (2020) show that the lockdown reduced infection rates using real-time movement
               data, Kissler et al. (2020) show that commuting correlates with cases within New York, and Hsiang
               et al. (2020) and Flaxman et al. (2020) show that interventions like lockdown reduced the spread.
                  Spatial SIR models were first used to study influenza and measles (Rvachev and Longini Jr,
               1985; Bolker and Grenfell, 1995). Germann et al. (2006), Eubank et al. (2004) and Drakopolous


                                                                 2
                                                                                                                         Page 4 of 42




and Zheng (2017) study targeted policies in spatial or network models, and Rowthorn et al. (2009)
analyze their theoretical properties. For Covid-19, Azzimonti et al. (2020), Birge et al. (2020),
Chang et al. (2020), Chinazzi et al. (2020), and Giannone et al. (2020) simulate policies in spatial
and network SIR models, Argente et al. (2020) consider case information disclosure, and Antràs
et al. (2020) study pandemics in a trade model with human interactions.
    Our contribution is three-fold. First, we implement optimal lockdown over both time and space
in a commuting network. Second, to evaluate the diffusion of economic costs through changes in
spending we integrate a general-equilibrium trade framework. Third, we use real-time commuting
and expenditure data to estimate and compare the actual commuting responses over space with
optimal lockdowns.


2     Model
    We use a standard spatial epidemiology model similar to Arino and Van den Driessche (2003).
The general equilibrium corresponds to a standard quantitative gravity trade model (e.g., Anderson
and Van Wincoop 2003 and Eaton and Kortum 2002).

2.1    Spatial Diffusion
    The economy consists of J locations in continuous time. Before the pandemic, in each location
```
