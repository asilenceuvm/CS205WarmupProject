#!/usr/bin/env python
# coding: utf-8

# In[18]:


import pandas as pd
import numpy as np

# import data: csv -> pandas df
df = pd.read_csv('spotify_global_2019_most_streamed_tracks_audio_features.csv')


# In[55]:


# attributes for all data
df.columns


# In[59]:


# table of song-artist data
df.head(10)


# In[60]:


# table of artist data with given attributes
artistsDB = df[['Artist','Artist_popularity','Artist_follower','Artist_id']]
artistsDB.head(10)


# In[63]:


# table of songs data with given attributes
songsDB = df[['Rank','Track_id','Streams','Track Name']]
songsDB.head(10)


# In[62]:


# export artist and song DBs as csv files
artistsDB.to_csv('CS205 warmup artistsDB.csv',index=False)
songsDB.to_csv('CS205 warmup songsDB.csv',index=False)


# In[12]:


# numpy array of artist names
artists = artistsDB['Artist'].values


# In[67]:


# loop to count artists, store the max count and index of artist
# in order to find the most common artist in our data

index = 0
maxCount = 0
for i in range(len(artists)):
    count = 0
    for j in range(len(artists)):
        if artists[i] == artists[j]:
            count+=1
    if count > maxCount:
        maxCount = count
        index = i


# In[68]:


print(artists[index],'was on the list',maxCount,'times')

