#!/usr/bin/env python
# coding: utf-8

# In[1]:

# Firstly lets import the packages
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


# In[2]:

#Lets load the data 
IPL2018 = pd.read_excel('C:/Users/consumer/Desktop/ARMAN/Coursera Datasets/Data/Week 3/IPL2018_results.xlsx')
pd.set_option('display.max_columns', 50)
display(IPL2018)


# In[ ]:


# let's see the names of varibles in the data


# In[3]:


print(IPL2018.columns.tolist())


# In[ ]:


#The variables we are interested in are the runs scored by each team, which are listed
#in "innings1" and "innings2". 
#A histogram will show us the variation of runs scored. 
#We specify the number of 'bins' - we use 10 bins here, which divides the data between the highest and lowest scores into ten equals ranges of 20 runs. 
#The vertical axis then tells us the percentage of scores in innings1 in each data range.


# In[4]:


IPL2018.hist(column = 'innings1', bins = 10)


# In[5]:


IPL2018.hist(column = 'innings2', bins = 10)


# Comparing these two graphs it looks as if the scores in innings1 are skewed slightly to the left, and in innings2 slightly to the right. This could tell us something, but we should be careful. The x-axis for innings1 runs from 80 to 240, while for innings2 runs from 60 to 220. To compare, we really should specify that the x-axis has the same range for both sets of data. We do that in the next line:

# In[6]:


IPL2018.hist(column = 'innings1', bins = 10)
plt.xlim((60, 250))
plt.ylim((0, 20))
IPL2018.hist(column = 'innings2', bins = 10)
plt.xlim((60, 250))
plt.ylim((0, 20))
plt.plot


# We can now see that the two innings have quite similar distributions centered around roughly the same median score. The two main differences are that the scores for innings2 seem truncated around the 200-215 mark. That is probably a result of the run chase effect - teams batting second either reach the required target and stop, or the target set in the first place was so high that the team batting second collapsed with a very low score.

# In[7]:


IPL2018[['innings1','innings2']].plot.hist(alpha=.5,bins=10)
plt.xlabel('Runs')
plt.ylabel('Frequency')
plt.title("Runs distribution by innings", fontsize=15)
plt.xlim((60, 250))
plt.ylim((0, 20))


# Having looked at the distributions comparing the team batting first and second, now let's compare the histograms for the teams that win and the teams that lose.
# 
# First, define winning and losing teams - which is derived by comparing the number of runs scored.

# In[8]:


IPL2018['WinScore'] = np.where(IPL2018['innings1']> IPL2018['innings2'],
                               IPL2018['innings1'], IPL2018['innings2'])
IPL2018['LoseScore'] = np.where(IPL2018['innings1']> IPL2018['innings2'],
                               IPL2018['innings2'], IPL2018['innings1'])


# In[10]:


# Now we can plt 2 histograms together

IPL2018[['WinScore', 'LoseScore']].plot.hist(alpha = .5, bins = 10)
plt.xlabel('Runs')
plt.ylabel('Frequency')
plt.title("Runs Distibution by Innings", fontsize = 16)
plt.xlim(60,250)
plt.ylim(0, 20)


# We can see that the winning score appears like a rightward shift of the losing score- which should not be surprising! For a low score, losing scores must outnumber winning scores, while for high scores, winning scores must outnumber losing scores
