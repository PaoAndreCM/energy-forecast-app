import pandas as pd
import torch
import model
import data

def predict():
    model = model.load_model()
    x_raw = data.get_input()
    raw_seq = x_raw.values

    x = raw_seq # TODO scale and tensorize, but actually this must be done in data.py

    with torch.no_grad():
        pred = model(x)
    
    return pred