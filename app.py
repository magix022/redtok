from os import environ as env
from dotenv import load_dotenv
import db
import schedule
import main
import gdrive
import datetime
import os

db.create_db()

load_dotenv()

print(env['DEBUG'])


def daily_video_generation():
    subreddits = env['SUBREDDITS'].split(',')
    
    paths = []
    for subreddit in subreddits:
        try:
            path = main.generateVideoFromTopPost(subreddit)
            paths.append(path)
        except Exception as e:
            print(f"An error occurred: {e}")
            continue

        if env['DEBUG'] == "TRUE":
            break

    date = datetime.datetime.now().strftime("%Y-%m-%d")
    if len(paths) > 0 and env['DEBUG'] != "TRUE":
        try:
            service = gdrive.authenticate()
            file = gdrive.create_folder(service, date, env['DRIVE_PARENT_FOLDER_ID'])
            for path in paths:
                gdrive.upload_file(service, path, file.get("id"))
                # Delete the file after uploading
                os.remove(path)
        except Exception as e:
            print(f"An error occurred: {e}")


# schedule.every().day.at("12:00").do(daily_video_generation)

# while True:
#     schedule.run_pending()
#     time.sleep(60)

daily_video_generation()