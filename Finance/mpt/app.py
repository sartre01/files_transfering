from flask import Flask, render_template, request
import plotly.graph_objects as go
import numpy as np
import pandas as pd
import yfinance as yf
from scipy.optimize import minimize
import matplotlib.pyplot as plt
import seaborn as sns

app = Flask(__name__)

def download_data(symbols, start_date, end_date, interval='1d'):
    data = yf.download(symbols, start=start_date, end=end_date, interval=interval)['Adj Close']
    return data.pct_change().dropna()

def minimize_variance(returns):
    cov_matrix = returns.cov() * 252  # Annualize covariance, 252 trading days in year
    n = len(cov_matrix)
    init_guess = np.ones(n) / n
    bounds = ((0, 1),) * n
    constraints = {'type': 'eq', 'fun': lambda weights: np.sum(weights) - 1}

    def portfolio_variance(weights):
        return weights.T @ cov_matrix @ weights

    result = minimize(portfolio_variance, init_guess, method='SLSQP', bounds=bounds, constraints=constraints)
    return result.x

def mean_variance_optimization(returns):
    cov_matrix = returns.cov() * 252
    n = len(cov_matrix)
    init_guess = np.ones(n) / n
    bounds = ((0, 1),) * n
    constraints = {'type': 'eq', 'fun': lambda weights: np.sum(weights) - 1}

    def objective(weights):
        return -((returns.mean() @ weights * 252) / (np.sqrt(weights.T @ cov_matrix @ weights)))

    result = minimize(objective, init_guess, method='SLSQP', bounds=bounds, constraints=constraints)
    return result.x

def calculate_dollar_allocation(weights_array, symbols, total_investment):
    allocations = np.round(weights_array * total_investment, 2)
    return pd.DataFrame(allocations, index=symbols, columns=['Dollar Allocation'])

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/optimize', methods=['POST'])
def optimize_portfolio():
    symbols = request.form['symbols'].split(',')
    start_date = request.form['start_date']
    end_date = request.form['end_date']
    initial_investment = float(request.form['initial_investment'])

    returns = download_data(symbols, start_date, end_date, interval='1d')

    min_var_weights = minimize_variance(returns)
    mean_var_weights = mean_variance_optimization(returns)

    allocation_min_var = calculate_dollar_allocation(min_var_weights, symbols, initial_investment)
    allocation_mean_var = calculate_dollar_allocation(mean_var_weights, symbols, initial_investment)

    return render_template('results.html', symbols=symbols, min_var_weights=min_var_weights,
                           mean_var_weights=mean_var_weights, allocation_min_var=allocation_min_var,
                           allocation_mean_var=allocation_mean_var)

if __name__ == '__main__':
    app.run(debug=True)
