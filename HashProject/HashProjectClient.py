import sys
from socket import *
import os
import platform
import hashlib

serverHost = 'localhost'
serverPort = 3000
pingmsg = b'ping'
serverACK = b'connection established'
filename: str = ''
path_to_file = ''
filenameList = []
connectionReady: bool = False
searchPath=''
filename_path = []  #earlier a dic
hashResult = []
rescan = False

if len(sys.argv) == 4:
    serverHost = sys.argv[1]
    serverPort = int(sys.argv[2])
    if sys.argv[3] == "rescan":
        rescan = True
    else:
        filename = sys.argv[3]
else:
    print("Insufficient parameters for the job")

print("serverHost: "+str(serverHost))
print("serverPort: "+str(serverPort))
print("filename: "+str(filename))

sockobj = socket(AF_INET, SOCK_STREAM)
sockobj.connect((serverHost,serverPort))
sockobj.send(pingmsg)
data = sockobj.recv(1024)
if data == serverACK:
    print("Client received ACK: "+str(data)," => Ready to communicate")
    connectionReady = True

print("rescan state:", rescan)
"""   
print(connectionReady)
print(filename)
"""


def preparepathtofile():
    global path_to_file
    currentDir = os.getcwd()
    path_to_file = os.path.join(currentDir, str(filename))
    print(path_to_file)


def readfile(path_to_file):
    myfileObject = open(path_to_file, 'r')
    while True:
        currentLine = myfileObject.readline()
        if currentLine != '':
            filenameList.append(currentLine)
        else:
            break
    myfileObject.close()


def sanitizeFilenames():
    for i in range(0,len(filenameList)):
        filenameList[i] = filenameList[i].strip("\n")
        filenameList[i] = filenameList[i].strip(",")

def updateSearchPath():
    global searchPath
    if platform.system() == 'Linux':
        searchPath = "/"


def buildFilePaths(filenames, searchpath):
    print(filenames)
    #len = len(filenames)
    x=0
    global filename_path
    tempdict = {}
    for root, dir, files in os.walk(searchpath):
        for obj in filenames:
            for file in files:
                if file.find(obj)>=0:
                    #print(root, file)
                    tempdict = {obj:os.path.join(root, file)}
                    filename_path.append(tempdict)
                else:
                     if obj == file:
                         tempdict = {obj:os.path.join(root, file)}
                         filename_path.append(tempdict)

    # for root, dir, files in os.walk(searchpath):
    #     #for obj in filenames:
    #         for file in files:
    #             if file.find(filenames[x])>=0:
    #                 print(root, file)
    #                 tempdict = {filenames[x]:os.path.join(root, file)}
    #                 filename_path.append(tempdict)
    #             # else:
    #             #     if filenames[x] == file:
    #             #         tempdict = {file:os.path.join(root, file)}
    #             #         filename_path.update(tempdict)
            


def hash_file(pathToFilename):
    h = hashlib.md5()

    myfileObject = open(pathToFilename, 'rb')
    chunk = 0
    while chunk != b'':
           # read only 1024 bytes at a time
           chunk = myfileObject.read(1024)
           h.update(chunk)
    myfileObject.close()
    return h.hexdigest()


def hash_director():
    global hashResult

    for element in filename_path:
        for key, value in element.items():
            templist = []
            templist.append(key)
            templist.append(value)
            hashrecv = hash_file(value)
            templist.append(hashrecv)
            hashResult.append(templist)

        

def display_result():
    print('Displaying Result')
    for i in range(0, len(hashResult)):
        for j in range(0, len(hashResult[i])):
            print(hashResult[i][j], end= " "),
        print()
    print()


def sendData():
    strdata = str(hashResult)
    strdata = strdata.encode()
    sockobj.send(strdata)

def close_connection():
    sockobj.send(b'')

#print(path_to_file)

def receiveFileData():
    global filename_path
    while True:
        data1 = sockobj.recv(3072)
        data1 = data1.decode('utf-8')
        data1 = eval(data1)
        filename_path = data1
        print(filename_path)
        if data1:
            break
    return


if connectionReady and (rescan == False):
    print('Normal scan')
    preparepathtofile()
    readfile(path_to_file)
    sanitizeFilenames()
    updateSearchPath()
    buildFilePaths(filenameList, searchPath)
    hash_director()
    display_result()
    sendData()
    close_connection()

if connectionReady and (rescan == True):
    print("In rescan mode")
    receiveFileData()
    hash_director()
    display_result()
    sendData()
    close_connection()




"""
print(searchPath)
print(platform.system())
print(filenameList)
print(filename_path)
print(hashResult)

print(len(hashResult))
"""





