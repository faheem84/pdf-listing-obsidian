import os
import time
from datetime import datetime

# ChatGPT gave me this date_format when i asked it "what is the 
# date format string for this date Wed May 17 09:24:08 2023"  
date_format = "%a %b %d %H:%M:%S %Y"
dt_string = datetime.now().strftime(date_format)
booksFile = 'C:\Faheem\\vault\Glossary.md'
skip_dir_list = ['QuickNotes', 'templates', 'Files', '.obsidian', '.trash', '.tmp', 'Diary', 'Personal']
path = 'C:\Faheem\\vault\Files'  # \v was giving some format error, hence escaping it by \\v  
personalPath = 'C:\Faheem\\vault\Files\Personal'
root_dir = 'C:\Faheem\\vault'


def skip_dirs(root_dir):
    found = False
    for s in skip_dir_list:
        root_dir_lower = root_dir.lower()
        if s.lower() in root_dir_lower:
            return True
    return False


def create_glossary(directory, sectionTitle, fileMode):
    glossary_map = {}
    glossary_count = dict()
    for root, dirs, files in os.walk(directory):
        for file_name in files:
            if skip_dirs(root):
                continue
            start_char = file_name[0].upper()
            file_names = glossary_map.get(start_char, [])
            file_path = os.path.join(root, file_name)
            last_modified_time = datetime.strptime(time.ctime(os.path.getmtime(file_path)), date_format)
            current_datetime = datetime.now()
            time_diff = current_datetime - last_modified_time
            file_name = "[[%s]] %s" % (file_name, time_diff.days)
            file_names.append(file_name)
            glossary_map[start_char] = file_names
            if start_char not in glossary_count:
                glossary_count[start_char] = 1
            else:
                glossary_count[start_char] += 1

    file_chars = list(glossary_map.keys())
    file_chars.sort()

    with open(booksFile, fileMode) as fhand:
        print('# %s' % sectionTitle, file=fhand)
        for key in file_chars:
            print('## %s' % key, file=fhand)
            # print('*%d*' % glossary_count[key], file=fhand)
            print('<font size="4" color="turquoise">%s</font>' % glossary_count[key], file=fhand)
            fileNameList = glossary_map.get(key)
            for fileName in fileNameList:
                print('%s' % fileName, file=fhand)
    print('Updated %s in %s at %s' % (sectionTitle, booksFile, dt_string))


def createFileDir(filesPath, sectionTitle, fileMode):
    fileMap = dict()
    fileCount = dict()
    with os.scandir(
            filesPath) as it:  # Doc -> https://docs.python.org/3.10/library/os.html?highlight=scandir#os.scandir
        for entry in it:
            if entry.is_file() and not entry.name.startswith('.'):
                fileName = entry.name
                startChar = fileName[0].upper()
                fileNameList = fileMap.get(startChar, [])
                fileNameList.append(fileName)
                fileMap[startChar] = fileNameList
                if startChar not in fileCount:
                    fileCount[startChar] = 1
                else:
                    fileCount[startChar] += 1

    charList = list(fileMap.keys())
    charList.sort()

    with open(booksFile, fileMode) as fhand:
        print('# %s' % sectionTitle, file=fhand)
        for key in charList:
            print('## %s' % key, file=fhand)
            print('*%d*' % fileCount[key], file=fhand)
            fileNameList = fileMap.get(key)
            for fileName in fileNameList:
                print('[[%s]]\n' % fileName, file=fhand)
    print('Updated %s in %s at %s' % (sectionTitle, booksFile, dt_string))


createFileDir(path, 'Books', "w")
createFileDir(personalPath, 'Personal', "a")
create_glossary(root_dir, 'Concepts', "a")
