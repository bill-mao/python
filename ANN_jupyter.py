#%% Change working directory from the workspace root 
# to the ipynb file location. 、
# Turn this addition off with the DataScience.changeDirOnImportExport setting
import os
try:
	# os.chdir(os.path.join(os.getcwd(), '..\jupyter'))
	print(os.getcwd())
except:
	pass

#%%
import numpy as np
from sklearn.datasets import load_digits


#%%
import matplotlib.pyplot as plt
digits = load_digits()
data = digits.data
image = data[9].reshape(8,8)
plt.imshow(image) # 把二维数据用图片色深画出
plt.show()

#%%
data.shape
image.shape
plt.imshow(image)
image

#%%
# Data class : in the ANN； one batch
# shuffle the data index 
class Data:
    def __init__(self,x, y, batch_size):
        self.x = x
        self.y = y
        self.l = x.shape[1]
        self.batch_size = batch_size
        self.pos = 0
        
    def forward(self):
        #Mini-batch
        pos = self.pos
        bat = self.batch_size
        l = self.l
        if pos + bat >= l:
            ret = (self.x[:,pos:l], self.y[pos:l])
            self.pos = 0
            index = range(l)
            np.random.shuffle(list(index))
            self.x = self.x[:,index]
            self.y = self.y[index]
        else:
            ret = (self.x[:,pos:pos+bat], self.y[pos:pos+bat])
            self.pos += self.batch_size
        
        return ret, self.pos
    def backward(self, d):
        pass


#%%
# 每一层： 全连接
class FullyConnect:
    def __init__(self, l_x, l_y, L2 = 0, keep_prob = 1, methods = 'Grad',
                 k1=0.9, k2=0.999, batch_normal = False, predict = False):
        np.random.seed(42)
        self.l_x = l_x
        self.weights = np.random.randn(l_y, l_x)*np.sqrt(2/l_x)
        self.bias = np.random.randn(l_y, 1)
        self.lr = 0 # 
        self.L2 = L2
        self.keep_prob = keep_prob # drop out
        self.methods = methods # 
        #Monmentum
        self.vdw = 0
        self.vdb = 0
        #RmSprop
        self.sdw = 0
        self.sdb = 0
        #Adam
        
        #batch-Normalization # 
        self.batch_normal =  batch_normal
        self.gram = np.random.randn(l_y, 1)
        self.beta = np.random.randn(l_y, 1)
        self.mean = np.zeros((l_y, 1))
        self.std = np.zeros((l_y, 1))
        self.predict = predict
        
    def forward(self, x):
        #drop-out
        iskeep = np.random.rand(1, self.l_x)<self.keep_prob
        self.keep_weights = self.weights*iskeep/self.keep_prob
        
        self.x = x # 输入初始化
        
        self.y = np.dot(self.keep_weights, self.x)+self.bias
        
        # batch-Normalization
        if self.batch_normal:
            self._batch_normalization()
        
        return self.y 
    
    def _batch_normalization(self):
        if self.predict:
            predict_y_norm = (self.y-self.mean)/(self.std+1e-8)
            self.y = self.gram*predict_y_norm + self.beta  # **
        else:
            n = self.y.shape[1]
            self.tmean = np.mean(self.y, axis = 1, keepdims=True)
            self.tstd = np.std(self.y, axis = 1, keepdims=True)
            self.y_norm = (self.y-self.tmean)/(self.tstd+1e-8)
            self.y = self.gram*self.y_norm + self.beta

            self.mean = 0.9*self.mean + 0.1*self.tmean  # **y输出？
            self.std = 0.9*self.std + 0.1*self.tstd
    
    # 
    def backward(self, d):
        if self.batch_normal:
            d = d*self.gram/self.tstd
            self.dgram = d*self.y_norm
            self.gram -= self.lr*np.sum(self.dgram, axis = 1, keepdims=True)/self.y.shape[1]
            self.beta -= self.lr*np.sum(d, axis = 1, keepdims=True)/self.y.shape[1]
            
        self.dw = np.dot(d, self.x.T)/self.x.shape[1]+self.L2*self.keep_weights/(2*self.x.shape[1])
        self.db = np.sum(d, axis = 1, keepdims=True)/self.x.shape[1]
        self.dx = np.dot(self.keep_weights.T, d)
        
        #优化
        self._optimize(self.methods)
        return self.dx
    
    # 梯度优化 --？
    def _optimize(self, methods='Grad', k1=0.9, k2=0.999):
        if methods == 'Grad':
            self.weights -= self.lr * self.dw
            self.bias -= self.lr * self.db
        elif methods == 'Monmentum':
            #未修正
            self.vdw = k1*self.vdw+(1-k1)*self.dw
            self.vdb = k1*self.vdb+(1-k1)*self.db
            self.weights -= self.lr * self.vdw
            self.bias -= self.lr * self.vdb
        elif methods == 'RMSprop':
            #未修正
            self.sdw = k2*self.sdw + (1-k2)*self.dw**2
            self.sdb = k2*self.sdb + (1-k2)*self.db**2
            self.weights -= self.lr*self.dw/(np.sqrt(self.sdw)+1e-8)
            self.bias -= self.lr*self.db/(np.sqrt(self.sdb)+1e-8)
        elif methods == 'Adam':
            self.vdw = k1*self.vdw+(1-k1)*self.dw
            self.vdb = k1*self.vdb+(1-k1)*self.db
            self.sdw = k2*self.sdw + (1-k2)*self.dw**2
            self.sdb = k2*self.sdb + (1-k2)*self.db**2
            
            self.weights -= self.lr*self.vdw/(np.sqrt(self.sdw)+1e-8)
            self.bias -= self.lr*self.vdb/(np.sqrt(self.sdb)+1e-8)


