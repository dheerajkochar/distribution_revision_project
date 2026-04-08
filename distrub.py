import streamlit as st
import yfinance as yf
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import norm, weibull_min, pareto

st.title("📊 Stock Market Distribution Dashboard ")

# -------------------------------
# 📅 Sidebar: Date Range
# -------------------------------
start_year = st.sidebar.slider("Start Year", 2000, 2024, 2010)
end_year = st.sidebar.slider("End Year", start_year+1, 2026, 2019)

start_date = f"{start_year}-01-01"
end_date = f"{end_year}-03-01"

st.write(f"### Data Range: {start_date} to {end_date}")

# -------------------------------
# 📥 Data Download
# -------------------------------
# -------------------------------
# 📊 Stock Selection
# -------------------------------
st.sidebar.subheader("📊 Select Stock / Index")

stock_options = {
    "NIFTY 50": "^NSEI",
    "silver": "SILVERBEES.NS",
    "BANK NIFTY": "^NSEBANK",
    "Reliance": "RELIANCE.NS",
    "TCS": "TCS.NS",
    "HDFC Bank": "HDFCBANK.NS",
    "Infosys": "INFY.NS",
    "ICICI Bank": "ICICIBANK.NS"
}

selected_stock_name = st.sidebar.selectbox(
    "Choose Stock",
    list(stock_options.keys())
)

ticker = stock_options[selected_stock_name]
# -------------------------------
# 📉 Returns
# -------------------------------
data = yf.download(ticker, start=start_date, end=end_date)
data = data[['Close']].dropna()
data['Returns'] = np.log(data['Close'] / data['Close'].shift(1))
data.dropna(inplace=True)
# -------------------------------
# 📈 CUMULATIVE RETURNS
# -------------------------------
st.subheader("📈 Cumulative Returns")

data['Cumulative Returns'] = (1 + data['Returns']).cumprod()

fig4, ax4 = plt.subplots()
ax4.plot(data.index, data['Cumulative Returns'])
ax4.set_title("Cumulative Returns Over Time")
ax4.set_xlabel("Date")
ax4.set_ylabel("Growth of ₹1")
st.pyplot(fig4)
# -------------------------------
# 📊 BINOMIAL DISTRIBUTION (UP/DOWN DAYS)
# -------------------------------
st.subheader("📊 Binomial Distribution (Market Direction)")

from scipy.stats import binom

# Convert to Up/Down
data['Up'] = (data['Returns'] >= 0).astype(int)

# Probability of up day
p = data['Up'].mean()
st.write(f"Probability of Up Day (p): {p:.3f}")

n = st.sidebar.slider("Binomial Window (days)", 5, 20, 10)

x_vals = np.arange(0, n+1)
binom_probs = binom.pmf(x_vals, n, p)

fig7, ax7 = plt.subplots()
ax7.bar(x_vals, binom_probs)
ax7.set_title(f"Binomial Distribution (n={n})")
ax7.set_xlabel("Number of Up Days")
ax7.set_ylabel("Probability")
st.pyplot(fig7)
# Rolling count of up days
rolling_up = data['Up'].rolling(n).sum()

# Remove NaN
rolling_up = rolling_up.dropna()

# Actual frequency
actual_counts = rolling_up.value_counts(normalize=True).sort_index()

# Plot comparison
fig8, ax8 = plt.subplots()

ax8.bar(actual_counts.index - 0.2, actual_counts.values, width=0.4, label="Actual")
ax8.bar(x_vals + 0.2, binom_probs, width=0.4, label="Binomial")

ax8.set_title("Actual vs Binomial Distribution")
ax8.set_xlabel("Number of Up Days")
ax8.set_ylabel("Probability")
ax8.legend()

