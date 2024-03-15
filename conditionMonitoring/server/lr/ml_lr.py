import sys
import os
import pickle
import numpy as np
import datetime

script_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(script_dir)
sys.path.append(parent_dir)

from ml_abc import MLModel
from lr import __display_name__, __qualified_name__

class LRegression(MLModel):

    display_name = __display_name__
    qualified_name = __qualified_name__

    def __init__(self):
        dir_path = os.path.dirname(os.path.realpath(__file__))
        file = open(os.path.join(dir_path, "lr_model.pickle"), 'rb')
        self._reg = pickle.load(file)
        file.close()

    def input_schema(self):
        # Implement the input schema logic
        pass

    def validate_input(self, data):
        # Implement input validation logic
        pass

    def output_schema(self):
        """ Define the output schema for the status check """
        return {'alert': str}

    def predict(self,data):
        irradiation = np.array(data.get("IRRADIATION"), dtype=np.float64).reshape(-1, 1)
        pred = self._reg.predict(irradiation)
        pred_int = float(pred[0])
        residual = abs(pred_int - float(data.get("DC_POWER")))

        limit_fault = 4000
        if residual > limit_fault:
            if float(data.get("DC_POWER")) == 0:
                return {"alert": "FAULT"}
            else:
                return {"alert": "ATTENTION"}
        else:
            return {"alert": "NORMAL"}

    
    


