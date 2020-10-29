#!/usr/bin/env python
# coding: utf-8

# in this code i cleaned Raw data as well as for business model i analysed data in this code but for better understatnding 
# of model you would have to see my ppt and business rules i made.

# In[139]:


#code will work on df2 name data which is partial clean data of given data


# #importing library 

# In[2]:


import pandas as pd
from pandas import DataFrame
from pandas import Series
import matplotlib.pyplot as plt
import numpy as np
from fuzzywuzzy import fuzz
from functools import partial
from fuzzywuzzy import process


# In[3]:


#loading dataset


# In[4]:


df = pd.read_excel(r'C:\Users\lohani\Desktop\projects\peacock solar\data\df2.xlsx')


# In[5]:


df.head()


# In[6]:


df.dtypes


# In[7]:


#changing data type 


# In[8]:


df['Sex'] = df['Sex'].astype('category')
df['homeloan'] = df['homeloan'].astype('category')
df['relativehave'] = df['relativehave'].astype('category')
df['knowsolar'] = df['knowsolar'].astype('category')
df['except_least_save_elec'] = df['except_least_save_elec'].astype('category')
df['roofnotsuitable'] = df['roofnotsuitable'].astype('category')
df['not_know_installer'] = df['not_know_installer'].astype('category')
df['dont_undr_solr'] = df['dont_undr_solr'].astype('category')
df['outlook_house'] = df['outlook_house'].astype('category')
df['highcost'] = df['highcost'].astype('category')
df['lack_loan'] = df['lack_loan'].astype('category')
df['lack_govt'] = df['lack_govt'].astype('category')
df['not_suff_money'] = df['not_suff_money'].astype('category')
df['inv_pay_back'] = df['inv_pay_back'].astype('category')


# In[9]:


df['earnfromroof'] = df['earnfromroof'].astype('category')
df['status_symbol'] = df['status_symbol'].astype('category')
df['env_fri'] = df['env_fri'].astype('category')
df['newtec'] = df['newtec'].astype('category')
df['lowmaint'] = df['lowmaint'].astype('category')
df['bill_save'] = df['bill_save'].astype('category')
df['elec_price_inc'] = df['elec_price_inc'].astype('category')
df['pwrbckup'] = df['pwrbckup'].astype('category')
df['How much aware are you about solar?'] = df['How much aware are you about solar?'].astype('category')


# In[12]:


#changing all responses into lower case 


# In[13]:


df['What is the type of home that you own?'] = df['What is the type of home that you own?'].str.lower()
df['Do you plan to build an additional floor? (If other, what does it depend on?)'] = df['Do you plan to build an additional floor? (If other, what does it depend on?)'].str.lower()
df['Name the Solar company you know'] = df['Name the Solar company you know'].str.lower()
df['What Power Backup do you use? '] = df['What Power Backup do you use? '].str.lower()
df['Plot size of the house (In Square yards)'] = df['Plot size of the house (In Square yards)'].str.lower()


# In[14]:


# removing all spaces present between responses 


# In[15]:


df['What is the type of home that you own?'] = df['What is the type of home that you own?'].str.strip()
df['Do you plan to build an additional floor? (If other, what does it depend on?)'] = df['Do you plan to build an additional floor? (If other, what does it depend on?)'].str.strip()
df['Name the Solar company you know'] = df['Name the Solar company you know'].str.strip()
df['What Power Backup do you use? '] = df['What Power Backup do you use? '].str.strip()
df['Plot size of the house (In Square yards)'] = df['Plot size of the house (In Square yards)'].str.strip()


# In[ ]:


# cleaning home type column 
#checking what are are unique responses of home type
# changing some similar name of house type into 'independent house or villa'


# In[ ]:


df['What is the type of home that you own?'].unique()


# In[19]:


df['What is the type of home that you own?'] = df['What is the type of home that you own?'].replace({'independent house':'independent house or villa', 'my permanent home':'independent house or villa', 'own house':'independent house or villa', '3floors building':'independent house or villa'})


# In[20]:


#counting no. of different types houses 


# In[21]:


df.groupby('What is the type of home that you own?').count()


# In[22]:


#creating dummies of house type 
#independent house or villa = 1
# dropping 'What is the type of home that you own?', 'Sex', 'Marital Status', "Who owns the house you live in?" as unnecessary column


# In[23]:


dummy = pd.get_dummies(df['What is the type of home that you own?'])
df = pd.concat((df, dummy['independent house or villa']), axis =1)
df = df.drop(['What is the type of home that you own?', 'Sex', 'Marital Status', "Who owns the house you live in?"], axis=1)


