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


victoria_df.set_index('ACCIDENT_DATE', inplace=True)
victoria_df.sort_values(by=['ACCIDENT_DATE'] , inplace=True)




def accident_details(initial_date, final_date):
    #if wanna view all rows and columns
    #pd.set_option('display.max_rows', None) 
    #pd.set_option('display.max_columns', None)
    #pd.set_option('display.width', None)
    #pd.set_option('display.max_colwidth', -1)
    victoria_temp2_df = victoria_df.loc[initial_date : final_date]
    victoria_temp2_df.to_csv('victoria_temp2_df.csv')
    return victoria_temp2_df


def accidents_by_hours(initial_date, final_date):
    vc_df = victoria_df.loc[initial_date : final_date]
    column1 = vc_df.ACCIDENT_STATUS == 'Finished'
    vc_df['Column1'] = column1
    vc_temp_df = pd.DataFrame(vc_df, columns=['ACCIDENT_TIME', 'Column1'])
    vc_temp_df = vc_temp_df.groupby('ACCIDENT_TIME')['Column1'].count()
    list1 = ['00.00.00','01.00.00','02.00.00','03.00.00','04.00.00','05.00.00','06.00.00','07.00.00','08.00.00','09.00.00'
    ,'10.00.00','11.00.00','12.00.00','13.00.00','14.00.00','15.00.00','16.00.00','17.00.00','18.00.00','19.00.00','20.00.00','21.00.00'
    ,'22.00.00','23.00.00']
    l1 = []
    for i in range(0, len(list1) - 1):  
        l1.append(vc_temp_df.loc[list1[i]:list1[i+1]].sum())
    
    sns.set_style("darkgrid")
    plt.plot(l1, 'o-b')
    plt.title('ACCIDENT ANALYSIS WITH TIME')
    plt.xlabel('time in intervals of 5 hours')
    plt.ylabel('Accidents every hour')
    plt.show()



def precise_accident_details(initial_date, final_date, key_from_list):
    victoria_temp_df = victoria_df.loc[initial_date : final_date]
    victoria_temp3_df = victoria_temp_df[victoria_temp_df['ACCIDENT_TYPE'] == key_from_list]
    victoria_temp3_df.to_csv('victoria_temp_df.csv')
    return victoria_temp3_df

def alcohol_accident():
    alchohol_impact = victoria_df.ALCOHOL_RELATED == 'Yes'
    victoria_df['Alcohol_impact'] = alchohol_impact
    victoria_set2_df = pd.DataFrame(victoria_df, columns=['ACCIDENT_TYPE', 'Alcohol_impact'])
    df = victoria_set2_df.groupby('ACCIDENT_TYPE')['Alcohol_impact'].sum()
    accident_type = ['fixed object', 'vehicle', 'fall', 'no object struck',
    'other accident', 'struck pedestrian', 'struck animal', 'vehicle overturned', 'other object']
    sns.set_style("darkgrid")
    plt.plot(accident_type, df, 'o-r')
    plt.title('Types of Accidents involving Alcohol')
    plt.xlabel('Types of collision ')
    plt.ylabel('Number of accidents ')
    plt.show()


def alcohol_accidents_trend():
    alchohol_impact = victoria_df.ALCOHOL_RELATED == 'Yes'
    victoria_df['Alcohol_impact'] = alchohol_impact
    vc_set2_df = pd.DataFrame(victoria_df, columns=['year', 'Alcohol_impact'])
    v3_df = vc_set2_df.groupby('year')['Alcohol_impact'].sum()
    sns.set_style("darkgrid")
    plt.plot(v3_df, 'o-r')
    plt.title('Trend of Alcohol related accidents over the years')
    plt.xlabel('years')
    plt.ylabel('Number of accidents')
    plt.show()

