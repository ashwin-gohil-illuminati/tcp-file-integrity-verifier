
from fastapi import APIRouter
from fastapi import Response, status, HTTPException, Depends
from ..database import get_db
from sqlalchemy.orm import Session
from .. import schemas, models, oauth2
from sqlalchemy import Integer, func

from typing import List
import subprocess
import socket


router = APIRouter(
    prefix="/hash",
    tags=['Hashing flow']
)
# "-x", "sh", "-c",

userID = ''
jobID = None

def launch():
    # pro line is not used
   #pro = subprocess.call(["bash",  "-x", "-c", "python /home/ashwin/Documents/HashProject/server/server1.py ; bash"])
    #subprocess.Popen(f"python /home/ashwin/Documents/FastAPI_AUTH_ORM/server/servermain.py {userID} {jobID}", shell=True)                      
     subprocess.Popen(f"python ./server/servermain.py {userID} {jobID}", shell=True)

 
@router.post("/connection", status_code=status.HTTP_200_OK, response_model=schemas.ConnectionInfo)
def get_connectionInfo(description: schemas.ConnectionDescription, db: Session = Depends(get_db), user_id: int = Depends(oauth2.get_current_user)):

    global jobID
    global userID
    webserverport:int = 8000
    databaseport:int = 5432
    apiserverport:int = 5000
    portToPush:int = None
    found:bool = False
    
    if description.jobid:
        checkjobid = db.query(models.HashData).filter(models.HashData.userid == user_id.id, models.HashData.jobid == description.jobid).first()
        if checkjobid is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Jobid does not exist for rescan")
        else:
            jobID = str(description.jobid)

    checkuser = db.query(models.Port).filter(models.Port.userid == user_id.id).first()
    if checkuser:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"Job in process")

    lastrow = db.query(models.Port).order_by(models.Port.portno.desc()).first()
        
    if not lastrow:
        portToPush = 3000
    elif lastrow:
        allports = db.query(models.Port.portno).all()
        allportsunpacked = [value for (value,) in allports]
        for i in [x for x in range(3000,65535) if x!= webserverport and x!= databaseport and x!= apiserverport]:
            if i not in allportsunpacked:
                found = True
                portToPush = i
                break
            if found:
                break
      
    print(user_id.id)
    userID = str(user_id.id)
    
    if portToPush == None:
        raise HTTPException(status_code=status.HTTP_226_IM_USED, detail=f"All ports occupied. Try after sometime")
    
    newport = models.Port(userid = user_id.id, portno = portToPush, jobdescription=description.jobdescription)
    db.add(newport)
    db.commit()
    db.refresh(newport)
    
    launch()

    ip = socket.gethostbyname(socket.gethostname())
    
    return {"ip": ip, "port": newport.portno, "instruction": "connect info", "note": "server waiting"}
    


#@router.get("/lastscan", status_code=status.HTTP_200_OK, response_model=List[schemas.ScanResult])
@router.get("/lastscan", status_code=status.HTTP_200_OK, response_model=List[schemas.ScanResult] )
def get_lastscan(db: Session = Depends(get_db), user_id: int = Depends(oauth2.get_current_user)):
    
    user = db.query(models.HashData).filter(models.HashData.userid == user_id.id).all()
    
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"No scan submitted by user")
    elif user:
       
        subqry = db.query(func.max(models.HashData.jobid)).filter(models.HashData.userid == user_id.id).scalar()
        returnqry = db.query(models.HashData).filter(models.HashData.jobid==subqry,models.HashData.userid==user_id.id).all()
          
        return returnqry
        

#@router.get("/lastrescan", status_code=status.HTTP_200_OK, response_model=List[schemas.RescanResult])
@router.get("/lastrescan", status_code=status.HTTP_200_OK, response_model=List[schemas.RescanResult])
def get_lastrescan(db: Session = Depends(get_db), user_id: int = Depends(oauth2.get_current_user)):

    user = db.query(models.HashDataRescan).filter(models.HashDataRescan.userid == user_id.id).first()

    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"No Rescan done by user")
    elif user:
        maxtimestamp = db.query(func.max(models.HashDataRescan.created_at)).filter(models.HashDataRescan.userid == user_id.id).scalar()
        
        maxtimerow = db.query(models.HashDataRescan).filter(models.HashDataRescan.created_at == maxtimestamp).first()
        latestjobid = maxtimerow.jobid

        rescanByJobid = db.query(models.HashDataRescan).filter(models.HashDataRescan.jobid == latestjobid, models.HashDataRescan.userid == user_id.id).all()
        return rescanByJobid


