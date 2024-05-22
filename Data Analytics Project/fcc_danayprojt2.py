import numpy as np
import os
import pandas as pd
import matplotlib.pyplot as plt
from pandas.tseries import frequencies
import seaborn as sns


victoria_df = pd.read_csv(r'Crash Statistics Victoria.csv')
victoria_df['ACCIDENT_DATE'] = pd.to_datetime(victoria_df.ACCIDENT_DATE)
victoria_df['year'] = pd.DatetimeIndex(victoria_df.ACCIDENT_DATE).year
victoria_df['month'] = pd.DatetimeIndex(victoria_df.ACCIDENT_DATE).month
victoria_df['day'] = pd.DatetimeIndex(victoria_df.ACCIDENT_DATE).day
victoria_df['weekday'] = pd.DatetimeIndex(victoria_df.ACCIDENT_DATE).weekday




