#!/usr/bin/env python
# coding: utf-8

# # Finding the most profitable apps for apple store and google play market
# 

# My aim in this project is to find the most profitable apps for apple store and goofle play market. to achieved that I filtered the apps, deleted unnecessary duplicates, deleted non english apps, because I'm interested only in english apps and wanted to find out what genres are the most profitable.

# In[2]:


from csv import reader

# The Google Play data set #
opened_file = open('Googleplaystore.csv',encoding="utf8")
read_file = reader(opened_file)
android = list(read_file)
android_header = android[0]
android = android[1:]

# The App Store data set #
opened_file = open('AppleStore.csv',encoding="utf8")
read_file = reader(opened_file)
ios = list(read_file)
ios_header = ios[0]
ios = ios[1:]


# In[3]:



def explore_data(dataset, start, end, rows_and_columns=False):
    dataset_slice = dataset[start:end]    
    for row in dataset_slice:
        print(row)
        print('\n') # adds a new (empty) line between rows
        
    if rows_and_columns:
        print('Number of rows:', len(dataset))
        print('Number of columns:', len(dataset[0]))

print(android_header)
print('\n')
explore_data(android, 0, 5, True)
print('\n')
print(ios_header)
print('\n')
explore_data(ios, 0, 5, True)


# In[4]:


print(len(android))
del android[10472]
print(len(android))


# In[5]:


print(android_header)


# In[6]:


duplicate_apps = []
unique_apps = []
for app in android:
    name=app[0]
    if name in unique_apps:
        duplicate_apps.append(name)
    else:
        unique_apps.append(name)
x=len(duplicate_apps)
print(x)


# So we have 1181 duplicate and we won't deleted them randomly. Ones with the most reviews are the newest one so we will use them.

# In[7]:



reviews_max={}
for apps in android:
    name=apps[0]
    n_reviews=float(apps[3])
    if name in reviews_max and reviews_max[name]<n_reviews:
        reviews_max[name]=n_reviews
    elif name not in reviews_max:
        reviews_max[name]=n_reviews
        
len(reviews_max)


# In[8]:


android_clean=[]
already_added=[]
for apps in android:
    name=apps[0]
    n_reviews=float(apps[3])
    if (reviews_max[name] == n_reviews) and (name not in already_added):
        android_clean.append(apps)
        already_added.append(name)


# In[9]:


explore_data(android_clean,0,2,True)


# Now we will keep only apps that are directed for english users.

# In[10]:


def english_apps(string):
    non_ascii = 0
    
    for character in string:
        if ord(character) > 127:
            non_ascii += 1
    
    if non_ascii > 3:
        return False
    else:
        return True

print(english_apps('Docs To Go™ Free Office Suite'))
print(english_apps('Instachat 😜'))


# In the cell above we also rejected this apps that have more than 3 special sign like emoji etc.

# In[11]:


android_english = []
ios_english = []

for app in android_clean:
    name = app[0]
    if english_apps(name):
        android_english.append(app)
        
for app in ios:
    name = app[1]
    if english_apps(name):
        ios_english.append(app)
        
explore_data(android_english, 0, 1, True)
print('\n')
explore_data(ios_english, 0, 1, True)


# Now we will do our final step, which is separate free apps from paid ones.

# In[12]:


android_final=[]
for apps in android_english:
    price=apps[7]
    if price=='0':
        android_final.append(apps)
        
ios_final=[]
for apps in ios_english:
    price=apps[4]
    if price=='0.0':
        ios_final.append(apps)

print(len(android_final))
print(len(ios_final))


# As we mentioned in the introduction, our aim is to determine the kinds of apps that are likely to attract more users because our revenue is highly influenced by the number of people using our apps.
# 
# To minimize risks and overhead, our validation strategy for an app idea is comprised of three steps:
# 
# 1.Build a minimal Android version of the app, and add it to Google Play.
# 
# 2.If the app has a good response from users, we develop it further.
# 
# 3.If the app is profitable after six months, we build an iOS version of the app and add it to the App Store.

# In[13]:


