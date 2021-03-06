import preprocess.file_processing as fp
import preprocess.data_preprocessing as dp
import AI_model.model as model

import argparse
import pandas as pd

'''
##############################################################################
 2021.10.04 16:22 DongWon Choo
 executor 함수 수정
  - DB 저장 위치
  - SmartShip mmsi 값 받아옴
  - SmartShip 데이터 경로 받아옴
  - verbose로 진행 상황 확인할 수 있음
 execute.py Argument 추가
  - DB 저장 위치(Requirement)
  - SmartShip mmsi(Default값 있음)
  - SmartShip data path (Default값 있음)
  - verbose로 진행 상황 확인
  사용 예시는 execute_script.sh에 있음
##############################################################################
'''

def executor(
        data_folder,
        xml_folder,
        json_folder,
        db_folder,
        smartship_mmsi = '538008382',
        smartship_data_path = 'data/smartship_data/538008382_SmartShipData.csv',
        verbose=False,
    ):
    if verbose: print(f'Check data folder {data_folder}')
    file_dict = fp.take_file_path(data_folder)
    if verbose: print(file_dict.keys())

    dataframe_list = list()
    for _key, _path_list in file_dict.items():
        if verbose: print(f'Load data, Ship : {_key}')
        __dataframe = fp.merge_excel_file(_path_list)
        dataframe_list.append(__dataframe)
    dataframe_t = pd.concat(dataframe_list)
    del dataframe_list
    if verbose: print(f'Finish load data')

    if verbose: print(f"Preprocessing data")
    pp_dataframe = dp.preprocessing_excel_df(
        data_excel = dataframe_t,
    )

    if verbose: print(f"Generate DataBase")
    database = dp.generate_db(
        pp_dataframe   = pp_dataframe,
        db_save_folder = db_folder,
        save_file      = True,
    )

    if verbose: print(f'Generate XML files')
    dp.generate_xml(
        xml_folder   = xml_folder,
        pp_dataframe = pp_dataframe,
        database     = database,
    )

    if verbose: print(f'Generate JSON files')
    dp.generate_json(
        json_folder         = json_folder,
        database             = database,
        mmsi                = smartship_mmsi,
        smartship_data_path = smartship_data_path,
    )

    #if verbose: print(f'Finish')
        

def AI_model_compare(train_data_path,result_save_path,verbose=False):

    if verbose: print(f'Model compare Start')

    if verbose: print(f'Load data')
    dataframe = model.import_SmartShip_AI_data(train_data_path)
    kfold_data = model.generate_kfold_data(
        dataframe= dataframe,
        n_splits = 5,
        shuffle = True,
    )
    del dataframe
    
    if verbose: print(f'Training LinearRegression model')
    LR_model = model.LinearRegression_model(
        kfold_data = kfold_data
    )
    
    if verbose: print(f'Training PolynomialRegression model')
    PR_model = model.PolynomialRegression_model(
        kfold_data = kfold_data
    )

    if verbose: print(f'Training GradientBoost model')
    GBR_model = model.GradientBoost_model(
        kfold_data = kfold_data
    )

    if verbose: print(f'Training RandomForest model')
    RFR_model = model.RandomForest_model(
        kfold_data = kfold_data
    )

    if verbose: print(f'Training VotingRegressor model')
    VR_model = model.VotingRegressor_model(
        kfold_data = kfold_data
    )

    if verbose: print(f'Training MultiLayerPerceptron model')
    MLP_model = model.MultiLayerPerceptron_model(
        kfold_data = kfold_data
    )


    result_dict = {
            'method' : [
                    'LinearRegression'    ,
                    'PolynomialRegression',
                    'GradientBoost'       ,
                    'RandomForest'        ,
                    'VotingRegressor'     ,
                    'MultiLayerPerceptron',
                ],
            'RMSE'   : [
                    LR_model.kfold_RMSE,
                    PR_model.kfold_RMSE,
                    GBR_model.kfold_RMSE,
                    RFR_model.kfold_RMSE,
                    VR_model.kfold_RMSE,
                    MLP_model.kfold_RMSE,
                ],
    }
    result_df = pd.DataFrame(result_dict)
    dp.check_folder_exist(result_save_path)
    result_df.to_csv(result_save_path,index=False)

def main():
    parser = argparse.ArgumentParser(description='Hackaton')

    parser.add_argument('-f', '--data_folder',required=True,help='Data file folder')
    parser.add_argument('-tr', '--ai_train', required=True, help='AI_train file folder')
    parser.add_argument('-x', '--xml_folder', required=True, help='XML file folder')
    parser.add_argument('-j', '--json_folder', required=True, help='JSON file folder')
    parser.add_argument('-db', '--database', required=True, help='Database file folder')
    parser.add_argument('-ai', '--ai_result', required=True, help='AI model result rmse file folder')
    parser.add_argument('--SH_mmsi', default='538008382', help='SmartShip MMSI')
    parser.add_argument(
            '--SH_data',
            default='./data/smartship_data/538008382_SmartShipData.csv',
            help='SmartShip MMSI'
        )
    parser.add_argument('-v','--verbose',default=False, help='Show progress message')

    args = parser.parse_args()
    executor(
        data_folder         = args.data_folder,
        xml_folder          = args.xml_folder,
        json_folder         = args.json_folder,
        db_folder           = args.database,
        smartship_mmsi      = args.SH_mmsi,
        smartship_data_path = args.SH_data,
        verbose             = args.verbose,
    )

    AI_model_compare(
        train_data_path  = args.ai_train,
        result_save_path = args.ai_result,
        verbose          = args.verbose,
    )


if __name__ == '__main__':
    main()
