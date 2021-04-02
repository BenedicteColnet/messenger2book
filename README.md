This code will allow you to make a book (📔 pdf) from your messenger and telegram messages.

You can find explanations to use the code step by step. You can also read the post HERE. 

Enjoy!

__PS1: feel free to contribute, add features, ⭐️ it, and/or share it!__
__PS2: I did this project on my free time and super quickly. I opened it because friends asked me to. So please, be gentle with the current features and code quality 🙈 __

# Background

To launch the code you will require python3 and Latex (in fact, xelatex). Be sure to have it installed on your computer. To be honest, you will probably need to have a little knowledge in both of these tools to complete your book, but it is very easy to find documentations online.

Toy data are available in this repository, and before doing your own book, please be sure that the command line `python main.py` is working. It should produce the `.tex` files in the section part. 
Then, open the document `template.tex` and compile it with `Xelatex`. Normally it whould produce a toy example. Note that you can custom the `template.tex` to change the color, the font, of your document.

# Download your data

## Messenger

First, go on your Facebook account and download your messages and pictures. It can take a few hours, and to my experience you have to download all your messages and you can not choose only one conversation. You will obtain something like this:

.

+-- archived_threads

+-- inbox

|   +-- your_friend

+-- message_requests

+-- stickers_used


Note the name of the folder with the messages you are interested in. Typically it can contain gifs, photos, videos, audio and one - or several ir you are talking a lot (😉) - `json` files. It contains the messages in questions. Please, don't touch anything from this folder, and just keep note of the name of the folder and the path.

Please, rename your `photos` folder with `photos_old` name. (I know it is a little bit dirty, but it is to manage telegram and messenger)

## Telegram 

Telegram allows you to download your messages per conversation. Be careful to export it in `json` format. The resulting folder should contain:

.

+-- photos

+-- result.json

+-- stickers

+-- video_files

Please, don't touch anything from this folder, and just keep note of the name of the folder and the path.


# Second: launch the script

Once your have your data, you will need to set up the parameters for the `main.py`. I know I could have written a beautiful command line, but in fact, I find easier that you open the `main.py` script, and just change the parameters in the top of the document, rather than having a super long command line in bash.

Anyway, you only need to change the path to the previously downloaded data, the source of the data (messenger or telegram), and to put your name and your friend's name. For this last step, open the `json` document that contains your messages and spot the names that are registered. And then replace the names. The `ME` corresponds to the flushleft author in the final book. Be carefull to put exactly the same string sequence as in the `json`.

```
DATA_PATH =  'data/messenger/' # './data/telegram/ChatExport_2020-12-06/' for typical telegram path
SOURCE = 'messenger' # or 'telegram'
ME = 'Me' # update with what you see in the json
MY_FRIEND = 'My friend' # update with what you see in the json
```

You don't need to change other parts of the code.

# Last, but not least

Compile the `.tex` files into youf `.pdf` book! (using `Xelatex`)


Now, you can print it! 🎉
