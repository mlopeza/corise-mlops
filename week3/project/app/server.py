from fastapi import FastAPI
from pydantic import BaseModel
from loguru import logger

from classifier import NewsCategoryClassifier
import time
import json
import math
from datetime import datetime 

class PredictRequest(BaseModel):
    source: str
    url: str
    title: str
    description: str


class PredictResponse(BaseModel):
    scores: dict
    label: str


MODEL_PATH = "../data/news_classifier.joblib"
LOGS_OUTPUT_PATH = "../data/logs.out"
NEWS_CLASSIFIER = None
FILE_LOGGING = None

app = FastAPI()

@app.on_event("startup")
def startup_event():
    """
    [TO BE IMPLEMENTED]
    1. Initialize an instance of `NewsCategoryClassifier`.
    2. Load the serialized trained model parameters (pointed to by `MODEL_PATH`) into the NewsCategoryClassifier you initialized.
    3. Open an output file to write logs, at the destimation specififed by `LOGS_OUTPUT_PATH`
        
    Access to the model instance and log file will be needed in /predict endpoint, make sure you
    store them as global variables
    """
    global NEWS_CLASSIFIER
    global FILE_LOGGING
    logger.info("Initializing NewsClassifier")
    nc = NewsCategoryClassifier()
    nc.load(MODEL_PATH)
    NEWS_CLASSIFIER = nc
    FILE_LOGGING = open(LOGS_OUTPUT_PATH, 'a')
    logger.info("Setup completed")


@app.on_event("shutdown")
def shutdown_event():
    # clean up
    """
    [TO BE IMPLEMENTED]
    1. Make sure to flush the log file and close any file pointers to avoid corruption
    2. Any other cleanups
    """
    if FILE_LOGGING:
        FILE_LOGGING.flush()
        FILE_LOGGING.close()
    logger.info("Shutting down application")

def request_logger(func):
    """
    File logging logic
    """
    def wrapper(request: PredictRequest):
        request_time = datetime.now().strftime("%Y:%m:%d %H:%M:%S")
        start = time.time()
        result = func(request)
        end = time.time()
        FILE_LOGGING.write(
            json.dumps({
                "timestamp": request_time,
                "request": request.dict(),
                "response": result.dict(),
                "latency": math.trunc((end - start) * 1000)
            }) + "\n"
        )
        return result
    return wrapper

@app.post("/predict", response_model=PredictResponse)
@request_logger
def predict(request: PredictRequest):
    # get model prediction for the input request
    # construct the data to be logged
    # construct response
    """
    [TO BE IMPLEMENTED]
    1. run model inference and get model predictions for model inputs specified in `request`
    2. Log the following data to the log file (the data should be logged to the file that was opened in `startup_event`)
    {
        'timestamp': <YYYY:MM:DD HH:MM:SS> format, when the request was received,
        'request': dictionary representation of the input request,
        'prediction': dictionary representation of the response,
        'latency': time it took to serve the request, in millisec
    }
    3. Construct an instance of `PredictResponse` and return
    """
    proba = NEWS_CLASSIFIER.predict_proba(request.dict())
    label = NEWS_CLASSIFIER.predict_label(request.dict())
    return PredictResponse(scores=proba, label=label)


@app.get("/")
def read_root():
    return {"Hello": "World"}
