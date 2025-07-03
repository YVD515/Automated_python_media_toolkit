import os
import shutil
import datetime

# folder path
source_folder = input('enter path to the folder: ') # /Users/danushvdarshan/Desktop/YVD

# List all files/folders in that path
items = os.listdir(source_folder)

#log
log_file = os.path.join(source_folder, 'organizer_log.txt')

def log(message):
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S") # gets the date and time
    with open(log_file, 'a') as f:
        f.write(f'[{timestamp}] {message}\n')
        print(message)

def unique_dest(dest_path):
    base, ext = os.path.splitext(dest_path) 
    counter = 1 # number to add in the duplicates
    while os.path.exists(dest_path): # if true
        dest_path = f"{base}_{counter}{ext}"
        counter += 1 #loops until 'false'
    return dest_path


destinations = {
    'Images': ['.jpg', '.jpeg', '.heic', '.heif', '.webp'],
    'Videos': ['.mp4', '.mov', '.mov'],
    'Audios': ['.mp3', '.m4a', '.wav', '.avi'], 
    'Docs': ['.docx', '.xlsx', '.csv', '.pdf', '.pptx'], 
    'code': ['.py', '.ipynb', '.json', '.html']
}       # Add extensions or Folders whenever you want

for item in items:
    item_path = os.path.join(source_folder, item) #path name + item name

    if os.path.isfile(item_path):
        _, ext = os.path.splitext(item_path) # splits name, .ext
        ext = ext.lower()

        moved = False

        for folder in destinations.keys(): # creates a folder if it didn't exist
            folder_path = os.path.join(source_folder, folder)
            if not os.path.exists(folder_path): # True/False
                os.makedirs(folder_path) # creates the folder
                log(f"Created folder: {folder_path}") #message

        for folder, extensions in destinations.items(): # folder => imgs, vids, etc.. ; extensions => .jpg, .mp4, .mp3 ..
            if ext in extensions:
                dest_path = os.path.join(source_folder, folder, item) # '/Users/danushvdarshan/Desktop/YVD + /Images + /pfp.jpg'
                dest_path = unique_dest(dest_path)
                shutil.move(item_path, dest_path) #moves the files
                log(f'moved {item} to {folder} as {os.path.basename(dest_path)}')
                moved = True
                #Flag

        if not moved:
            log(f'❌ {item} (unknown file type)')
        