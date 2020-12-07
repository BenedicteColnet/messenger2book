import pandas as pd
import emoji
import re

from src.models import BaseChatAppModel
from src.utils.formatting import process_for_latex

TELEGRAM_PHOTOS_FOLDER = "../data/telegram/ChatExport_2020-12-06/"
MAX_NUMBER_MESSAGE = 100000000

class TelegramModel(BaseChatAppModel):
    def _load_data(self, data_path):
        """Opens and reads the specified file in the chat app native format."""
        return pd.read_json(data_path)

    def _pre_process(self, raw_data):
        """Reformats the data from native chat app format to standardized format."""
        concatenated_table = {'source': [],  # telegram or messenger (string)
                              'datetime': [],  # date (string)
                              'sender': [],  # M or B (string)
                              'message': [],  # content in text (string)
                              'path': []}  # path to images or gifs (list of string)

        concatenated_table = pd.DataFrame(concatenated_table)

        # Deal with telegram messages
        for element in raw_data["messages"][1:MAX_NUMBER_MESSAGE]: 
            # simplify sender
            if element["from"] == 'Marc Negre':
                sender = "M"
            elif element["from"] == 'Bénédicte Colnet':
                sender = "B"
            else:
                print("Error on sender on message number "+str(element))
                break

            # Deal with picture (apparently several pictures are send as several messages) TODO: check it is true
            if 'photo' in element:
                photo = [TELEGRAM_PHOTOS_FOLDER + element['photo']]
                #print(photo)
            else:
                photo = []


            gifs = []
            # naive add for video
            if 'thumbnail' in element:
                 thumbnail_name = element["thumbnail"]
                 if 'jpg' in thumbnail_name:
                    if "tgs" in thumbnail_name:
                        continue
                    else:
                     gifs.append(TELEGRAM_PHOTOS_FOLDER + thumbnail_name)
                     print(TELEGRAM_PHOTOS_FOLDER + element["thumbnail"])

            videos = []


            # deal with text type
            text = ""

            # if a simple message (simplest case)
            if type(element["text"]) == str:
                text = text + element["text"]

            # else: browse messages
            elif type(element["text"]) == list:
                for message in element["text"]:
                    if type(message) == str:
                        text = text + message
                    if type(message) == dict:
                        if message["type"] == "italic":
                            text = text + " \\textit{" + message['text']+"}"
                        elif message["type"] == "bold":
                            text = text + " \\textbf{" + message['text']+"}"
                        elif message["type"] in ["code", "pre", "phone", "mention", "email"]:
                            text = text + " \\texttt{" + message['text']+"}"
                        elif message["type"] == "hashtag":
                            text = text + " \\texttt{{\#} " + message['text'][1:]+"}"
                        elif message["type"] == "link":
                            #text = text + " \\texttt{" + message['text']+"}"
                            text = text + " \\texttt{LINK}"
                        else:
                            print("Missing type: "+message["type"])


            else:
                print("Error in the type of text")
                break

            # deal with & 
            text= text.replace('&', '\\&', 30)

            # deal with % 
            text= text.replace('%', '\\%', 30)

            # deal with $
            text= text.replace('$', '\\$', 30)
            
            # deal with ^ 
            text= text.replace('^^', '$\wedge$ $\wedge$', 30)

             # deal with _
            text= text.replace('_', '\\_', 30)

            # deal with #
            # text= text.replace('#', '\\#', 30)

            # deal with \n
            text= text.replace('\n', '\\\\', 30)

            # deal with emoji
            new_text = "".join(f"\emoji[ios]{{{ord(c):X}}}" if c in emoji.UNICODE_EMOJI else c for c in text)  

            # deal with formatting
            #new_text = process_for_latex(new_text)

            # replace \n with \\
            new_text = new_text.replace("\n", "\\ ")

            new_row = {'source': "Telegram",
                       'datetime': element["date"], 'sender': sender, 'message': new_text, 'path': photo, 'reactions': "", 'gifs' : gifs, 'videos' : videos}
            concatenated_table = concatenated_table.append(
                new_row, ignore_index=True)
        return concatenated_table

