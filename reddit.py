import praw
import random
import os
from datetime import datetime

"""
Initiates Reddit Class imported from praw.
"""
client_ID = str(os.environ['REDDIT_CLIENT_ID'])
client_secret = str(os.environ['REDDIT_CLIENT_SECRET'])
reddit = praw.Reddit(client_id = client_ID,
                    client_secret = client_secret,
                    user_agent = "Slacker Discord bot")

"""
Initiates 2 lists:
memes - list of imported memes from reddit.
memes_removed - list of seen memes by discord user (used so memes do not repeat).
"""
memes = []
memes_removed = []

"""
Populates memes list from "memes" subreddit, hot tab.
params: limit (int) - value of how many memes from reddit should it import. (e.g. limit = 200 means that top 200 memes from fresh will be imported)
        this value needs to be higher than list_max_range, because if some memes are removed (seen), list might not be fully populated.
        e.g. if I populated list with top 100 memes, and 20 memes would be seen, repopulating it with top 100 again would probably mean they would duplicate, therefore list might not reach its maximum size (list_max_range)
        list_max_range (int; default = 100) - maximum size of memes list, needs to be lower than limit.
returns nothing
"""
def populate_memes(limit, list_max_range = 100):
    for submission in reddit.subreddit("memes").hot(limit = limit):
        if len(memes) <= list_max_range:
            if not submission.stickied: # if not sticked
                if not submission in memes and not submission in memes_removed: # if not in removed and already in list
                        memes.append(submission)

"""
Removes elements from memes list which contain memes uploaded more than difference_hours ago.
params: difference_hours (int) - amount of hours that passed since meme in memes list was created.
returns nothing
"""
def remove_old_memes(difference_hours):
    for meme in memes:
        time_diff = datetime.now() - datetime.utcfromtimestamp(meme.created_utc)
        if (time_diff.seconds // 3600) > difference_hours:
            memes.remove(meme)

"""
Removes elements from memes_remove list which contain memes uploaded more than difference_hours ago.
params: difference_hours (int) - amount of hours that passed since meme in memes_removed list was created.
returns nothing
"""
def clean_removed_memes(difference_hours):
    for meme in memes_removed:
        time_diff = datetime.now() - datetime.utcfromtimestamp(meme.created_utc)
        if (time_diff.seconds // 3600) > difference_hours:
            memes_removed.remove(meme)

"""
Chooses randomly element from memes_list and gets it's title, number of upvotes and corresponding url (in the case of "memes" subreddit, url means image url). Then it adds this meme to memes_removed list and removes it from memes list.
returns title (string), upvotes (int), meme_url (string)
"""
def get_meme():
    meme = random.choice(memes) # gets meme
    title = meme.title
    upvotes = meme.ups
    text = meme.selftext
    meme_url = meme.url
    memes_removed.append(meme) # adds to removed (or seen)
    memes.remove(meme) # removes from memes list
    return title, upvotes, meme_url