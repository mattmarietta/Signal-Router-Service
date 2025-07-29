#Import libraries and modules needed for the application
from classifier import SignalClassifier
from router import Router
from drift_detector import DriftDetector
from biometric import get_hrv

from fastapi import FastAPI
from pydantic import BaseModel
from typing import Optional

#Sample data model that we will need for our /ingest endpoint
class SignalData(BaseModel):
    user: str
    #Optional field for the text as well
    text: Optional[str] = None 
    #Optional field for the HRV being input
    hrv: Optional[int] = None 

#Make an instance of the application
app = FastAPI()

#Make instances of the classifier, router, and drift detector to use
classifier = SignalClassifier()
router = Router()
drift_detector = DriftDetector()

#Display a simple message when root endpoint is accessed
@app.get("/")
def read_root():
    return {"message": "Signal Router is online."}


@app.post("/ingest")
def signal_ingest(data: SignalData):
    #Classify the signal and then route to destination later
    tag = classifier.classify(data) 
    destination = router.route(tag)


    if destination == "drift_detector":
        if data.hrv is None:
            #Simulate the HRV if not provided by the user
            base_score, _ = drift_detector._base_score_message(data.text or "")
            data.hrv = get_hrv(base_score)
        
        #The process method will return the complete JSON log
        result_log = drift_detector.process(data)
        return result_log
    else:
        #Handle other destinations like the storage or error message
        return {"status": "logged", "destination": destination}

@app.get("/status")
#Returns current coherence score, use the signal tag and score to determine the state
def status():
    return { "coherence_score": drift_detector.coherence_score, "signal_tag": drift_detector.signal_tag}


@app.get("/log")
#Dumps the current log
def log():
    #Return the last 10 logs from the history
    return {"logs": drift_detector.log_history[-10:]}