# In[24]:


#changing name of male as sex and 'independent house or villa' as 'ownhome'


# In[25]:


df = df.rename(columns = {'Male' : 'sex', 'independent house or villa': 'ownhome'})


# In[26]:


df.head()


# In[132]:


# cleaning Do you plan to build an additional floor? (If other, what does it depend on?  column 
#checking what are are unique responses


# In[29]:


df['Do you plan to build an additional floor? (If other, what does it depend on?)'].unique()


# In[30]:


#creating dummies of Do you plan to build an additional floor?
#yes = 1
# dropping 'Do you plan to build an additional floor? (If other, what does it depend on?)'
# renaming yes as 'plantobuildflor'


# In[31]:


dummy = pd.get_dummies(df['Do you plan to build an additional floor? (If other, what does it depend on?)'])
df = pd.concat((df, dummy['yes']), axis =1)
df = df.drop(['Do you plan to build an additional floor? (If other, what does it depend on?)'], axis=1)
df = df.rename(columns = {'yes': 'plantobuildflor'})


# In[32]:


#cleaning Name the Solar company you know 
# checking what are are unique responses of Name the Solar company you know


# In[33]:


df['Name the Solar company you know'].unique()


# In[34]:


df.groupby('Name the Solar company you know').count()


# In[35]:


#string matching using fuzzy-wuzzy


# In[36]:


categories = ['peacock']


# In[37]:


categories


# In[38]:


for company in categories:
          matches = process.extract(company, df['Name the Solar company you know'], 
                            limit = df.shape[0])


# In[39]:


for possible_match in matches:
  if possible_match[1] >= 70:
    # Find matching cuisine type
    matching_cuisine = df['Name the Solar company you know'] == possible_match[0]
    df.loc[matching_cuisine, 'Name the Solar company you know'] = company


# In[40]:


#creating dummies of Name the Solar company you know
# peacock = 1
# dropping Name the Solar company you know
# renaming peacock' as 'knowpeacock'


# In[41]:


dummy = pd.get_dummies(df['Name the Solar company you know'])


# In[42]:


df = pd.concat((df, dummy['peacock']), axis =1)
df = df.drop(['Name the Solar company you know'], axis=1)
df = df.rename(columns = {'peacock': 'knowpeacock'})


# In[43]:


df.groupby('knowpeacock').count()


# In[ ]:


# cleaning wWhat Power Backup do you use? column 
#1st by viewing what are unique values
#renaming those which are similar to solar as solar
#renaming those which are similar to invertor as invertor
#renaming those which are similar to generator as generator 


# In[44]:


df.groupby('What Power Backup do you use? ').count()


# In[46]:


df['What Power Backup do you use? '].unique()


# In[47]:


cat = ['solar']


# In[48]:


for backup in cat:
          matches1 = process.extract(backup, df['What Power Backup do you use? '], 
                            limit = df.shape[0])


# In[49]:


matches1


# In[50]:


for possible_match in matches1:
  if possible_match[1] >= 60:
    # Find matching cuisine type
    matching_backup = df['What Power Backup do you use? '] == possible_match[0]
    df.loc[matching_backup, 'What Power Backup do you use? '] = backup


# In[51]:


df['What Power Backup do you use? '].unique()


# In[52]:


df.groupby(['What Power Backup do you use? ', 'State']).count()


# In[53]:


cat2 = ['inverter']


# In[54]:


for backup1 in cat2:
          matches3 = process.extract(backup1, df['What Power Backup do you use? '], 
                            limit = df.shape[0])


# In[55]:


for possible_match in matches3:
    if possible_match[1] >= 90:
      # Find matching cuisine type
      matching_backup1 = df['What Power Backup do you use? '] == possible_match[0]
      df.loc[matching_backup1, 'What Power Backup do you use? '] = backup1


# In[56]:


matches3


# In[57]:


df['What Power Backup do you use? '].unique()


# In[58]:


cat3 = ['generator']


# In[59]:


for backup2 in cat3:
          matches4 = process.extract(backup2, df['What Power Backup do you use? '], 
                            limit = df.shape[0])


# In[60]:


matches4


# In[61]:


for possible_match in matches4:
    if possible_match[1] >= 67:
      # Find matching cuisine type
      matching_backup2 = df['What Power Backup do you use? '] == possible_match[0]
      df.loc[matching_backup2, 'What Power Backup do you use? '] = backup2


# In[62]:


df['What Power Backup do you use? '].unique()


# In[63]:


df.groupby(['What Power Backup do you use? ', 'State']).count()


# In[64]:


