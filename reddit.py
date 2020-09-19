import praw
import random
import os
from datetime import datetime

client_ID = str(os.environ['REDDIT_CLIENT_ID'])
client_secret = str(os.environ['REDDIT_CLIENT_SECRET'])

reddit = praw.Reddit(client_id = client_ID,
                    client_secret = client_secret,
                    user_agent = "Slacker Discord bot")

memes = []
memes_removed = []

def populate_memes(limit):
    for submission in reddit.subreddit("memes").hot(limit = limit):
        if len(memes) <= 100:
            if not submission.stickied: # if not sticked
                if not submission in memes and not submission in memes_removed: # if not in removed and already in list
                        memes.append(submission)

def remove_old_memes(difference_hours):
    for meme in memes:
        time_diff = datetime.now() - datetime.utcfromtimestamp(meme.created_utc)
        if (time_diff.seconds // 3600) > difference_hours:
            memes.remove(meme)

def clean_removed_memes():
    for meme in memes_removed:
        time_diff = datetime.now() - datetime.utcfromtimestamp(meme.created_utc)
        if (time_diff.seconds // 3600) > 12:
            memes_removed.remove(meme)

def get_meme():
    meme = random.choice(memes) # gets meme
    title = meme.title
    upvotes = meme.ups
    text = meme.selftext
    meme_url = meme.url
    memes_removed.append(meme) # adds to removed (or seen)
    memes.remove(meme) # removes from memes list
    return title, upvotes, meme_url