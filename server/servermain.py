from fileinput import filename
from socket import *
import os, sys
from subprocess import check_output
from signal import SIGKILL, signal
import multiprocessing, time



#from pydantic import FilePath
from sqlalchemy import func

#sys.path.append(r'/home/ashwin/Documents/FastAPI_AUTH_ORM/server/')
sys.path.append(r'./server/')

import serverdatabase, servermodels

userid = ''
myHost = ''
myPort = 50040
acceptconfirm = b'connection established'
clientACK = b'ping'
connecttruth = True
toPushData = []
jobID = ''
toSendData = [] #earlier dict
rescan:bool = False

if len(sys.argv) == 3:
    userid = (sys.argv[1])
    jobID = sys.argv[2]
else:
    print("Insufficient parameters for the job")

print('userid:', userid)
print('jobid:', jobID)

if jobID == 'None':
    rescan = False
else:
    rescan = True


def populateDataToSend():
    global toSendData
    jobidlist = serverdatabase.session.query(servermodels.HashData).filter(servermodels.HashData.userid == int(userid),
                                             servermodels.HashData.jobid == int(jobID)).all()
       
    for i in range(0, len(jobidlist)):        
            tempdic = {}
            tempdic = {jobidlist[i].filename: jobidlist[i].filepath}
            toSendData.append(tempdic)
    

def getPort():
    global userid
    global myPort

    userrow = serverdatabase.session.query(servermodels.Port).filter(servermodels.Port.userid == int(userid)).first()
    if userrow:
        myPort = userrow.portno
    else:
        print("job time expired or user has not connected with connection info")

getPort()

print('myPort', myPort)
print('rescan state', rescan)

if rescan == True:
    populateDataToSend()
    print('dic:', toSendData)


sockobj = socket(AF_INET, SOCK_STREAM)
try:
    sockobj.bind((myHost,myPort))
    
except: # socket.error as msg: this does not work
    #print('bind failed. Error code: ' + str(msg[0])+ 'Message ' + msg[1])
    print('error in binding')
    
sockobj.listen(1)





def datafetch():
    global connecttruth
    global toPushData
    global toSendData

    while True:
        
        if connecttruth == False:
            connection.close()
            break

        print('waiting for connection....')
        connection, address = sockobj.accept()
        print('Server connected by', address)

                     
        while True:
            data = connection.recv(3072)
            if data == clientACK:
                connection.send(acceptconfirm)
                if rescan:
                    strdata = str(toSendData)
                    strdata = strdata.encode()
                    connection.send(strdata)
            elif data:
                if rescan:
                    data = data.decode('utf-8')
                    data = eval(data)
                    toPushData = data
                    print(data) 
                    pushDataRescan()                
                else:
                    data = data.decode('utf-8')
                    data = eval(data)
                    toPushData = data
                    print(toPushData)
                    pushData()
            if not data:
                print('no data')
                connecttruth = False
                
                #pid = os.getpid()
                #os.kill(pid, SIGKILL) # this works
                #os.system("kill {0}".format(pid)) # this does not close

                # below 2 lines closed the terminal 
                #p = check_output(["pidof","-s","bash"])
                #os.kill(int(p), SIGKILL)                
                break
       
    return
    

def deletePortRow():
    global userid
    delrow = serverdatabase.session.query(servermodels.Port).filter(servermodels.Port.userid == int(userid)).first()
    serverdatabase.session.delete(delrow)
    serverdatabase.session.commit()

def pushData():
    global userid
    jobid = 0
    jobdescription = ''

    currentuser = serverdatabase.session.query(servermodels.HashData).filter(servermodels.HashData.userid == int(userid)).all()
    currentportuser = serverdatabase.session.query(servermodels.Port).filter(servermodels.Port.userid == int(userid)).first()
    jobdescription = currentportuser.jobdescription

    if not currentuser:
        jobid = 1

        for i in range(0, len(toPushData)):
            listrow = servermodels.HashData(userid = int(userid), filename = toPushData[i][0], filepath = toPushData[i][1],
                                            hash = toPushData[i][2], jobid = jobid, jobdescription=jobdescription)
            serverdatabase.session.add(listrow)
            serverdatabase.session.commit()
    elif currentuser:
        datamaxid = serverdatabase.session.query(func.max(servermodels.HashData.jobid)).filter(servermodels.HashData.userid == int(userid)).scalar()
        
        jobid = datamaxid + 1
        print('jobid found is ', jobid)
        print('len of pushdata', len(toPushData))
        print(toPushData[0][0], toPushData[0][1], toPushData[0][2])
        for i in range(0, len(toPushData)):
            listrow = servermodels.HashData(userid = int(userid), filename = toPushData[i][0], filepath = toPushData[i][1],
                                            hash = toPushData[i][2], jobid = jobid, jobdescription=jobdescription)
            serverdatabase.session.add(listrow)
            serverdatabase.session.commit()

    print(len(toPushData))


def pushDataRescan():
    global userid
    global jobID
    altered = False

    currentportuser = serverdatabase.session.query(servermodels.Port).filter(servermodels.Port.userid == int(userid)).first()
    userrescan = serverdatabase.session.query(servermodels.HashDataRescan).filter(servermodels.HashDataRescan.userid == int(userid), servermodels.HashDataRescan.jobid == int(jobID)).first()
    if not userrescan:
        oldscanresult = serverdatabase.session.query(servermodels.HashData).filter(servermodels.HashData.userid == int(userid), servermodels.HashData.jobid == int(jobID)).all()
        for i in range(0, len(toPushData)):
            if oldscanresult[i].hash == toPushData[i][2]:
                altered = False
            else:
                altered = True

            pushrescan = servermodels.HashDataRescan(userid = int(userid), filename = oldscanresult[i].filename, filepath = oldscanresult[i].filepath,
                                                      hash = oldscanresult[i].hash, latesthash = toPushData[i][2], altered = altered,
                                                       jobid = int(jobID), jobdescription = currentportuser.jobdescription)
            serverdatabase.session.add(pushrescan)
            serverdatabase.session.commit()
    else:
        oldrescanresult = serverdatabase.session.query(servermodels.HashDataRescan).filter(servermodels.HashDataRescan.userid == int(userid), servermodels.HashDataRescan.jobid == int(jobID)).all()
        for i in range(0,len(toPushData)):
            if oldrescanresult[i].latesthash ==  toPushData[i][2]:
                altered = False
            else:
                altered = True

            eachrow = serverdatabase.session.query(servermodels.HashDataRescan).filter(servermodels.HashDataRescan.userid == int(userid),
                                                                                         servermodels.HashDataRescan.jobid == int(jobID),
                                                                                         servermodels.HashDataRescan.filename == toPushData[i][0],
                                                                                         servermodels.HashDataRescan.filepath == toPushData[i][1])
            eachrow.update({servermodels.HashDataRescan.hash: servermodels.HashDataRescan.latesthash,
                            servermodels.HashDataRescan.latesthash: toPushData[i][2],
                            servermodels.HashDataRescan.altered: altered,
                            servermodels.HashDataRescan.jobdescription:currentportuser.jobdescription
                            }, synchronize_session=False)     
            serverdatabase.session.commit()


p = multiprocessing.Process(target=datafetch, name="Datafetch")
p.start()
time.sleep(300)
p.terminate()
p.join()


deletePortRow()

print("Server closed")