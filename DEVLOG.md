## 2026-03-14
- Created repo, wrote README, started planning of code refactoring
- Learned that Streamlit is a framework that allows me to build a web app in python. Also that I can deploy my model on Hugging Face -- needs more research.
- Blocked on how to refactor code. What exactly do I need to do to deploy my model?
- Next: Go over Jupyter notebook from my thesis code and figure out how the refactoring needs to be done to actually deploy the model. Set aside best performing checkpoint.

## 2026-03-16
- Created safe copy from thesis code from remote server to local machine (will lose access to Uni server).
- Learned that I can use my mac to create predictions via MPS. Identified best checkpoint (checkpoints/electricity_configs_multivariateftM_pl16_st8_dm128_nh16_el3_df256_ds0.2_eb32_seed1337/checkpoint.pth). 
Decided on target structure:
```
grid-load-forecast/
├── src/
│   ├── layers/ 
│   ├── utils/
│   ├── dataset.py
│   ├── model.py
│   ├── data.py
│   ├── train.py
│   ├── predict.py
│   └── evaluate.py
├── data/
│   └── SMARD_converted.csv
├── models/
│   └── best_checkpoint.pth
├── app.py
├── config.py
├── requirements.txt
├── README.md
└── DEVLOG.md
```
- Blocked by lack of time.
- Next: 
1. Create folder structure + move best checkpoint (rename when moving)
2. Adapt DEMO to `predict.py`
3. Build a skeleton Streamlit app that calls `predict.py` and displays something.

## 2026-03-17
- Created folder structure:
```
grid-load-forecast/
├── data/
│   └── SMARD_converted.csv
├── models/
│   └── best_checkpoint.pth
├── src/
│   ├── layers/ 
│   ├── utils/
│   ├── data.py
│   ├── dataset.py
│   ├── evaluate.py
│   ├── model.py
│   ├── predict.py
│   └── train.py
├── app.py
├── config.py
├── requirements.txt
├── DEVLOG.md
└── README.md
```
- Transferred class `Dataset_SMARD`  to `dataset.py`
- Figured out:
    - `predict.py` must contain only what needs to happen every time the user requests a prediction:
    - only predict (takes in prepared input which `data.py` has prepared)
    - `data.py` will contain the input fetching from SMARD API and preparation for prediction. Will serve the app
    - `model.py` will load and initialize the model
    - `app.py` will handle user interaction, and will call the previous three.
    - `dataset.py` will serve the training pipeline.
- Learned that the scaler can be saved as a `pkl`. It should live in my `models/` directoy.
- Blocked by Clara's BD party.
- Next:
1. Work on `data.py` first, for input fetching and preparation... save the scaler 
2. Work on `model.py`
3. Work on `predict.py`