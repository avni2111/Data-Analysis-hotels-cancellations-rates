#!/usr/bin/env python
# coding: utf-8

# ## Business Problem 
#  In recent years, City Hotel and Resort Hotel have seen high cancellation rates. Each hotel is now dealing 
#  with a number of issues as a result, including fewer revenues and less than ideal hotel room use. Consequently, lowering cancellation rates is both hotels' primary goal in order to increase their efficiency in generating revenues, and for us to offer thorough business advice to address this problem.
#  
#  The analysis of hotel cancellation as well as other factors that have no bearing on business and yearly revenue generation are the main topics of this report.
# 

# ## Importing Libraries 

# In[1]:


import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import warnings
warnings.filterwarnings('ignore')


# ## Loading Dataset

# In[2]:


df = pd.read_csv('hotel_bookings 2.csv')


# ## Exploratory Data Analysis and Data Cleaning

# In[3]:


df.head()


# In[4]:


df.tail()


# In[5]:


df.shape #For number of rows and column


# In[6]:


df.columns


# In[7]:


df.info()


# In[8]:


df['reservation_status_date'] = pd.to_datetime(df['reservation_status_date'])


# In[9]:


df.info()


# In[10]:


df.describe(include = 'object')


# In[11]:


for col in df.describe(include='object').columns:
    print(col)
    print(df[col].unique())
    print('-'*50)


# In[12]:


df.isnull().sum()


# In[13]:


df.drop(['company','agent'],axis=1,inplace=True) # column me drop krna hai toh axis =1, and dataframe me changes krne hai toh inplace=True dena pdta hai
df.dropna(inplace = True)


# In[14]:


df.isnull().sum()


# In[15]:


df.describe() # summery statistics jbtk aapne include = object na dia ho


# In[16]:


df = df[df['adr']<5000]


# ## Data analysis and visualizations

# In[17]:


cancelled_perc = df['is_canceled'].value_counts(normalize = True)
print(cancelled_perc)

plt.figure(figsize = (5,4))
plt.title('Reservation status count')
plt.bar(['Not canceled','Canceled'],df['is_canceled'].value_counts(),edgecolor = 'k',width=0.7)
plt.show()


# In[22]:


plt.figure(figsize=(8, 4))
ax1 = sns.countplot(x='hotel', hue='is_canceled', data=df, palette='Blues')
legend_labels, _ = ax1.get_legend_handles_labels()
ax1.legend(bbox_to_anchor=(1, 1))
plt.title('Reservation status in different hotels', size=20)
plt.xlabel('Hotel')  
plt.ylabel('Number of reservations')  
plt.show()


# In[23]:


resort_hotel = df[df['hotel'] == 'Resort Hotel']
resort_hotel['is_canceled'].value_counts(normalize = True)


# In[25]:


city_hotel = df[df['hotel'] == 'City Hotel']
city_hotel['is_canceled'].value_counts(normalize = True)


# In[27]:


resort_hotel = resort_hotel.groupby('reservation_status_date')[['adr']].mean()
city_hotel = city_hotel.groupby('reservation_status_date')[['adr']].mean()


# In[29]:


plt.figure(figsize =(20,8))
plt.title('Average Daily Rate in City and Resort Hotel', fontsize = 30)
plt.plot(resort_hotel.index, resort_hotel['adr'],label = 'Resort Hotel')
plt.plot(city_hotel.index, city_hotel['adr'],label = 'City Hotel')
plt.legend(fontsize = 20)
plt.show()


# In[32]:


df['month'] = df['reservation_status_date'].dt.month
plt.figure(figsize = (16,8))
ax1 = sns.countplot(x = 'month', hue = 'is_canceled', data = df, palette = 'bright')
legend_labels,_ = ax1.get_legend_handles_labels()
ax1.legend(bbox_to_anchor=(1,1))
plt.title('Reservation status per month', size = 20)
plt.xlabel('month')
plt.ylabel('number of reservations')
plt.legend(['not canceled','canceled'])
plt.show()


# In[42]:


data = df[df['is_canceled'] == 1].groupby('month')[['adr']].sum().reset_index()
plt.figure(figsize =(15,8))
plt.title('ADR per month', fontsize = 30)
sns.barplot(x='month',y='adr',data = data)
plt.show()


# In[43]:


cancelled_data = df[df['is_canceled'] == 1]
top_10_country = cancelled_data['country'].value_counts()[:10]
plt.figure(figsize = (8,8))
plt.title('Top 10 country with reservation canceled')
plt.pie(top_10_country, autopct = '%.2f', labels = top_10_country.index)
plt.show()


# In[44]:


df['market_segment'].value_counts()


# In[45]:


df['market_segment'].value_counts(normalize = True)


# In[46]:


cancelled_data['market_segment'].value_counts(normalize = True)


# In[51]:


cancelled_df_adr = cancelled_data.groupby('reservation_status_date')[['adr']].mean()
cancelled_df_adr.reset_index(inplace = True)
cancelled_df_adr.sort_values('reservation_status_date', inplace = True)

not_cancelled_data = df[df['is_canceled'] ==0]
not_cancelled_df_adr = not_cancelled_data.groupby('reservation_status_date')[['adr']].mean()
not_cancelled_df_adr.reset_index(inplace = True)
not_cancelled_df_adr.sort_values('reservation_status_date', inplace = True)

plt.figure(figsize = (20,6))
plt.title('Average Daily Rate')
plt.plot(not_cancelled_df_adr['reservation_status_date'],not_cancelled_df_adr['adr'],label ='not cancelled')
plt.plot(cancelled_df_adr['reservation_status_date'],cancelled_df_adr['adr'],label = 'cacelled')
plt.legend()


# In[52]:


cancelled_df_adr = cancelled_df_adr[(cancelled_df_adr['reservation_status_date']>'2016')& (cancelled_df_adr['reservation_status_date']<'2017-09')]
not_cancelled_df_adr = not_cancelled_df_adr[(not_cancelled_df_adr['reservation_status_date']>'2016')& (not_cancelled_df_adr['reservation_status_date']<'2017-09')]


# In[55]:


plt.figure(figsize = (20,6))
plt.title('Average Daily Rate',size = 20)
plt.plot(not_cancelled_df_adr['reservation_status_date'],not_cancelled_df_adr['adr'],label = 'not cancelled')
plt.plot(cancelled_df_adr['reservation_status_date'],cancelled_df_adr['adr'],label = 'cancelled')
plt.legend(fontsize = 20)
plt.show()

