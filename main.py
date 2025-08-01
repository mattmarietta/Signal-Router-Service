from fastapi import FastAPI
from pydantic import BaseModel
from typing import Dict, List
import random

#New imports
from router import route_to_axis
from history_storage import HistoryStorage

#Make an instance of the application along with the history storage
app = FastAPI()
history = HistoryStorage()

#New model for input data and to validate it
class IngestPayload(BaseModel):
    user_id: str
    session_id: str
    hrv_data: Dict[str, float]
    text_context: str
    context_tag: str
    timestamp: str 

#Display a simple message when root endpoint is accessed
@app.get("/")
def read_root():
    return {"message": "Signal Router is online."}


@app.post("/ingest")
def process_signal(data: IngestPayload):
    #Updated endpoint: Receives mixed signals, analysis from AXIS, assembles recursive log, saves the encrypted log, returns result to user
    
    #Prepare the data for processing using the AXIS hook
    #We will only select the fields that the AXIS stub expects
    axis_data = data.model_dump(include={'user_id', 'hrv_data', 'text_context', 'timestamp'})
    axis_result = route_to_axis(axis_data)

    #Assemble the recursive log entry by using the exact structure that we want to save

    log_entry = {
        "session_id": data.session_id,
        "context_state": {
            "last_score": axis_result["axis_score"],
            "recursion_patterns": axis_result["recursion_flags"],
            "history_depth": random.randint(1, 5),  # Simulated depth
        },
        "signals": [
            {
                "timestamp": data.timestamp,
                "type": "chat",
                "content": data.text_context,
                "hrv": data.hrv_data,
                "context": data.context_tag
            }
        ]
    }

    #Use our history module to write the log entry
    history.write_log(log_entry)

    #Return a simple useful response to confirm what happened
    return {
        "status": "logged",
        "axis_result": axis_result,
        "log_status": f"Session {data.session_id} logged and encrypted successfully.",
    }

#To test both the endpoints of status and log, make sure the application is running and then access the endpoints while it is running
@app.get("/status")
#Returns current coherence score, use the signal tag and score to determine the state
def status():
    #Simple return for score and the signal tag
    last_log = history.get_last_log()
    if not last_log:
        return {"status": "no_logs_found"}
    
    #If successful, return the last log's context state
    return {"latest_context_state": last_log.get("context_state", {})}

#Change old endpoint to use our history storage to retrieve logs
@app.get("/logs")
#Dumps the current log
def get_log(): 
    #Returns the entire decrypted log history
    return {"logs": history.get_all_logs()}
