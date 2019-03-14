# encoding=utf-8

import pandas as pd
import time

from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
from sklearn.metrics import recall_score
from sklearn.tree import DecisionTreeClassifier
from sklearn.model_selection import cross_val_score
from sklearn import metrics
from sklearn.metrics import auc

if __name__ == '__main__':

    print("Start read data...")
    time_1 = time.time()

    raw_data = pd.read_csv('winequality-red.csv')
    data = raw_data.values
    
    features = data[:,0:6]
    labels = data[:,6]

    # 随机选取33%数据作为测试集，剩余为训练集
    train_features, test_features, train_labels, test_labels = train_test_split(features, labels, test_size=0.33, random_state=0)

    time_2 = time.time()
    print('read data cost %f seconds' % (time_2 - time_1))
   

    print('Start training...') 
    # criterion可选‘gini’, ‘entropy’，默认为gini(对应CART算法)，entropy为信息增益（对应ID3算法）
    #clf = DecisionTreeClassifier(criterion='gini')
    clf = DecisionTreeClassifier(criterion='entropy')
    clf.fit(train_features.astype('float'),train_labels.astype('int'))
    time_3 = time.time()
    print('training cost %f seconds' % (time_3 - time_2))


    print('Start predicting...')
    test_predict = clf.predict(test_features.astype('float'))
    time_4 = time.time()
    print('predicting cost %f seconds' % (time_4 - time_3))


    score = accuracy_score(test_labels.astype('int'), test_predict.astype('int'))
    print("The accruacy score is %f" % score)
    score1 = recall_score(test_labels.astype('int'),test_predict.astype('int'),average='macro')
    print("The recall score based on macro is %f" % score1)
    score1 = recall_score(test_labels.astype('int'),test_predict.astype('int'),average='micro')
    print("The recall score based on micro is %f" % score1)
    score1 = recall_score(test_labels.astype('int'),test_predict.astype('int'),average='weighted')
    print("The recall score based on weighted is %f" % score1)
    score1 = cross_val_score(clf,features,labels,cv=10)
    print("Accuracy: %0.2f (+/- %0.2f)" % (score1.mean(), score1.std() * 2))
