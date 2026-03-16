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
