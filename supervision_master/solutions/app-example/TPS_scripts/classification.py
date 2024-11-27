import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.neural_network import MLPClassifier
from sklearn.metrics import classification_report,confusion_matrix
from sklearn.neural_network import MLPRegressor
from sklearn import metrics
import matplotlib.pyplot as plt    
import seaborn as sns




poll = pd.read_csv('polluants.csv')

list_pollutants =['CO','NO','NO2','NOX','O3','PM10','PM25',"SO2"]
list_var =['T2MMEAN','TMP','RH','WDR','WSP',"T2MMAX","T2MMIN","HOURNORAIN"]

#X = poll.drop(list_pollutants,axis=1)
X = poll[list_var]
y = poll['CO'] * 10
y = y.astype(int)


X_train, X_test, y_train, y_test = train_test_split(X, y)


#preprocessing
scaler = StandardScaler()
scaler.fit(X_train)
#StandardScaler(copy=True, with_mean=True, with_std=True)

X_train = scaler.transform(X_train)
X_test = scaler.transform(X_test)


#TRAINING
clf = MLPClassifier(solver='adam',activation="tanh",max_iter=300, alpha=1e-5, hidden_layer_sizes=(100,100),verbose=True)

clf.fit(X_train, y_train)



#EVALUATION
predictions = clf.predict(X_test)

print(confusion_matrix(y_test,predictions))
print(classification_report(y_test,predictions))


plt.figure(figsize=(10,10))     
sns.regplot(y_test, predictions, fit_reg=True, scatter_kws={"s": 100})
plt.show()