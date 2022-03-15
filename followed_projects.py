import pandas as pd

converters = {
    'user_mentions_last_50': lambda x: x.strip("[]").replace("'","").split(", "),
    'favorites_users': lambda x: x.strip("[]").replace("'","").split(", "),
    }

# df = pd.read_csv('reserve/crypto_influencers.csv', converters=converters)
df_1 = pd.read_csv('crypto_influencers_1.csv', converters=converters)
df_2 = pd.read_csv('crypto_influencers_2.csv', converters=converters)

df = df_1.append(df_2)

user_mentions = df['user_mentions_last_50'].values.tolist()
favorites_users = df['favorites_users'].values.tolist()

def count_occurences(lst):
    ranking_dict = {}

    for user_mentions_per_account in lst:
        for user_mention in user_mentions_per_account:
            if user_mention not in ranking_dict:
                ranking_dict[user_mention] = 1
            else:
                ranking_dict[user_mention] += 1

    sorted_ranking_dict = {k: v for k, v in sorted(ranking_dict.items(), key=lambda item: item[1], reverse=False)}
    return sorted_ranking_dict

occurences_user_mentions = count_occurences(user_mentions)
occurences_favorites_users = count_occurences(favorites_users)
# print('Users/Projects that Crypto Influencers Follow:', occurences_user_mentions)
# print('Users/Projects that Crypto Influencers Like:', occurences_favorites_users)

result_df = pd.DataFrame({'user_mentions': pd.Series(occurences_user_mentions), 'favorites_users': pd.Series(occurences_favorites_users)})
result_df = result_df.dropna()
result_df.to_csv('influencers_project_reaction.csv')

# Ranked by popularity?

# print(df[df['follower_count'] > 10000])