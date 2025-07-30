# Signal-Router-Service

## 1. Project Overview
I built a lightweight prototype that builds off of the drift detection logic from the first assignment. This new version takes that core "drift detection engine" and places it inside a  web service that acts like a  sorting office for a team's communication data.

Its main job is to take in different types of signals—like chat messages and stress-level data (HRV)—figure out what they are, and send them to the right specialist for analysis. This is done through files like the router and classification which will classify first and then route to the correct module. 

I designed it to be simple and flexible, with each part of the sorting process (identifying, routing, and analyzing) handled by its own separate module. This makes the whole system easy to understand and upgrade in the future. The application has a simple API, so other programs can easily send it data or check on the team's overall well-being. I used a simple client python file to show this and simulate the old script to see how it changes. Obviously, real-time AI would enhance this much further by replacing things such as the scoring engine, but could also plug in something such as AXIS.

---

## 2. System Architecture

The pipeline is structured as follows:

 ```text
[ Signal Input ] -> [ Classifier ] -> [ Router ] -> [ Drift Detector ] -> [ Score + Log ]
   (FastAPI)         (Tags data)        (Routes)       (Analyzes & Stores State) 
```

### Components

- **Signal Input**  
  `/ingest` endpoint accepts JSON with a `user`, optional `text`, and optional `hrv`.

- **Classifier**  
  `SignalClassifier` analyzes inputs and assigns tags like `"text_only"`, `"hrv_only"`, or `"mixed_signal"`.

- **Router**  
  `Router` uses the tag to route data to the appropriate module (e.g., `"drift_detector"`).

- **Drift Detector**  
  Stateful `DriftDetector` tracks conversation history, calculates drift, and updates a coherence score.

- **Score + Log**  
  Returns a JSON log containing results, which is stored internally for future reference.

---

## 3. API Endpoints
The service provides three core endpoints:

To test both the status and log endpoints, make sure that the main app is running, and then reload as it keeps running. It will show the state change and also the logs will update.

POST /ingest: The main endpoint for submitting new data. It accepts a JSON body with user, text, and hrv fields and returns a full analysis log.

GET /status: Returns a real-time snapshot of the system's health, including the current coherence_score and signal_tag.

GET /log: Dumps a JSON object containing the 10 most recent event logs processed by the system, useful for debugging and historical analysis.


---

## 4. State Persistence
To maintain context across restarts, the DriftDetector saves and loads state automatically.

File: detect_state.json

Saved: After every processed message

Loaded: On startup if the file exists

This prevents loss of conversation history between sessions.

---
## 5. Example Log Output
```text
{
  "timestamp": "2025-07-30T12:24:15.123456",
  "user": "Sara",
  "text": "Whatever. I'll believe it when I see the pull request.",
  "hrv": 42,
  "individual_drift_score": 1.0,
  "reason": "Dismissive tone, can be rude to colleagues. (Sudden Negative Shift)",
  "system_coherence_score": 0.46,
  "system_signal_tag": "critical_drift"
}
```
---
## 6. Future Integrations

Plugging in AXIS: An agent like AXIS, which likely specializes in physiological data, would be integrated by adding a new rule to the Router. When the Classifier tags a signal as "physiological_only", the Router would forward that data to the AXIS agent instead of the Drift Detector. This ensures that each specialist agent only receives the data relevant to its function. No other data would be necessary because that could confuse the agent and not give us the result that we are looking for.

Drift Detector:  The DriftDetector itself is a swappable component. A more advanced scoring engine, such as a fine-tuned AI model, could be built as a new class. As long as it has a .process() method, it could be dropped in to replace the current rule-based detector without changing the rest of the application's architecture.


---

## 7. How to Run & Test the Service
Prerequisites: Ensure Python 3, fastapi, uvicorn, and requests are installed.

`pip install fastapi "uvicorn[standard]" requests`

Start the Server: In your first terminal, run the main service:

`uvicorn main:app --reload`

Run the Test Client: In a second terminal, run the test simulation script. This will send the pre-written conversation to your running service.

`python test_client.py`

Check Status: While the server is running, you can visit http://127.0.0.1:8000/status and http://127.0.0.1:8000/log in your browser to monitor the system's state.