#%%
# 可以看做一个隐藏的层
class Sigmoid:
    def __init__(self):
        pass
    def sigmoid(self, x):
        return 1/(1+np.exp(-x))
    def forward(self, x):
        self.x = x
        self.y = self.sigmoid(x)
        return self.y
    def backward(self, d):
        sig = self.sigmoid(self.x)
        self.dx = d*sig*(1-sig)
        return self.dx


#%%
class Relu1:
    def __init__(self):
        pass
    def relu1(self, x):
        s = np.ones_like(x)/10 # ones_like : 1 的同维度的张量
        s[x > 0] = 1
        return x*s
    def forward(self, x):
        self.x = x
        self.y = self.relu1(x)
        return self.y
    def backward(self, d):
        s = np.ones_like(self.x)/10
        s[self.x > 0] = 1
        return d*s


#%%
class Relu:
    def __init__(self):
        pass
    def relu(self, x):
        return x*(x>0)
    def forward(self, x):
        self.x = x
        self.y = self.relu(x)
        return self.y
    def backward(self, d):
        r = self.x > 0
        return d*r


#%%
class Tanh:
    def __init__(self):
        pass
    def tanh(self, x):
        return (np.exp(x)-np.exp(-x))/(np.exp(x)+np.exp(-x))
    def forward(self, x):
        self.x = x
        self.y = self.tanh(x)
        return self.y
    def backward(self, d):
        t = 1-self.tanh(self.x)**2
        return d*t


#%%
class QuadraticLoss:
    def __init__(self, L2):
        self.L2 = L2
    def forward(self, x, label):
        self.x = x
        self.label = np.zeros_like(x)
        for i in range(len(label)):
            self.label[label[i], i] = 1 # 单位矩阵？ 为什么一定要除以batch size

        self.loss = np.sum(np.square(self.x - self.label))/self.x.shape[1]/2
        return self.loss
    def backward(self):
        self.dx = (self.x - self.label)
        return self.dx


