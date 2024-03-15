class Config(object):
    DEBUG = False
    TESTING = False
    CSRF_ENABLED = True
    MODELS = [
        {
            "module_name": "threshold.threshold",
            "class_name": "Threshold"
        },
        {
            "module_name": "lr.ml_lr",
            "class_name": "LRegression"
        },
	{
            "module_name": "nlr.ml_nlr",
            "class_name": "NLRegression"
        }

    ]


class ProductionConfig(Config):
    DEBUG = False


class StagingConfig(Config):
    DEVELOPMENT = True
    DEBUG = True


class DevelopmentConfig(Config):
    DEVELOPMENT = True
    DEBUG = True


class TestingConfig(Config):
    TESTING = True
    DEBUG = True