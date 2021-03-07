This code will allow you to make a book (📔 pdf) from your messenger and telegram messages.

You can find explanations to use the code step by step. You can also read the post HERE. 

Enjoy!

__PS: feel free to contribute, add features, ⭐️ it, and/or share it!__

# Zero: Background

To launch the code you will require python3 and Latex (and more, xelatex). Be sure to have it installed on your computer. To be honest, you will probably need to have a little knowledge in both of these tools to complete your book, but it is very easy to find documentations online.

# First: download your data

## Messenger

First, go on your Facebook account and download your messages and pictures. It can take a few hours, and to my experience you have to download all your messages and you can not choose only one conversation. You will obtain something like this:

.

+-- archived_threads

+-- inbox

|   +-- your_friend

+-- message_requests

+-- stickers_used


Note the name of the folder with the messages you are interested in. Typically it can contain gifs, photos, videos, audio and one - or several (😉) - `json` files. It contains the messages in questions. Please, don't touch anything from this folder, and just keep note off the name of the folder and the path.


## Telegram 

Telegram allows you to download your messages per conversation. Be careful to export it in `json` format. The resulting folder should contain:

.

+-- photos

+-- result.json

+-- stickers

+-- video_files

Please, don't touch anything from this folder, and just keep note off the name of the folder and the path.

# Second: launch the script

Once your have your data, all the rest should work with one big line of code. This line of code will read the `json` files and associated data and produce the so called `.tex` files. These are the source of your final document.


# Last, but not least

Compile the `.tex` files into youf `.pdf` book! (This is the best part)


Now, you can print it! 🎉
