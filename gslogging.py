try:
    from rites import logger
except ImportError:
    print("Import Error >> Please run pip install -r requirements.txt in the folder's workplace")

GSLogger = logger.Logger("./logs")