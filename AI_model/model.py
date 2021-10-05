import numpy as np
import pandas as pd

import sklearn as sk
from sklearn.model_selection import train_test_split
from sklearn.ensemble import GradientBoostingRegressor, RandomForestRegressor, AdaBoostRegressor, VotingRegressor


def rmse(pred_y, true_y):
    pred_y = np.array(pred_y).reshape(-1,)
    true_y = np.array(true_y).reshape(-1,)
    assert pred_y.shape == true_y.shape, f'Check shape, pred:{pred_y.shape}, true:{true_y.shape}'
    return np.sqrt(np.mean(np.power(pred_y-true_y,2)))

def import_SmartShip_AI_data(train_data_path):
    dataframe = pd.read_csv(train_data_path)
    return dataframe

def data_split(dataframe, test_ratio=0.2):
    x_data = dataframe[['EngineLoad_%','WindSpeed','Draught','PropellerRPM']].to_numpy()
    y_data = dataframe['VesselSpeed_km/h'].to_numpy()
    train_x, test_x, train_y, test_y = train_test_split(
                                            x_data, y_data,
                                            test_size = test_ratio,
                                        )
    return train_x, train_y, test_x,test_y


class machine_learning_model:
    def __init__(self,
        train_x,
        train_y,
        test_x,
        test_y,
    ):
        train_data = (train_x, train_y)
        test_data = (test_x, test_y)

        self.model = self.Model()
        self.model.fit(*train_data)
        self.test_RMSE = self.Model_eval(*test_data)

    def Model(self,):
        # example
        GBR = GradientBoostingRegressor(
            learning_rate = 0.1,
            n_estimators = 200,
            max_depth = 4,
            random_state = 123,
            verbose = 0,
        )
        return GBR

    def Model_eval(self,x,y):
        test_pred_y = self.model.predict(x)
        test_RMSE   = rmse(test_pred_y,y)
        return test_RMSE


class GradientBoost_model(machine_learning_model):
    def Model(self,):
        GBR = GradientBoostingRegressor(
            learning_rate = 0.1,
            n_estimators = 200,
            max_depth = 4,
            random_state = 123,
            verbose = 0,
        )
        return GBR

class RandomForest_model(machine_learning_model):
    def Model(self,):
        RFR = RandomForestRegressor(
            n_estimators = 20,
            max_depth = 8,
            #n_jobs = 4,
            #warm_start=True,
            random_state = 1234,
            verbose = 0,
        )
        return RFR


class VotingRegressor_model(machine_learning_model):
    def Model(self,):
        tmp_GBR = GradientBoostingRegressor(
            learning_rate = 0.1,
            n_estimators = 200,
            max_depth = 4,
            random_state = 123,
            verbose = 0,
        )
        tmp_RFR = RandomForestRegressor(
            n_estimators = 20,
            max_depth = 8,
            #n_jobs = 4,
            #warm_start=True,
            random_state = 1234,
            verbose = 0,
        )
        VR = VotingRegressor(
            estimators = [('GB',tmp_GBR),('RFR',tmp_RFR)]
        )
        return VR
    


if __name__ == '__main__':
    data_path = '../data/AI_train_data/538008382_SmartShipData_forAI.csv'

    dataframe = import_SmartShip_AI_data(data_path)
    train_x, train_y, test_x,test_y = data_split(dataframe,test_ratio=0.2)
    del dataframe

    GBR_model = GradientBoost_model(
        train_x = train_x,
        train_y = train_y,
        test_x  = test_x,
        test_y  = test_y,
    )

    RFR_model = RandomForest_model(
        train_x = train_x,
        train_y = train_y,
        test_x  = test_x,
        test_y  = test_y,
    )

    VR_model = VotingRegressor_model(
        train_x = train_x,
        train_y = train_y,
        test_x  = test_x,
        test_y  = test_y,
    )

    print(f'GradientBoost_model RMSE : {GBR_model.test_RMSE}')
    print(f'RandomForest_model RMSE : {RFR_model.test_RMSE}')
    print(f'VotingRegressor_model RMSE : {VR_model.test_RMSE}')
