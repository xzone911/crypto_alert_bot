import praw
import requests
from praw.models import MoreComments

reddit = praw.Reddit(
    client_id="8gzf_gTOkVrDYn2pjUEYdw",
    client_secret="UeMH2v4XkC__k3HjBg05G-uzpBhClg",
    refresh_token="788244593804-IxUKuWQFhw_9GbRCaFryg8wx_6KsQg",
    user_agent="crypto_alert_bot by u/nickeleye141",
)

url = "https://www.reddit.com/r/funny/comments/3g1jfi/buttons/"
submission = reddit.submission(url=url)
for top_level_comment in submission.comments:
    if isinstance(top_level_comment, MoreComments):
        continue
    print(top_level_comment.body)