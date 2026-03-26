# config.py

# Model architecture (needed for loading checkpoint)
SEQ_LEN = 672  # Input length (7 days at 15-min intervals)
PRED_LEN = 96  # Output length (24 hours at 15-min intervals)
OFFSET = 56  # Gap between input end and prediction start (14 hours at 15-min intervals)
OFFSET_HOURS = 14

# Model hyperparameters (needed for loading model)
ENC_IN = 1
E_LAYERS = 3
N_HEADS = 16
D_MODEL = 128
D_FF = 256
DROPOUT = 0.2
PATCH_LEN = 16
STRIDE = 8

# Data
SMARD_BASE_URL = 'https://www.smard.de/app/chart_data/410/DE/'