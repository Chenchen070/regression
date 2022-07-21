import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy import stats
from sklearn.linear_model import LinearRegression
from sklearn.feature_selection import f_regression 
from math import sqrt
import seaborn as sns
from sklearn.metrics import mean_squared_error, r2_score, explained_variance_score


def plot_residuals(x, y, yhat):
    plt.scatter(x.sample(100000, random_state=123), (y-yhat).sample(100000, random_state=123))
    plt.axhline(y = 0, ls = ':', color = 'red')
    plt.xlabel('x')
    plt.ylabel('Residual')
    plt.title('OLS model residuals');

def regression_errors(y, yhat):
    
    SSE = mean_squared_error(y, yhat) * len(train)
    ESS = sum((yhat - y.mean())**2)
    TSS = ESS + SSE
    MSE = mean_squared_error(y, yhat)
    RMSE = sqrt(mean_squared_error(y, yhat))
    
    ss = pd.DataFrame(np.array(["SSE", "ESS", "TSS", "MSE", "RMSE"]), columns=["metric"])
    ss['model_results'] = np.array([SSE, ESS, TSS, MSE, RMSE])
    
    return ss

def baseline_mean_errors(y, baseline):
    
    SSE_bs = mean_squared_error(y, baseline) * len(y)
    MSE_bs = mean_squared_error(y, baseline)
    RMSE_bs = sqrt(mean_squared_error(y, baseline))
    
    ss_bs = pd.DataFrame(np.array(["SSE_bs", "MSE_bs", "RMSE_bs"]), columns=["metric"])
    ss_bs['model_results'] = np.array([SSE_bs, MSE_bs, RMSE_bs])
    
    return ss_bs

def better_than_baseline(y, yhat,baseline):
    RMSE = sqrt(mean_squared_error(y, yhat))
    RMSE_bs = sqrt(mean_squared_error(y, baseline))
    
    if RMSE < RMSE_bs:
        return True
    else:
        return False