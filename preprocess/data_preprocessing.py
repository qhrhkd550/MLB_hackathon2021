import pandas as pd
import numpy as np
from pathlib import Path
from xml.etree.ElementTree import Element, dump, ElementTree
import json


'''
###########################################################################################
 2021.10.01. 22:15 DongWon Choo                                                           
 각 함수별 사용 방법은 if __name__ == '__main__': 아래에 넣어 두었음                     
 순서대로 사용하기만 하면 됨                                                             
 Json 만드는 부분 추가 부탁   
 ----------------------------------------------------------------------------------
 2021.10.02 Bokwang Hwang
 xml 파일 생성 위치 수정
 json 파일 생성 코드 추가
 ----------------------------------------------------------------------------------
 2021.10.04 16:20 DongWon Choo
 json 만드는 함수 수정 - mmsi 값 받아와서 그 데이터만 수행, SmartShip 데이터 경로 인자 추가
 json 빈 파일 만들도록 소스코드 수정
###########################################################################################
'''


def preprocessing_excel_df(data_excel):
    dataframe = header_update(data_excel)
    # 필요없는 칼럼 제거
    df_droped = dataframe.copy()
    df_droped.drop(
        ['SHIP_NAME', 'IMO', 'SOG', 'SOURCE', 'ETA', 'NAV_STATUS', 'NAV_STATUS_CODE', 'CALL_SIGN', 'VESSEL_TYPE',
        'VESSEL_TYPE_CODE', 'VESSEL_TYPE_CARGO', 'VESSEL_CLASS', 'LENGTH', 'WIDTH', 'FLAG', 'FLAG_CODE', 'COG',
        'ROT', 'HEADING', 'VESSEL_TYPE_MAIN', 'VESSEL_TYPE_SUB', 'MESSAGE_TYPE'], axis=1, inplace=True)

    # Convert data type
    pp_dataframe = df_droped.astype(
        {
            'MMSI' : 'category',
            'DESTINATION' : 'category',
        }
    )
    pp_dataframe['TRACKING_DATE'] = pd.to_datetime(pp_dataframe['TRACKING_DATE'])

    # Generate DESTINATION_KEY
    pp_dataframe = generate_DESTINATION_KEY(pp_dataframe)

    preprocessed_dataframe = pp_dataframe
    return preprocessed_dataframe


# 파일 저장하는 기능 사용시 False->True
def generate_db(pp_dataframe, db_save_folder='./db', save_file=False):
    mmsi_list = pp_dataframe['MMSI'].unique()

    df_sailing = pd.DataFrame(
        columns=['MMSI', 'DESTINATION', 'DRAUGHT', 'DESTINATION_KEY', 'first(DT_POS_UTC)', 'last(DT_POS_UTC)',
                 'count*(SEQ_NO)' ])

    for id_name, mmsi in enumerate(mmsi_list):
        df_new = pp_dataframe[pp_dataframe['MMSI'] == mmsi]


        # ------------------------------------------------------------------- 항차 별 feature 생성 -------------------------------------------------------------------------------------------------


        for sailing in range(1, max(df_new['DESTINATION_KEY']) + 1):
            tmp = df_new[df_new['DESTINATION_KEY'] == sailing]
            sailing_mmsi = str(tmp['MMSI'].iloc[0])
            sailing_destination = tmp['DESTINATION'].iloc[0]
            sailing_draught = tmp['DRAUGHT'].value_counts(sort=True).index.tolist()[0]
            sailing_destination_key = tmp['DESTINATION_KEY'].iloc[0]
            sailing_first = tmp['DT_POS_UTC'].iloc[0]
            sailing_last = tmp['DT_POS_UTC'].iloc[-1]
            sailing_count = len(tmp)

            data = {
                'MMSI': sailing_mmsi,
                'DESTINATION': sailing_destination,
                'DRAUGHT' : sailing_draught,
                'DESTINATION_KEY': sailing_destination_key,
                'first(DT_POS_UTC)': sailing_first,
                'last(DT_POS_UTC)': sailing_last,
                'count*(SEQ_NO)': sailing_count,

            }
            df_sailing = df_sailing.append(data, ignore_index=True)

    # Convert data type
    data_type = {
        'MMSI'             : 'category',
        'DESTINATION'      : 'category',
        'DRAUGHT'          : 'float16',
        'DESTINATION_KEY'  : 'int16',
        'count*(SEQ_NO)'   : 'int32',
    }

    df_sailing = df_sailing.astype(data_type)
    df_sailing['first(DT_POS_UTC)'] = pd.to_datetime(df_sailing['first(DT_POS_UTC)'], format="%Y-%m-%d %H:%M:%S")
    df_sailing['last(DT_POS_UTC)'] = pd.to_datetime(df_sailing['last(DT_POS_UTC)'], format="%Y-%m-%d %H:%M:%S")
    # 운항일 계산
    df_sailing['PERIOD'] = (df_sailing['last(DT_POS_UTC)'] - df_sailing['first(DT_POS_UTC)']).dt.days.astype('int16')

    # save csv file
    if save_file:
        for id_name, mmsi in enumerate(mmsi_list):
            _tmp_df = df_sailing[df_sailing['MMSI'] == str(mmsi)]
            db_save_path = f'{db_save_folder}/{mmsi}_DB.csv'
            check_folder_exist(db_save_path)
            _tmp_df.to_csv(db_save_path,index=False)


    return df_sailing
 

