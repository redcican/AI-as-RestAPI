from fastapi import FastAPI
import pathlib
from typing import Optional
from . import ml

app = FastAPI()

BASE_DIR = pathlib.Path(__file__).resolve().parent

MODEL_DIR = BASE_DIR.parent / 'models'
SMS_SPAM_MODEL_PATH = MODEL_DIR / "spam-sms"
MODEL_PATH = SMS_SPAM_MODEL_PATH / "spam-model.h5"
TOKENIZER_PATH = SMS_SPAM_MODEL_PATH / "spam-classifer-tokenizer.json"
METADATA_PATH = SMS_SPAM_MODEL_PATH / "spam-classifer-metadata.json"

AI_MODEL = None


@app.on_event("startup")
def on_startup():
    global AI_MODEL
    AI_MODEL = ml.AIModel(
        model_path=MODEL_PATH, 
        tokenizer_path=TOKENIZER_PATH, 
        metadata_path = METADATA_PATH
    )
    
    

@app.get("/")
def read_index(q: Optional[str] = None):
    global AI_MODEL
    query = q or "This is an useful email."
    preds_dict = AI_MODEL.predict_text(query)
    return {"query": query, "results":preds_dict}
