import os
from data_simulator import scripted_conversation
import datetime
import json

#File will detect drift from a prewritten script from our previous module
class DriftDetector:
    def __init__(self):
        #Drift detector is now class based so we need to initialize it with the correct parameters and variables.

        #Save the state to a file so that we can keep track of the memory over time
        self.STATE_FILE = "detect_state.json"


        all_users = set(message["user"] for message in scripted_conversation)
        self.user_states = {user: {"recent_scores": [], "last_score": 0.0} for user in all_users}
        self.WINDOW_SIZE = 5
        self.TRUST_DECAY_THRESHOLD = 0.5

        #New tags for the score, signal currently, and log history
        self.coherence_score = 1.0
        self.signal_tag = "stable_signal"
        self.log_history = []

        
        #Scoring rules are apart of the class now
        self.DRIFT_SIGNALS = {
            "a 'snag'?": (0.62, "Sarcastic questioning; challenges a colleague's statement."),
            "just circling back": (0.61, "Passive-aggressive follow-up; implies lateness."),
            "per my last message": (0.7, "Passive-aggressive; implies 'you didn't read my message'."),
            "noted.": (0.53, "Dismissive acknowledgement."),
            "making progress": (0.3, "Ambiguous update, not very informative."),
            "maybe": (0.4, "Hesitant language, indicates uncertainty."),
            "i thought": (0.72, "Potential contradiction or blame-shifting."),
            "actually": (0.54, "Corrective/Contradictory statement."),
            "it's fine": (0.66, "Passive-aggressive tone."),
            "whatever": (0.84, "Dismissive tone, can be rude to colleagues."),
            "i guess": (0.4, "Reluctance or lack of buy-in to the conversation."),
            "swamped": (0.5, "Avoiding responsibility in some cases."),
            "must be nice": (0.93, "High passive-aggressive tone detected."),
            "you know what": (0.85, "Defensive and confrontational."),
            "sure, whatever": (0.90, "Dismissive and confrontational."),
        }

    def save_state(self):
    #Save current user states and a log history to a JSON file
        state = {
            "user_states": self.user_states,
            "log_history": self.log_history,
        }
        with open(self.STATE_FILE, 'w') as f:
            json.dump(state, f, indent=4)

    def load_state(self):
        #This will load the state from the JSON file if it exists
        if os.path.exists(self.STATE_FILE):
            with open(self.STATE_FILE, 'r') as f:
                state = json.load(f)
                self.user_states = state.get("user_states", {})
                self.log_history = state.get("log_history", [])


    def _base_score_message(self, text):
        #Score a basic message based on the drift signals defined above

        #Lower the text to make matching case-insensitive
        text_lower = text.lower()

        for signal, (score, description) in self.DRIFT_SIGNALS.items():
            if signal in text_lower:
                #Need to return the signal score and description
                return score, description
                
        #If no drift signals are found then we will return a score of 0.0
        return 0.0, "No drift detected"
    

    def _context_score_message(self, current_text, last_score, synthetic_hrv):
        """A private helper method for the advanced, context-aware scoring."""
        current_score, reason = self._base_score_message(current_text)

        if current_score > 0.5 and last_score > 0.5:
            #Boost the score for repeated negative pattern and make sure it doesn't exceed 1.0
            current_score = min(1.0, current_score + 0.1)
            reason += " (Pattern of Negative Behavior from this user)"

        is_sudden_shift = last_score < 0.2 and current_score > 0.7
        if is_sudden_shift:
            #For simplicity, if there is a sudden shift, we will set the score to 1.0
            current_score = 1.0
            reason += " (Sudden Negative Shift)"


        #If the message is already negative and the synthetic HRV is low, this is a stronger signal of drift
        if current_score > 0.4 and synthetic_hrv < 40:
            current_score = min(1.0, current_score + 0.1)
            reason += " (Affected by Low HRV)"


        #Return final score and reason
        return round(current_score, 2), reason
    
    def _update_system_coherence(self):
        highest_avg_score = 0
        for user_state in self.user_states.values():
            if len(user_state["recent_scores"]) == self.WINDOW_SIZE:
                avg_score = sum(user_state["recent_scores"]) / self.WINDOW_SIZE
                if avg_score > highest_avg_score:
                    highest_avg_score = avg_score
        
        # Coherence is the inverse of drift
        self.coherence_score = round(1.0 - highest_avg_score, 2)

        # Determine the signal tag based on the coherence score
        if self.coherence_score < 0.5:
            self.signal_tag = "critical_drift"
        elif self.coherence_score < 0.8:
            self.signal_tag = "rising_stress"
        else:
            self.signal_tag = "stable"

    def process(self, data):
        #This is the main public method and it will be called to process the incoming data
        #Very similar to the main program file in the other implementation of the signal drift
        user = data.user
        text = data.text
        hrv = data.hrv

        #Retrieve the state for the user
        user_state = self.user_states[user]
        
        #Score the message using the scoring methods we had defined earlier
        drift_score, reason = self._context_score_message(text, user_state["last_score"], hrv)
        
        #Update the user's sliding window of recent scores
        user_state["recent_scores"].append(drift_score)
        if len(user_state["recent_scores"]) > self.WINDOW_SIZE:
            user_state["recent_scores"].pop(0)

        #Update the user's last score for the next iteration
        user_state["last_score"] = drift_score

        #Update the system coherence score based on all users' states
        self._update_system_coherence()
        
        #Assemble the final result for this message
        json_log = {
            "timestamp": datetime.datetime.now().isoformat(),
            "user": user,
            "text": text,
            "hrv": hrv,
            "individual_drift_score": drift_score,
            "reason": reason,
            "system_coherence_score": self.coherence_score,
            "system_signal_tag": self.signal_tag
        }

        
        #Finally store the log in the history
        self.log_history.append(json_log)
        
        #Save the state to the file
        self.save_state()

        return json_log