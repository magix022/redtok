import praw
import db


class Scraper:
    def __init__(self, env, subreddit):
        self.env = env
        self.post = None

        # Read-only instance
        self.reddit = praw.Reddit(client_id=env['CLIENT_ID'],
                                  client_secret=env['CLIENT_SECRET'],
                                  user_agent=env['USER_AGENT'])
        self.reddit.read_only = True
        self.subreddit = self.reddit.subreddit(subreddit)
        self.minPostLength = int(env['MIN_POST_LENGTH'])
        self.maxPostLength = int(env['MAX_POST_LENGTH'])

    def getHotPosts(self):
        for post in self.subreddit.hot():
            if not post.stickied and post.is_self and (self.minPostLength <= len(post.selftext) <= self.maxPostLength) and len(self.hotPosts) < 2:
                if db.findTitle(post.title) is None:
                    self.post = post
                    break
                
        return (self.post.title, self.post.title+"\n"+self.post.selftext)
