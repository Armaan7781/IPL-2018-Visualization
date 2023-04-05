#!/usr/bin/env python
# coding: utf-8

# In[1]:


#Let's import the packages first

import pandas as pd
import numpy as np
import statsmodels.formula.api as smf
import matplotlib.pyplot as plt
import seaborn as sns


# In[2]:


#Let's Read the data
ENG18 = pd.read_excel('C:/Users/consumer/Desktop/ARMAN/Coursera Datasets/Data/Week 1/Engsoccer2017-18.xlsx')
print(ENG18.columns.tolist())


# In[3]:


ENG18


# In[13]:


# Once again our data is in the form of game results. We first identify whether the result was a win for the home team (H),
# the away team (A) or a draw (D). We also create the counting variable.

ENG18['hwin'] = np.where(ENG18['FTR'] == 'H',1,np.where(ENG18['FTR']=='D',.5,0))
ENG18['awin'] = np.where(ENG18['FTR'] == 'A',1,np.where(ENG18['FTR']=='D',.5,0))
ENG18['count'] = 1
ENG18


# In[15]:


# Once again we have to create separate dfs to calculate home team and away team performance.
# Here is the home team df, including only the variables we need.

ENGhome = ENG18.groupby(['HomeTeam','Div'])['count','hwin','FTHG','FTAG'].sum().reset_index()
ENGhome = ENGhome.rename(columns={'HomeTeam':'Team', 'FTHG':'HGh', 'FTAG':'AGh', 'count':'ph'})
ENGhome


# In[16]:


# Now we create the mirror image df for the away team results.

ENGaway = ENG18.groupby(['AwayTeam'])['count','awin','FTHG','FTAG'].sum().reset_index()
ENGaway = ENGaway.rename(columns={'AwayTeam':'Team', 'count':'pa', 'FTHG':'HGa', 'FTAG':'AGa'})
ENGaway


# In[17]:


#Now let's merge it
ENG18c = pd.merge(ENGhome,ENGaway, on=['Team'])
ENG18c


# In[18]:


# Sum the results by home and away measures to get the team overall performance for the season
ENG18c['W'] = ENG18c['hwin'] + ENG18c['awin']
ENG18c['G'] = ENG18c['ph'] + ENG18c['pa']
ENG18c['GF'] = ENG18c['HGh']+ ENG18c['AGa']
ENG18c['GA'] = ENG18c['AGh']+ ENG18c['HGa']
ENG18c


# In[19]:


#Now. let's create Win% and Pythagorean%
ENG18c['WPC'] = ENG18c['W']/ ENG18c['G']
ENG18c['PYTH'] = ENG18c['GF']**2/ (ENG18c['GF']**2 + ENG18c['GA']**2)
ENG18c


# In[30]:


# Plot the data
# Seaborn allows us to color code teams based on division

sns.relplot(x="PYTH", y="WPC", data =ENG18c, hue='Div')


# In[28]:


#Run The Regression

pyth_reg = smf.ols(formula = 'WPC ~ PYTH', data= ENG18c).fit()
pyth_reg.summary()