#renaming those which donot falls in above 3 categories as no backup


# In[65]:


df['What Power Backup do you use? '] = df['What Power Backup do you use? '].replace({'candle':'no backup'})


# In[66]:


df['What Power Backup do you use? '] = df['What Power Backup do you use? '].replace({'captive power pack for whole colonyy':'backup not required', 'mi power bank':'no backup', 'nuclear reactor':'no backup','electrycity': 'no backup'})


# In[67]:


df['What Power Backup do you use? '] = df['What Power Backup do you use? '].replace({"rechargable emergency light":'no backup'})


# In[68]:


df['What Power Backup do you use? '] = df['What Power Backup do you use? '].replace({"light doesn't go in our area" :'backup not required', 'candles': 'no backup', 'no':'no backup', 'no idea' :'no backup', 'hindalco provides electricity 24*7':'backup not required', 'owned thermal power plant':'no backup', 'cng':'no backup', 'g e.b':'no backup'})


# In[69]:


df['What Power Backup do you use? '] = df['What Power Backup do you use? '].replace({'society power back up': 'backup not required', "two connections":'backup not required', 'nai batana':'no backup', "h":"no backup"})


# In[70]:


df['What Power Backup do you use? '] = df['What Power Backup do you use? '].replace({'candle, rechargable emergency light': 'no backup', 'none':'no backup'})


# In[71]:


df['What Power Backup do you use? '].unique()


# In[72]:


df.groupby(['What Power Backup do you use? ', 'State']).count()


# In[ ]:


#checking null 


# In[73]:


df.isnull().sum()


# In[133]:


#cleaning plot size of house
# removing 'square feet from responses 
#checking what are unique values 


# In[75]:


df['Plot size of the house (In Square yards)'] = df['Plot size of the house (In Square yards)'].str.replace('square feet','')


# In[76]:


df['Plot size of the house (In Square yards)'].unique()


# In[77]:


#dropping null values of state


# In[78]:


df1 = df.dropna(subset = ['State'])


# In[79]:


df1


# ANALYSING DATA for business model

# In[ ]:


# state wise how much people have home owner ship


# In[81]:


ownhouse  = df.groupby(['ownhome', 'State']).count()


# In[82]:


a = plt.bar(df1.loc[:, 'State'], df1.loc[:, 'bill_save'])
plt.xlabel('lead answer')
plt.ylabel('No. of person')
plt.title('lead answer about project', fontsize=20)
plt.style.use('fivethirtyeight')

plt.show()


# as graph is not clear because of long states names 
# i will download analysed data from now and will plot graph in excel for better representation. 
# so that i can make business model and flags and analyse in which state we should expand our business

# In[83]:


#downloading dataset so that can visualize it in excel.


# In[ ]:


ownhouse.to_excel(r"C:\Users\lohani\Desktop\peacock solar\ownhouse1.xlsx")


# In[84]:


state= df.groupby(['State']).count()


# In[85]:


state


# as very few responses are from rest of state and only 7 states have sufficient responses so, that we can analyse, 
# from now our analysis will only focus on these states

# 'Uttar Pradesh','Delhi', 'Maharashtra', 'West Bengal', 'Odisha', 'Gujarat', 'Haryana'

# In[ ]:


state.to_excel(r"C:\Users\lohani\Desktop\peacock solar\state.xlsx")


# In[86]:


homeloan  = df.groupby(['homeloan', 'State']).count()


# In[87]:


homeloan


# In[ ]:


homeloan.to_excel(r"C:\Users\lohani\Desktop\peacock solar\homeloan.xlsx")


# In[88]:


avg_earning  = df.groupby(['average monthly earnings', 'State']).count()


# In[89]:


avg_earning


# In[ ]:


avg_ear = avg_earning.to_excel(r"C:\Users\lohani\Desktop\peacock solar\avg_earning.xlsx")


# In[91]:


df["pwrbckup"] = df["pwrbckup"].astype('category')


# ANALYSING factors which encourage and discourage people from purchasing solar 

# In[92]:


df["pwrbckup"].describe()


# In[93]:



plt.hist(df["pwrbckup"])
plt.ylabel('no. of person')
plt.title('Average rating of powerbackup factor in purchasing decision (1-5)')


# In[94]:


df["elec_price_inc"].describe()


# In[95]:


plt.hist(df["elec_price_inc"])
plt.ylabel('no. of person')
plt.title('Average rating of increasing electricity price factor in purchasing decision (1-5)')


# In[96]:


df["bill_save"].describe()


# In[97]:


plt.hist(df["bill_save"])
plt.ylabel('no. of person')
plt.title('Average rating of electricity bill saving factor in purchasing decision (1-5)')


