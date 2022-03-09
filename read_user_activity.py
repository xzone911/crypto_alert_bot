import tweepy
import pandas as pd
import numpy as np
from tweepy import Client
from datetime import datetime, timezone
import re
import json
import matplotlib.pyplot as plt
import requests


CONSUMER_KEY='a0i2M7y9QyyKbrz1C8f5Hr78V'
CONSUMER_SECRET='5MoyjPl9B9rnziB8FkF52tbD7hOlXarxoGnF1GISvYeRLNefrL'
ACCESS_TOKEN='1446611503671492615-X6sYkn25AbeCx7nQ3FeG1056ST7Tyv'
ACCESS_TOKEN_SECRET='bE2CqctY2qUN9Kx2jVYaqBwGK9zjnxLhCQ5D1E368DpGL'

############################################################

# Authentication

# oauth2_user_handler = tweepy.OAuth2UserHandler(
#     client_id="QmoyWlZwaTd4Z1FBaVBqblVtOTA6MTpjaQ",
#     redirect_uri="https://twitter.com/CryptoVIPAlerts",
#     scope=[
#         'tweet.read',
#         'tweet.write',
#         'tweet.moderate.write',
#         'users.read',
#         'follows.read',
#         'follows.write',
#         'offline.access',
#         'space.read',
#         'mute.read',
#         'mute.write',
#         'like.read',
#         'like.write',
#         'list.read',
#         'list.write',
#         'block.read',
#         'block.write'
#     ],
#     # Client Secret is only necessary if using a confidential client
#     client_secret="As-QJsapWG7cFGFUjYF3CkmX1qRq8j6M2BMNjfeN18p42eftkn"
# )

# oauth1_user_handler = tweepy.OAuth1UserHandler(
#     "a0i2M7y9QyyKbrz1C8f5Hr78V", "5MoyjPl9B9rnziB8FkF52tbD7hOlXarxoGnF1GISvYeRLNefrL",
#     callback="https://twitter.com/CryptoVIPAlerts"
# )

# print(oauth1_user_handler.get_authorization_url(signin_with_twitter=True))

# https://twitter.com/CryptoVIPAlerts?oauth_token=blRFdwAAAAABZ4LwAAABf11Jnts&oauth_verifier=o8rtkkvaEiA228fHWqRreWn895ml1Y71

# request_token = oauth1_user_handler.request_token["oauth_token"]
# request_secret = oauth1_user_handler.request_token["oauth_token_secret"]

# new_oauth1_user_handler = tweepy.OAuth1UserHandler(
#     "a0i2M7y9QyyKbrz1C8f5Hr78V", "5MoyjPl9B9rnziB8FkF52tbD7hOlXarxoGnF1GISvYeRLNefrL",
#     callback="https://twitter.com/CryptoVIPAlerts"
# )
# new_oauth1_user_handler.request_token = {
#     "oauth_token": 'blRFdwAAAAABZ4LwAAABf11Jnts',
#     "oauth_token_secret": 'KU5ruDh8Rysdkabr5qeHyTMPStxctqXX'
# }
# access_token, access_token_secret = (
#     new_oauth1_user_handler.get_access_token(
#         'o8rtkkvaEiA228fHWqRreWn895ml1Y71'
#     )
# )

# print(access_token)
# print(access_token_secret)

################################################

# v2

# client = Client(
#     bearer_token='AAAAAAAAAAAAAAAAAAAAAPCCZwEAAAAARCL%2FXiNTUIZMHj9iVWbMlQC3oqM%3D0CbbQX2dhpKcjlAZT4MRYCGDAB9aMtTrW2sOWBsDsreL1qto3Z',
#     consumer_key='a0i2M7y9QyyKbrz1C8f5Hr78V',
#     consumer_secret='5MoyjPl9B9rnziB8FkF52tbD7hOlXarxoGnF1GISvYeRLNefrL',
#     access_token='1446611503671492615-X6sYkn25AbeCx7nQ3FeG1056ST7Tyv',
#     access_token_secret='bE2CqctY2qUN9Kx2jVYaqBwGK9zjnxLhCQ5D1E368DpGL',
# )

# elon_id = client.get_user(username='elonmusk').data.id

# elon_tweets = client.get_users_tweets(id=elon_id)

# for tweet in elon_tweets.data:
#     print(tweet.text)
#     if len(tweet.context_annotations) > 0:
#         print(tweet.context_annotations)

# elon_likes = client.get_liked_tweets(id=elon_id)
# print(elon_likes)

# for tweet in elon_likes.data:
#     print(tweet.text)
#     if len(tweet.context_annotations) > 0:
#         print(tweet.context_annotations)

# client.create_tweet(text='test')

#####################################################

# v1

auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
api = tweepy.API(auth)

