



#%%
# precondition 
# needed import
import numpy as np 
from sklearn.datasets import load_digits
import matplotlib.pyplot as plt

#%%
# data preview 
data = load_digits()['data']
plt.imshow(data[0].reshape(8,8))
plt.show()


#%%
# Data class : in the ANN
# shuffle the data index 
class Data:
    def __init__(self, X, y, batchSize, ):
        self.X = X
        self.y = y
        self.bachSize = batchSize
        self.pos = 0
        self.dataSize = len(X)
    
    def nextBatch(self):
        if self.pos + self.batchSize >= self.dataSize:
            n = self.dataSize - self.pos
            index = np.random.shuffle(list(range(n)))
            self.pos = 0
            batch = (X[self.pos:][index], y[index])
        else:
            index = list(range(self.bachSize))
            np.random.shuffle(index)
            self.pos += self.bachSize
            batch = (X[self.pos: self.batchSize][index], y[index])
        return batch


#%%

class FullyConnect:
    def __init__(self, xl, yl, batchNorm = True, dropout = True):
        self.xl = xl
        self.yl = yl
        self.batchNorm = batchNorm
        self.dropout= dropout

        
        np.seed(42)
        self.weights = np.random.randn(xl, yl)/np.sqrt(2/xl)
        self.bias = np.random.randn



    def forward(self, x ):
        if self.dropout:
            isKeep = np.random.rand(1, self.xl) < self.keepProb 
            self.keepWeights = self.weights * isKeep / self.keepProb 
        self.y = np.dot(x, self.keepWeights) + self.bias

        if self.batchNorm:
            pass 
        return self.y