@router.get("/scanjobs", status_code=status.HTTP_200_OK, response_model=List[schemas.ScanJobs])
def get_jobs(db: Session = Depends(get_db), user_id: int = Depends(oauth2.get_current_user)):

    jobids = db.query(models.HashData).distinct(models.HashData.jobid).filter(models.HashData.userid == user_id.id).all()
    
    if not jobids:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"No scan submitted by user")

    return jobids


@router.get("/rescanjobs", status_code=status.HTTP_200_OK, response_model=List[schemas.ScanJobs])
def get_rescanjobs(db: Session = Depends(get_db), user_id: int = Depends(oauth2.get_current_user)):
    
    jobids = db.query(models.HashDataRescan).distinct(models.HashDataRescan.jobid).filter(models.HashDataRescan.userid == user_id.id).all()
    
    if not jobids:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"No Rescan submitted by user")
    
    return jobids


@router.get("/scans/{jobID}", status_code=status.HTTP_200_OK, response_model=List[schemas.ScanResult])
def getscanjob(jobID: int, db: Session = Depends(get_db), user_id: int = Depends(oauth2.get_current_user)):

    scanjob = db.query(models.HashData).filter(models.HashData.userid == user_id.id, models.HashData.jobid == jobID).all()
    
    if not scanjob:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"No scanjob by jobid = {jobID}")
    
    return scanjob

@router.get("/rescans/{jobID}", status_code=status.HTTP_200_OK, response_model=List[schemas.RescanResult])
def getrescanjob(jobID: int, db: Session = Depends(get_db), user_id: int = Depends(oauth2.get_current_user)):

    rescanjob = db.query(models.HashDataRescan).filter(models.HashDataRescan.userid == user_id.id,
                                                models.HashDataRescan.jobid == jobID).all()
    
    if not rescanjob:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"No Rescanjob by jobid = {jobID}")

    return rescanjob


@router.delete("/deletescanjobs", status_code=status.HTTP_204_NO_CONTENT)
def deleteScanJobs(joblist: List[schemas.DeleteScanJobs], db: Session = Depends(get_db), user_id: int = Depends(oauth2.get_current_user)):
   
    for job in joblist:
        foundscan_query = db.query(models.HashData).filter(models.HashData.userid == user_id.id,
                                                     models.HashData.jobid == job.jobid)

        foundrescan_query = db.query(models.HashDataRescan).filter(models.HashDataRescan.userid == user_id.id,
                                                     models.HashDataRescan.jobid == job.jobid)
        
        foundscan = foundscan_query.all()
        foundrescan = foundrescan_query.all()

        if foundscan:
            foundscan_query.delete(synchronize_session=False)
            db.commit()
            if foundrescan:
                foundrescan_query.delete(synchronize_session=False)
                db.commit()

    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.delete("/deleterescanjobs", status_code=status.HTTP_204_NO_CONTENT)
def deleteReScanJobs(joblist: List[schemas.DeleteScanJobs], db: Session = Depends(get_db), user_id: int = Depends(oauth2.get_current_user)):

    notfoundjobid = []

    for job in joblist:
        foundrescan_query = db.query(models.HashDataRescan).filter(models.HashDataRescan.userid == user_id.id,
                                                     models.HashDataRescan.jobid == job.jobid)
        foundrescan = foundrescan_query.all()

        if foundrescan:
            foundrescan_query.delete(synchronize_session=False)
            db.commit()
        else:
            notfoundjobid.append(job.jobid)
    
    if notfoundjobid:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"JobID - {notfoundjobid} were not found")

    return Response(status_code=status.HTTP_204_NO_CONTENT)
    

