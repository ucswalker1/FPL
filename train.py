import joblib
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

from sklearn.model_selection import GridSearchCV, train_test_split
from sklearn.ensemble import RandomForestRegressor

from process.lib.config import *

class Model:

    def __init__(self, data: pd.DataFrame): 

        self.pos = data['pos'].values[0]
        self.regr = RandomForestRegressor(oob_score = True, n_estimators = 75000, max_features = 5, verbose=2)
        self.features = FEATURE_MAP[self.pos]

        data = data[data['team_spi'].notna()]

        self.X = data.loc[:, self.features]
        self.y = data['total_points']

    def train(self):

        X_train, X_test, y_train, y_test = train_test_split(self.X, self.y, test_size=0.10, random_state=1)
        self.regr.fit(X_train, y_train)

        joblib.dump(self.regr, f"/Users/calvinwalker/Documents/Projects/FPL/models/new/model_{int(self.pos)}.pkl")

        predict_train = self.regr.predict(X_train)
        predict_test = self.regr.predict(X_test)
        out_of_bag_predict = self.regr.oob_score

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

        importances = self.regr.feature_importances_

        plt.figure()
        plt.title("Feature importances")
        ax = plt.barh(list(self.features), importances, align="center")
        plt.savefig(f'/Users/calvinwalker/Desktop/feature_{int(self.pos)}', format='png')

        plt.figure()
        plt.scatter(predict_test, y_test)
        plt.savefig(f'/Users/calvinwalker/Desktop/result_{int(self.pos)}', format='png')

if __name__ == "__main__":

    df = pd.read_csv('/Users/calvinwalker/Documents/Projects/FPL/data/training_data.csv')

    FORWARDS = df[df['pos'] == 4]
    MIDFIELDERS = df[df['pos'] == 3]
    DEFENDERS = df[df['pos'] == 2]
    GOALKEEPERS = df[df['pos'] == 1]

    for position in [
                FORWARDS, 
                MIDFIELDERS, 
                DEFENDERS, 
                GOALKEEPERS,
    ]:

        model = Model(position)
        model.train()


### TODO ### 

# Priority:
# Continue tuning model, consider different specifications

# Low: 
# Transfer solver
# import team 
