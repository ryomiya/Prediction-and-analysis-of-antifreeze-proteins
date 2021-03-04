import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
import lightgbm as lgb_original
import optuna.integration.lightgbm as lgb
import optuna
from sklearn.metrics import accuracy_score
import sklearn
from sklearn import metrics

df = pd.read_csv("all_AP.csv")

negative = df[0:9193]
positive = df[9193:]
negative = negative.sample(frac=1, random_state=0)
positive = positive.sample(frac=1, random_state=0)

train_negative = negative[0:240]
val_negative = negative[240:300]
test_negative = negative[300:]

train_positive = positive[0:240]
val_positive = positive[240:300]
test_positive = positive[300:]

train = pd.concat([train_negative, train_positive])
val = pd.concat([val_negative, val_positive])
test = pd.concat([test_negative, test_positive])

train = train.sample(frac=1, random_state=1)
val = val.sample(frac=1, random_state=1)
test = test.sample(frac=1, random_state=1)

y_train = train['class']
X_train = train.drop('class', axis=1)

y_val = val['class']
X_val = val.drop('class', axis=1)

y_test = test['class']
X_test = test.drop('class', axis=1)

lgb_train = lgb.Dataset(X_train, y_train)
lgb_eval = lgb.Dataset(X_val, y_val, reference=lgb_train)

params = {
        'objective': 'binary',
        'metric': 'auc',
        }

best_params, history = dict(), list()

model = lgb.train(params, lgb_train, valid_sets=lgb_eval,
                  num_boost_round=500,
                  early_stopping_rounds=20,
                 )

best_params = model.params
model_best = lgb_original.train(best_params, lgb_train,
                                num_boost_round=1000,
                                valid_sets=lgb_eval,
                                early_stopping_rounds=20)

y_pred_test = np.rint(model_best.predict(X_test))

table=sklearn.metrics.confusion_matrix(y_test, y_pred_test)
tn,fp,fn,tp=table[0][0],table[0][1],table[1][0],table[1][1]
ACC = (tp+tn)/(tp+fp+fn+tn)
REC = tp/(tp+fn)
SPE = tn/(tn+fp)

ACC = str(ACC).encode('utf-8','ignore')
REC = str(REC).encode('utf-8','ignore')
SPE = str(SPE).encode('utf-8','ignore')

li = ['ACC:', str(ACC_ave), '¥n', 'SPE:', str(SPE_ave), '¥n', 'REC:', str(REC_ave), '¥n', 'F1:', str(F1_ave), '¥n', 'MCC:', str(MCC_ave)]

with open('DatasetAP_evidence.txt', 'a') as f:
    f.writelines(li)
