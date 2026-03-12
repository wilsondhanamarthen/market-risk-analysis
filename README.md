# Quantitative Market Risk Analysis

This project performs a quantitative risk analysis on major U.S. equities using Python.  
The script retrieves historical market data and computes several financial risk metrics commonly used in quantitative finance and portfolio management.

## Assets Analyzed

- SPY (S&P 500 ETF)
- AAPL (Apple)
- MSFT (Microsoft)
- GOOGL (Alphabet)
- AMZN (Amazon)

Historical data is obtained using the **yfinance API**.

---

## Financial Concepts Used

Financial Concepts Used
This project implements several core financial risk metrics commonly used in quantitative finance and portfolio risk analysis.

Log Returns — Measures continuous asset returns and is widely used in financial modeling.
Annual Return — Scales the average daily return to yearly performance.
Annual Volatility — Measures the dispersion of returns and represents market risk.
Sharpe Ratio — Evaluates risk-adjusted return by comparing return to volatility.
Skewness — Measures asymmetry in the return distribution.
Kurtosis — Measures the presence of extreme values (fat tails) in returns.
Value at Risk (VaR) — Estimates potential losses at a given confidence level (95% in this project).
Maximum Drawdown — Measures the largest peak-to-trough decline in cumulative returns.
Rolling Volatility — Tracks how volatility evolves over time using moving windows.
Correlation Matrix — Shows how assets move relative to each other, useful for diversification analysis.

---

## Key Calculations

### Log Returns

Log returns are calculated as:
r_t = ln(P_t / P_(t-1))


Log returns are widely used in financial modeling because they are **time-additive and statistically convenient**.

---

### Annual Return

Annual return is calculated by scaling the average daily return:
Annual Return = Mean Daily Return × 252


(252 trading days per year)

---

### Annual Volatility

Volatility measures the dispersion of returns and represents market risk:
Annual Volatility = Daily Standard Deviation × √252


---

### Sharpe Ratio

The Sharpe Ratio measures **risk-adjusted performance**:
Sharpe Ratio = Annual Return / Annual Volatility

Higher Sharpe ratios indicate better returns relative to risk.

---

### Value at Risk (VaR)

Value at Risk estimates the potential loss at a given confidence level.

This project calculates **95% daily VaR**, which represents the 5th percentile of returns.

Example interpretation:

> A VaR of -2.7% means there is a 5% probability that the asset loses more than 2.7% in a single day.

---

### Maximum Drawdown

Maximum drawdown measures the largest peak-to-trough loss in cumulative returns.

This metric is commonly used by portfolio managers to assess downside risk.

---

## Visualizations

The script generates several plots:

- Rolling Volatility (30-day and 90-day)
- Drawdown Over Time
- Distribution of Returns

These visualizations help illustrate how risk evolves over time.

---

## Installation

Install required dependencies:
pip install -r requirements.txt

---

## Running the Project

Run the script with:
python market_risk_analysis.py

The program will:

1. Download market data
2. Calculate financial risk metrics
3. Print the results table
4. Display risk visualizations

---

## Technologies Used

- Python
- Pandas
- NumPy
- Matplotlib
- yFinance API

## Project Workflow

The script follows the following workflow:

1. Download historical price data using the yfinance API  
2. Calculate log returns for each asset  
3. Compute financial risk metrics (volatility, Sharpe ratio, VaR, etc.)  
4. Analyze correlations between assets  
5. Measure downside risk using drawdown analysis  
6. Generate visualizations to illustrate market risk behavior

---
## Example Output

The script prints a table of financial risk metrics including:

- Annual Return
- Annual Volatility
- Sharpe Ratio
- Skewness
- Kurtosis
- Maximum Drawdown

It also generates visualizations for:

- Rolling volatility
- Drawdown over time
- Return distribution

## Author

Wilson Dhana Marthen

This project was created as a learning exercise in quantitative finance and financial data analysis using Python.

---

## Project Purpose

This project demonstrates how Python can be used to analyze financial market risk and compute common metrics used in quantitative finance and portfolio management.
