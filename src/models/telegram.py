import pandas as pd

from src.models import BaseChatAppModel
from src.utils.formatting import process_for_latex

# TODO: Remove the limit below
MAX_NUMBER_MESSAGE = 15  # Maximum number of messages to keep

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

            # Deal with picture (apparently several pictures are send as several messages)
            if 'photo' in element:
                photo = element["photo"]
            else:
                photo = []

            # deal with text that are list or hastag
            if type(element["text"]) == str:
                text = element["text"]
            elif type(element["text"]) == list:
                text = element["text"][0]
                if type(text) == dict:
                    text = "\\" + element['text'][0]['text']
            else:
                print("Error in the type of text")
                break

            # deal with emoji
            new_text = ""
            for c in text:
                if True:  # TODO: fix this undefined emoji: "not(c in emoji.UNICODE_EMOJI):"
                    new_text = new_text + c
                else:
                    # Change for f string instead of [2:]
                    new_text = new_text + \
                        "\emoji[ios]{"+f"{hex(ord(c))[2:]}"+"}"

            # deal with formatting
            new_text = process_for_latex(new_text)

            # replace \n with \\
            new_text = new_text.replace("\n", "\\ ")

            new_row = {'source': "Telegram",
                       'datetime': element["date"], 'sender': sender, 'message': new_text, 'path': photo}
            concatenated_table = concatenated_table.append(
                new_row, ignore_index=True)
        return concatenated_table
