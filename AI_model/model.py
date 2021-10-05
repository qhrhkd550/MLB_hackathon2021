import numpy as np
import pandas as pd

import sklearn as sk
from sklearn.model_selection import train_test_split, KFold
from sklearn.ensemble import GradientBoostingRegressor, RandomForestRegressor, AdaBoostRegressor, VotingRegressor
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import PolynomialFeatures

import tensorflow as tf
import tensorflow.keras as k


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

def generate_kfold_data(dataframe,n_splits=5,shuffle=True):
    x_data = dataframe[['EngineLoad_%','WindSpeed','Draught','PropellerRPM']].to_numpy()
    y_data = dataframe['VesselSpeed_km/h'].to_numpy()
    kf = KFold(n_splits=n_splits, shuffle=shuffle)
    kfold_data_dict = {}
    for i, (_train_index, _test_index) in enumerate(kf.split(x_data)):
        kfold_data_dict[i] = {}
        kfold_data_dict[i]['train_x'] = x_data[_train_index]
        kfold_data_dict[i]['train_y'] = y_data[_train_index]
        kfold_data_dict[i]['test_x']  = x_data[_test_index]
        kfold_data_dict[i]['test_y']  = y_data[_test_index]
    return kfold_data_dict
    
    
    
    
class machine_learning_model:
    def __init__(self,
        kfold_data
    ):
        self.model = self.Model()
        self.kfold_RMSE = self.Model_eval_kfold(kfold_data)

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

    def Model_eval_kfold(self,kfold_data):
        rmse_list = list()
        for _fold_data in kfold_data.values():
            __train_data = (_fold_data['train_x'],_fold_data['train_y'])
            __test_data = (_fold_data['test_x'],_fold_data['test_y'])
            __model = self.Model()
            __model.fit(*__train_data)
            __rmse = self.calc_rmse(*__test_data,__model)
            rmse_list.append(__rmse)
        mean_rmse = np.mean(rmse_list)
        return mean_rmse

    def calc_rmse(self,x,y, model):
        pred_y = model.predict(x)
        model_rmse   = rmse(pred_y,y)
        return model_rmse


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
    
class LinearRegression_model(machine_learning_model):
    def Model(self, ):
        reg = LinearRegression()
        return reg
    
    
class PolynomialRegression_model(machine_learning_model):
    def Model(self, ):
        reg = LinearRegression()
        return reg
        
    def Model_eval_kfold(self,kfold_data):
        rmse_list = list()
        poly = PolynomialFeatures(degree=2, include_bias=True)
        for _fold_data in kfold_data.values():
            __train_data = (poly.fit_transform(_fold_data['train_x']),_fold_data['train_y'])
            __test_data = (poly.transform(_fold_data['test_x']),_fold_data['test_y'])            
            __model = self.Model()
            __model.fit(*__train_data)
            __rmse = self.calc_rmse(*__test_data,__model)
            rmse_list.append(__rmse)
        mean_rmse = np.mean(rmse_list)
        return mean_rmse


class MultiLayerPerceptron_model(machine_learning_model):
    def Model(self,):
        model = k.Sequential([
            k.layers.Dense(64,activation='relu'),
            k.layers.Dense(32,activation='relu'),
            k.layers.Dense(8,activation='relu'),
            k.layers.Dense(1,activation='linear'),
        ])
        model.compile(
            optimizer='adam',
            loss = 'mse',
        )
        return model


    def Model_eval_kfold(self,kfold_data):
        rmse_list = list()
        for _fold_data in kfold_data.values():
            __train_data = (_fold_data['train_x'],_fold_data['train_y'])
            __test_data = (_fold_data['test_x'],_fold_data['test_y'])
            __model = self.Model()
            __model.fit(*__train_data,
                epochs=20,
                verbose=0
            )
            __rmse = self.calc_rmse(*__test_data,__model)
            rmse_list.append(__rmse)
            del __model
        mean_rmse = np.mean(rmse_list)
        return mean_rmse



    

if __name__ == '__main__':
    data_path = '../data/AI_train_data/538008382_SmartShipData_forAI.csv'

    dataframe = import_SmartShip_AI_data(data_path)
    #train_x, train_y, test_x,test_y = data_split(dataframe,test_ratio=0.2)
    kfold_data = generate_kfold_data(
        dataframe= dataframe,
        n_splits = 5,
        shuffle = True,
    )
    del dataframe

    GBR_model = GradientBoost_model(
        kfold_data = kfold_data
    )

    RFR_model = RandomForest_model(
        kfold_data = kfold_data
    )

    VR_model = VotingRegressor_model(
        kfold_data = kfold_data
    )
    
    LR_model = LinearRegression_model(
        kfold_data = kfold_data
    )
    
    PR_model = PolynomialRegression_model(
        kfold_data = kfold_data
    )

    MLP_model = MultiLayerPerceptron_model(
        kfold_data = kfold_data
    )

    print(f'GradientBoost_model RMSE : {GBR_model.kfold_RMSE}')
    print(f'RandomForest_model RMSE : {RFR_model.kfold_RMSE}')
    print(f'VotingRegressor_model RMSE : {VR_model.kfold_RMSE}')
    print(f'LinearRegression_model RMSE : {LR_model.kfold_RMSE}')
    print(f'PolynomialRegression_model RMSE : {PR_model.kfold_RMSE}')
    print(f'MultiLayerPerceptron_model RMSE : {MLP_model.kfold_RMSE}')



