import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

from sklearn.model_selection import GridSearchCV, train_test_split
from sklearn import svm

from lib.config import *

df = pd.read_csv("/Users/calvinwalker/Documents/Projects/FPL/data/2022-23/cleaned_averages")

df = df[df["GW"] >= 6]
df.drop(columns=UNUSED)

positions = np.unique(df['position'])
position_to_int = {pos: i for i, pos in enumerate(positions)} 

teams = np.unique(df['team'])
team_to_int = {team: i for i, team in enumerate(teams)}

df['position'] = [position_to_int[pos] for pos in df['position']]
df['team'] = [team_to_int[team] for team in df['team']]

X = df.loc[:, FEATURES]
y = df["goals_scored"]

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.1)

regr = svm.SVR() 
regr.fit(X_train, y_train)

predict_train = regr.predict(X_train)
predict_test = regr.predict(X_test)

residuals = predict_train - y_train
residuals2 = predict_test - y_test

mse_train = np.sqrt(sum(residuals**2)/len(residuals))
mse_test = np.sqrt(sum(residuals2**2)/len(residuals2))

abs_train = sum(abs(residuals))/len(residuals)
abs_test = sum(abs(residuals2))/len(residuals2)

print('sqrt(MSE) on train set: ', mse_train)
print('sqrt(MSE) on test set: ', mse_test)
print('Mean Absolute value of residuals on train set: ', abs_train)
print('Mean Absolute value of residuals on test set: ', abs_test)

plt.figure()
plt.scatter(predict_test, y_test)
# plt.scatter(predict_train, y_train)
plt.show()