#%%
class Accuracy:
    def __init__(self):
        pass
    def forward(self, x, label):
        self.accuracy = 0
        for i in range(len(label)):
            xx = np.argmax(x[:, i]) # 取最大值
            if xx == label[i]:
                self.accuracy += 1
        self.accuracy = 1.0*self.accuracy/x.shape[1]
        return self.accuracy


#%%
class ANN:
    def __init__(self, layer_sizes, epochs = 20,batch_size = 1, learning_rate = 0.01, L2 = 0, keep_probs=None,
                methods = 'Grad', k1=0.9, k2=0.999, batch_normal = False):
        self.ls = layer_sizes
        self.bs = batch_size
        self.lr = learning_rate
        self.epochs = epochs
        
        #正则化
        self.L2 = L2
        self.keeｐ_probs = keep_probs
        
        #优化算法
        self.methods = methods
        self.k1 = k1
        self.k2 = k2
        
        #batch-normal
        self.batch_normal = batch_normal
        
    def fit(self, X, y):
        data_layer = Data(X, y, self.bs)
        input_size = X.shape[0]
        out_size = len(set(y))
        inner_layers = []   
        
        losslayer = QuadraticLoss(0)
        
        if self.ls == []:
            inner_layers.append(FullyConnect(input_size, out_size, self.L2))
            inner_layers.append(Sigmoid())
        elif self.ls != None:
            inner_layers.append(FullyConnect(input_size, self.ls[0], self.L2, batch_normal=self.batch_normal))
            inner_layers.append(Relu1())
            
            for i in range(0, len(self.ls)-1):
                full_layer = FullyConnect(self.ls[i], self.ls[i+1], self.L2, batch_normal=self.batch_normal)
                if self.keep_probs != None:
                    full_layer.keep_prob = self.keep_probs[i]
                inner_layers.append(full_layer)
                inner_layers.append(Relu1())
            
            inner_layers.append(FullyConnect(self.ls[-1], out_size, self.L2))
            inner_layers.append(Sigmoid())
            
        for layer in inner_layers:
            layer.lr = self.lr # 为所有中间层设置学习速率
            
            layer.methods = self.methods
            layer.k1 = self.k1
            layer.k2 = self.k2
        
        #学习
        for i in range(self.epochs):
            losssum = 0
            iters = 0
            # print('epochs:', i)   
            while True:
                data, pos = data_layer.forward()  # 从数据层取出数据
                x, label = data
                for layer in inner_layers:  # 前向计算
                    x = layer.forward(x)
                
                loss = losslayer.forward(x, label)  # 调用损失层forward函数计算损失函数值
                losssum += loss
                iters += 1
                d = losslayer.backward()  # 调用损失层backward函数层计算将要反向传播的梯度
                for layer in inner_layers[::-1]:  # 反向传播
                    d = layer.backward(d)
                if pos == 0:
                    # print('loss:', losssum / iters)
                    break
        self.inner_layers = inner_layers
    
    def predict(self,X):
        for layer in self.inner_layers:
            layer.predict = True
            X = layer.forward(X)
        return Ｘ
    
    def accuracy(self, y2, y):
        accuracy = Accuracy()
        accu = accuracy.forward(y2, y)  # 调用准确率层forward()函数求出准确率
        print('accuracy:', accu)
        return accu


#%%
from sklearn.preprocessing import StandardScaler
digits = load_digits()
data = digits.data
target = digits.target
scaler = StandardScaler()
data = scaler.fit_transform(data)

train_x = data[:1500].T; train_y = target[:1500]
test_x = data[1500:].T; test_y = target[1500:]

#%% [markdown]
# #### 正常的ANN

#%%
ann = ANN([30, 10], batch_size = 256, epochs=100, learning_rate=1,batch_normal=False)
ann.fit(train_x, train_y)


#%%
y2 = ann.predict(test_x)
ann.accuracy(y2, test_y)

#%% [markdown]
# #### L2正则化

