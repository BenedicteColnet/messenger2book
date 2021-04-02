
# dependencies 
import sys
sys.path.append('src')
import locale
locale.setlocale(locale.LC_TIME, 'fr_FR')   ## set French as local language, useful for date display

import pandas as pd
import numpy as np
import os
import re
import cv2 
from PIL import Image 
import glob

from models.telegram import TelegramModel
from models.messenger import MessengerModel
from utils.formatting import process_for_latex
from utils.timing import add_timing_to_df
from utils.formatting import left_formating, right_formating, left_formating_with_bubbles
from utils.formatting import right_formating_with_bubbles, format_msg


# GLOBAL PARAMETERS YOU HAVE TO SET
DATA_PATH =  'data/messenger/' # './data/telegram/ChatExport_2020-12-06/' for typical telegram path
SOURCE = 'messenger' # or 'telegram'
ME = 'Me' # update with what you see in the json
MY_FRIEND = 'My friend' # update with what you see in the json
# STOP EDITING BELOW THIS

def listdir_nohidden(path):
    return glob.glob(os.path.join(path, '*'))

def proces_gif_and_videos_messenger():

	new_directory_gifs = DATA_PATH+'gifs_as_frame'
	if not os.path.exists(new_directory_gifs):
		os.makedirs(new_directory_gifs)

	new_directory_videos = DATA_PATH+'/videos_as_frame'
	if not os.path.exists(new_directory_videos):
		os.makedirs(new_directory_videos)


	path_to_gifs = DATA_PATH+'gifs'
	messenger_gifs = listdir_nohidden(path_to_gifs)
	for gif in messenger_gifs:
		im = Image.open(path_to_gifs+'/'+gif)
		im.seek(0)
		res = re.search("([0-9]*)_([0-9]*)_([0-9]*)_(.).", gif)
		new_name = f"{res.group(1)}_{res.group(2)}_{res.group(3)}_{res.group(4)}"
		im.save(new_directory_gifs+'/'+new_name+'.png')

	path_to_videos = DATA_PATH+'videos'
	messenger_video = listdir_nohidden(path_to_videos)
        
	for video in messenger_video:
		if ".mp4" in video:
			vidcap = cv2.VideoCapture(path_to_videos + video)
			success, image = vidcap.read()
			if success:
				new_name = video[5:-4]+'.png'
				cv2.imwrite(new_directory_videos+"/"+new_name, image)

def process_photo_names_messenger():
	photos_dir = DATA_PATH+'photos_old'
	new_photos_dir = DATA_PATH+'photos'

	if not os.path.exists(new_photos_dir):
		os.makedirs(new_photos_dir)

	arr = listdir_nohidden(photos_dir)
	new_name = []
	for item in arr:
		res = re.search("([0-9]*)_([0-9]*)_([0-9]*)_(.).", item)
		if 'png' in item:
			file_name = f"{res.group(1)}_{res.group(2)}_{res.group(3)}_{res.group(4)}.png"
		else:
			file_name = f"{res.group(1)}_{res.group(2)}_{res.group(3)}_{res.group(4)}.jpg"
		#print(f"{res.group(1)}_{res.group(2)}_{res.group(3)}_{res.group(4)}.jpg")
		os.popen('cp '+item+' '+new_photos_dir+'/'+file_name)