# In[98]:


df["lowmaint"].describe()


# In[99]:


plt.hist(df["lowmaint"])
plt.ylabel('no. of person')
plt.title('Average rating of low maintainance cost factor in purchasing decision (1-5)')


# In[100]:


df["newtec"].describe()


# In[101]:


plt.hist(df["newtec"])
plt.ylabel('no. of person')
plt.title('Average rating of interest in new technology factor in purchasing decision (1-5)')


# In[102]:


df["env_fri"].describe()


# In[103]:


plt.hist(df["env_fri"])
plt.ylabel('no. of person')
plt.title('Average rating of environment friendly factor in purchasing decision (1-5)')


# In[104]:


df["status_symbol"].describe()


# In[105]:


plt.hist(df["status_symbol"])
plt.ylabel('no. of person')
plt.title('Average rating of status symbol factor in purchasing decision (1-5)')


# In[106]:


df["earnfromroof"].describe()


# In[107]:


plt.hist(df["earnfromroof"])
plt.ylabel('no. of person')
plt.title('Average rating of earning from roof factor in purchasing decision (1-5)')


# In[108]:


df["inv_pay_back"].describe()


# In[109]:


plt.hist(df["inv_pay_back"])
plt.ylabel('no. of person')
plt.title('Average rating of No. of years takes for the investment to pay back factor in discouraging from purchasing')


# In[110]:


df["not_suff_money"].describe()


# In[111]:


plt.hist(df["not_suff_money"])
plt.ylabel('no. of person')
plt.title('Average rating of having not sufficient fund factor in discouraging from purchasing')


# In[112]:


print(df["lack_govt"].describe())
plt.hist(df["lack_govt"])
plt.ylabel('no. of person')
plt.title('Average rating of lack of govt. incentive factor in discouraging from purchasing')


# In[113]:


print(df["lack_loan"].describe())
plt.hist(df["lack_loan"])
plt.ylabel('no. of person')
plt.title('Average rating of lack of loan option factor in discouraging from purchasing')


# In[114]:


lack_loan                                                            0
highcost                                                             0
outlook_house                                                        0
dont_undr_solr                                                       0
not_know_installer                                                   0
roofnotsuitable                                                      0


# In[115]:


print(df["highcost"].describe())
plt.hist(df["highcost"])
plt.title('Average rating of high installation factor in discouraging from purchasing')


# In[116]:


print(df["outlook_house"].describe())
plt.hist(df["outlook_house"])
plt.title('Average rating of look of house factor in discouraging from purchasing')


# In[117]:


print(df["dont_undr_solr"].describe())
plt.hist(df["dont_undr_solr"])
plt.title("Average rating of don't understand solar factor in discouraging from purchasing")


# In[118]:


print(df["not_know_installer"].describe())
plt.hist(df["not_know_installer"])
plt.title("Average rating of not know installer factor in discouraging from purchasing")


# In[119]:



print(df["roofnotsuitable"].describe())
plt.hist(df["roofnotsuitable"])
plt.title("Average rating of roof not suitable factor in discouraging from purchasing")


# In[134]:


state= ['Uttar Pradesh','Delhi', 'Maharashtra', 'West Bengal', 'Odisha', 'Gujarat', 'Haryana']


# In[135]:


r = df['State'].isin(state)


# In[136]:


rr = df[r]


# Analysing company factor for business model, 
# for better understanding from now see ppt of this business model analysis 

# In[137]:


maxinv = rr.groupby(['What maximum investment would you be willing to make in solar?', 'State']).count()


# In[138]:


aware.to_excel(r"C:\Users\lohani\Desktop\peacock solar\aware1.xlsx")


# In[125]:


flor = rr.groupby(['plantobuildflor', 'State']).count()


# In[126]:


flor


# In[127]:


roof = rr.groupby(["What percentage of your roof are you ready to give for solar?", 'State']).count()


# In[128]:



aware = rr.groupby(["How much aware are you about solar?", 'State']).count()
aware


# In[129]:


knowpeacock = rr.groupby(["knowpeacock", 'State']).count()


# In[130]:


knowpeacock


# In[131]:


knowsolarknowsolar= rr.groupby(["knowsolar", 'State']).count()


# In[ ]:


knowsolarknowsolar


# 
#  Haryana is most profitable, UP is the second option.
#  In Haryana maximum people own a house,
# only 17 percent of people have a home loan,
# more than 57 percent of people Average earning between (45000 – 85000),
# About 4 percent of people want to invest more than 250,000 highest as compared to others states.
# 
