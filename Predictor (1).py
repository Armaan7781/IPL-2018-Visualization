#!/usr/bin/env python
# coding: utf-8

# In[1]:


# Import packages

import pandas as pd
import numpy as np
import statsmodels.formula.api as smf
import matplotlib.pyplot as plt
import seaborn as sns
import datetime


# In[4]:


# Read in the data

ENG = pd.read_excel('C:/Users/consumer/Desktop/ARMAN/Coursera Datasets/Data/Week 1/Engsoccer2017-18.xlsx')
print(ENG.columns.tolist())


# In[5]:


ENG


# In[6]:


# Create df containing only the variables we need
# Create a counter

ENG18 = ENG[['AwayTeam','HomeTeam', 'FTAG','FTHG','Date','Ndate','Div']]
ENG18 = ENG18.rename(columns={'FTAG':'AG', 'FTHG':'HG'})
ENG18['count'] = 1
ENG18


# In[7]:


# Create df recording team performance as home team
# We create an additional column 'home' which here has a value

ENGhome = ENG18[['HomeTeam','HG','AG','count','Date','Ndate','Div']].copy()
ENGhome['home']= 1
ENGhome = ENGhome.rename(columns={'HomeTeam':'Team','AG':'GA','HG':'GH'})
ENGhome


# In[8]:


# Create df recording team performance as visiting team
# As above, we create an additional column 'home', which now has a value 0 to designate that these were away team games
ENGaway = ENG18[['AwayTeam','AG','HG','count','Date','Ndate','Div']].copy()
ENGaway['home']=0
ENGaway =ENGaway.rename(columns={'AwayTeam':'Team', 'AG':'GH','HG':'GA'})
ENGaway


# In[9]:


# Here is where the approach differs from the previous notebooks. Instead of taking sums and averages, we first 
# concatenate, meaning that we stack performances as home team and away team. This creates a list of games played
# by each team across the season.

ENG18c = pd.concat([ENGhome,ENGaway])
ENG18c


# In[10]:


#Let's Define A win
ENG18c['win']= np.where(ENG18c['GH']> ENG18c['GA'],1,0)
ENG18c


# In[11]:


ENG_EPL= ENG18c[ENG18c['Div']=='EPL']
ENG_EPL


# In[12]:


#Now we Define the season up to matchday 19, which was on 24-12-2017

Half1EPL = ENG_EPL[ENG_EPL.Ndate <= 20171223]
Half1EPL.describe()


# In[13]:


#Now we Define the season after matchday 19, which was on 24-12-2017

Half2EPL = ENG_EPL[ENG_EPL.Ndate >= 20171223]
Half2EPL.describe()


# In[14]:


# We now use .groupby to sum the number of games, wins, HG and AG for the first half of the season.

Half1EPLperf = Half1EPL.groupby('Team')['count','win','GH','GA'].sum().reset_index()
Half1EPLperf = Half1EPLperf.rename(columns={'count':'cnt1','win':'Win1','GH':'GF1','GA':'GA1'})
Half1EPLperf


# In[19]:


# From these statistics we calculate win percentage and Pythagorean Expectation for the first half of the season.

Half1EPLperf['WPC1'] = Half1EPLperf['Win1']/Half1EPLperf['cnt1']
Half1EPLperf['PYTH1'] = Half1EPLperf['GF1']**2/ (Half1EPLperf['GF1']**2 + Half1EPLperf['GA1']**2)
Half1EPLperf


# In[15]:


# We now use .groupby to sum the number of games, wins, HG and AG for the Later half of the season.

Half2EPLperf = Half2EPL.groupby('Team')['count','win','GH','GA'].sum().reset_index()
Half2EPLperf = Half2EPLperf.rename(columns={'count':'cnt2','win':'Win2','GH':'GF2','GA':'GA2'})
Half2EPLperf


# In[16]:


# From these statistics we calculate win percentage and Pythagorean Expectation for the Later half of the season.

Half2EPLperf['WPC2'] = Half2EPLperf['Win2']/Half2EPLperf['cnt2']
Half2EPLperf['PYTH2'] = Half2EPLperf['GF2']**2/ (Half2EPLperf['GF2']**2 + Half2EPLperf['GA2']**2)
Half2EPLperf


# In[21]:


# Now we merge the two dfs

Half2predictor = pd.merge(Half1EPLperf,Half2EPLperf, on='Team')
Half2predictor


# In[22]:


# First, plot Pythagorean Expectation against win percentage in the second half of the season

sns.relplot(x="PYTH1", y="WPC2", data = Half2predictor)


# In[26]:


# Now, compare this with a plot of win percentage from the first half of the season against win percentage
#in the second half of the season


sns.relplot(x="PYTH2", y="WPC1", data = Half2predictor)


# In[24]:


# The two plots look similar
# We can be more precise still if we compare the correlation coefficients. The first row of the table shows the 
# correlation of win percentage in second half of the season against itself, win percentage in the first half of the season,
# Pythagorean Expectation in the first half of the season, and Pythagorean Expectation in the second half of the season.
# Our focus is on comparing the second and third columns.

keyvars = Half2predictor[['Team','WPC2','WPC1','PYTH1','PYTH2']]
keyvars.corr()


# In[167]:


# We can also sort the variables to show for each club how close the relationships are between the first and second half
# of the season

keyvars = keyvars.sort_values(by=['PYTH2'],ascending=False)
keyvars


# In[ ]:




