# 📊 Statistical Analysis of Stock Market Behavior using Probability Distributions

### *(NIFTY 50 and Selected Indian Equities | 2000–2025)*

---

## 1. Introduction

Financial markets are complex, stochastic systems influenced by economic, behavioral, and structural factors. Traditional financial models often assume that stock returns are normally distributed and independent over time. However, empirical evidence contradicts these assumptions, showing features such as fat tails, volatility clustering, and time-dependent risk.

This project investigates the statistical behavior of stock market returns using multiple probability distributions and extends the analysis to include conditional risk estimation and advanced modeling perspectives.

---

## 2. Objectives

* Analyze stock return behavior using classical probability distributions
* Identify deviations from normality and randomness
* Model crash timing and extreme losses
* Quantify risk using statistical tools
* Build an interactive dashboard for real-time analysis
* Propose advanced modeling extensions for improved accuracy

---

## 3. Data Collection and Preprocessing

* **Data Source:** Yahoo Finance (`yfinance`)
* **Assets:** NIFTY 50 index and selected Indian stocks
* **Time Period:** 2000–2025 (user-selectable in dashboard)
* **Frequency:** Daily closing prices

### Data Transformation

Log returns were computed as:

[
R_t = \ln\left(\frac{P_t}{P_{t-1}}\right)
]

This transformation stabilizes variance and enables better statistical modeling.

---

## 4. Methodology

The analysis is divided into four major components:

### 4.1 Distribution-Based Analysis

* Normal Distribution
* Lognormal Distribution
* Binomial Distribution
* Weibull Distribution
* Pareto Distribution

### 4.2 Time-Series Analysis

* Rolling Mean
* Rolling Variance

### 4.3 Risk Metrics

* Annualized Return
* Annualized Volatility
* Conditional Crash Probability

### 4.4 Statistical Validation

* Chi-Square Goodness-of-Fit Test

---

## 5. Distribution Analysis

---

### 5.1 Normal Distribution (Returns)

* Mean (daily): ~0.00039
* Standard deviation (daily): ~0.013

#### Findings:

* Returns are approximately symmetric but exhibit **fat tails**
* Extreme values occur more frequently than predicted

#### Conclusion:

The normal distribution underestimates extreme market risk.

---

### 5.2 Lognormal Distribution (Prices)

Stock prices were found to follow a lognormal pattern, consistent with multiplicative growth processes in finance.

---

### 5.3 Binomial Distribution (Market Direction)

* Up day probability ≈ 0.55

#### Analysis:

* Compared theoretical binomial distribution with actual data
* Applied Chi-square test

#### Result:

* **p-value ≈ 0.0000**

#### Interpretation:

* Strong rejection of independence assumption
* Market movements exhibit **dependence / structure**

---

### 5.4 Weibull Distribution (Crash Timing)

Crash defined as return < -3%

#### Results (2000–2025):

* Shape (k) ≈ 0.49
* Scale (λ) ≈ 21.9 days

#### Interpretation:

* ( k < 1 ) → **decreasing hazard rate**
* Indicates **volatility clustering**

#### Outlier Handling:

* Extreme gap (~1492 days) identified
* Removed using IQR method
* Improved parameter stability

#### Conditional Probability:

[
P(a < T \le a+t \mid T > a)
]

Used to estimate probability of crash in next 10 days given time since last crash.

---

### 5.5 Pareto Distribution (Tail Risk)

* Threshold: 3% loss
* Shape (α) ≈ 4.39
* Scale ≈ 0.05

#### Interpretation:

* Moderate fat tails
* Extreme losses occur more frequently than normal model predicts

#### Important Note:

Outliers were **not removed**, as they represent true tail behavior.

---

## 6. Time-Series Analysis

### 6.1 Cumulative Returns

* Demonstrates long-term market growth
* Highlights drawdowns and recovery phases

### 6.2 Rolling Mean

* Fluctuates around zero
* Indicates weak short-term predictability

### 6.3 Rolling Variance

* Shows time-varying volatility
* Confirms **volatility clustering**

---

## 7. Risk Metrics

### Annualized Return:

[
\mu_{annual} = \mu_{daily} \times 252
]

### Annualized Volatility:

[
\sigma_{annual} = \sigma_{daily} \times \sqrt{252}
]

#### Findings:

* Annual return ≈ 10–12%
* Annual volatility ≈ 18–22%

---

## 8. Key Findings

### 🔥 Major Insights:

1. **Non-Normality**

   * Returns exhibit fat tails

2. **Non-Random Behavior**

   * Binomial model rejected (Chi-square test)

3. **Volatility Clustering**

   * Confirmed by Weibull and rolling variance

4. **Time-Dependent Risk**

   * Crash probability depends on time since last event

5. **Moderate Tail Risk**

   * Extreme losses present but controlled in large-cap indices

6. **Non-Stationarity**

   * Market behavior changes across time periods

---

## 9. Dashboard Implementation

An interactive Streamlit dashboard was developed with:

* Stock selection (NIFTY, Reliance, TCS, etc.)
* Adjustable date range
* Distribution visualizations
* Weibull crash analysis
* Pareto tail analysis
* Binomial vs actual comparison
* Chi-square testing
* Rolling statistics
* Annual metrics

---

## 10. Advanced Model Extensions

To address limitations of static models:

| Component        | Advanced Model             |
| ---------------- | -------------------------- |
| Market Direction | Hidden Markov Models (HMM) |
| Volatility       | HAR / GAS Models           |
| Crash Timing     | Hawkes Process             |
| Tail Risk        | Dynamic GPD (POT approach) |

These models capture regime shifts, self-exciting behavior, and time-varying risk.

---

## 11. Limitations

* Model assumptions may not fully capture market dynamics
* Threshold selection affects results
* Limited predictive capability
* External macroeconomic factors not included

---

## 12. Future Scope

* Implement HMM for regime detection
* Add Value-at-Risk (VaR) analysis
* Develop real-time trading signals
* Extend to multi-asset portfolios
* Deploy dashboard as web application

---

## 13. Conclusion

This study demonstrates that financial markets cannot be fully explained using simple probabilistic models. While short-term price movements exhibit near-random behavior, deeper analysis reveals:

* Volatility clustering
* Time-dependent crash risk
* Fat-tailed distributions

The rejection of the binomial model and presence of Weibull and Pareto characteristics confirm that markets are **structured, non-normal, and dynamic systems**.

---

## 🎯 Final Takeaway

> Financial markets are not purely random, not normally distributed, and exhibit clustering and fat-tailed risk behavior.

---

## 📚 References (Suggested)

* Hull, J. – *Options, Futures, and Other Derivatives*
* Tsay, R. – *Analysis of Financial Time Series*
* McNeil, Frey & Embrechts – *Quantitative Risk Management*
* Cont, R. – *Empirical Properties of Asset Returns*

---

**End of Report**
