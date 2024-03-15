import sys
import os
import pickle
#import numpy as np
import datetime
import dill as pickle

script_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(script_dir)
sys.path.append(parent_dir)

from ml_abc import MLModel
from nlr import __display_name__, __qualified_name__

class NLRegression(MLModel):

    display_name = __display_name__
    qualified_name = __qualified_name__

    def __init__(self):
        try:
            dir_path = os.path.dirname(os.path.realpath(__file__))
            file = open(os.path.join(dir_path, "nlr_model.pickle"), 'rb')
            self._nlreg = pickle.load(file)
            file.close()
        except Exception as e:
            return {e}

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
        #extract coefficients and function
        try: 
            coefficients = self._nlreg['coefficients']
            nlr_func = self._nlreg['function']

            irradiation = float(data.get("IRRADIATION"))
            temperature = float(data.get("MODULE_TEMPERATURE"))
            pred = nlr_func((irradiation, temperature), *coefficients)
            pred_int = float(pred)
            residual = abs(pred_int - float(data.get("DC_POWER")))

            limit_fault = 4000
            if residual > limit_fault:
                if float(data.get("DC_POWER")) == 0:
                    return {"alert": "FAULT"}
                else:
                    return {"alert": "ATTENTION"}
            else:
                return {"alert": "NORMAL"}
        except Exception as e:
            return {e}
