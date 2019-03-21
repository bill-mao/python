'''
https://tianchi.aliyun.com/dataset/notebook/detail?postId=4796

[description]

Variables:
    feature {[type]} -- [description]
    data {[type]} -- [description]
    print(data['label'].value_counts()) {[type]} -- [description]
    train, test {[type]} -- [description]
    predictors {list} -- [description]
    print(len(predictors), predictors) {[type]} -- [description]
    trainSub, validSub {[type]} -- [description]
    model {[type]} -- [description]
    validSub['pred_prob'] {[type]} -- [description]
    validgroup {[type]} -- [description]
    aucs {list} -- [description]
    for i in validgroup: {[type]} -- [description]
    print(np.average(aucs)) {[type]} -- [description]
    model {[type]} -- [description]
    model.fit(trainSub[predictors], trainSub['label']) {[type]} -- [description]
    validSub['pred_prob'] {[type]} -- [description]
    validgroup {[type]} -- [description]
    aucs {list} -- [description]
    for i in validgroup: {[type]} -- [description]
    print(np.average(aucs)) {[type]} -- [description]
    y_test_pred {[type]} -- [description]
    submit {[type]} -- [description]
    submit['label'] {[type]} -- [description]
    submit.to_csv('submit2.csv', index {[type]} -- [description]
    submit.head() {[type]} -- [description]
'''

def userFeature(df):
    u = df[['User_id']].copy().drop_duplicates()
    
    # u_coupon_count : num of coupon received by user
    u1 = df[df['Date_received'] != 'null'][['User_id']].copy()
    u1['u_coupon_count'] = 1
    u1 = u1.groupby(['User_id'], as_index = False).count()

    # u_buy_count : times of user buy offline (with or without coupon)
    u2 = df[df['Date'] != 'null'][['User_id']].copy()
    u2['u_buy_count'] = 1
    u2 = u2.groupby(['User_id'], as_index = False).count()

    # u_buy_with_coupon : times of user buy offline (with coupon)
    u3 = df[((df['Date'] != 'null') & (df['Date_received'] != 'null'))][['User_id']].copy()
    u3['u_buy_with_coupon'] = 1
    u3 = u3.groupby(['User_id'], as_index = False).count()

    # u_merchant_count : num of merchant user bought from
    u4 = df[df['Date'] != 'null'][['User_id', 'Merchant_id']].copy()
    u4.drop_duplicates(inplace = True)
    u4 = u4.groupby(['User_id'], as_index = False).count()
    u4.rename(columns = {'Merchant_id':'u_merchant_count'}, inplace = True)

    # u_min_distance
    utmp = df[(df['Date'] != 'null') & (df['Date_received'] != 'null')][['User_id', 'distance']].copy()
    utmp.replace(-1, np.nan, inplace = True)
    u5 = utmp.groupby(['User_id'], as_index = False).min()
    u5.rename(columns = {'distance':'u_min_distance'}, inplace = True)
    u6 = utmp.groupby(['User_id'], as_index = False).max()
    u6.rename(columns = {'distance':'u_max_distance'}, inplace = True)
    u7 = utmp.groupby(['User_id'], as_index = False).mean()
    u7.rename(columns = {'distance':'u_mean_distance'}, inplace = True)
    u8 = utmp.groupby(['User_id'], as_index = False).median()
    u8.rename(columns = {'distance':'u_median_distance'}, inplace = True)

    user_feature = pd.merge(u, u1, on = 'User_id', how = 'left')
    user_feature = pd.merge(user_feature, u2, on = 'User_id', how = 'left')
    user_feature = pd.merge(user_feature, u3, on = 'User_id', how = 'left')
    user_feature = pd.merge(user_feature, u4, on = 'User_id', how = 'left')
    user_feature = pd.merge(user_feature, u5, on = 'User_id', how = 'left')
    user_feature = pd.merge(user_feature, u6, on = 'User_id', how = 'left')
    user_feature = pd.merge(user_feature, u7, on = 'User_id', how = 'left')
    user_feature = pd.merge(user_feature, u8, on = 'User_id', how = 'left')

    user_feature['u_use_coupon_rate'] = user_feature['u_buy_with_coupon'].astype('float')/user_feature['u_coupon_count'].astype('float')
    user_feature['u_buy_with_coupon_rate'] = user_feature['u_buy_with_coupon'].astype('float')/user_feature['u_buy_count'].astype('float')
    user_feature = user_feature.fillna(0)
    
    print(user_feature.columns.tolist())
    return user_feature


