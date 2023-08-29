import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

from sklearn.model_selection import GridSearchCV, train_test_split
from sklearn.ensemble import RandomForestRegressor

from .process.lib.config import *

df = pd.read_csv("/Users/calvinwalker/Documents/Projects/FPL/data/2022-23/cleaned_averages")

df = df[df["GW"] >= 6]
df.drop(columns=UNUSED)

X = df.loc[:, FEATURES]
y = df["total_points"]

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.25, random_state=1)

regr = RandomForestRegressor(oob_score = True, n_estimators = 100000, max_features = 5, verbose=3, n_jobs=2)
regr.fit(X_train, y_train)

predict_train = regr.predict(X_train)
predict_test = regr.predict(X_test)
out_of_bag_predict = regr.oob_score

residuals = predict_train - y_train
residuals2 = predict_test - y_test
residuals3 = out_of_bag_predict - y_train

mse_train = np.sqrt(sum(residuals**2)/len(residuals))
mse_test = np.sqrt(sum(residuals2**2)/len(residuals2))
mse_out_of_bag = np.sqrt(sum(residuals3**2)/len(residuals3))

abs_train = sum(abs(residuals))/len(residuals)
abs_test = sum(abs(residuals2))/len(residuals2)
abs_out_of_bag = sum(abs(residuals3))/len(residuals3)

print('sqrt(MSE) on train set: ', mse_train)
print('sqrt(MSE) on test set: ', mse_test)
print('Mean Absolute value of residuals on train set: ', abs_train)
print('Mean Absolute value of residuals on test set: ', abs_test)

importances = regr.feature_importances_

plt.figure()
plt.title("Feature importances")
ax = plt.barh(list(FEATURES), importances, align="center")
plt.show()

plt.figure()
plt.scatter(predict_test, y_test)
plt.show()

### TODO ### 

# GOAL for EOD: display some predictions for next week #

# Priority: 
# Continue tuning model, consider different specifications 
# Pipeline FPL API to update data 
# Create bones of website

# Lower: 
# Merge understat data to past seasons for more training data

# Low: 
# Transfer solver
# import team 
