# config.py
from argparse import Namespace

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

def get_configs(
                name,
                enc_in=1, 
                seq_len = 672, 
                pred_len = 96, 
                e_layers = 3, 
                n_heads = 16, 
                d_model = 128, 
                d_ff = 256, 
                dropout = 0.2, 
                fc_dropout = 0.2,
                head_dropout = 0,
                individual_head = 0, 
                patch_len = 16, 
                stride = 8, 
                padding_patch = 'end', 
                revin = 1,  
                affine = 0, 
                subtract_last = 0, 
                decomposition = 0, 
                kernel_size = 25, # end of PatchTST params
                label_len = 0,
                features = 'S',
                batch_size = 128,
                learning_rate = 0.0001,
                num_epochs = 100,
                pct_start = 0.4, #for scheduler
                patience = 20,
                # root_path_name='./dataset/',
                # data_path_name='SMARD_converted.csv',
                num_workers=10,
                window_stride=1,
                shuffle_train=True
                ):
    configs = Namespace(
        name = name,
        enc_in=enc_in,
        seq_len=seq_len,
        pred_len=pred_len,
        e_layers=e_layers,
        n_heads=n_heads,
        d_model=d_model,
        d_ff=d_ff,
        dropout=dropout,
        fc_dropout=fc_dropout,
        head_dropout=head_dropout,
        individual=individual_head,
        patch_len=patch_len,
        stride=stride,
        padding_patch=padding_patch,
        revin=revin,
        affine=affine,
        subtract_last=subtract_last,
        decomposition=decomposition,
        kernel_size=kernel_size,
        label_len=label_len,
        features = features,
        batch_size = batch_size,
        learning_rate = learning_rate,
        num_epochs = num_epochs,
        pct_start = pct_start,
        patience = patience,
        # root_path_name=root_path_name,
        # data_path_name=data_path_name,
        num_workers=num_workers,
        window_stride=window_stride,
        shuffle_train=shuffle_train
    )
    return configs