import requests
from requests_oauthlib import OAuth1
import os

CONSUMER_KEY='a0i2M7y9QyyKbrz1C8f5Hr78V'
CONSUMER_SECRET='5MoyjPl9B9rnziB8FkF52tbD7hOlXarxoGnF1GISvYeRLNefrL'
ACCESS_TOKEN='1446611503671492615-X6sYkn25AbeCx7nQ3FeG1056ST7Tyv'
ACCESS_TOKEN_SECRET='bE2CqctY2qUN9Kx2jVYaqBwGK9zjnxLhCQ5D1E368DpGL'


# consumer_key = os.environ.get("CONSUMER_KEY")
# consumer_secret = os.environ.get("CONSUMER_SECRET")
# access_token = os.environ.get("ACCESS_TOKEN")
# access_token_secret = os.environ.get("ACCESS_TOKEN_SECRET")


def random_fact():
    fact = requests.get("https://catfact.ninja/fact?max_length=280").json()
    return fact["fact"]


def format_fact(fact):
    return {"text": "{}".format(fact)}


def connect_to_oauth(consumer_key, consumer_secret, acccess_token, access_token_secret):
    url = "https://api.twitter.com/2/tweets"
    auth = OAuth1(consumer_key, consumer_secret, acccess_token, access_token_secret)
    return url, auth


def main():
    fact = random_fact()
    payload = format_fact(fact)
    url, auth = connect_to_oauth(
        consumer_key, consumer_secret, access_token, access_token_secret
    )
    request = requests.post(
        auth=auth, url=url, json=payload, headers={"Content-Type": "application/json"}
    )


if __name__ == "__main__":
    main()
