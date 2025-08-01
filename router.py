#Depending on what signal it is, we will route it to the correct module

from axis_agent_stub import AxisAgentStub
from typing import Dict


#If it is a mixed_signal or emotional_signal, we will route it to the drift detector to be analyzed
#If it is a physiological_signal, we will route it to the drift detector and only HRV, lets route it for now

axis = AxisAgentStub()

def route_to_axis(payload: Dict) -> Dict:
    print("Router: Routing payload to AXIS for analysis")
    #Used logic from the requirements to route the payload to AXIS
    #Mock stub, real application would have more complex logic
    analysis_result = axis.analyze(payload)
    return analysis_result
        