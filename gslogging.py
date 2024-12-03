try:
    from rites.logger import Logger
except ImportError as e:
    print("Import Error >> Please run pip install -r requirements.txt in the folder's workplace")
    print(f"Error details: {e}")


GSLogger = Logger("./logs")
