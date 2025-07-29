#This file will classify the signals and then give them to the router to direct where they need to go

class SignalClassifier:
    def classify(self, data):

        #We need to classify the data as emotional, physiological, or cognitive
        
        #If we have both text and HRV, we classify it as a mixed_signal
        if (data.text and data.hrv is not None):
            return "mixed_signal"

        #If we have text, we classify it as a emotional_signal
        elif (data.text):
            return "emotional_signal"
        
        #If we have HRV, we classify it as a physiological_signal
        elif (data.hrv is not None):
            return "physiological_signal"
        
        #If we have nothing, we classify it as a invalid_signal
        else:
            return "invalid_signal"