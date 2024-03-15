import sys
import os
from numpy import array
import datetime

script_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(script_dir)
sys.path.append(parent_dir)

from ml_abc import LogicModel, ModelException
from threshold import __display_name__, __qualified_name__

class Threshold(LogicModel):

    # accessing the package metadata
    display_name = __display_name__
    qualified_name = __qualified_name__

    def input_schema(self):
        # Implement the input schema logic
        pass

    def validate_input(self, data):
        # Implement input validation logic
        pass

    def output_schema(self):
        """ Define the output schema for the status check """
        return {'alert': str}

    def __init__(self):
        """ Initialization method """
        pass  # No initialization needed for this logic-based model

    def predict(self, data):
        """ Method to predict status based on time and DC power """
        time_value = datetime.datetime.strptime(data.get("TIME"), '%H:%M:%S').time() if data.get("TIME") else None
        dc_power_value = float(data.get("DC_POWER")) if data.get("DC_POWER") else None

        if time_value is None or dc_power_value is None:
            return {"alert": "ERROR"}

        start = datetime.time(6, 30, 0)  # sunrise
        end = datetime.time(17, 30, 0)  # sunset

        def time_in_range(start, end, x):
            """Return true if x is in the range [start, end]"""
            if start <= end:
                return start <= x <= end
            else:
                return start <= x or x <= end

        if time_in_range(start, end, time_value) and dc_power_value == 0:
            return {"alert": "FAULT"}
        else:
            return {"alert": "NORMAL"}
