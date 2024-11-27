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

#list_pollutants =['CO','NO','NO2','NOX','O3',"SO2"] #COLUMNS TO BE PREDICTED

list_var =['TMP','RH','WDR','WSP',"PM10","PM25"] #LIST OF COLUMNS TO PREDICT DATA

polluant = "CO" #POLLUTANT TO PREDICT

X = poll[list_var]
y = poll[polluant]

X_train, X_test, y_train, y_test = train_test_split(X, y)

#preprocessing
scaler = StandardScaler()
scaler.fit(X_train)
#StandardScaler(copy=True, with_mean=True, with_std=True)

X_train = scaler.transform(X_train)
X_test = scaler.transform(X_test)


#TRAINING
mlp = MLPRegressor(hidden_layer_sizes=(40,80,40),max_iter=500,solver = 
'adam',verbose=True,alpha=.1)
mlp.fit(X_train,y_train)


#EVALUATION
predictions = mlp.predict(X_test)
score = metrics.r2_score(y_test, predictions)
print(); print(score)


#figure
plt.figure(figsize=(10,10))     
sns.regplot(y_test, predictions, fit_reg=True, scatter_kws={"s": 100})
plt.ylabel("real values")
plt.title("Pollutant: "+polluant+" . R2 score:"+str(score))
plt.xlabel("predicted values")
plt.show()
#print(confusion_matrix(y_test,predictions))
#print(classification_report(y_test,predictions))
