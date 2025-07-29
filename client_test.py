import requests
import json
import time
from data_simulator import generate_message_stream

#Set the URL of the service for the main endpoint
SERVICE_URL = "http://127.0.0.1:8000/ingest"

def run_test_simulation():
    #This will represent a simulation of the client sending data, acting as a stream of chats 
    print("*** Starting Test Client Simulation ***")
    print(f"Sending data to: {SERVICE_URL}\n")

    #Use the generator from data simulator to simulate the stream of messages
    for message in generate_message_stream():
        user = message["user"]
        text = message["text"]

        #Create a payload for the POST request, which will be repeated
        payload = {
            "user": user,
            "text": text
            #Not sending the HRV here because we can use our biometric function to simulate it for now
            #Could send HRV as well if needed for testing purposes
        }

        try:
            #Send the POST request to the service
            response = requests.post(SERVICE_URL, json=payload)
            response.raise_for_status() # Raise an exception for bad status codes

            #Print the detailed JSON log we recieved from the service
            print(f"*** Sent: '{text}' from '{user}' ***")
            print(f"*** Received Analysis from Service: ***")
            print(json.dumps(response.json(), indent=2))
            print("\n" + "="*50 + "\n")

        #Handle any request exceptions
        except requests.exceptions.RequestException as e:
            print(f"Error sending request: {e}")
            break
        
        #Wait for a short time to simulate a real-time conversation
        time.sleep(1) 

    print("*** Client Simulation Complete ***")

if __name__ == "__main__":
    run_test_simulation()
