import os  
from datetime import datetime
# datetime object containing current date and time
now = datetime.now() 
#print("now =", now)
# dd/mm/YY H:M:S
dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
#print("date and time =", dt_string)

def createFileDir(filesPath, outputFilePath, sectionTitle, fileMode):  
    fileMap = dict()  
    fileCount = dict()  
    with os.scandir(filesPath) as it:  # Doc -> https://docs.python.org/3.10/library/os.html?highlight=scandir#os.scandir  
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
    print('Updated %s in %s at %s file' % (sectionTitle, booksFile, dt_string))  
  
path = 'C:\Faheem\\vault\Files'  # \v was giving some error, hence escaping it by \\v  
personalPath = 'C:\Faheem\\vault\Files\Personal'  
booksFile = 'C:\Faheem\\vault\AllFiles.md'  
createFileDir(path, booksFile, 'Books', "w")  
createFileDir(personalPath, booksFile, 'Personal', "a")