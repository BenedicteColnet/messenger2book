import datetime
import json
import pandas as pd

from src.models import BaseChatAppModel


class MessengerModel(BaseChatAppModel):
    def _load_data(self, data_path):
        """Opens and reads the specified file in the chat app native format."""
        with open(data_path, encoding='ascii') as f:
            return json.load(f)

    def _pre_process(self, raw_data):
        """Reformats the data from native chat app format to standardized format."""


        # Faced issues with messenger, went on Chatistics repo and parse.py messenger
        concatenated_table_messenger = {'source': [], # telegram or messenger (string)
                'datetime': [], # date (string)
                'sender': [], # M or B (string)
                'message': [], # content in text (string)
                'path': []} # path to images or gifs (list of string)

        concatenated_table_messenger = pd.DataFrame(concatenated_table_messenger)

        participants = raw_data["participants"]
        #raw_data_messenger = pd.read_json('messenger/inbox/marcnegre_hwizlpvhxw/message_1.json', lines=True)
        #raw_data_messenger.info()
        #raw_data_messenger.head()
        for message in raw_data["messages"][1:100]:  # only 100 messages to test
            
            timestamp = message["timestamp_ms"] / 1000
            timestamp = datetime.datetime.fromtimestamp(timestamp).strftime('%Y-%m-%d %H:%M:%S.%f')
            
            sender = message["sender_name"]
            if sender == "BÃ©nÃ©dicte Cnt":
                sender = 'B'
            elif sender == "Marc Negre":
                sender = 'M'
            else:
                print("Error in a sender name")
                print(sender)
                break
            
            # check if 'content' exists in dictionary by checking if get() returned None
            # if not content it is because it is a sticker or picture for example
            if message.get('content') is not None:
                text = message["content"]
                text = text.encode('latin-1').decode('raw_unicode_escape').encode('latin-1').decode('utf-8') #I think better solution exist!
            else:
                text = ""
            
            
            # deal with emoji
            new_text = ""
            for c in text:
                if True:  # TODO: fix this undefined emoji: "not(c in emoji.UNICODE_EMOJI):"
                    new_text = new_text + c
                else:
                    new_text = new_text + "\emoji[ios]{"+f"{hex(ord(c))[2:]}"+"}" #Change for f string instead of [2:]
            
            
            
            if message.get('photos') is not None:
                photo = []
                for p in message['photos']:
                    photo.append(p['uri']) # now grap the proper png name
                    
            else:
                photo = [] # 
            
            new_row = {'source' : "Messenger", 'datetime': timestamp, 'sender' : sender, 'message': new_text, 'path': photo}
            concatenated_table_messenger = concatenated_table_messenger.append(new_row, ignore_index = True)

            
        return concatenated_table_messenger
