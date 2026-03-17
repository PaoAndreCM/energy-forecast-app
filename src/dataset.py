import os
import numpy as np
import pandas as pd
from torch.utils.data import Dataset, DataLoader
from sklearn.preprocessing import StandardScaler
from utils.timefeatures import time_features

class Dataset_SMARD(Dataset):
    def __init__(self, root_path, flag='train', size=None,
                 features='S', data_path='SMARD_converted.csv',
                 target='OT', scale=True, offset=56, window_stride=96,
                 split_mode='ratio', ratio_train=0.7, ratio_val=0.2,
                 train_start_date="2015-01-01 00:00:00", train_stop_date="2020-12-31 23:45:00",
                 val_start_date="2021-01-01 10:00:00", val_stop_date="2022-12-31 23:45:00",
                 test_start_date="2023-01-01 10:00:00", test_stop_date="2023-12-31 22:45:00"):
        # size [seq_len, label_len, pred_len]
        self.seq_len = size[0]
        self.label_len = size[1]
        self.pred_len = size[2]
        # init
        assert flag in ['train', 'test', 'val']
        type_map = {'train': 0, 'val': 1, 'test': 2}
        self.set_type = type_map[flag]

        self.features = features
        self.target = target
        self.scale = scale
        self.window_stride = window_stride

        self.root_path = root_path
        self.data_path = data_path
        self.gap = offset

        self.split_mode = split_mode
        self.ratio_train = ratio_train
        self.ratio_val = ratio_val

        self.train_start_date = train_start_date
        self.train_stop_date = train_stop_date
        self.val_start_date = val_start_date
        self.val_stop_date = val_stop_date
        self.test_start_date = test_start_date
        self.test_stop_date = test_stop_date
        
        assert split_mode in ['ratio', 'fixed']

        self.__read_data__()

    def __read_data__(self):
        self.scaler = StandardScaler()
        df_raw = pd.read_csv(os.path.join(self.root_path,
                                          self.data_path))

        '''
        df_raw.columns: ['date', ...(other features), target feature]
        '''
        cols = list(df_raw.columns)
        cols.remove(self.target)
        cols.remove('date')
        df_raw = df_raw[['date'] + cols + [self.target]]

        border1s, border2s = None, None 
        
        if self.split_mode == 'fixed':
            idx_train_start = df_raw.index[df_raw['date'].astype(str).str[:19] == self.train_start_date][0]
            idx_train_stop = df_raw.index[df_raw['date'].astype(str).str[:19] == self.train_stop_date][0]
            idx_val_start = df_raw.index[df_raw['date'].astype(str).str[:19] == self.val_start_date][0]
            idx_val_stop = df_raw.index[df_raw['date'].astype(str).str[:19] == self.val_stop_date][0]
            idx_test_start = df_raw.index[df_raw['date'].astype(str).str[:19] == self.test_start_date][0]
            idx_test_end = df_raw.index[df_raw['date'].astype(str).str[:19] == self.test_stop_date][0]
            border1s = [idx_train_start, idx_val_start, idx_test_start]
            border2s = [idx_train_stop+1, idx_val_stop+1, idx_test_end+1]
        else:  # ratio-based split
            num_train = int(len(df_raw) * self.ratio_train) 
            num_test = int(len(df_raw) * self.ratio_val) 
            num_vali = len(df_raw) - num_train - num_test
            border1s = [0, num_train - self.seq_len, len(df_raw) - num_test - self.seq_len]
            border2s = [num_train, num_train + num_vali, len(df_raw)]
        
        border1 = border1s[self.set_type]
        border2 = border2s[self.set_type]

        if self.features == 'M' or self.features == 'MS':
            cols_data = df_raw.columns[1:]
            df_data = df_raw[cols_data]
        elif self.features == 'S':
            df_data = df_raw[[self.target]]

        if self.scale:
            train_data = df_data[border1s[0]:border2s[0]]
            self.scaler.fit(train_data.values)
            data = self.scaler.transform(df_data.values)
        else:
            data = df_data.values

        self.data_x = data[border1:border2]
        self.data_y = data[border1:border2]

        self.timestamps = df_raw['date'][border1:border2].values

    def __getitem__(self, index):
        i = index * self.window_stride
        s_begin = i
        s_end = s_begin + self.seq_len
        r_begin = s_end + self.gap
        r_end = r_begin + self.pred_len

        seq_x = self.data_x[s_begin:s_end]
        seq_y = self.data_y[r_begin:r_end]

        return seq_x, seq_y

    def __len__(self):
        return (len(self.data_x) - self.seq_len - self.pred_len - self.gap) // self.window_stride + 1

    def inverse_transform(self, data):
        return self.scaler.inverse_transform(data)
    
    def get_timestamps(self):
        # Return timestamp windows corresponding to each prediction window.
        stamps = []
        for i in range(len(self)):
            s_begin = i * self.window_stride
            s_end = s_begin + self.seq_len
            r_begin = s_end + self.gap
            r_end = r_begin + self.pred_len
            stamps.append(self.timestamps[r_begin:r_end])
        return np.array(stamps)