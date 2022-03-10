import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import PolynomialFeatures


# a = "Atlas is a Tethys reflective token soon running on Andromeda $METIS. Hold $ATLAS, earn $TETHYS."
# coin_symbol = [t[1::] for t in a.replace('.', ' ').replace(',', ' ').split() if t.startswith('$') and t[1::].isalpha()]
# print(coin_symbol)
# if coin_symbol:
#     print('yes')

# https://coinmarketcap.com/new/
# tokensniffer, r/cryptomoonshots

web3_df = pd.read_csv('web3_data.csv', encoding = 'unicode_escape')
web3_df = web3_df.drop(['Unnamed: 0', 'description'], axis=1)
# plt.scatter(web3_df.age_days, web3_df.follower_count, c=web3_df.quality_score / 35)
# plt.legend()
# plt.show()

user_projects_df = pd.read_csv('user_projects_train.csv')
user_projects_df = user_projects_df.drop(['Unnamed: 0', 'user_mentions_last_5', 'links', 'url', 'description'], axis=1)
# user_projects_df = user_projects_df.drop(['Unnamed: 0', 'user_mentions_last_5', 'links', 'url', 'description'], axis=1)

# intersection_columns = list(set(web3_df.columns).intersection(set(user_projects_df.columns)))

merged_df = web3_df.merge(user_projects_df, how='inner', on=['name'])

merged_df = merged_df.drop(['age_days_y', 'follower_count_y'], axis=1)
merged_df = merged_df.drop(['name', 'screen_name', 'created_at', 'age'], axis=1)

# Model
poly = PolynomialFeatures(degree=2, include_bias=False)

X = merged_df.drop(['quality_score'], axis=1)
y = merged_df.quality_score
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=1)
poly_X_train = poly.fit_transform(X_train)
poly_X_test = poly.fit_transform(X_test)

lr = LogisticRegression(random_state=1, solver='liblinear', max_iter=1000) # liblinear, lbfgs
lr.fit(poly_X_train, y_train)
print(lr.score(poly_X_test, y_test))
