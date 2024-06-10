#!/usr/bin/env python
# coding: utf-8

# In[1]:


#import the packages

import pandas as pd

from statsbombpy import sb

from mplsoccer import Pitch

import matplotlib.pyplot as plt

from matplotlib.lines import Line2D

from matplotlib.patches import Rectangle

from matplotlib.offsetbox import OffsetImage, AnnotationBbox


# In[2]:


#check the data
sb.competitions()


# In[3]:


sb.matches(competition_id = 9, season_id= 281)


# In[4]:


#let's select the match_id
MATCH = 3869685


# In[5]:


#let's create a df to store this data
match_events_df = sb.events(match_id = MATCH)


# In[6]:


#let's create a new df to read the json file we insatlled and store the data
match_360_df = pd.read_json(f'C:/Users/HP/Documents/GitHub/open-data/data/three-sixty/{MATCH}.json')


# In[7]:


match_events_df


# In[8]:


#here we are doing a left join through which we will be able to create the df we need
df = pd.merge(left = match_events_df, right = match_360_df, left_on = 'id', right_on = 'event_uuid', how = 'left')


# In[9]:


df.head()


# In[10]:


#Let;s first check the column names
df.columns


# In[11]:


#let's first see the players and thier passes

# Filter rows where 'type' is 'Pass'
df_pass = df[df['type'] == 'Pass']
# Group by 'player' and 'player_id' and count occurrences
df_pass_count = df_pass.groupby(['player', 'player_id', 'team']).size().reset_index(name='count')

# Display counts
print(df_pass_count)


# In[12]:


# Now we'll calculate Argentina's apsses and will store it in

Arg_Pass = df_pass_count[df_pass_count['team'] == 'Argentina']

# Group by 'player' and 'player_id' and count occurrences
df_pass_count = df_pass.groupby(['player', 'player_id']).size().reset_index(name='count')

# Display counts
Arg_Pass


# In[13]:


#Now let's create a diff df for Argentina
Argentina_team = 'Argentina'

# Select all passes of the Argentina team
Argentina_passes = df[(df['team'] == Argentina_team) & (df['type'] == 'Pass')].reset_index(drop=True)

Argentina_passes


# In[14]:


# Ensure the index is correct
Argentina_passes[['x_start', 'y_start']] = pd.DataFrame(Argentina_passes.location.tolist(), index=Argentina_passes.index)
Argentina_passes[['x_end', 'y_end']] = pd.DataFrame(Argentina_passes.pass_end_location.tolist(), index=Argentina_passes.index)


# In[15]:


# Determine the pass direction
def pass_direction(row):
    if row['x_end'] - row['x_start'] > 10:
        return 'Forward'
    elif 0 <= abs(row['x_end'] - row['x_start']) <= 10:
        return 'Sideways'
    else:
        return 'Backward'

Argentina_passes['pass_direction'] = Argentina_passes.apply(pass_direction, axis=1)


# In[16]:


# Group by 'player' and 'player_id' and count occurrences
Arg_pass_count = Argentina_passes.groupby(['pass_direction']).size().reset_index(name='count')

# Display counts
print(Arg_pass_count)


# In[23]:


p = Pitch(pitch_type = 'statsbomb')

fig, ax = p.draw(figsize=(12,8))


# Custom background rectangle to color the pitch
pitch_background = Rectangle((-50, -50), 210, 200, edgecolor='none', facecolor='green', zorder=0)
ax.add_patch(pitch_background)

# List of unique pass_outcome values
pass_outcome_values = ['Incomplete', 'Unknown', 'Pass Offside', 'nan']

# Define colors for each pass direction
colors = {
    'Forward': 'red',
    'Sideways': 'blue',
    'Backward': 'black'
}

# Scatter plot for the starting points of passes
p.scatter(x=Argentina_passes['x_start'], y=Argentina_passes['y_start'], ax=ax, color='white', s=50, edgecolors='black', zorder=3, label='Pass Start')

# Loop through pass directions and plot lines
for direction, color in colors.items():
    filtered_passes = Argentina_passes[Argentina_passes['pass_direction'] == direction]
    for i, row in filtered_passes.iterrows():
        p.lines(xstart=row['x_start'], ystart=row['y_start'], xend=row['x_end'], yend=row['y_end'], ax=ax, color=color, linewidth=0.5, comet=True, zorder=1)

