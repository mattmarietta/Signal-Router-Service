# Signal-Router-Service

## 1. Project Overview
I built a lightweight prototype that builds off of the drift detection logic from the first assignment. This new version takes that core "drift detection engine" and places it inside a  web service that acts like a  sorting office for a team's communication data.

Its main job is to take in different types of signals—like chat messages and stress-level data (HRV)—figure out what they are, and send them to the right specialist for analysis. This is done through files like the router and classification which will classify first and then route to the correct module. 

I designed it to be simple and flexible, with each part of the sorting process (identifying, routing, and analyzing) handled by its own separate module. This makes the whole system easy to understand and upgrade in the future. The application has a simple API, so other programs can easily send it data or check on the team's overall well-being. I used a simple client python file to show this and simulate the old script to see how it changes. Obviously, real-time AI would enhance this much further by replacing things such as the scoring engine, but could also plug in something such as AXIS.

---

## 2. System Architecture
The service follows the  architectural pattern, creating a clean and efficient data processing pipeline.

Signal Input → Classifier → Router → Drift Detector → Score + Log

Signal Input: The /ingest endpoint accepts a JSON object containing a user, optional text, and optional hrv.

Classifier: The SignalClassifier class inspects the input and assigns a tag (e.g., "mixed_signal", "text_only") to give to the router.

Router: The Router class takes this tag and returns a destination string (e.g., "drift_detector") for a simple approach.

Drift Detector: The DriftDetector class is a stateful module that maintains the conversation history. It processes the signal, calculates an individual drift score, and updates the overall system coherence score and signal tag. This was acquired from the previous module and mostly changed into classes.

Score + Log: The final, detailed JSON log is returned by the endpoint and stored in the detector's history.

---

## 3. API Endpoints
The service provides three core endpoints:

To test both the status and log endpoints, make sure that the main app is running, and then reload as it keeps running. It will show the state change and also the logs will update.

POST /ingest: The main endpoint for submitting new data. It accepts a JSON body with user, text, and hrv fields and returns a full analysis log.

GET /status: Returns a real-time snapshot of the system's health, including the current coherence_score and signal_tag.

GET /log: Dumps a JSON object containing the 10 most recent event logs processed by the system, useful for debugging and historical analysis.

---

## 5. How to Run & Test the Service
Prerequisites: Ensure Python 3, fastapi, uvicorn, and requests are installed.

Start the Server: In your first terminal, run the main service:

uvicorn main:app --reload

Run the Test Client: In a second terminal, run the test simulation script. This will send the pre-written conversation to your running service.

python test_client.py

Check Status: While the server is running, you can visit http://127.0.0.1:8000/status and http://127.0.0.1:8000/log in your browser to monitor the system's state.
