from os import environ as env
from dotenv import load_dotenv
import db
import schedule
import run

db.create_db()

load_dotenv()

print(env['DEBUG'])


def daily_video_generation():
    subreddits = env['SUBREDDITS'].split(',')

    for subreddit in subreddits:
        run.generateVideoFromTopPost(subreddit)

schedule.every().day.at("12:00").do(daily_video_generation)

while True:
    schedule.run_pending()
    time.sleep(60)