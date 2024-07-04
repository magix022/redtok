import openai
import os
import re


class GPT:
    def __init__(self, env) -> None:
        self.env = env
        openai.api_key = env['OPENAI_API_KEY']
        self.model = "gpt-3.5-turbo"
        if (env['USE_GPT_4'].upper() == 'TRUE'):
            self.model = "gpt-4"

    def add_whitespace_before_punctuation(self, text):
        # This regular expression matches any punctuation character not preceded by a whitespace
        pattern = r'(?<!\s)([.,!?;:])'
        # Substitutes each match with a whitespace followed by the match
        modified_text = re.sub(pattern, r' \1', text)
        return modified_text

    def getGender(self, text):
        if self.env['DEBUG'].upper() == 'TRUE':
            return "M"
        instructions = "Given the following reddit post, determine the gender of the poster. Use the context of the post to aid you. If it is ambiguous, reply with the most likely answer. Reply with just a single letter, either M or F."
        return openai.ChatCompletion.create(model=self.model, messages=[{"role": "system", "content": instructions},
                                                                        {"role": "user", "content": text}], temperature=0.2).choices[0].message.content

    def expandAcronymsAndAbbreviations(self, text, language="english"):
        if self.env['DEBUG'].upper() == 'TRUE':
            print("Getting subtitles")
            with open('transcript_test.txt', 'r') as file:
                text = file.read()
                text = self.add_whitespace_before_punctuation(text)
                return text.replace('\n', '').replace('\r', '')
        sharedInstructions = "edit it so that the abbreviations/acronyms/contractions are expanded, and correct grammar mistakes/correct for general ease of understanding. A text to speech program will use this as input, so make sure the output will be easily processed by the program. Add additional punctuation if necessary to make the speech flow better. Replace any new lines or tabs with whitespaces so that everything can be split using only whitespace"
        if language != "english":
            instructions = "Translate the following reddit post to " + \
                language+", then "+sharedInstructions + \
                " Then expand/convert all characters that are not letters, into the equivalent word/letter representation in the target language."
        else:
            instructions = "Given the following reddit post, "+sharedInstructions
        return openai.ChatCompletion.create(model=self.model, messages=[{"role": "system", "content": instructions},
                                                                        {"role": "user", "content": text}], temperature=0.1).choices[0].message.content

    def getSubtitles(self, text):
        if self.env['DEBUG'].upper() == 'TRUE':
            print("Getting subtitles")
            with open('transcript_test.txt', 'r') as file:
                text = file.read()
                text = self.add_whitespace_before_punctuation(text)
                return text.replace('\n', ' ').replace('\r', ' ')
        instructions = "Given the following transcript, expand/convert all characters that are not letters, into the equivalent word/letter representation. Add punctuation if necessary to make the speech flow better. Add line breaks if necessary to make the text easier to read."
        return openai.ChatCompletion.create(model="gpt-3.5-turbo", messages=[{"role": "system", "content": instructions},
                                                                             {"role": "user", "content": text}], temperature=0.1).choices[0].message.content
