import requests
import json


#Set the URL of the service for the main endpoint
#We will simulate request to this endpoint 
BASE_URL = "http://127.0.0.1:8000"

def test_ingest_endpoint():
    #Tests the /ingest endpoint by sending a valid mixed-signal payload.

    print("*** Testing POST /ingest endpoint ***")

    #Sample payload to send to the /ingest endpoint
    #This payload would be replaced in a real test with actual data and something that can keep the recursive logs
    test_payload = {
        "user_id": "user_test_0001",
        "session_id": "session_test_0001",
        "hrv_data": {
            "rmssd": 39.7,
            "sdnn": 51.2
        },
        "text_context": "I'm fine... I guess. It's just a lot of pressure right now.",
        "context_tag": "TEAM_RESTRUCTURING",
        "timestamp": "2025-07-31T17:45:00Z"
    }

    try:
        response = requests.post(f"{BASE_URL}/ingest", json=test_payload)
        
        #Check if the request was successful and if not print a failure message
        if response.status_code == 200:
            print("SUCCESS: /ingest endpoint returned status 200 OK.")
            print("Response JSON:")
            #Pretty-print the JSON response
            print(json.dumps(response.json(), indent=4))
        else:
            print(f"FAILURE: /ingest endpoint returned status {response.status_code}.")
            print("Response Text:", response.text)
            
    except requests.exceptions.ConnectionError as e:
        print(f"CONNECTION ERROR: Could not connect to the server at {BASE_URL}.")

def test_read_logs_endpoint():
    """
    Tests the /read_all_logs endpoint to verify that data is being
    saved and can be decrypted.
    """
    print("\n*** Testing GET /read_all_logs endpoint ***")
    
    #Use try and except to handle the connection and response similar to the ingest test
    try:
        response = requests.get(f"{BASE_URL}/logs")
        
        if response.status_code == 200:
            print("SUCCESS: /read_all_logs endpoint returned status 200 OK.")
            print("Decrypted Log History:")
            print(json.dumps(response.json(), indent=4))
        else:
            print(f"FAILURE: /read_all_logs endpoint returned status {response.status_code}.")
            print("Response Text:", response.text)

    except requests.exceptions.ConnectionError as e:
        print(f"CONNECTION ERROR: Could not connect to the server at {BASE_URL}.")

if __name__ == "__main__":
    # Run the ingest test first to create a log entry
    test_ingest_endpoint()
    
    #Then run the read test to verify the entry was saved
    test_read_logs_endpoint()
