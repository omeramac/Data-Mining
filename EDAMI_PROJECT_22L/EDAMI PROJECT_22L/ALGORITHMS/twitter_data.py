#importing all necessary libraries
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import re
import fileinput

#to get tweets from the twitter snscrape algorithm use  for more info: https://github.com/JustAnotherArchivist/snscrape
import snscrape.modules.twitter as snstwitter
#to preprocess the tweets below libraries used
import nltk
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from nltk.tokenize import word_tokenize
from nltk.probability import FreqDist
import emoji
nltk.download('omw-1.4')
nltk.download('words')
nltk.download('punkt')
nltk.download('wordnet')
#for visualization below libraries used
from textblob import TextBlob
from wordcloud import WordCloud

words = set(nltk.corpus.words.words())
wordnet_lem = WordNetLemmatizer()

plt.style.use('fivethirtyeight')
stop = stopwords.words('english')


#Getting tweets from the twitter
query = "covid lang:en until:2022-05-16 since:2022-05-09"
tweets = []
limit = 7000

for tweet in snstwitter.TwitterSearchScraper(query).get_items():

    #print(vars(tweet))
    #break

    if len(tweets) == limit:
        break
    else:
        tweets.append([tweet.content])


column_val = ['Tweets']

df = pd.DataFrame(data=tweets, columns=column_val)
#print(df)
#save tweets in a csv file(raw version)
df.to_csv('covid10000.csv')

#cleaning the tweets from the unnecessary words and characters
def cleaner(tweet):
    tweet = re.sub("@[A-Za-z0-9]+","",tweet) #Remove @ sign
    tweet = re.sub(r"(?:\@|http?\://|https?\://|www)\S+", "", tweet) #Remove http links
    tweet = " ".join(tweet.split())
    tweet = ''.join(c for c in tweet if c not in emoji.UNICODE_EMOJI) #Remove Emojis
    tweet = tweet.replace("#", "").replace("_", " ") #Remove hashtag sign but keep the text
    tweet = " ".join(w for w in nltk.wordpunct_tokenize(tweet) \
         if w.lower() in words or not w.isalpha())
    return tweet

def cleanText(text):
    spec_chars = ["!",'"',"#","%","&","'","(",")",
              "*","+",",","-",".","/",":",";","<",
              "=",">","?","@","[","\\","]","^","_",
              "`","{","|","}","~","–","$","'"]
    text = re.sub(r'@[A-Za-z0-9]+', '', text) #remove @mentions
    text = re.sub(r'_[A-Za-z0-9]+', '', text) #remove @mentions
 
    text = re.sub(r'#','',text)
    text = re.sub(r'RT[\s]+', '',text )
    text =re.sub(r'https?:\/\/\S+', '',text)
    text = re.sub(r'\d+','',text)
    text = re.sub(r'\b\w\b','',text)
    text = re.sub(r'’','',text)
    
    return text    
    
df['Tweets'] = df['Tweets'].map(lambda x: cleaner(x))
df['Tweets'] = df['Tweets'].apply(lambda x: ' '.join([word for word in x.split() if word not in (stop)]))
df['Tweets'] = df['Tweets'].apply(cleanText)
spec_chars = ["!",'"',"#","%","&","'","(",")",
              "*","+",",","-",".","/",":",";","<",
              "=",">","?","@","[","\\","]","^","_",
              "`","{","|","}","~","–","$","'"]
for char in spec_chars:
    df['Tweets'] = df['Tweets'].str.replace(char, '')
df.astype(str).apply(lambda x: x.str.encode('ascii', 'ignore').str.decode('ascii'))
#df['Tweets'] = df['Tweets'].str.replace("\'",'',regex=True)
#emoji cleaner
df['Tweets'] = df['Tweets'].str.replace('[^\w\s#@/:%.,_-]', '', flags=re.UNICODE)

df.to_csv('covid_clean10000.csv')
#print(df)
print(df.head(5))
#convert all to lower case
df['Tweets'] = df['Tweets'].str.lower()

#tokenize the words, split
df['Tweets'] = df.apply(lambda row: nltk.word_tokenize(row['Tweets']), axis=1)

#print(df)
df.to_csv('covid_clean_token10000.csv')
#delete the words which appear less than 2 times
df['Tweets'] = df['Tweets'].apply(lambda x: ' '.join([item for item in x if len(item)>2]))

#print(df.head(5))

#tokenize again
df['Tweets'] = df.apply(lambda row: nltk.word_tokenize(row['Tweets']), axis=1)

#print(df)
#just to change the format of the frame
df['Tweets'] = df['Tweets'].apply(lambda x: ' '.join([item for item in x if len(item)>2]))
print(df.head(5))

#lemmatize, make more meaningful
df['Tweets'] = df['Tweets'].apply(wordnet_lem.lemmatize)

df.to_csv('covid_clean_token_final10000.csv')

#print the most common words
all_words = ' '.join([word for word in df['Tweets']])

#to plot the wordcloud of words in tweets
import matplotlib.pyplot as plt
from wordcloud import WordCloud

wordcloud = WordCloud(width=600, 
                     height=400, 
                     random_state=2, 
                     max_font_size=100).generate(all_words)

plt.figure(figsize=(10, 7))
plt.imshow(wordcloud, interpolation='bilinear')
plt.axis('off')
plt.show()

words = nltk.word_tokenize(all_words)
fd = FreqDist(words)
#print(fd.most_common(3))
#print(fd.tabulate(3))
#check if it has correct number
print(fd["covid"])

#transfer the tweets into a list
list_of_data1 = df["Tweets"].to_list()
"""
my_list= pd.unique(df["Tweets"])

print(df["Tweets"])

for word in df["Tweets"].str.split():
    if word not in my_list:
        my_list.append(word)
"""
#print(list_of_data)


list_of_data = ' '.join(list_of_data1)

print(list_of_data)
my_list=[]

for word in list_of_data.split():
    if word not in my_list:
        my_list.append(word)

print(my_list)
#create a dictionary from the unique words
def listToDict(my_list):
    op = { i : my_list[i] for i in range(0, len(my_list) ) }
    return op


dict_for_data = listToDict(my_list)
#print(dict_for_data)
#print(dict_for_data[1])

#replace words and the numbers in dixtionary
my_dict2 = {y: x for x, y in dict_for_data.items()}
#check the dictionary
print(my_dict2)


import json

with open('dict10000.txt', 'w') as convert_file:
     convert_file.write(json.dumps(my_dict2))
#for word in df["Tweets"].str.split():
#    word = my_dict2[word]

#print(df)
#np.savetxt(r'np2.txt', df.values, fmt='%d')      

with open(r'np2_10000.txt', 'a',encoding="utf-8") as f:
    dfAsString = df.to_string(header=False, index=False)
    f.write(dfAsString)

filename = "np2_10000.txt"
#fields = {"pattern 1": "replacement text 1", "pattern 2": "replacement text 2"}

ls=[]
#replace words in tweets dataset with the related numbers from dictionary
with open(filename,'r', encoding="utf-8") as file:
    for line in file:

        line = line.strip().split()
        temp_ls=[]
        
        for element in line:
            if str(my_dict2[element]) not in temp_ls:
                temp_ls.append(str(my_dict2[element]))
            
           
        print(temp_ls)
        ls.append(temp_ls)

#write the transactions in text file.
with open('covid10000.txt', 'w') as f:
    for item in ls:
        for ele in item:
            f.write(ele+" ")
        f.write("\n")

