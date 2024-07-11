from os import environ as env
from dotenv import load_dotenv
from scraper import Scraper
from tts import TTS
from videoGen import VideoGenerator
from forcedAligner import ForcedAligner
import os
from gpt import GPT
import db

load_dotenv()

print(env['DEBUG'])

def videoGen(postTitle, postText):
    postTitleAndText = postTitle + "\n" + postText

    languages = env['LANGUAGES'].split(',')
    languages = [lang.lower() for lang in languages]

    gpt = GPT(env)
    gender = gpt.getGender(postTitleAndText)
    print("Gender: " + gender)

    for language in languages:
        editedPost = gpt.expandAcronymsAndAbbreviations(postTitleAndText, language)

        print("Edited post: " + editedPost)

        tts = TTS(env)
        audioFile = tts.createAudio(editedPost, gender, language)
        print("Created audio file: " + audioFile)

        if env['SUBTITLES'].upper() == 'TRUE' and language == 'english':
            subtitlesPath = 'tts-audio-files/subtitles.srt'
            forcedAligner = ForcedAligner(
                env['GENTLE_URL'], env)
            forcedAligner.align(audioFile, editedPost, subtitlesPath)
        else:
            subtitlesPath = None
        videoGen = VideoGenerator(env)
        directory = 'background-videos'
        fileName = postTitle if len(postTitle) < 50 else postTitle[:100]
        outputPath = os.path.join('output', fileName.replace(' ', '_') +'.mp4')
        bgVideoFileName = env['BG_VIDEO_FILENAME']
        videoFile = videoGen.generateVideo(
            bgVideoFileName, audioFile, outputPath, directory, subtitlesPath)
        if (videoFile != False):
            if env['DEBUG'] != "TRUE":
                db.insert_post(postTitle)
            print("Created output video file at: " + videoFile)
            return outputPath
        else:
            print("Failed to create output video file")
    

def generateVideoFromTopPost(subreddit):
    scraper = Scraper(env, subreddit)
    post = scraper.getHotPost()
    postTitle = post[0]
    postText = post[1]
    print("Scraped post: "+ postTitle + "\n" + postText)

    path = videoGen(postTitle, postText)
    return path


if __name__ == "__main__":
    db.create_db()
    generateVideoFromTopPost('AmItheAsshole')
