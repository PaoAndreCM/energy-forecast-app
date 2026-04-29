import pandas as pd
import torch
from model import load_model
import data
import time
from datetime import datetime
import pickle

def predict(ts):
    model, device = load_model()
    
    x = data.get_input(ts)
    x = x.to(device)

    with torch.no_grad():
        pred = model(x)
    
    # scale back
    with open('models/scaler.pkl', 'rb') as f:
        scaler = pickle.load(f)

    pred = pred.cpu().squeeze(0).numpy()
    pred = scaler.inverse_transform(pred)
    
    # select last column (column containing consumption)
    pred = pred[:,-1]
    return pred

if __name__ == "__main__":
    test_timestamp = 1741682931691
    # preds = predict(test_timestamp)
    # print(preds)
    # print(f"num preds: {len(preds)}")