import pandas as pd
from torch.utils.data import Dataset
from sklearn.preprocessing import LabelEncoder 
import torch

class SNACSDataset(Dataset):
    def __init__(self, data, concatenated_embeddings, mode='train'):
        self.mode = mode
        parsed_data = []
        for x in data:
            try:
                parsed_data.append(concatenated_embeddings[x[3]][x[4]][0].tolist() + [x[1], x[2], x[0]])
            except:
                pass
        self.df = pd.DataFrame(parsed_data, columns=['e' + str(x) for x in range(3072)] + ['scene', 'function', 'name'])
        le = LabelEncoder() # one-hot encoding
            
    def __len__(self):
        return len(self.df)
    
    def __getitem__(self, idx):
        return self.df[idx]

class NN(torch.nn.Module):
    def __init__(self, num_labels, input_size):
        super(NN, self).__init__()
        self.fc1 = torch.nn.Linear(input_size, num_labels)
    
    def forward(self, input):
        return self.fc1(input[:,-1])