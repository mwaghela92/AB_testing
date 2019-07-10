#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jul  9 11:52:32 2019

@author: mayur
"""

import pandas as pd

# importing data into a dataframe
data = pd.read_csv('/Users/mayur/Documents/GitHub/AB_testing/'
                   'Data/ab_data.csv')

data.dtypes

# converting timestamp to datetime()
data['timestamp'] = pd.to_datetime(data['timestamp'])
data['group'] = data['group'].str.split(',')

# finding results not aligned for campaign

not_aligned_data1 = data[(data['group']=='control') 
                    & (data['landing_page']== 'new_page')]

not_aligned_data2 = data[(data['group']=='treatment') 
                    & (data['landing_page']== 'old_page')]

# dropping data that is not aligned

data_aligned = data.merge(not_aligned_data1, how = 'left', indicator = True)
data_aligned = data_aligned[data_aligned['_merge'] == 'left_only']
data_aligned = data_aligned.drop('_merge', axis = 1)

data_aligned = data.merge(not_aligned_data2, how = 'left', indicator = True)
data_aligned = data_aligned[data_aligned['_merge'] == 'left_only']
data_aligned = data_aligned.drop('_merge', axis = 1)



# calculating number of converted transactions
control_converted = data[(data['converted'] == 1) & 
                         (data['group'] == 'control')].user_id.count()

treatment_converted = data[(data['converted'] == 1) & 
                           (data['group'] == 'treatment')].user_id.count()

data_by_date = data.groupby([data['timestamp'].dt.date, 
                             'converted']).user_id.count()