def generate_json(json_folder, database, mmsi, smartship_data_path):
    #db_mmsi_list = databse['MMSI'].unique()
    assert Path(smartship_data_path).is_file(), f'Check Smartship data path: {smartship_data_path}'
    df_sailing = database[database['MMSI'] == mmsi]
    #df_sailing['first(DT_POS_UTC)'] = pd.to_datetime(df_sailing['first(DT_POS_UTC)'])
    #df_sailing['last(DT_POS_UTC)'] = pd.to_datetime(df_sailing['last(DT_POS_UTC)'])

    df_sailing['first'] = df_sailing['first(DT_POS_UTC)'].dt.strftime('%Y-%m-%d %H:%M')
    df_sailing['first'] = pd.to_datetime(df_sailing['first'])

    df_sailing['last'] = df_sailing['last(DT_POS_UTC)'].dt.strftime('%Y-%m-%d %H:%M')
    df_sailing['last'] = pd.to_datetime(df_sailing['last'])

    #df_smartship = pd.read_csv(str(df_sailing.iloc[0]['MMSI']) + "_SmartShipData.csv")
    df_smartship = pd.read_csv(smartship_data_path)
    df_smartship['DateTime'] = pd.to_datetime(df_smartship['DateTime'])

    for i in range(len(df_sailing)):
        json_data = []
        start_date = df_sailing.iloc[i]['first']
        end_date = df_sailing.iloc[i]['last']
        file_name = json_folder + "/" + str(df_sailing.iloc[i]['MMSI']) + "_" + str(df_sailing.iloc[i]['DESTINATION_KEY']) + ".json"

        df_for_json = df_smartship[(start_date < df_smartship['DateTime']) & (df_smartship['DateTime'] <= end_date)]

        if len(df_for_json) > 0:
            for j in range(len(df_for_json)):
                json_data.append([str(df_for_json.iloc[j]['DateTime']), 'ShipSpeed_km/h',
                                  round(abs(df_for_json.iloc[j]['VesselSpeed_km/h']), 1)])

            with open(file_name, 'w', encoding="utf-8") as make_file:
                json.dump(json_data, make_file, ensure_ascii=False, indent="\t")
        else:
            with open(file_name, 'w', encoding="utf-8") as make_file:
                json.dump(json_data, make_file, ensure_ascii=False, indent="\t")