def merchantFeature(df):
    m = df[['Merchant_id']].copy().drop_duplicates()

    # m_coupon_count : num of coupon from merchant
    m1 = df[df['Date_received'] != 'null'][['Merchant_id']].copy()
    m1['m_coupon_count'] = 1
    m1 = m1.groupby(['Merchant_id'], as_index = False).count()

    # m_sale_count : num of sale from merchant (with or without coupon)
    m2 = df[df['Date'] != 'null'][['Merchant_id']].copy()
    m2['m_sale_count'] = 1
    m2 = m2.groupby(['Merchant_id'], as_index = False).count()

    # m_sale_with_coupon : num of sale from merchant with coupon usage
    m3 = df[(df['Date'] != 'null') & (df['Date_received'] != 'null')][['Merchant_id']].copy()
    m3['m_sale_with_coupon'] = 1
    m3 = m3.groupby(['Merchant_id'], as_index = False).count()

    # m_min_distance
    mtmp = df[(df['Date'] != 'null') & (df['Date_received'] != 'null')][['Merchant_id', 'distance']].copy()
    mtmp.replace(-1, np.nan, inplace = True)
    m4 = mtmp.groupby(['Merchant_id'], as_index = False).min()
    m4.rename(columns = {'distance':'m_min_distance'}, inplace = True)
    m5 = mtmp.groupby(['Merchant_id'], as_index = False).max()
    m5.rename(columns = {'distance':'m_max_distance'}, inplace = True)
    m6 = mtmp.groupby(['Merchant_id'], as_index = False).mean()
    m6.rename(columns = {'distance':'m_mean_distance'}, inplace = True)
    m7 = mtmp.groupby(['Merchant_id'], as_index = False).median()
    m7.rename(columns = {'distance':'m_median_distance'}, inplace = True)

    merchant_feature = pd.merge(m, m1, on = 'Merchant_id', how = 'left')
    merchant_feature = pd.merge(merchant_feature, m2, on = 'Merchant_id', how = 'left')
    merchant_feature = pd.merge(merchant_feature, m3, on = 'Merchant_id', how = 'left')
    merchant_feature = pd.merge(merchant_feature, m4, on = 'Merchant_id', how = 'left')
    merchant_feature = pd.merge(merchant_feature, m5, on = 'Merchant_id', how = 'left')
    merchant_feature = pd.merge(merchant_feature, m6, on = 'Merchant_id', how = 'left')
    merchant_feature = pd.merge(merchant_feature, m7, on = 'Merchant_id', how = 'left')

    merchant_feature['m_coupon_use_rate'] = merchant_feature['m_sale_with_coupon'].astype('float')/merchant_feature['m_coupon_count'].astype('float')
    merchant_feature['m_sale_with_coupon_rate'] = merchant_feature['m_sale_with_coupon'].astype('float')/merchant_feature['m_sale_count'].astype('float')
    merchant_feature = merchant_feature.fillna(0)
    
    print(merchant_feature.columns.tolist())
    return merchant_feature


def usermerchantFeature(df):

    um = df[['User_id', 'Merchant_id']].copy().drop_duplicates()

    um1 = df[['User_id', 'Merchant_id']].copy()
    um1['um_count'] = 1
    um1 = um1.groupby(['User_id', 'Merchant_id'], as_index = False).count()

    um2 = df[df['Date'] != 'null'][['User_id', 'Merchant_id']].copy()
    um2['um_buy_count'] = 1
    um2 = um2.groupby(['User_id', 'Merchant_id'], as_index = False).count()

    um3 = df[df['Date_received'] != 'null'][['User_id', 'Merchant_id']].copy()
    um3['um_coupon_count'] = 1
    um3 = um3.groupby(['User_id', 'Merchant_id'], as_index = False).count()

    um4 = df[(df['Date_received'] != 'null') & (df['Date'] != 'null')][['User_id', 'Merchant_id']].copy()
    um4['um_buy_with_coupon'] = 1
    um4 = um4.groupby(['User_id', 'Merchant_id'], as_index = False).count()

    user_merchant_feature = pd.merge(um, um1, on = ['User_id','Merchant_id'], how = 'left')
    user_merchant_feature = pd.merge(user_merchant_feature, um2, on = ['User_id','Merchant_id'], how = 'left')
    user_merchant_feature = pd.merge(user_merchant_feature, um3, on = ['User_id','Merchant_id'], how = 'left')
    user_merchant_feature = pd.merge(user_merchant_feature, um4, on = ['User_id','Merchant_id'], how = 'left')
    user_merchant_feature = user_merchant_feature.fillna(0)

    user_merchant_feature['um_buy_rate'] = user_merchant_feature['um_buy_count'].astype('float')/user_merchant_feature['um_count'].astype('float')
    user_merchant_feature['um_coupon_use_rate'] = user_merchant_feature['um_buy_with_coupon'].astype('float')/user_merchant_feature['um_coupon_count'].astype('float')
    user_merchant_feature['um_buy_with_coupon_rate'] = user_merchant_feature['um_buy_with_coupon'].astype('float')/user_merchant_feature['um_buy_count'].astype('float')
    user_merchant_feature = user_merchant_feature.fillna(0)

    print(user_merchant_feature.columns.tolist())
    return user_merchant_feature


