from dataclasses import dataclass

from keras_preprocessing.text import tokenizer_from_json
from pathlib import Path
from typing import Optional, List
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing.text import tokenizer_from_json
from tensorflow.keras.preprocessing.sequence import pad_sequences

import numpy as np
import json

from . import numpy_encoder

@dataclass
class AIModel:
    model_path: Path
    tokenizer_path: Optional[Path] = None
    metadata_path: Optional[Path] = None
        
    model = None
    tokenizer = None
    metadata = None
    
    def __post_init__(self):
        if self.model_path.exists():
            self.model = load_model(self.model_path)
            
        if self.tokenizer_path and self.tokenizer_path.exists():
            if self.tokenizer_path.name.endswith("json"):
                tokenizer_text = self.tokenizer_path.read_text()
                self.tokenizer = tokenizer_from_json(tokenizer_text)
                
        if self.metadata_path and self.metadata_path.exists():
            if self.metadata_path.name.endswith("json"):
                self.metadata = json.loads(self.metadata_path.read_text())
                                                     
                                                     
    def get_model(self):
        if not self.model:
            raise Exception("Model not loaded")
        return self.model
    
    def get_tokenizer(self):
        if not self.tokenizer:
            raise Exception("Tokenizer not loaded")
        return self.tokenizer
    
    def get_metadata(self):
        if not self.metadata:
            raise Exception("Metadata not loaded")
        return self.metadata
    
    def get_sequences_from_text(self, texts: List[str]):
        tokenizer = self.get_tokenizer()
        sequences =  tokenizer.texts_to_sequences(texts)
        return sequences
    
    def get_input_from_sequences(self, sequences):
        maxlen = self.get_metadata().get('max_sequence') or 280
        x_input = pad_sequences(sequences, maxlen=maxlen)
        return x_input
    
    def get_label_legend_inverted(self):
        legend = self.get_metadata().get('labels_legend_inverted') or {}
        if len(legend.keys()) != 2:
            raise Exception("You legend is incorrect.")
        return legend
    
    def get_label_pred(self, idx, val):
        legend = self.get_label_legend_inverted()
        return {"label": legend[str(idx)], "confidence": val}
    
    def get_top_pred_lable(self, preds):
        top_idx_val = np.argmax(preds)
        val = preds[top_idx_val]
        top_pred = self.get_label_pred(top_idx_val, val)
        return top_pred
    
    def predict_text(self, query: str, include_top=True, encode_to_json=True):
        model = self.get_model()
        sequences = self.get_sequences_from_text([query])
        x_input = self.get_input_from_sequences(sequences)
        preds = model.predict(x_input)[0]
        labeled_preds = [self.get_label_pred(idx, val) for idx, val in enumerate(list(preds))]
        results = {"predictions": labeled_preds}
        if include_top:
            results["top"] = self.get_top_pred_lable(preds)
        if encode_to_json:
            encoded_results =  numpy_encoder.encode_to_json(results, as_py=True)
        return encoded_results