#%%
ann = ANN([30, 10], batch_size = 256, epochs=1000, learning_rate=1,batch_normal=False, L2 = 1)
ann.fit(train_x, train_y)


#%%
y2 = ann.predict(test_x)
ann.accuracy(y2, test_y)


#%%
#有点过拟合
ann = ANN([30, 10], batch_size = 256, epochs=1000, learning_rate=1,batch_normal=False, L2 = 0)
ann.fit(train_x, train_y)


#%%
y2 = ann.predict(test_x)
ann.accuracy(y2, test_y)

#%% [markdown]
# #### 增量梯度下降

#%%
#有点过拟合
ann = ANN([30, 10], batch_size = 256, epochs=1000, learning_rate=0.001,batch_normal=False, methods='Adam')
ann.fit(train_x, train_y)


#%%
y2 = ann.predict(test_x)
ann.accuracy(y2, test_y)

#%% [markdown]
# ## 绘图

#%%
def my_learning_curve(estimator, X, y,cv=3, train_sizes = np.linspace(.1, 1.0, 5)):
    train_s = []
    train_scores = []
    test_scores = []
    for size in train_sizes:
        size = int(size*len(X))
        childX = X[:size]
        childy = y[:size]
        scores1 = [] #训练
        scores2 = [] #测试
        childTrainSize = int(len(childX)*(1-1/cv))
        for c in range(cv):
            randomIndex = list(range(size))
            np.random.shuffle(randomIndex)
            randomIndex = np.array(randomIndex)
            childTrainX, childTestX = childX[randomIndex[:childTrainSize]].T, childX[randomIndex[childTrainSize+1:]].T
            childTrainy, childtesty = childy[randomIndex[:childTrainSize]], childy[randomIndex[childTrainSize+1:]]
            estimator.fit(childTrainX, childTrainy)
            
            trainPredicty = estimator.predict(childTrainX)
            train_score = estimator.accuracy(trainPredicty, childTrainy)
            scores1.append(train_score)
            testPredicty = estimator.predict(childTestX)
            test_score = estimator.accuracy(testPredicty, childtesty)
            scores2.append(test_score)
        train_s.append(size)
        train_scores.append(scores1)
        test_scores.append(scores2)
    
    return train_sizes, train_scores, test_scores


#%%
ann = ANN([30, 10], batch_size = 256, epochs=100, learning_rate=1,batch_normal=False)
train_sizes, train_scores, test_scores = my_learning_curve(ann, data, target)


#%%
print(train_scores)
print(test_scores)


#%%
def plot_learning_curve(estimator, title, X, y, ylim=None, cv=None, train_sizes=np.linspace(.1, 1.0, 5)):
    plt.figure()
    plt.title(title)
    if ylim is not None:
        plt.ylim(*ylim)
    plt.xlabel("Training examples")
    plt.ylabel("Score")
    
    train_sizes,train_scores, test_scores = my_learning_curve(
        estimator, X, y, cv=cv,train_sizes=train_sizes)
    train_scores_mean = np.mean(train_scores, axis=1)
    train_scores_std = np.std(train_scores, axis=1)
    test_scores_mean = np.mean(test_scores, axis=1)
    test_scores_std = np.std(test_scores, axis=1)
    plt.grid()

    plt.fill_between(train_sizes, train_scores_mean - train_scores_std,
                     train_scores_mean + train_scores_std, alpha=0.1,
                     color="r")
    plt.fill_between(train_sizes, test_scores_mean - test_scores_std,
                     test_scores_mean + test_scores_std, alpha=0.1, color="g")
    plt.plot(train_sizes, train_scores_mean, 'o-', color="r",
             label="Training score")
    plt.plot(train_sizes, test_scores_mean, 'o-', color="g",
             label="Cross-validation score")

    plt.legend(loc="best")
    return plt


#%%
ann = ANN([30, 10], batch_size = 256, epochs=1000, learning_rate=0.001,batch_normal=False, methods='Adam', L2 = 1)
plot_learning_curve(ann, 'ann', data, target, ylim=[0.8, 1.01], cv = 3)
plt.show()