# Adding lines to legend
legend_lines = [
    Line2D([0], [0], color='red', linewidth=2, linestyle='-', label='Forward'),
    Line2D([0], [0], color='blue', linewidth=2, linestyle='-', label='Sideways'),
    Line2D([0], [0], color='black', linewidth=2, linestyle='-', label='Backward')
]

# Scatter plot legend handles and labels
handles, labels = ax.get_legend_handles_labels()

# Combine legend handles and labels
ax.legend(handles + legend_lines, labels + ['Forward', 'Sideways', 'Backward'], loc='upper left')

# Adding a title and labels
ax.set_title('Argentina Passes in the World Cup Final(Filtered)', fontsize=16)

# Display the counts in the top left corner
counts_text = '\n'.join([f"{row['pass_direction']}: {row['count']}" for index, row in Arg_pass_count.iterrows()])
ax.text(-3.5, 17, counts_text, fontsize=12, bbox=dict(facecolor='white', alpha=0.7))


plt.show()


# In[18]:


# Assuming 'team' column contains team names
France = 'France'

# Select all passes of the Argentina team
France_passes = df[(df['team'] == France) & (df['type'] == 'Pass')].reset_index(drop=True)

France_passes


# In[19]:


# Ensure the index is correct
France_passes[['x_start', 'y_start']] = pd.DataFrame(France_passes.location.tolist(), index=France_passes.index)
France_passes[['x_end', 'y_end']] = pd.DataFrame(France_passes.pass_end_location.tolist(), index=France_passes.index)


# In[20]:


# Determine the pass direction
def pass_direction(row):
    if row['x_end'] - row['x_start'] > 10:
        return 'Forward'
    elif 0 <= abs(row['x_end'] - row['x_start']) <= 10:
        return 'Sideways'
    else:
        return 'Backward'

France_passes['pass_direction'] = France_passes.apply(pass_direction, axis=1)


# In[21]:


# Group by 'player' and 'player_id' and count occurrences
France_pass_count = France_passes.groupby(['pass_direction']).size().reset_index(name='count')

# Display counts
print(France_pass_count)


# In[24]:


p = Pitch(pitch_type = 'statsbomb')

fig, ax = p.draw(figsize=(12,8))


# Custom background rectangle to color the pitch
pitch_background = Rectangle((-50, -50), 210, 200, edgecolor='none', facecolor='green', zorder=0)
ax.add_patch(pitch_background)

# List of unique pass_outcome values
pass_outcome_values = ['Incomplete', 'Unknown', 'Pass Offside', 'nan']

# Define colors for each pass direction
colors = {
    'Forward': 'red',
    'Sideways': 'blue',
    'Backward': 'black'
}

# Scatter plot for the starting points of passes
p.scatter(x=France_passes['x_start'], y=France_passes['y_start'], ax=ax, color='white', s=50, edgecolors='black', zorder=3, label='Pass Start')

# Loop through pass directions and plot lines
for direction, color in colors.items():
    filtered_passes = France_passes[France_passes['pass_direction'] == direction]
    for i, row in filtered_passes.iterrows():
        p.lines(xstart=row['x_start'], ystart=row['y_start'], xend=row['x_end'], yend=row['y_end'], ax=ax, color=color, linewidth=0.5, comet=True, zorder=1)

# Adding lines to legend
legend_lines = [
    Line2D([0], [0], color='red', linewidth=2, linestyle='-', label='Forward'),
    Line2D([0], [0], color='blue', linewidth=2, linestyle='-', label='Sideways'),
    Line2D([0], [0], color='black', linewidth=2, linestyle='-', label='Backward')
]

# Scatter plot legend handles and labels
handles, labels = ax.get_legend_handles_labels()

# Combine legend handles and labels
ax.legend(handles + legend_lines, labels + ['Forward', 'Sideways', 'Backward'], loc='upper left')

# Adding a title and labels
ax.set_title('France Passes in the World Cup Final(Filtered)', fontsize=16)

# Display the counts in the top left corner
counts_text = '\n'.join([f"{row['pass_direction']}: {row['count']}" for index, row in France_pass_count.iterrows()])
ax.text(-3.5, 17, counts_text, fontsize=12, bbox=dict(facecolor='white', alpha=0.7))

plt.show()


# In[ ]:





# In[ ]:





# In[ ]:




