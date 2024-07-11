import requests
import json
from datetime import timedelta
import string


class ForcedAligner:
    def __init__(self, gentleUrl, env):
        self.gentleUrl = gentleUrl
        self.env = env
        self.subtitleCharGroupSize = 10

    def align(self, audioPath, transcription, srtOutputPath):
        # Open the audio file
        with open(audioPath, 'rb') as audioFile:
            # Send a POST request to the Gentle API
            response = requests.post(
                f'{self.gentleUrl}/transcriptions?async=false',
                data={'transcript': transcription},
                files={'audio': audioFile}
            )

        # Check the status code of the response
        if response.status_code != 200:
            print(
                f"Error: received status code {response.status_code} from Gentle")
            return

        # Parse the alignment results
        alignment = json.loads(response.text)

        # Convert the alignment to SRT format and save it to the output file
        with open(srtOutputPath, 'w') as srtFile:
            srtIndex = 1
            phrase = []
            phraseCharCount = 0
            transcript_index = 0
            #extract tokens from the alignment.transcript 
            transcript = alignment['transcript'].replace('-', ' ').split(' ')

            print(transcript)

            for index, word in enumerate(alignment['words']):
                if word['case'] != 'success':
                    transcript_index += 1
                    continue
                if transcript_index+1 < len(transcript) and transcript[transcript_index+1] in string.punctuation:
                    word['word'] = word['word'] + transcript[transcript_index+1]
                    phrase.append(word)
                    transcript_index += 2
                    self.writeSrtCue(srtFile, srtIndex, phrase)
                    srtIndex += 1
                    phrase = []
                    phraseCharCount = 0
                else:
                    if word['word'] != transcript[transcript_index]:
                        found = False
                        for i in range(1, 4):
                            if transcript[transcript_index+i] == word['word']:
                                found = True
                                transcript_index += i
                                break
                        if not found:
                            for i in range(1, 4):
                                if transcript[transcript_index-i] == word['word']:
                                    found = True
                                    transcript_index -= i
                                    break
                        
                    wordLen = len(word['word'])
                    phraseCharCount += wordLen
                    phrase.append(word)
                    transcript_index += 1
                    if phraseCharCount >= self.subtitleCharGroupSize:
                        self.writeSrtCue(srtFile, srtIndex, phrase)
                        srtIndex += 1
                        phrase = []
                        phraseCharCount = 0

            # Write the final phrase, if any
            if phrase:
                self.writeSrtCue(srtFile, srtIndex, phrase)

    def writeSrtCue(self, srtFile, index, phrase):
        startTime = timedelta(seconds=phrase[0]['start'])
        endTime = timedelta(seconds=phrase[-1]['end'])
        words = [word['word'] for word in phrase]
        srtFile.write(f"{index}\n")
        srtFile.write(
            f"{self.format_time(startTime)} --> {self.format_time(endTime)}\n")
        srtFile.write(' '.join(words) + "\n\n")

    def format_time(self, td):
        # Total seconds as a float
        total_seconds = td.total_seconds()
        # Hours
        hours = int(total_seconds // 3600)
        total_seconds %= 3600
        # Minutes
        minutes = int(total_seconds // 60)
        total_seconds %= 60
        # Seconds and milliseconds
        seconds = int(total_seconds)
        milliseconds = int(round((total_seconds - seconds) * 1000))
        # Format and return
        return f"{hours:02}:{minutes:02}:{seconds:02},{milliseconds:03d}"
