#!/usr/bin/env python
# coding: utf-8

# In[1]:


#First Let's Import Packages
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


# In[5]:


MI_CSK = pd.read_excel('C:/Users/consumer/Desktop/ARMAN/Coursera Datasets/Data/Week 3/MIvCSKadj.xlsx')
print(MI_CSK.columns.tolist())
MI_CSK


# In[6]:


#Now Let's plot runs by deliveries
plt.plot(MI_CSK['MI_delivery_no'], MI_CSK['MI_runs_total_end'])


# We can see from this chart that Mumbai maintained a steady pace throughout the inning - the score increases more or less linearly with the number of balls.
# The next thing we want to do is incorporate the fall of wickets into the chart, to see how their batting resources changed as the inning progressed.
# he "wicket" columns for each team tell us if a wicket fell on that delivery ('1') or not ('0'). We can create dfs as subsets of main df, to identify the delivery number and runs scored when the wicket fell.

# In[7]:


MIwicket = MI_CSK[MI_CSK['MI_wicket']> 0]
CSKwicket = MI_CSK[MI_CSK['CSK_wicket']> 0]
MIwicket


# In[9]:


# We can now plot the fall of wickets alongside the runs total.
# Note that we obtain the red dots for wickets by specifying 'ro' - 'r' for red and 'o' for circle dots

plt.plot(MI_CSK['MI_delivery_no'], MI_CSK['MI_runs_total_end'], MIwicket['MI_runs_total_end'], 'ro')


# In[11]:


# Now let's compare runs of Mumbai Indians and Chennai Super Kings
plt.plot(MI_CSK['CSK_delivery_no'], MI_CSK['MI_runs_total_end'],MI_CSK['CSK_runs_total_end'])


# We can see that Chennai's innings (in orange) progressed rather differently. Initially Chennai were well ahead of the pace set by Mumbai. However, Chennai slowed down considerably after about 25 deliveries, and were well behind Mumbai's scoring rate by mid-innings. Only at the end did Chennai accelerate, and overtake Mumbai's score to win the game.

# In[14]:


plt.plot(MI_CSK['MI_delivery_no'], MI_CSK['MI_runs_total_end'], MIwicket['MI_runs_total_end'], 'bo')
plt.plot(MI_CSK['CSK_delivery_no'], MI_CSK['CSK_runs_total_end'], CSKwicket['CSK_runs_total_end'], 'ro')


# Now we can see why Chennai fell behind after the initial good start. Unlike Mumbai, Chennai's wickets fell steadily throughout the innings, a fact which tended to slow down the scoring rate. In fact, Chennai had lost eight wickets before its final accleration around the 100 delivery mark.
# 
# This analysis was for just one game. We now write a program which will allow us to reproduce these profiles for any game in IPL 2018 season, and compare profiles for any pair of games.
# 
# We now load a dataframe that includes every delivery for the season:

# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:




