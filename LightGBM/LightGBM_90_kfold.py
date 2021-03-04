import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.model_selection import StratifiedKFold
import lightgbm as lgb_original
import optuna.integration.lightgbm as lgb
import optuna
from sklearn.metrics import accuracy_score
import sklearn
from sklearn import metrics
import matplotlib.pyplot as plt

df = pd.read_csv("all_cdhit90.csv")
df = df.sample(frac=1, random_state=0)

y = df['class']
X = df.drop('class', axis=1)

params = {
        'objective': 'binary',
        'metric': 'auc',
        'random_seed':0
        }

skf = StratifiedKFold(n_splits=5, shuffle=True, random_state=0)

ACC = []
PRE = []
SPE = []
REC = []
F1 = []
MCC = []

f_importance = np.zeros(X.shape[1])

auc_list = []
y_list = []
pred_list = []


for fold_index, (train_index,test_index) in enumerate(skf.split(X,y)):

    lgb_train = lgb.Dataset(X.iloc[train_index], y.iloc[train_index])
    lgb_eval =  lgb.Dataset(X.iloc[test_index], y.iloc[test_index], reference=lgb_train)

    model = lgb.train(params, lgb_train, valid_sets=lgb_eval,
                  num_boost_round=500,
                  early_stopping_rounds=20,
                  verbose_eval = 50,
                 )

    y_list.append(y.iloc[test_index].values.tolist())
    y_pred_test_pro = model.predict(X.iloc[test_index])
    pred_list.append(y_pred_test_pro.tolist())
    y_pred_test = np.rint(y_pred_test_pro)

    table=sklearn.metrics.confusion_matrix(y.iloc[test_index], y_pred_test)
    tn,fp,fn,tp=table[0][0],table[0][1],table[1][0],table[1][1]

    ACC.append((tp+tn)/(tp+fp+fn+tn))
    pre = tp/(tp+fp)
    PRE.append(pre)
    SPE.append(tn/(tn+fp))
    rec = tp/(tp+fn)
    REC.append(rec)
    F1.append((2*pre*rec)/(pre+rec))
    MCC.append((tp*tn-fp*fn)/((tp+fp)*(tp+fn)*(tn+fp)*(tn+fn))**(1/2))

    f_importance += np.array(model.feature_importance(importance_type='gain'))

    #ROC
    fpr, tpr, thresholds = metrics.roc_curve(y.iloc[test_index], y_pred_test_pro)
    auc = metrics.auc(fpr, tpr)
    auc_list.append(auc)

max_ = np.argmax(np.array(auc_list))
fpr, tpr, thresholds = metrics.roc_curve(y_list[max_], pred_list[max_])
plt.plot(fpr, tpr, label='ROC curve (area = %.2f)'%auc)
plt.legend()
plt.title('ROC curve (Dataset 90)')
plt.xlabel('FPR: False positive rate')
plt.ylabel('TPR: True positive rate')
plt.grid(True)
plt.rcParams["font.size"] = 12
plt.savefig('ROC_Dataset90.png')

ACC_ave = sum(ACC)/len(ACC)
PRE_ave = sum(PRE)/len(PRE)
SPE_ave = sum(SPE)/len(SPE)
REC_ave = sum(REC)/len(REC)
F1_ave = sum(F1)/len(F1)
MCC_ave = sum(MCC)/len(MCC)

f_importance2 = f_importance / np.sum(f_importance)
f_importance2

np.savetxt('Fimportance_Dataset90.csv', np.sort(f_importance2)[::-1], delimiter=',')

arg = np.argsort(f_importance)[::-1]

np.savetxt('Fimportance_arg_Dataset90.csv', arg.astype(np.uint64), delimiter=',')

ACC_ave = str(ACC_ave).encode('utf-8','ignore')
PRE_ave = str(PRE_ave).encode('utf-8','ignore')
SPE_ave = str(SPE_ave).encode('utf-8','ignore')
REC_ave = str(REC_ave).encode('utf-8','ignore')
F1_ave = str(F1_ave).encode('utf-8','ignore')
MCC_ave = str(MCC_ave).encode('utf-8','ignore')

li = ['ACC:', str(ACC_ave), '¥n', 'PRE', str(PRE_ave), '¥n', 'SPE:', str(SPE_ave), '¥n', 'REC:', str(REC_ave), '¥n', 'F1:', str(F1_ave), '¥n', 'MCC:', str(MCC_ave)]

with open('Dataset90_evidence.txt', 'a') as f:
    f.writelines(li)