st.pyplot(fig8)
# Probability of majority up days
prob_theoretical = 1 - binom.cdf(n//2, n, p)

# Actual probability
prob_actual = (rolling_up > n/2).mean()

st.write(f"Probability of ≥{n//2 + 1} Up Days (Theoretical): {prob_theoretical:.3f}")
st.write(f"Actual Probability: {prob_actual:.3f}")
# -------------------------------
# 📊 CHI-SQUARE TEST (BINOMIAL FIT)
# -------------------------------
st.subheader("📊 Chi-Square Test (Binomial Fit)")

from scipy.stats import chisquare

# Expected frequencies (theoretical)
expected = binom.pmf(x_vals, n, p) * len(rolling_up)

# Actual frequencies
actual = rolling_up.value_counts().sort_index()

# Align indices
actual = actual.reindex(x_vals, fill_value=0)

# Convert to arrays
observed = actual.values

# Avoid zeros in expected
expected = np.where(expected == 0, 1e-6, expected)

# Chi-square test
chi_stat, p_value = chisquare(f_obs=observed, f_exp=expected)

st.write(f"Chi-Square Statistic: {chi_stat:.3f}")
st.write(f"P-value: {p_value:.5f}")
# -------------------------------
# 📊 Rolling Mean & Variance
# -------------------------------
st.subheader("📊 Rolling Mean & Variance")

window = st.sidebar.slider("Rolling Window (days)", 5, 100, 20)

# Rolling statistics
data['Rolling Mean'] = data['Returns'].rolling(window).mean()
data['Rolling Variance'] = data['Returns'].rolling(window).var()

# Plot Mean
fig5, ax5 = plt.subplots()
ax5.plot(data.index, data['Rolling Mean'])
ax5.set_title(f"Rolling Mean ({window}-day)")
ax5.set_xlabel("Date")
st.pyplot(fig5)

# Plot Variance
fig6, ax6 = plt.subplots()
ax6.plot(data.index, data['Rolling Variance'])
ax6.set_title(f"Rolling Variance ({window}-day)")
ax6.set_xlabel("Date")
st.pyplot(fig6)

# -------------------------------
# 📊 NORMAL DISTRIBUTION
# -------------------------------
st.subheader("📈 Normal Distribution (Returns)")

mu, sigma = norm.fit(data['Returns'])

st.write(f"Mean: {mu:.6f}")
st.write(f"Std Dev: {sigma:.6f}")
# -------------------------------
# 📊 Annual Metrics
# -------------------------------
st.subheader("📊 Annualized Metrics")

trading_days = 252

annual_return = mu * trading_days
annual_volatility = sigma * np.sqrt(trading_days)

st.write(f"Annual Return: {annual_return:.2%}")
st.write(f"Annual Volatility: {annual_volatility:.2%}")
fig1, ax1 = plt.subplots()
x = np.linspace(data['Returns'].min(), data['Returns'].max(), 100)
pdf = norm.pdf(x, mu, sigma)
ax1.hist(data['Returns'], bins=50, density=True)
ax1.plot(x, pdf)
ax1.set_title("Normal Fit")
st.pyplot(fig1)

# -------------------------------
# ⚠️ WEIBULL (CRASH ANALYSIS)
# -------------------------------
st.subheader("⚠️ Weibull Distribution (Crash Timing)")

threshold = st.sidebar.slider("Crash Threshold (%)", -10, -1, -3) / 100

crash_days = data[data['Returns'] < threshold]

st.write(f"Number of crash days: {len(crash_days)}")

if len(crash_days) > 10:

    # -------------------------------
    # 📊 Compute crash gaps
    # -------------------------------
    crash_dates = crash_days.index
    crash_gaps = np.diff(crash_dates).astype('timedelta64[D]').astype(int)
    crash_gaps = crash_gaps[crash_gaps > 0]

    st.subheader("📊 Crash Gap Analysis")
    st.write("Crash gaps (days):", crash_gaps)

    # -------------------------------
    # 🚨 Outlier Detection (IQR)
    # -------------------------------
    q1 = np.percentile(crash_gaps, 25)
    q3 = np.percentile(crash_gaps, 75)
    iqr = q3 - q1

    upper_bound = q3 + 1.5 * iqr

    outliers = crash_gaps[crash_gaps > upper_bound]

    st.write(f"Detected Outliers (> {upper_bound:.2f} days):", outliers)

    # -------------------------------
    # 🔄 Remove outliers
    # -------------------------------
    filtered_gaps = crash_gaps[crash_gaps <= upper_bound]

    st.write(f"Data points after removing outliers: {len(filtered_gaps)}")

    # -------------------------------
    # 📊 Fit Weibull (RAW vs FILTERED)
    # -------------------------------
    shape_raw, loc_raw, scale_raw = weibull_min.fit(crash_gaps)
    shape_filt, loc_filt, scale_filt = weibull_min.fit(filtered_gaps)

    st.subheader("🔍 Weibull Comparison")

    st.write("With Outliers:")
    st.write(f"Shape (k): {shape_raw:.3f}, Scale (λ): {scale_raw:.3f}")

    st.write("Without Outliers:")
    st.write(f"Shape (k): {shape_filt:.3f}, Scale (λ): {scale_filt:.3f}")

    # -------------------------------
    # 📈 Plot (Filtered Data)
    # -------------------------------
    fig2, ax2 = plt.subplots()

    x = np.linspace(min(filtered_gaps), max(filtered_gaps), 100)
    pdf = weibull_min.pdf(x, shape_filt, loc_filt, scale_filt)

    ax2.hist(filtered_gaps, bins=10, density=True)
    ax2.plot(x, pdf)
    ax2.set_title("Weibull Fit (Outliers Removed)")
    ax2.set_xlabel("Days Between Crashes")
    ax2.set_ylabel("Density")

    st.pyplot(fig2)

    # -------------------------------
    # 📊 Probability Calculation
    # -------------------------------
    prob = weibull_min.cdf(10, shape_filt, loc_filt, scale_filt)

    st.write(f"Probability of crash within 10 days: {prob:.2f}")

else:
    st.warning("Not enough crash data. Increase threshold.")
# -------------------------------
# ⏱️ Time since last crash
# -------------------------------
last_crash_date = crash_dates[-1]
current_date = data.index[-1]

days_since_last_crash = (current_date - last_crash_date).days
st.write(f"Last crash date: {last_crash_date.date()}")
st.write(f"Days since last crash: {days_since_last_crash}")
# Conditional probability
prob_future = (
    weibull_min.cdf(days_since_last_crash + 10, shape_filt, loc_filt, scale_filt)
    - weibull_min.cdf(days_since_last_crash, shape_filt, loc_filt, scale_filt)
) / (1 - weibull_min.cdf(days_since_last_crash, shape_filt, loc_filt, scale_filt))

st.write(f"Probability of crash in next 10 days (given current state): {prob_future:.2f}")
# -------------------------------
# 🔥 PARETO (TAIL RISK)
# -------------------------------
st.subheader("🔥 Pareto Distribution (Extreme Losses)")

losses = -data[data['Returns'] < 0]['Returns']

tail_threshold = st.sidebar.slider("Tail Threshold (%)", 1, 10, 3) / 100
tail_losses = losses[losses > tail_threshold]

st.write(f"Number of extreme losses: {len(tail_losses)}")

if len(tail_losses) > 5:
    shape, loc, scale = pareto.fit(tail_losses)

    st.write(f"Shape (α): {shape:.3f}")
    st.write(f"Scale: {scale:.3f}")

    # Plot
    fig3, ax3 = plt.subplots()
    x = np.linspace(min(tail_losses), max(tail_losses), 100)
    pdf = pareto.pdf(x, shape, loc, scale)

    ax3.hist(tail_losses, bins=20, density=True)
    ax3.plot(x, pdf)
    ax3.set_title("Pareto Tail Fit")
    st.pyplot(fig3)

    # Tail probability
    prob_extreme = 1 - pareto.cdf(0.05, shape, loc, scale)
    st.write(f"Probability of loss > 5%: {prob_extreme:.4f}")

else:
    st.warning("Not enough tail data. Adjust threshold.")

# -------------------------------
# 📊 FINAL INSIGHTS
# -------------------------------
st.subheader("🧠 Key Insights")

st.markdown("""
- Returns are not perfectly normal  
- Market crashes show clustering (Weibull)  
- Extreme losses follow fat-tail behavior (Pareto)  
- Risk is time-dependent and non-stationary  
""")
st.markdown("""
### 🧠 Binomial Insights

- The binomial model assumes independence between days  
- If actual ≈ theoretical → market behaves randomly  
- If actual > theoretical → momentum exists  
- If actual < theoretical → mean reversion  

👉 This helps test market efficiency
""")