#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jul  9 11:52:32 2019

@author: mayur
"""

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import math
import scipy.stats as st


# importing data into a dataframe
data = pd.read_csv('/Users/mayur/Documents/GitHub/A_B_testing/'
                   'AB_testing/Data/ab_data.csv')

data.dtypes

# converting timestamp to datetime()
data['timestamp'] = pd.to_datetime(data['timestamp'])

# finding results not aligned for campaign

not_aligned_data_control = data[(data['group']=='control') 
                    & (data['landing_page']== 'new_page')]

not_aligned_data_treatment = data[(data['group']=='treatment') 
                    & (data['landing_page']== 'old_page')]

# dropping data that is not aligned

data_aligned = data.merge(not_aligned_data_control, how = 'left', indicator = True)
data_aligned = data_aligned[data_aligned['_merge'] == 'left_only']
data_aligned = data_aligned.drop('_merge', axis = 1)

data_aligned = data.merge(not_aligned_data_treatment, how = 'left', indicator = True)
data_aligned = data_aligned[data_aligned['_merge'] == 'left_only']
data_aligned = data_aligned.drop('_merge', axis = 1)

# segregating data into different dataframes

converted_control = data_aligned[(data_aligned['converted']==1) & 
                           (data_aligned['group']== 'control')].reset_index()

non_converted_control = data_aligned[(data_aligned['converted']==0) & 
                           (data_aligned['group']== 'control')].reset_index()

converted_treatment = data_aligned[(data_aligned['converted']==1) & 
                           (data_aligned['group']== 'treatment')].reset_index()

non_converted_treatment = data_aligned[(data_aligned['converted']==0) & 
                           (data_aligned['group']== 'treatment')].reset_index()

data_control = pd.concat([converted_control, non_converted_control], ignore_index = True)
data_treatment = pd.concat([converted_treatment, non_converted_treatment], ignore_index= True)

Y_values_aligned = [converted_control.user_id.count() + (
        non_converted_control.user_id.count()),
     converted_treatment.user_id.count() + non_converted_treatment.user_id.count()
     ]

Y_values_not_aligned = [not_aligned_data_control.user_id.count(),
                        not_aligned_data_treatment.user_id.count()
                        ]
# Plotting bar chart to see how many records were aligned and how many weren't
N = len(Y_values_aligned)
ind = np.arange(N)
width = 0.35

X_values = ['Aligned_control', 'Not_aligned_control', 'Aligned_treatment',
            'Not_alignmed_treatment']

plt.bar(ind,Y_values_aligned, width, label = 'Aligned' )
plt.bar(ind+width,Y_values_not_aligned, width, label = 'Not Aligned' )
plt.ylabel('Count of records')
plt.xticks(ind+width/2, ('Control', 'Treatment'))
plt.legend(loc = 'best')
plt.show()


# Finding different statistical values
total_control = converted_control.user_id.count() + non_converted_control.user_id.count()
total_treatment = converted_treatment.user_id.count() + non_converted_treatment.user_id.count()

percent_converted_control = converted_control.user_id.count()/total_control

percent_converted_treatment = converted_treatment.user_id.count()/total_treatment


p = percent_converted_control
pc = percent_converted_treatment
n = total_control
nc = total_treatment

z_score = (p-pc)/math.sqrt((p*(1-p)/n) + (pc*(1-pc)/nc))
p_value = st.norm.sf(abs(z_score))*2



df.resample('D', on='Date_Time').mean()

C_C = converted_control.resample('d', on='timestamp').count()




