def user_info(screen_name, n_posts):

    user = api.get_user(screen_name=screen_name)

    # Verified
    # print(f'{screen_name} Verified {user.verified}')

    # # Age of Account
    created = user.created_at
    now = datetime.now(timezone.utc)
    age = now - created
    years = age.days // 365
    days = age.days % 365
    # print(f'{screen_name} created on {created.date()}, {years} years and {days} days ago.')

    # # URL
    url = user.url
    description = user.description
    links = re.findall(r'(https?://\S+)', description)
    # print(f'{screen_name} URL: {url}, Links in Description: {links}')

    # # Number of Followers
    # followers_count = user.followers_count
    # print(f'{screen_name} number of followers: {followers_count}')

    # # Individual Followers
    follower_list = []
    followers = api.get_followers(screen_name=screen_name, count=10)
    # print(f'{screen_name} followers:')
    for follower in followers:
        follower_list.append(follower.screen_name)
        # print(follower.screen_name)

    # # Number of Likes They Have Made
    # favourites_count = user.favourites_count
    # print(f'{screen_name} number of posts liked: {favourites_count}')

    # Last 20 Posts
    likes_last_n = []
    rt_last_n = []
    user_mentions_set = set()
    tweets = api.user_timeline(screen_name=screen_name, count=20, tweet_mode='extended')
    for tweet in tweets:
        likes_last_n.append(tweet.favorite_count)
        rt_last_n.append(tweet.retweet_count)
        user_mentions = tweet.entities['user_mentions']
        for mention in user_mentions:
            user_mentions_set.add(mention['screen_name'])
    avg_likes = sum(likes_last_n) / len(likes_last_n)
    avg_rt = sum(rt_last_n) / len(rt_last_n)
    # print(f'{screen_name} Average Number of Likes Over Last {n_posts} Posts: {avg_likes}')
    # print(f'{screen_name} Average Number of Retweets Over Last {n_posts} Posts: {avg_rt}')
    # print(f'{screen_name} User Mentions Over Last {n_posts} Posts: {user_mentions_set}')

    user_dict = {
        'screen_name': screen_name,
        'verified': user.verified,
        'created_at': user.created_at,
        'age': age, 
        'url': user.url,
        'description': user.description,
        'links': links, 
        'follower_count': user.followers_count,
        'followers': follower_list,
        'favourites_count': user.favourites_count,
        f'avg_likes_{n_posts}': avg_likes,
        f'avg_rt_{n_posts}': avg_rt,
        f'user_mentions_{n_posts}': list(user_mentions_set)
    }

    return user_dict

def pretty(d, indent=0):
   for key, value in d.items():
      print('\t' * indent + str(key))
      if isinstance(value, dict):
         pretty(value, indent+1)
      else:
         print('\t' * (indent+1) + str(value))

# print(pretty(user_info('elonmusk', 20), indent=0))

# SEARCH QUERY
# superhero since:2015-12-21    containing “superhero” and sent since date “2015-12-21” (year-month-day).
# hilarious filter:links     containing “hilarious” and linking to URL.
# :)        positive attitude
# #haiku    containing the hashtag “haiku”.
# to:NASA   a Tweet authored in reply to Twitter account “NASA”.
# @NASA   mentioning Twitter account “NASA”.
# Look at topics?



# # GOOGLE TRENDS with pytrends
# from pytrends.request import TrendReq

# pytrends = TrendReq()

# # keywords = pytrends.suggestions(keyword='Facebook')
# # df = pd.DataFrame(keywords)
# # print(df.head(5))

# # trendingtoday = pytrends.today_searches(pn='US')
# # print(trendingtoday.head(20))

# baseline_kw = 'SunblockFinance'

# #provide your search terms
# # kw_list=['crypto', 'nft', 'bitcoin', 'ethereum', 'coinbase']
# kw_list=[baseline_kw, 'DemeterOnAvax', 'vaultinc', 'VersusMetaverse', 'HyphaLink']

# #search interest per region
# #run model for keywords (can also be competitors)
# pytrends.build_payload(kw_list, timeframe='today 1-m')

# # Interest by Region
# df = pytrends.interest_over_time()
# print(df)
# df = df.drop(['isPartial'], axis=1)
# #looking at rows where all values are not equal to 0
# df = df[(df != 0).all(1)]

# #drop all rows that have null values in all columns
# # df.dropna(how='all', axis=0, inplace=True)

# #visualise
# print(df)
# df.plot(figsize=(10, 6))
# plt.show()


# A WAY TO PICK UP PROJECTS

crypto_compare_api_key = 'f78fea12b032c8d3b1e8e2b1674433e4758c07692f79537447db10b374f77f56'

def coin_price_history(crypto_symbol, num_days=20):

    # request_url = f'https://min-api.cryptocompare.com/data/v2/histoday?fsym=ETH&tsym=USD&limit=20&toTs=-1&api_key={crypto_compare_api_key}'
    request_url = f'https://min-api.cryptocompare.com/data/v2/histoday?fsym={crypto_symbol}&tsym=USD&limit={num_days}&toTs=-1&api_key=YOURKEYHERE'

    r = requests.get(url=request_url)

    data = r.json()['Data']['Data']
    timestamp_prices = {}
    for datum in data:
        datum_date = datetime.fromtimestamp(datum['time']).date()
        timestamp_prices[datum_date] = datum['close']
    # print(timestamp_prices)

    ts = list(timestamp_prices.keys())
    prices = list(timestamp_prices.values())

    plt.plot(ts, prices)
    plt.show()

    percent_increase = ((prices[-1] / prices[0]) - 1) * 100
    price_variance = np.var(prices)
    price_std = np.std(prices)
    print(f'Percent change over {num_days} days: {np.round(percent_increase, 1)}%')
    print(f'Max: {max(prices)}, Min: {min(prices)}, Current: {prices[-1]}')
    print(f'Variance: {int(price_variance)}, STD: {int(price_std)}')

coin_price_history('LOOT')

# def coin_increase_percent(crypto_symbol):