#%%
ann = ANN([30, 10], batch_size = 256, epochs=1000, learning_rate=0.001,batch_normal=False, methods='Adam')
plot_learning_curve(ann, 'ann', data, target, ylim=[0.8, 1.01], cv = 3)
plt.show()


#%%
randomIndex = list(range(20))
np.random.shuffle(randomIndex)
randomIndex = np.array(randomIndex)
randomIndex[:10]


#%%
from sklearn.learning_curve import learning_curve
def plot_learning_curve(estimator, title, X, y, ylim=None, cv=None,
                        n_jobs=1, train_sizes=np.linspace(.1, 1.0, 5)):
    """
    Generate a simple plot of the test and traning learning curve.

    Parameters
    ----------
    estimator : object type that implements the "fit" and "predict" methods
        An object of that type which is cloned for each validation.

    title : string
        Title for the chart.

    X : array-like, shape (n_samples, n_features)
        Training vector, where n_samples is the number of samples and
        n_features is the number of features.

    y : array-like, shape (n_samples) or (n_samples, n_features), optional
        Target relative to X for classification or regression;
        None for unsupervised learning.

    ylim : tuple, shape (ymin, ymax), optional
        Defines minimum and maximum yvalues plotted.

    cv : integer, cross-validation generator, optional
        If an integer is passed, it is the number of folds (defaults to 3).
        Specific cross-validation objects can be passed, see
        sklearn.cross_validation module for the list of possible objects

    n_jobs : integer, optional
        Number of jobs to run in parallel (default 1).
    """
    plt.figure()
    plt.title(title)
    if ylim is not None:
        plt.ylim(*ylim)
    plt.xlabel("Training examples")
    plt.ylabel("Score")
    train_sizes, train_scores, test_scores = learning_curve(
        estimator, X, y, cv=cv, n_jobs=n_jobs, train_sizes=train_sizes)
    train_scores_mean = np.mean(train_scores, axis=1)
    train_scores_std = np.std(train_scores, axis=1)
    test_scores_mean = np.mean(test_scores, axis=1)
    test_scores_std = np.std(test_scores, axis=1)
    plt.grid()

    plt.fill_between(train_sizes, train_scores_mean - train_scores_std,
                     train_scores_mean + train_scores_std, alpha=0.1,
                     color="r")
    plt.fill_between(train_sizes, test_scores_mean - test_scores_std,
                     test_scores_mean + test_scores_std, alpha=0.1, color="g")
    plt.plot(train_sizes, train_scores_mean, 'o-', color="r",
             label="Training score")
    plt.plot(train_sizes, test_scores_mean, 'o-', color="g",
             label="Cross-validation score")

    plt.legend(loc="best")
    return plt
# title = "Learning Curves"
# plot_learning_curve(RandomForestClassifier(oob_score=True, n_estimators=30000, max_depth=5), title, X, y, ylim=(0.5, 1.01), cv=None, n_jobs=4, train_sizes=[50, 100, 150, 200, 250, 350, 400])
# plt.show()

#%% [markdown]
# # 测试

