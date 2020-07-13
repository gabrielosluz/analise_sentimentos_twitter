import numpy as np
import pandas as pd
import tweepy
import matplotlib as plt
import seaborn as sns
import textblob
from IPython.display import display
from credencial import * # lê o script criado anteriormente
from textblob import TextBlob
import re

# API setup:
def twitter_setup():
    # Authentication and access using keys:
    auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
    auth.set_access_token(ACCESS_TOKEN, ACCESS_SECRET)

    # Retorna a api autenticada:
    api = tweepy.API(auth)

    return api

#extração dos tweets
extractor = twitter_setup()

# Criação de uma listas dos 200 (não consegui pegar mais do que isso) últimos tweets do #Trump. Cada elemento da lista é do tipo tweet, do Tweepy.
tweets = extractor.user_timeline(screen_name="realDonaldTrump", count=200)
print("Number of tweets extracted: {}.\n".format(len(tweets)))

# Printando no Console IPython os primeiros 5 registros:
print("5 recent tweets:\n")

for tweet in tweets[:5]:
    print(tweet.text)

data = pd.DataFrame(data=[tweet.text for tweet in tweets], columns=['Tweets'])
display(data.head(10))

print(tweets[0].id)
print(tweets[0].created_at)
print(tweets[0].source)
print(tweets[0].favorite_count)
print(tweets[0].retweet_count)
print(tweets[0].geo)
print(tweets[0].coordinates)
print(tweets[0].entities)

data['len'] = np.array([len(tweet.text) for tweet in tweets])
data['ID'] = np.array([tweet.id for tweet in tweets])
data['Date'] = np.array([tweet.created_at for tweet in tweets])
data['Source'] = np.array([tweet.source for tweet in tweets])
data['Likes'] = np.array([tweet.favorite_count for tweet in tweets])
data['RTs'] = np.array([tweet.retweet_count for tweet in tweets])

#Análises básicas

mean = np.mean(data['len'])
print("The lenght's average in tweets: {}".format(mean))

fav_max = np.max(data['Likes'])
rt_max = np.max(data['RTs'])
fav = data[data.Likes == fav_max].index[0]
rt = data[data.RTs == rt_max].index[0]

# Max FAVs:
print("The tweet with more likes is: \n{}".format(data['Tweets'][fav]))
print("Number of likes: {}".format(fav_max))
print("{} characters.\n".format(data['len'][fav]))

# Max RTs:
print("The tweet with more retweets is: \n{}".format(data['Tweets'][rt]))
print("Number of retweets: {}".format(rt_max))
print("{} characters.\n".format(data['len'][rt]))

tlen = pd.Series(data=data['len'].values, index=data['Date'])
tfav = pd.Series(data=data['Likes'].values, index=data['Date'])
tret = pd.Series(data=data['RTs'].values, index=data['Date'])

# grafico do tamanho dos tweets ao longo do tempo.
tlen.plot(figsize=(16,4), color='r');

#quantidade de likes versus de retweets
tfav.plot(figsize=(16,4), label="Likes", legend=True)
tret.plot(figsize=(16,4), label="Retweets", legend=True);

#Relação entre a quantidade de likes e retweets?
corr = data.corr()
sns.heatmap(corr,
xticklabels=corr.columns.values,
yticklabels=corr.columns.values)

#Análise de sentimentos

def clean_tweet(tweet):
    return ' '.join(re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t])|       (\w+:\/\/\S+)", " ", tweet).split())

def analize_sentiment(tweet):
    analysis = TextBlob(clean_tweet(tweet))
    if analysis.sentiment.polarity > 0:
       return 1
    elif analysis.sentiment.polarity == 0:
       return 0
    else:
    return -1

data['SA'] = np.array([ analize_sentiment(tweet) for tweet in data['Tweets'] ])

pos_tweets = [ tweet for index, tweet in enumerate(data['Tweets']) if data['SA'][index] > 0]
neu_tweets = [ tweet for index, tweet in enumerate(data['Tweets']) if data['SA'][index] == 0]
neg_tweets = [ tweet for index, tweet in enumerate(data['Tweets']) if data['SA'][index] < 0]

# Printando as porcentagens:
print("Percentage of positive tweets: {}%".format(len(pos_tweets)*100/len(data['Tweets'])))
print("Percentage of neutral tweets: {}%".format(len(neu_tweets)*100/len(data['Tweets'])))
print("Percentage de negative tweets: {}%".format(len(neg_tweets)*100/len(data['Tweets'])))

#Variável que irá armazenar todos os Tweets com a palavra escolhida na função search da API
public_tweets = api.search('Trump')

#Variável que irá armazenar as polaridades
analysis = None

#calcular a polaridade
for tweet in public_tweets:
    print(tweet.text)
    analysis = TextBlob(tweet.text)
    print(analysis.sentiment.polarity)

print('MÉDIA DE SENTIMENTO: ' + str(np.mean(analysis.sentiment.polarity)))