# messenger2book
Take your messenger and telegram messages (json) and produce a book with it (pdf)

Telegram: contain examples of typical telegram messages

To compile the latex, use XeLatex (due to emoji)


# First: download your data

## Messenger

First, go on your Facebook account and download your messages and pictures. It can take a few hours, and to my experience you have to download all your messages and you can not choose only one conversation. You will obtain something like this:

.
+-- archived_threads
+-- inbox
|   +-- your_friend
+-- message_requests
+-- stickers_used

Note the name of the folder with the messages you are interested in. Typically it can contain gifs, photos, videos, audio and one - or several (😉) - `json` files. It contains the messages in questions.
