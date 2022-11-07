# Create an AI that rates finnish words according to how cool they sound

import random
import re
import sys
import time
from collections import defaultdict
from pathlib import Path
from typing import List, Tuple

import numpy as np
import pandas as pd
import torch
import torch.nn as nn
import torch.nn.functional as F
import torch.optim as optim
from torch.utils.data import DataLoader, Dataset

# Path to the data
DATA_PATH = Path("data/finnish_words.txt")

# Path to the model

MODEL_PATH = Path("model/model.pt")


class WordDataset(Dataset):
    def __init__(self, data_path: Path, max_len: int = 20):
        self.max_len = max_len
        self.data = self.read_data(data_path)

    def __len__(self):
        return len(self.data)

    def __getitem__(self, idx: int) -> Tuple[torch.Tensor, torch.Tensor]:
        word = self.data[idx]
        word = self.preprocess_word(word)
        word = self.encode_word(word)
        word = self.pad_word(word)
        word = torch.tensor(word)
        return word[:-1], word[1:]

    def read_data(self, data_path: Path) -> List[str]:
        with open(data_path, "r") as f:
            data = f.read().splitlines()
        return data

    def preprocess_word(self, word: str) -> str:
        word = word.lower()
        word = re.sub(r"[^a-zåäö]", "", word)
        return word

    def encode_word(self, word: str) -> List[int]:
        return [ord(c) - 97 for c in word]

    def pad_word(self, word: List[int]) -> List[int]:
        return word + [0] * (self.max_len - len(word))

        