## xml file path : ./web/XML/{MMSI}/*.xml
def generate_xml(xml_folder, pp_dataframe, database):
    mmsi_list = database['MMSI'].unique()
    
    
    for i in range(len(database)):
        _mmsi     = database.iloc[i]['MMSI']
        _dest_key = database.iloc[i]['DESTINATION_KEY']

        df_for_xml = pp_dataframe[pp_dataframe['DESTINATION_KEY'] == _dest_key][
                        ['SHIP_ID', 'MMSI', 'TRACKING_DATE', 'DT_STATIC_UTC', 'DT_POS_UTC', 'INSERT_DATE', 'LATITUDE',
                        'LONGITUDE', 'DESTINATION']
                    ]
        df_for_xml['YYYY-MM-DD HH'] = df_for_xml['TRACKING_DATE'].dt.strftime('%Y-%m-%d %H')

        # ---------------------------- YYYY-MM-DD HH   Mean(LATITUDE)   Mean(LONGITUDE) ----------------------------
        YYYY_MM_DD_list = df_for_xml['YYYY-MM-DD HH'].unique()

        df_xml = pd.DataFrame(columns=['YYYY-MM-DD HH', 'Mean(LATITUDE)', 'Mean(LONGITUDE)'])
        
        for YYYY in YYYY_MM_DD_list:
            df_YYYY = df_for_xml[df_for_xml['YYYY-MM-DD HH'] == YYYY]
            _data = {
                'YYYY-MM-DD HH': YYYY,
                'Mean(LATITUDE)': str(df_YYYY['LATITUDE'].mean()),
                'Mean(LONGITUDE)': str(df_YYYY['LONGITUDE'].mean())
            }
            df_xml = df_xml.append(_data, ignore_index=True)
        # -------------------------- xml 만들기 ------------------------------------
        root = Element("markers")
        for j in range(len(df_xml)):
            node1 = Element("marker")
            node1.text = "\n" + "lat='" + str(df_xml.iloc[j]['Mean(LATITUDE)']) + "' lng='" + str(
                df_xml.iloc[j]['Mean(LONGITUDE)']) + "'"
            root.append(node1)
        #dump(root)

        tree = ElementTree(root)
        # file_path = f'{xml_folder}/{_mmsi}/dest_key_{_dest_key}.xml'
        file_path = f'{xml_folder}/{_mmsi}_{_dest_key}.xml'
        check_folder_exist(file_path)
        tree.write(file_path)







def header_update(data):
    # header 추출
    index = data.columns.values.tolist()

    # 대문자 변경
    index = list(map(lambda x: x.upper(), index))

    # 공백 -> _, .제거
    index = list(map(lambda x: x.replace(" ", "_").replace(".", ""), index))

    # header 변경
    data.columns = index

    return data

def generate_DESTINATION_KEY(pp_dataframe):
    pp_dataframe['DESTINATION_KEY'] = 0
    mmsi_list = pp_dataframe['MMSI'].unique()
    pp_dataframe.sort_values(by=['MMSI','DT_POS_UTC'],ascending=[True, True])
    for _mmsi in mmsi_list:
        __pp_df = pp_dataframe.loc[pp_dataframe['MMSI'] == _mmsi,['DESTINATION']]
        __pp_df['DESTINATION(-1)'] = 0
        __pp_df['DESTINATION(-1)'][1:] = __pp_df['DESTINATION'][:-1]
        _DEST_KEY_list = list()
        _key = 0
        for i in range(len(__pp_df)):
            if __pp_df.iloc[i,0] == __pp_df.iloc[i,1]:
                _DEST_KEY_list.append(_key)
            else:
                _key += 1
                _DEST_KEY_list.append(_key)
        __pp_df['DESTINATION_KEY'] = np.array(_DEST_KEY_list, dtype=np.int16)
        pp_dataframe.loc[__pp_df.index, 'DESTINATION_KEY'] = __pp_df['DESTINATION_KEY']
    return pp_dataframe

def check_folder_exist(file_path):
    path = Path(file_path)
    assert len(path.suffix) != 0 , f'Final path must be file, not folder and not include dot(.), {file_path}'
    folder_path = path.parents[0]
    if not folder_path.is_dir():
        folder_path.mkdir(parents=True, exist_ok=True)
    else:
        pass

## 필요 없음 삭제 요청
def exist_smartship_data(file_path):
    path = Path(file_path)
    if '538008382' in os.listdir(path):
        return True
    return False




if __name__ == '__main__':
    import os, sys
    sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    import file_processing as fp

    data_folder = '../data/AIS_data'
    xml_folder  = '../web/XML'
    json_folder = '../web/JSON'
    db_folder   = '../web/DB'
    smartship_mmsi = '538008382'
    smartship_data_path = '../data/smartship_data/538008382_SmartShipData.csv'

    file_dict = fp.take_file_path(data_folder)
    print(file_dict.keys())
    dataframe_list = list()
    for _path_list in file_dict.values():
        __dataframe = fp.merge_excel_file(_path_list)
        dataframe_list.append(__dataframe)
    dataframe_t = pd.concat(dataframe_list)
    del dataframe_list

    #Preprocessing된 dataframe 생성
    pp_dataframe = preprocessing_excel_df(dataframe_t)
    #DB - MMSI, 항차, Destination, Draught, 운항시작일시, 운항종료일시, 데이터 건수
    database     = generate_db(pp_dataframe,db_folder,save_file=True)
    # make xml files
    generate_xml(xml_folder, pp_dataframe, database)
    # make json files
    generate_json(
        json_folder         = json_folder,
        database            = database,
        mmsi                = smartship_mmsi,
        smartship_data_path = smartship_data_path,
    )
