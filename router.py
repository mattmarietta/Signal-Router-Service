
#Router will route the classified signals from classifier to the appropriate destination

#Depending on what signal it is, we will route it to the correct module
#If it is a mixed_signal or emotional_signal, we will route it to the drift to be analyzed
#If it is a physiological_signal, we will route it to the drift detector and only HRV, lets route it for now
class Router:
    def route(self, tag: str) -> str:
        if tag in ["mixed_signal", "emotional_signal"]:
            return "drift_detector"
        elif tag == "physiological_signal":
            return "history_storage"
        #Return an error message for now if the tag is invalid
        else:
            return "error_message"
        