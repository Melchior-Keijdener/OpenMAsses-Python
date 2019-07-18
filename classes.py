import pandas as pd
import numpy as np


class MyData:
    """Saves the data information, do not wish to store it on the database but keep a local copy"""
    def __init__(self):
        self.df = pd.DataFrame(np.zeros((11, 6)))  # fix, not flexible to update dfs
        self.df.columns = ['Internal Perspective', 'External Perspective', 'Peer rating', 'Social media',
                           'News reports', 'Survey data']
        self.home_file = ''
        self.pdf_files = []
        self.x_dim = self.df.iloc[:, 0]
        self.y_dim = self.df.iloc[:, 1]
