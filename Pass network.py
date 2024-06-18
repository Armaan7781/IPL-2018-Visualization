#!/usr/bin/env python
# coding: utf-8

# In[51]:


import pandas as pd
from mplsoccer import VerticalPitch
from mplsoccer import Pitch
import matplotlib.pyplot as plt


# In[2]:


df = pd.read_csv('C:/Users/HP/Desktop/ARMAN/Main Portfolio/Football Analytics/valladolidA.csv')


# In[3]:


df.head()


# In[4]:


bar_df= df[df['teamId']== 'Barcelona']


# In[5]:


bar_df


# In[6]:


bar_df['passer'] = bar_df['playerId']
bar_df['recipient'] = bar_df['playerId'].shift(-1)

passes = bar_df[bar_df['type']=='Pass']
successful = passes[passes['outcome']=='Successful']


# In[7]:


successful


# In[8]:


subs = bar_df[bar_df['type']=='SubstitutionOff']
subs = subs['minute']
FirstSub = subs.min()

FirstSub


# In[9]:


successful = successful[successful['minute']< FirstSub]
successful


# In[10]:


pas = pd.to_numeric(successful['passer'], downcast = 'integer')
rec = pd.to_numeric(successful['recipient'], downcast = 'integer')


# In[11]:


successful['passer'] = pas
successful['recipient'] = rec

successful


# In[12]:


average_locations = successful.groupby('passer').agg({'x':['mean'], 'y': ['mean','count']})
average_locations.columns = ['x','y','count']


# In[13]:


average_locations


# In[14]:


average_locations.rename({'count':'pass_count'}, axis = 'columns', inplace= True)


# In[15]:


pass_between = successful.groupby(['passer', 'recipient']).id.count().reset_index()


# In[16]:


pass_between.rename({'id':'count'}, axis = 'columns', inplace= True)


# In[17]:


pass_between


# In[18]:


pass_between = pass_between.merge(average_locations, left_on = 'passer', right_index = True)
pass_between = pass_between.merge(average_locations, left_on = 'recipient', right_index = True,suffixes = ['', '_end'])


# In[19]:


pass_between


# In[20]:


pass_between.rename({'pass_count|':'pass_count'}, axis = 'columns', inplace= True)


# In[21]:


pass_between


# In[24]:


pass_between = pass_between[pass_between['count']> 3]


# In[25]:


pass_between


# In[56]:


# Create a football pitch
pitch = Pitch(pitch_type='statsbomb', pitch_color='#22312b', line_color='white')
fig, ax = pitch.draw(figsize=(10, 6))


arrows = pitch.arrows(1.2*pass_between.x,0.8*pass_between.y, 1.2*pass_between.x_end, 0.8*pass_between.y_end, ax=ax,
                     width = 2, alpha = 0.7, color='yellow', headwidth = 3, zorder = 1)

noded = pitch.scatter(1.2*average_locations.x, 0.8*average_locations.y,
                     s=100, color= 'red', edgecolors = 'black', linewidth = 2.5, alpha = 1, zorder = 1, ax=ax)
ax.set_title('Pass Networks of Barelona(vs Vallodiad)', fontsize=20, color = 'black')


# In[53]:


# Create pitch
pitch = Pitch(pitch_type='statsbomb', pitch_color='#22312b', line_color='white')
fig, ax = pitch.draw(figsize=(10, 6))

# Plot pass networks with line width based on pass count
for i, row in pass_between.iterrows():
    pitch.arrows(row['x'], row['y'], row['x_end'], row['y_end'], ax=ax, width=row['count']*0.2, alpha=0.7, color='yellow', headwidth=3, zorder=1)

# Plot average locations with player names
nodes = pitch.scatter(average_locations.x, average_locations.y, s=100, color='red', edgecolors='black', linewidth=2.5, alpha=1, zorder=1, ax=ax)
for i, row in average_locations.iterrows():
    ax.text(row['x'], row['y'], f'#{row["passer"]}', fontsize=12, ha='center', color='white')


# In[44]:


average_locations


# In[ ]:




