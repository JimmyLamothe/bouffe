from zipfile import ZipFile
from pathlib import Path
import os
import time_methods as time

def remove_dupes(lst):
    return list(set(lst))

#saves all json files as zip to Dropbox. Keeps 10 versions.
def backup_json():
    date = time.today()
    now = time.now()
    dropbox_path_string = '/Users/jimmy/Dropbox/Bouffe/'
    dropbox_path = Path(dropbox_path_string)
    json_path = '/Users/jimmy/Programming/Python/bouffe/json/'
    backup_name = dropbox_path_string + 'backup_' + now + '.zip'
    dir_list = [x for x in dropbox_path.iterdir() if not x.stem[0] == '.']
    dir_list.sort(key = lambda x : x.stat().st_ctime)
    if len(dir_list) >= 10:
        dir_list[0].unlink() #Remove oldest file if more than 10
   #Following copied from: https://thispointer.com/python-how-to-create-a-zip-archive-from-multiple-files-or-directory/
    with ZipFile(backup_name, 'w') as zipObj:
        for folderName, subfolders, filenames in os.walk(json_path):
            for filename in filenames:
                #create complete filepath of file in directory
                filePath = os.path.join(folderName, filename)
                # Add file to zip
                zipObj.write(filePath)
