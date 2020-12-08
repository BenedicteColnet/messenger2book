import os 
import re
  
def rename_messenger_photos(folder_path):
    for count, filename in enumerate(os.listdir(folder_path)):
        res = re.search("([0-9]*)_([0-9]*)_([0-9]*)_(.)_([0-9]*).(([a-z]*))", filename)
        new_file_name = f"{res.group(1)}_{res.group(2)}_{res.group(3)}_{res.group(4)}.{res.group(6)}"
        old_full_path = os.path.join(folder_path, filename)
        new_full_path = os.path.join(folder_path, new_file_name)
        os.rename(old_full_path, new_file_name)

