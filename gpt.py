import openai


class GPT:
    def __init__(self, env) -> None:
        self.env = env
        openai.api_key = env['OPENAI_API_KEY']
        self.model = "gpt-3.5-turbo"
        if (env['USE_GPT_4'].upper() == 'TRUE'):
            self.model = "gpt-4"

    # def getGender(self, text):
    #     instructions = "Given the following reddit post, determine the gender of the poster. Use the context of the post to aid you. If it is ambiguous, reply with the most likely answer. Reply with just a single letter, either M or F."
    #     return openai.ChatCompletion.create(model=self.model, messages=[{"role": "system", "content": instructions},
    #                                                                     {"role": "user", "content": text}], temperature=0.2).choices[0].message.content

    # def expandAcronymsAndAbbreviations(self, text, language="english"):
    #     sharedInstructions = "edit it so that the abbreviations/acronyms are expanded, and correct grammar mistakes/correct for general ease of understanding. A text to speech program will use this as input, so make sure the output will be easily processed by the program. Add additional punctuation if necessary to make the speech flow better. You may leave commonly understood acronyms/abbreviations unexpanded."
    #     if language != "english":
    #         instructions = "Translate the following reddit post to " + \
    #             language+", then "+sharedInstructions + \
    #             " Then expand/convert all characters that are not letters, into the equivalent word/letter representation in the target language."
    #     else:
    #         instructions = "Given the following reddit post, "+sharedInstructions
    #     return openai.ChatCompletion.create(model=self.model, messages=[{"role": "system", "content": instructions},
    #                                                                     {"role": "user", "content": text}], temperature=0.1).choices[0].message.content

    # def getSubtitles(self, text):
    #     instructions = "Given the following transcript, expand/convert all characters that are not letters, into the equivalent word/letter representation. Add spaces if necessary in front of punctuation marks so that I can split the string properly. Add punctuation if necessary to make the speech flow better. Add line breaks if necessary to make the text easier to read."
    #     return openai.ChatCompletion.create(model="gpt-3.5-turbo", messages=[{"role": "system", "content": instructions},
    #                                                                          {"role": "user", "content": text}], temperature=0.1).choices[0].message.content


    def getGender(self, text):
        return "M"

    def expandAcronymsAndAbbreviations(self, text, language="english"):
        return """
            Am I the Asshole for refusing to take my sister to the Renaissance Faire because of what she wants to wear?

I, 25-year-old female, am the oldest of four kids. My brother Sam is a 20-year-old male, and my sisters are Maddy, a 17-year-old female, and Kiara, a 12-year-old female. I have been going to the Renaissance Faire since I was 16, usually with friends. However, once Sam and Maddy were 13, I started taking them with me. Kiara just turned 12 a few months ago and said she wanted to go to the Renaissance Faire this year. I was hesitant but asked our mom, and once she gave the okay, I actually got excited because, very sadly, Sam is in the Marines and can't go this year because he is deployed. That is, I was excited until I found out what she wanted to wear.

Maddy and I have been planning and making our outfits since the last Renaissance Faire (we are both avid seamstresses) and offered to help Kiara design her outfit. Kiara is really into Furries lately and has started making suits and masks, but I made it clear that the Renaissance Faire isn't the place for that, and I was uncomfortable taking her in that. She agreed, we came up with a few outfit designs, and set a day to go shopping for all the stuff.

She then came to me a week ago, gloating, saying that our mom said yes to her wearing a furry suit to the Renaissance Faire. I told her she absolutely could, but again, I wouldn't be the one taking her if she chose to wear that. She got upset and said I was being unfair because I was still taking Maddy. I told her again that the Renaissance Faire isn't the place for that, and who I take with me is up to me. She's now very upset with me and is trying to get our mom to make me take her wearing her furry suit.

So... Am I the Asshole?
        """

    def getSubtitles(self, text):
        return """
        Am I the Asshole for refusing to take my sister to the Renaissance Faire because of what she wants to wear ?

I, twenty-five-year-old female , am the oldest of four kids . My brother Sam is a twenty-year-old male , and my sisters are Maddy , a seventeen-year-old female , and Kiara , a twelve-year-old female . I have been going to the Renaissance Faire since I was sixteen , usually with friends . However, once Sam and Maddy were thirteen , I started taking them with me . Kiara just turned twelve a few months ago and said she wanted to go to the Renaissance Faire this year . I was hesitant but asked our mom , and once she gave the okay , I actually got excited because , very sadly , Sam is in the Marines and cannot go this year because he is deployed . That is , I was excited until I found out what she wanted to wear .

Maddy and I have been planning and making our outfits since the last Renaissance Faire (we are both avid seamstresses) and offered to help Kiara design her outfit . Kiara is really into Furries lately and has started making suits and masks , but I made it clear that the Renaissance Faire is not the place for that , and I was uncomfortable taking her in that . She agreed , we came up with a few outfit designs , and set a day to go shopping for all the stuff .

She then came to me a week ago , gloating , saying that our mom said yes to her wearing a furry suit to the Renaissance Faire . I told her she absolutely could , but again , I would not be the one taking her if she chose to wear that . She got upset and said I was being unfair because I was still taking Maddy . I told her again that the Renaissance Faire is not the place for that, and who I take with me is up to me . She is now very upset with me and is trying to get our mom to make me take her wearing her furry suit .

So... Am I the Asshole ?"""