#%%
#多层神经网络
from sklearn.preprocessing import StandardScaler 
def multiplilyNet(learning_rate = 1):
    digits = load_digits()
    data = digits.data
    target = digits.target
    scaler = StandardScaler()
    data = scaler.fit_transform(data)
    train_x = data[:1500].T; train_y = target[:1500]
    test_x = data[1500:].T; test_y = target[1500:]
    datalayer1 = Data(train_x, train_y, 256)
    datalayer2 = Data(test_x, test_y, 297)
    inner_layers = []
    inner_layers.append(FullyConnect(8*8, 30))
    inner_layers.append(Relu1())
    inner_layers.append(FullyConnect(30, 10))
    inner_layers.append(Sigmoid())
    losslayer = QuadraticLoss(0)
    accuracy = Accuracy()

    for layer in inner_layers:
        layer.lr = learning_rate # 为所有中间层设置学习速率

    epochs = 1
    for i in range(epochs):
        print('epochs:', i)
        losssum = 0
        iters = 0
        while True:
            data, pos = datalayer1.forward()  # 从数据层取出数据
            x, label = data
            for layer in inner_layers:  # 前向计算
                print(x[0][0])
                x = layer.forward(x)

            loss = losslayer.forward(x, label)  # 调用损失层forward函数计算损失函数值
            losssum += loss
            iters += 1
            d = losslayer.backward()  # 调用损失层backward函数层计算将要反向传播的梯度
            for layer in inner_layers[::-1]:  # 反向传播
                d = layer.backward(d)

            if pos == 0:  # 一个epoch完成后进行准确率测试
                data, _ = datalayer2.forward()
                x, label = data
                for layer in inner_layers:
                    x = layer.forward(x)
                accu = accuracy.forward(x, label)  # 调用准确率层forward()函数求出准确率
                print('loss:', losssum / iters)
                print('accuracy:', accu)
                break
        return x


#%%
x = multiplilyNet(0.1)


#%%
from sklearn.preprocessing import StandardScaler 
def main(mode, learning_rate = 1, L2 = 0):
    digits = load_digits()
    data = digits.data
    target = digits.target
    scaler = StandardScaler()
    data = scaler.fit_transform(data)
    
    train_x = data[:1500].T; train_y = target[:1500]
    test_x = data[1500:].T; test_y = target[1500:]
    datalayer1 = Data(train_x, train_y, 256)
    datalayer2 = Data(test_x, test_y, 297)
    inner_layers = []
    inner_layers.append(FullyConnect(8*8, 10, L2))
    if mode == 'sigmoid':
        #10
        inner_layers.append(Sigmoid())
    elif mode == 'relu':
        #0.3
        inner_layers.append(Relu())
    elif mode == 'relu1':
        #0.3
        inner_layers.append(Relu1())
    elif mode == 'tanh':
        #0.2
        inner_layers.append(Tanh())
    losslayer = QuadraticLoss(L2)
    accuracy = Accuracy()

    for layer in inner_layers:
        layer.lr = learning_rate # 为所有中间层设置学习速率

    epochs = 20
    for i in range(epochs):
        print('epochs:', i)
        losssum = 0
        iters = 0
        while True:
            data, pos = datalayer1.forward()  # 从数据层取出数据
            x, label = data
            
            for layer in inner_layers:  # 前向计算
                x = layer.forward(x)

            loss = losslayer.forward(x, label)  # 调用损失层forward函数计算损失函数值
            losssum += loss
            iters += 1
            d = losslayer.backward()  # 调用损失层backward函数层计算将要反向传播的梯度
            for layer in inner_layers[::-1]:  # 反向传播
                d = layer.backward(d)

            if pos == 0:  # 一个epoch完成后进行准确率测试
                data, _ = datalayer2.forward()
                x, label = data
                for layer in inner_layers:
                    x = layer.forward(x)
                accu = accuracy.forward(x, label)  # 调用准确率层forward()函数求出准确率
                print('loss:', losssum / iters)
                print('accuracy:', accu)
                break


#%%
main('relu1', 0.3, L2 = 200)


#%%
weights = np.array([
    [1,2,3],
    [2,3,4]
])
iskeep = np.array([
    [1,0,1]
])
print(weights*iskeep/0.7)


#%%
np.random.rand(1,5)


#%%
10-8


#%%
10e-8


#%%
1e-8


#%%
np.power(2,3)


#%%
np.z


#%%
a1 = np.array([
    [1,2,5],
    [3,4,4]
])
a2 = np.array([
    [1],
    [2]
])
print(a1-a2)


#%%
print(np.mean(a1, axis = 1, keepdims=True))


#%%
a2*a1


#%%



