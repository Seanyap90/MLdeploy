from abc import ABC, abstractmethod

class Model(ABC):
    """ An abstract base class for models, encompassing both logic and ML models """

    @property
    @abstractmethod
    def display_name(self):
        """ This abstract property returns a display name for the model.

        .. note::
            This is a name for the model that looks good in user interfaces.

        """
        raise NotImplementedError()

    @property
    @abstractmethod
    def qualified_name(self):
        """ This abstract property returns the qualified name of the model.

        .. note::
            A qualified name is an unambiguous identifier for the model. It should be possible to embed it in an URL.

        """
        raise NotImplementedError()

    @property
    @abstractmethod
    def input_schema(self):
        """ Abstract method to define output schema for logic-based models """
        pass

    @abstractmethod
    def predict(self, *args, **kwargs):
        """ Abstract method for making predictions """
        pass

    @abstractmethod
    def validate_input(self, data):
        """ Abstract method to validate input data """
        pass

class LogicModel(Model):
    """ An abstract base class for logic-based models """

    @property
    @abstractmethod
    def output_schema(self):
        """ Abstract method to define output schema for logic-based models """
        pass

    @abstractmethod
    def __init__(self):
        """ Abstract method for initializing logic-based models """
        pass

class MLModel(Model):
    """ An abstract base class for ML models """

    @property
    @abstractmethod
    def output_schema(self):
        """ Abstract method to define output schema for ML models """
        pass

    @abstractmethod
    def __init__(self):
        """ Abstract method for initializing ML models """
        pass

class ModelException(Exception):
    """ Exception type used to raise exceptions within Model derived classes """
    def __init__(self, *args, **kwargs):
        Exception.__init__(self, *args, **kwargs)