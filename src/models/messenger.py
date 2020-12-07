import datetime
import json
import os
import re
import pandas as pd
import emoji

from src.models import BaseChatAppModel

MESSENGER_PHOTOS_FOLDER = "../data/messenger/photos"
MESSENGER_GIFS_FOLDER = "../data/messenger/gifs_as_frame"
MESSENGER_VIDEOS_FOLDER = "../data/messenger/videos_as_frame"


class MessengerModel(BaseChatAppModel):
    def _load_data(self, data_path):
        """Opens and reads the specified file in the chat app native format."""
        with open(data_path, encoding='ascii') as f:
            return json.load(f)

    def _pre_process(self, raw_data):
        """Reformats the data from native chat app format to standardized format."""

        # Faced issues with messenger, went on Chatistics repo and parse.py messenger
        concatenated_table_messenger = {'source': [],  # telegram or messenger (string)
                                        'datetime': [],  # date (string)
                                        'sender': [],  # M or B (string)
                                        # content in text (string)
                                        'message': [],
                                        'path': []}  # path to images or gifs (list of string)

        concatenated_table_messenger = pd.DataFrame(
            concatenated_table_messenger)

        participants = raw_data["participants"]
        #raw_data_messenger = pd.read_json('messenger/inbox/marcnegre_hwizlpvhxw/message_1.json', lines=True)
        # raw_data_messenger.info()
        # raw_data_messenger.head()
        for message in raw_data["messages"][0:900000000]:  # only 100 messages to test

            timestamp = message["timestamp_ms"] / 1000
            timestamp = datetime.datetime.fromtimestamp(
                timestamp).strftime('%Y-%m-%d %H:%M:%S.%f')

            sender = message["sender_name"]
            if sender == "BÃ©nÃ©dicte Cnt":
                sender = 'B'
            elif sender == "Marc Negre":
                sender = 'M'
            """
            else:
                print("Error in a sender name")
                print(sender)
                break
            """

            # check if 'content' exists in dictionary by checking if get() returned None
            # if not content it is because it is a sticker or picture for example
            if message.get('content') is not None:
                text = message["content"]
                text = text.encode('latin-1').decode('raw_unicode_escape').encode(
                    'latin-1').decode('utf-8')  # I think better solution exist!
            else:
                text = ""

            # deal with & in latex
            text = text.replace('&', '\\&')
            # deal with % in latex
            text = text.replace('%', '\\%')
            # deal with _
            text= text.replace('_', '\\_', 30)
            # deal with #
            text = text.replace('#', '\\#')
            # deal with \n
            text= text.replace('\n', '\\\\')
            # deal with $
            text= text.replace('$', '\\$', 30)
            # deal with ^ 
            text= text.replace('^^', '$\wedge$ $\wedge$', 30)
            #deal with url
            urls = re.findall('http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', text)
            for url in urls:
                text = text.replace(url, "\\texttt{"+url[1:40]+"[...]}")
            # deal with emoji
                # TODO: fix this undefined emoji: "not(c in emoji.UNICODE_EMOJI):"
            new_text = "".join(f"\emoji[ios]{{{ord(c):X}}}" if c in emoji.UNICODE_EMOJI else c for c in text) 

            # new_text = ""
            # for c in text:
            #     # TODO: fix this undefined emoji: "not(c in emoji.UNICODE_EMOJI):"
            #     if True:
            #         new_text = new_text + c
            #     else:
            #         # Change for f string instead of [2:]
            #         new_text = new_text + \
            #             "\emoji[ios]{"+f"{hex(ord(c))[2:]}"+"}"

            if message.get('photos') is not None:
                photo = []
                for p in message['photos']:
                    photo.append(self._reformat_image_path(p['uri']))
                    #photo.append(p['uri'])
            else:
                photo = []

            gifs = []

            if message.get('gifs') is not None:
                for p in message['gifs']:
                    gifs.append(self._reformat_image_path(p['uri']))
                    

            # # put sticker with gifs
            # if message.get('sticker') is not None:
            #     for p in message['sticker']:
            #         print(type(p))
            #         path_to_sticker = "../data/messenger/"+str(p['uri'])
            #         gifs.append(path_to_sticker)

            videos = []
            if message.get('videos') is not None:
                for p in message['videos']:
                    videos.append(self._reformat_videos_path(p['uri']))

            # deal with reactions
            #reactions = [r.get("reaction") for r in message.get("reactions", [])]
            reactions = []
            if message.get('reactions') is not None:
            	react = (message["reactions"][0]["reaction"]).encode('latin-1').decode('raw_unicode_escape').encode(
                    'latin-1').decode('utf-8')
            	new_react = "".join(f"\emoji[ios]{{{ord(c):X}}}" if c in emoji.UNICODE_EMOJI else c for c in react)
            	reactions.append(new_react)
            	



            new_row = {'source': "Messenger", 'datetime': timestamp,
                       'sender': sender, 'message': new_text, 'path': photo, 'reactions': reactions, 'gifs' : gifs, 'videos' : videos}
            concatenated_table_messenger = concatenated_table_messenger.append(
                new_row, ignore_index=True)


        return concatenated_table_messenger


    def _reformat_videos_path(self, uri):
        #print(uri, re.search("([0-9]*)_([0-9]*)_([0-9]*)_(.).[(jpg)|(png)]", uri))
        #res = re.search("([0-9]*)_([0-9]*)_([0-9]*)_(.).[(jpg)|(png)]", uri)
        res = re.search("([0-9]*)_([0-9]*)_([0-9]*)_(.).", uri)
        #file_name = f"{res.group(1)}_{res.group(2)}_{res.group(3)}_{res.group(4)}_{res.group(2)}.png"
        file_name = f"{res.group(1)}_{res.group(2)}.png"
        file_location = os.path.join(MESSENGER_VIDEOS_FOLDER, file_name)
        return file_location

    def _reformat_gifs_path(self, uri):
        #print(uri, re.search("([0-9]*)_([0-9]*)_([0-9]*)_(.).[(jpg)|(png)]", uri))
        #res = re.search("([0-9]*)_([0-9]*)_([0-9]*)_(.).[(jpg)|(png)]", uri)
        res = re.search("([0-9]*)_([0-9]*)_([0-9]*)_(.).", uri)
        #file_name = f"{res.group(1)}_{res.group(2)}_{res.group(3)}_{res.group(4)}_{res.group(2)}.png"
        file_name = f"{res.group(1)}_{res.group(2)}_{res.group(3)}_{res.group(4)}.png"
        file_location = os.path.join(MESSENGER_GIFS_FOLDER, file_name)
        return file_location

    def _reformat_image_path(self, uri):
        #print(uri, re.search("([0-9]*)_([0-9]*)_([0-9]*)_(.).[(jpg)|(png)]", uri))
        #res = re.search("([0-9]*)_([0-9]*)_([0-9]*)_(.).[(jpg)|(png)]", uri)
        res = re.search("([0-9]*)_([0-9]*)_([0-9]*)_(.).", uri)
        if 'png' in uri:
            #file_name = f"{res.group(1)}_{res.group(2)}_{res.group(3)}_{res.group(4)}_{res.group(2)}.png"
            file_name = f"{res.group(1)}_{res.group(2)}_{res.group(3)}_{res.group(4)}.png"
        else:
            #file_name = f"{res.group(1)}_{res.group(2)}_{res.group(3)}_{res.group(4)}_{res.group(2)}.jpg"
            file_name = f"{res.group(1)}_{res.group(2)}_{res.group(3)}_{res.group(4)}.jpg"
        file_location = os.path.join(MESSENGER_PHOTOS_FOLDER, file_name)
        return file_location