def featureProcess(feature, train, test):
    """
    feature engineering from feature data
    then assign user, merchant, and user_merchant feature for train and test 
    """
    
    user_feature = userFeature(feature)
    merchant_feature = merchantFeature(feature)
    user_merchant_feature = usermerchantFeature(feature)
    
    train = pd.merge(train, user_feature, on = 'User_id', how = 'left')
    train = pd.merge(train, merchant_feature, on = 'Merchant_id', how = 'left')
    train = pd.merge(train, user_merchant_feature, on = ['User_id', 'Merchant_id'], how = 'left')
    train = train.fillna(0)
    
    test = pd.merge(test, user_feature, on = 'User_id', how = 'left')
    test = pd.merge(test, merchant_feature, on = 'Merchant_id', how = 'left')
    test = pd.merge(test, user_merchant_feature, on = ['User_id', 'Merchant_id'], how = 'left')
    test = test.fillna(0)
    
    return train, test


# model1
predictors = original_feature
print(predictors)

def check_model(data, predictors):
    
    classifier = lambda: SGDClassifier(
        loss='log', 
        penalty='elasticnet', 
        fit_intercept=True, 
        max_iter=100, 
        shuffle=True, 
        n_jobs=1,
        class_weight=None)

    model = Pipeline(steps=[
        ('ss', StandardScaler()),
        ('en', classifier())
    ])

    parameters = {
        'en__alpha': [ 0.001, 0.01, 0.1],
        'en__l1_ratio': [ 0.001, 0.01, 0.1]
    }

    folder = StratifiedKFold(n_splits=3, shuffle=True)
    
    grid_search = GridSearchCV(
        model, 
        parameters, 
        cv=folder, 
        n_jobs=-1, 
        verbose=1)
    grid_search = grid_search.fit(data[predictors], 
                                  data['label'])
    
    return grid_search

if not os.path.isfile('1_model.pkl'):
    model = check_model(train, predictors)
    print(model.best_score_)
    print(model.best_params_)
    with open('1_model.pkl', 'wb') as f:
        pickle.dump(model, f)
else:
    with open('1_model.pkl', 'rb') as f:
        model = pickle.load(f)

# -=-=-==--=-==-=-=- 

# repeat result above and process dftest data
feature = dfoff[(dfoff['Date'] < '20160516') | ((dfoff['Date'] == 'null') & (dfoff['Date_received'] < '20160516'))].copy()
data = dfoff[(dfoff['Date_received'] >= '20160516') & (dfoff['Date_received'] <= '20160615')].copy()
print(data['label'].value_counts())

# feature engineering
train, test = featureProcess(feature, data, dftest)


# features
predictors = ['discount_rate', 'discount_man', 'discount_jian', 'discount_type', 'distance',
              'weekday', 'weekday_1', 'weekday_2', 'weekday_3', 'weekday_4', 'weekday_5', 'weekday_6', 
              'weekday_7', 'weekday_type', 
              'u_coupon_count', 'u_buy_count', 'u_buy_with_coupon', 'u_merchant_count', 'u_min_distance', 
              'u_max_distance', 'u_mean_distance', 'u_median_distance', 'u_use_coupon_rate', 'u_buy_with_coupon_rate', 
              'm_coupon_count', 'm_sale_count', 'm_sale_with_coupon', 'm_min_distance', 'm_max_distance',
              'm_mean_distance', 'm_median_distance', 'm_coupon_use_rate', 'm_sale_with_coupon_rate', 'um_count', 'um_buy_count', 
              'um_coupon_count', 'um_buy_with_coupon', 'um_buy_rate', 'um_coupon_use_rate', 'um_buy_with_coupon_rate']
print(len(predictors), predictors)

trainSub, validSub = train_test_split(train, test_size = 0.2, stratify = train['label'], random_state=100)


# linear model
model = check_model(trainSub, predictors)

validSub['pred_prob'] = model.predict_proba(validSub[predictors])[:,1]
validgroup = validSub.groupby(['Coupon_id'])
aucs = []
for i in validgroup:
    tmpdf = i[1] 
    if len(tmpdf['label'].unique()) != 2:
        continue
    fpr, tpr, thresholds = roc_curve(tmpdf['label'], tmpdf['pred_prob'], pos_label=1)
    aucs.append(auc(fpr, tpr))
print(np.average(aucs))


model = lgb.LGBMClassifier(
                    learning_rate = 0.01,
                    boosting_type = 'gbdt',
                    objective = 'binary',
                    metric = 'logloss',
                    max_depth = 5,
                    sub_feature = 0.7,
                    num_leaves = 3,
                    colsample_bytree = 0.7,
                    n_estimators = 5000,
                    early_stop = 50,
                    verbose = -1)
model.fit(trainSub[predictors], trainSub['label'])


validSub['pred_prob'] = model.predict_proba(validSub[predictors])[:,1]
validgroup = validSub.groupby(['Coupon_id'])
aucs = []
for i in validgroup:
    tmpdf = i[1] 
    if len(tmpdf['label'].unique()) != 2:
        continue
    fpr, tpr, thresholds = roc_curve(tmpdf['label'], tmpdf['pred_prob'], pos_label=1)
    aucs.append(auc(fpr, tpr))
print(np.average(aucs))


# test prediction for submission
y_test_pred = model.predict_proba(test[predictors])
submit = test[['User_id','Coupon_id','Date_received']].copy()
submit['label'] = y_test_pred[:,1]
submit.to_csv('submit2.csv', index=False, header=False)
submit.head()

