import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

from sklearn.model_selection import train_test_split
from sklearn import svm

#Data cleaning 
df = pd.read_csv('/Users/calvinwalker/Documents/Projects/FPL/Fantasy-Premier-League/data/2022-23/gws/merged_gw.csv')

df = df.drop(columns=['xP', 'kickoff_time'])

positions = np.unique(df['position'])
position_to_int = {pos: i for i, pos in enumerate(positions)} 

teams = np.unique(df['team'])
team_to_int = {team: i for i, team in enumerate(teams)}

print(team_to_int)

df['position'] = [position_to_int[pos] for pos in df['position']]
df['team'] = [team_to_int[team] for team in df['team']]

X = df[df.columns.difference(['total_points', 'name'])]
y = df['total_points']

#split training data
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.5)

#fit model
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
plt.show()



### Model ### 


#split between gk, def, mid, fw 

#stats are rolling last 5-10 gws 
#results last time out in this fixture ? 

# y variable is total points 





