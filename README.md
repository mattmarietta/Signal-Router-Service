# Signal-Router-Service

## 1. Project Overview
This project is the final submission for the Coherence Protocol work trial. It implements a robust FastAPI service designed to process mixed signals (chat, HRV, context), integrate with the AXIS agent stub, and log events to a secure, encrypted, recursive history store.

---

## 2. System Architecture

The pipeline is structured as follows:

 ```text
[ API Input ] -> [ Router Module ] -> [ AXIS Agent ] -> [ History Storage ] -> [ Encrypted Log ]
  (FastAPI)      (Routes to Agent)    (Analyzes)       (Formats & Encrypts)      (history_store.json)
```

### Components

- **Signal Input**  
  `/ingest` endpoint accepts a complex JSON payload containing `user`, `session_id`, `text`, `hrv`, and a `context_tag`.

- **Router**  
  `Router` module acts as the central integration point. It routes incoming signals to the correct agent stub (currently AXIS).

- **AXIS Agent Stub**  
  `AXISAgentStub` simulates emotional/contextual analysis and returns an artificial context_state with score and interpretation.

- **Recursive Logging**  
  The output from the agent is used to create a structured, recursive log entry capturing conversation and biometric context over time.

- **Encrypted History Storage**  
  The `HistoryStorage` module encrypts and stores each log entry persistently in `history_store.json.encrypted`.

---

## 3. API Endpoints
The service provides three core endpoints:

- **POST `/ingest`**  
  The main endpoint for submitting new data. It accepts a JSON body with all required signal fields and returns a confirmation with the AXIS analysis.

- **GET `/status`**  
  Returns the `context_state` from the most recent log entry, providing a snapshot of the latest analysis and coherence score.

- **GET `/log`**  
  Returns the full decrypted log history for debugging and timeline reconstruction.


---

## 4. State Persistence

The recursive nature of the log makes state persistence implicit. Each log entry builds on prior data, enabling historical reconstruction of signal evolution.

- **File:** `history_store.json.encrypted`  
- **Format:** Encrypted JSON list of structured context entries  
- **Decryption:** Performed by the `HistoryStorage` module using a persistent key stored in `secret.key`

---
## 5. Example Log Output
```json
{
  "timestamp": "2025-07-30T12:24:15.123456",
  "user": "Sara",
  "session_id": "abc123",
  "text": "Whatever. I'll believe it when I see the pull request.",
  "hrv": 42,
  "context_tag": "mixed_signal",
  "context_state": {
    "score": 0.91,
    "notes": "Dismissive tone with physiological stress indicators"
  }
}
```
---
## 6. Key Files

`main.py`
Core FastAPI application defining routes and request orchestration.

`router.py`
Central integration logic, routing classified signals to agent modules.

`axis_agent_stub.py`
Mock agent that simulates emotional/contextual analysis.

`history_storage.py`
Appends, encrypts, and decrypts recursive conversation history logs.

`security_utils.py`
Provides AES-based encryption and persistent key management via secret.key.

`test_client.py`
Simulates client-side behavior to verify all endpoints and system integrity.

---

## 7. How to Run & Test the Service
Prerequisites: Ensure Python 3, fastapi, uvicorn, and requests are installed.

`pip install fastapi "uvicorn[standard]" requests`

Start the Server: In your first terminal, run the main service:

`uvicorn main:app --reload`

Run the Test Client: In a second terminal, run the test simulation script. This will send the pre-written conversation to your running service.

`python test_client.py`

This python test script will:

-Submit a POST request to /ingest

-Print the AXIS analysis returned

-Query /status and /log to confirm recursive state and successful log encryption