def process_concatenated_table_to_tex(df):
	
	# mark empty bubbles
	df['empty_message'] = np.where(df.message == "", True, False)

	# prepare intro and ccl for the latex bubbles
	df['introtex']  = np.where(df.right, "\\begin{rightbubbles}", "\\begin{leftbubbles}")
	df['conclutex'] = np.where(df.right, "\\end{rightbubbles}", "\\end{leftbubbles}")
	df['conclutex'] = df['conclutex'].apply(lambda x: x + "\\vspace*{-0.6cm}")

	# Add extra space for speaker switches
	is_after_switch = np.not_equal(df['sender'].values[1:], df['sender'].values[:-1])
	df['is_after_switch'] = np.not_equal(df['sender'].shift(-1), df['sender'].shift(1))
	df['switchtex'] = np.append('', np.where(is_after_switch, "\\vspace*{0.2cm}", " "))

	# add hour
	#df['datetex'] = "\\flushright{\\textcolor{mygray}{{\\footnotesize "+df.timeStr+"}}}"
	df['datetex'] = "\\hspace{0.5cm}\\hfill{\\textcolor{mygray}{{\\footnotesize "+df.timeStr+"}}}"

	# deal with & in latex
	df['message'] = df['message'].replace('&', '\\&')

	# concatenate
	df['message'] = df[['switchtex','introtex', 'message', 'datetex', 'conclutex']].apply(lambda x: ' '.join(x), axis=1)

	# delete empty bubbles
	df['message'] = np.where(df.empty_message, "", df.message)

	# deal with photo
	# is previous photo?
	df['is_photo'] =  np.where(df.path, True, False)
	df['is_after_photo'] = df['is_photo'].shift(-1) & df['is_photo']
	df['is_after_photo'].fillna("False", inplace = True) 
	df['is_before_photo'] = df['is_photo'].shift(1) & df['is_photo']
	df['is_before_photo'].fillna("False", inplace = True) 


	df['tex_for_photo'] = np.where((df.is_photo) & (df.right), '\\begin{figure}[H]'+ ' \n ' +'\\begin{flushright}' + ' \n ' + '\\includegraphics[width=8cm,height=8cm,keepaspectratio]{'+df.path.str.get(0)+'}'+'\\end{flushright}'+'\n'+'\\end{figure}', "")
	df['tex_for_photo'] = np.where((df.is_photo) & (df.right == False), '\\begin{figure}[H]'+ ' \n ' +'\\begin{flushleft}' + ' \n ' + '\\includegraphics[width=8cm,height=8cm,keepaspectratio]{'+df.path.str.get(0)+'}'+'\\end{flushleft}'+'\n'+'\\end{figure}', df.tex_for_photo)

	# deal with gifs
	df['is_gif'] =  np.where(df.gifs, True, False)
	df['tex_for_gif'] = np.where((df.is_gif) & (df.right), '\\begin{figure}[H]'+ ' \n ' +'\\begin{flushright} \emoji[ios]{1F3A5}  \\includegraphics[width=0.3\\textwidth]{'+df.gifs.str.get(0)+'}'+'\\end{flushright}'+'\n'+'\\end{figure}', "")
	df['tex_for_gif'] = np.where((df.is_gif) & (df.right == False), '\\begin{figure}[H]'+ ' \n ' +'\\begin{flushleft} \emoji[ios]{1F3A5}  \\includegraphics[width=0.3\\textwidth]{'+df.gifs.str.get(0)+'}'+' \\end{flushleft}'+'\n'+'\\end{figure}', df.tex_for_gif)

	# deal with videos 
	df['is_videos'] =  np.where(df.videos, True, False)
	df['tex_for_videos'] = np.where((df.is_videos) & (df.right), '\\begin{figure}[H]'+ ' \n ' +'\\begin{flushright} \emoji[ios]{1F3A5} \\includegraphics[width=0.3\\textwidth]{'+df.videos.str.get(0)+'} \\end{flushright}'+'\n'+'\\end{figure}', "")
	df['tex_for_videos'] = np.where((df.is_videos) & (df.right == False), '\\begin{figure}[H]'+ ' \n ' +'\\begin{flushleft} \emoji[ios]{1F3A5}  \\includegraphics[width=0.3\\textwidth]{'+df.videos.str.get(0)+' \\end{flushleft}'+'\n'+'\\end{figure}', df.tex_for_videos)

	# deal with reactions
	df['is_reactions'] =  np.where(df.reactions, True, False)
	df['tex_for_reactions'] = np.where((df.is_reactions) & (df.right == False), '\\vspace*{-0.6cm}\\begin{flushleft}' +df.reactions.str.get(0)+ '\\end{flushleft}\\vspace*{-0.2cm}', " ")
	df['tex_for_reactions'] = np.where((df.is_reactions) & (df.right), '\\vspace*{-0.6cm}\\begin{flushright} ' +df.reactions.str.get(0)+ '\\end{flushright}\\vspace*{-0.2cm}', df.tex_for_reactions)

	# join photo and message, with photo first
	df['message'] = df[['tex_for_gif', 'tex_for_photo', 'message','tex_for_reactions']].apply(lambda x: ' '.join(x), axis=1)


	for date, df_t in df.groupby('date'):
		date_str = df_t['dateStr'].unique()[0]
		title = '\\section*{' + date_str + '\markboth{\MakeLowercase{'+ date_str +'}}{}}'
		discussion = '\n'.join(df_t.message)
		text = f'{title}\n{discussion}'
		
		with open(f'./output/sections/{date}.tex', 'w', encoding='utf-8') as ft:
			ft.write(text)


def main():

	# read json
	if SOURCE == 'telegram':
		telegram_data_path = DATA_PATH + 'result.json'
		telegram_model = TelegramModel()
		concatenated_table = telegram_model.parse_from_json(telegram_data_path, "Me", "My friend")

	elif SOURCE == 'messenger':
		process_photo_names_messenger()
		proces_gif_and_videos_messenger()
		messenger_data_path = DATA_PATH + 'message.json'
		messenger_model = MessengerModel()
		concatenated_table = messenger_model.parse_from_json(messenger_data_path, "Me", "My friend")

	concatenated_table = add_timing_to_df(concatenated_table)
	process_concatenated_table_to_tex(concatenated_table)
	

if __name__ == "__main__":
    main()