import importlib
from ml_abc import LogicModel, MLModel

class ModelManager(object):
    _models = []

    @classmethod
    def load_models(cls, configuration):
        for c in configuration:
            model_module = importlib.import_module(c["module_name"])
            model_class = getattr(model_module, c["class_name"])
            model_object = model_class()

            # saving the model reference to the models list
            cls._models.append(model_object)
    
    @classmethod
    def get_models(cls):
        """Get a list of models in the model manager instance."""
        model_objects = [{
            "display_name": model.display_name,
            "qualified_name": model.qualified_name
        } for model in cls._models]

        return model_objects
    
    @classmethod
    def get_model(cls, qualified_name):
        """Get a model object by qualified name."""
        # searching the list of model objects to find the one with the right qualified name
        model_objects = [model for model in cls._models if model.qualified_name == qualified_name]

        if len(model_objects) == 0:
            return None
        else:
            return model_objects[0]