def freq_table(dataset,index):
    table={}
    total=len(dataset)
    for row in dataset:
        value=row[index]
        if value in table:
            table[value]+=1
        else:
            table[value]=1
            
    precentages_table={}
    for x in table:
        proportion=table[x]/total
        precentages_table[x]=proportion*100
    return  precentages_table

def display_table(dataset, index):
    table = freq_table(dataset, index)
    table_display = []
    for key in table:
        key_val_as_tuple = (table[key], key)
        table_display.append(key_val_as_tuple)

    table_sorted = sorted(table_display, reverse = True)
    for entry in table_sorted:
        print(entry[1], ':', entry[0])
        
display_table(android_final,1)
print('\n')
display_table(ios_final,11)


# Based on our analysis the best category for profitable apps would be entertainment as we can see app store is hugly dominated by gaming apps over 58%. Google store has less gaming apps but still focus mostly on entertainment.

# In[14]:


ios_genres=freq_table(ios_final,11)
for genre in ios_genres:
    total=0
    len_genre=0
    for apps in ios_final:
        genre_app=apps[11]
        if genre_app==genre:
            n_rating=float(apps[5])
            total+=n_rating
            len_genre+=1
    avg_n_of_user_rating=total/len_genre
    
    print(genre,':', avg_n_of_user_rating)
    


# In[15]:


categories_android = freq_table(android_final, 1)

for category in categories_android:
    total = 0
    len_category = 0
    for app in android_final:
        category_app = app[1]
        if category_app == category:            
            n_installs = app[5]
            n_installs = n_installs.replace(',', '')
            n_installs = n_installs.replace('+', '')
            total += float(n_installs)
            len_category += 1
    avg_n_installs = total / len_category
    print(category, ':', avg_n_installs)


# As we can see the most downland have communication apps, but this category is mostly dominated by few apps like WhatsApp, Facebook Messenger, Skype etc.

# In[16]:


for app in android_final:
    if app[1] == 'COMMUNICATION' and (app[5] == '1,000,000,000+'
                                      or app[5] == '500,000,000+'
                                      or app[5] == '100,000,000+'):
        print(app[0], ':', app[5])


# If we removed all the communication apps that have over 100 million installs, the average would be reduced roughly ten times.

# In[17]:


under_100_m = []

for app in android_final:
    n_installs = app[5]
    n_installs = n_installs.replace(',', '')
    n_installs = n_installs.replace('+', '')
    if (app[1] == 'COMMUNICATION') and (float(n_installs) < 100000000):
        under_100_m.append(float(n_installs))
        
sum(under_100_m) / len(under_100_m)


# So as we can see the most popular category will be hard to succeed, because it's dominated by few giants and will be very hard to gain any market share. The next most populat category is games, but in my opinion this is category that will be also hard to succeed, because there are thousands of games already in the market. The books and reference genre looks fairly popular as well, with an average number of installs of 8,767,811 so we will take a closer look at this category because it's quite unique.

# In[18]:


for app in android_final:
    if app[1] == 'BOOKS_AND_REFERENCE':
        print(app[0], ':', app[5])


# The book and reference genre includes a variety of apps: software for processing and reading ebooks, various collections of libraries, dictionaries, tutorials on programming or languages, etc. It seems there's still a small number of extremely popular apps.

# In[21]:


for app in android_final:
    if app[1] == 'BOOKS_AND_REFERENCE' and (app[5] == '1,000,000,000+'
                                            or app[5] == '500,000,000+'
                                            or app[5] == '100,000,000+'):
        print(app[0], ':', app[5])


# In[22]:



for app in android_final:
    if app[1] == 'BOOKS_AND_REFERENCE' and (app[5] == '1,000,000+'
                                    or app[5] == '5,000,000+'
                                    or app[5] == '10,000,000+'
                                    or app[5] == '50,000,000+'):
print(app[0], ':', app[5])


# As we can see there are few big players in this area, but there are also some less recognizable names that are doing good.
# However like almost with every thing market is full of ebooks so we will need take diffrent approach maybe focus on some quotes from books or focus just on one book and gather fans of this title in one place.

# # Conclusions

# Based on my anlysis I think that Books and Reference category is the best for new apps. There is still niche in this market but I recommend try to focus mainly on specific book rather than on popular thing like ebooks.
