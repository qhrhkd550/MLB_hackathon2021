import pandas as pd
from xml.etree.ElementTree import Element, dump, ElementTree

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


def type_update(data):
    # 어떤 항목을 어떤 타입으로 바꿀지 고민
    print(data.info())

    return data


def groupby_mmsi(data):
    # mmsi 별 그룹화 하기 위해 고유한 mmsi 추출
    mmsi_list = data['MMSI'].unique()

    # mmsi별 작업처리
    for id_name, mmsi in enumerate(mmsi_list):
        df_new = data[data['MMSI'] == mmsi]

        # 필요없는 컬럼 제거
        df_new.drop(
            ['SHIP_NAME', 'IMO', 'SOG', 'SOURCE', 'ETA', 'NAV_STATUS', 'NAV_STATUS_CODE', 'CALL_SIGN', 'VESSEL_TYPE',
             'VESSEL_TYPE_CODE', 'VESSEL_TYPE_CARGO', 'VESSEL_CLASS', 'LENGTH', 'WIDTH', 'FLAG', 'FLAG_CODE', 'COG',
             'ROT', 'HEADING', 'VESSEL_TYPE_MAIN', 'VESSEL_TYPE_SUB', 'MESSAGE_TYPE'], axis=1, inplace=True)

        # 시간 순 정렬
        df_new.sort_values(by=['DT_POS_UTC'])

        # DESTINATIIPN(-1) 생성
        df_new['DESTINATION(-1)'] = 0
        df_new['DESTINATION(-1)'][1:] = df_new['DESTINATION'][:-1]
        df_new['DESTINATION(-1)'][0] = 'missing'

        # DESTINATION_KEY 생성
        df_new['DESTINATION_KEY'] = 0
        for i, index in enumerate(df_new.index):
            if i == 0:
                df_new['DESTINATION_KEY'].loc[index] = 1
            else:
                if df_new['DESTINATION'].loc[index] == df_new['DESTINATION(-1)'].loc[index]:
                    df_new['DESTINATION_KEY'].loc[index] = df_new['DESTINATION_KEY'].loc[prev_index]

                else:
                    df_new['DESTINATION_KEY'].loc[index] = df_new['DESTINATION_KEY'].loc[prev_index] + 1

            prev_index = index

        # ------------------------------------------------------------------- 항차 별 feature 생성 -------------------------------------------------------------------------------------------------

        df_sailing = pd.DataFrame(
            columns=['MMSI', 'DESTINATION', 'DESTINATION_KEY', 'first(DT_POS_UTC)', 'last(DT_POS_UTC)',
                     'count*(SEQ_NO)', 'filepath_XML'])

        for sailing in range(1, max(df_new['DESTINATION_KEY']) + 1):
            tmp = df_new[df_new['DESTINATION_KEY'] == sailing]
            sailing_mmsi = str(tmp['MMSI'].iloc[0])
            sailing_destination = tmp['DESTINATION'].iloc[0]
            sailing_destination_key = tmp['DESTINATION_KEY'].iloc[0]
            sailing_first = tmp['DT_POS_UTC'].iloc[0]
            sailing_last = tmp['DT_POS_UTC'].iloc[-1]
            sailing_count = len(tmp)

            data = {
                'MMSI': sailing_mmsi,
                'DESTINATION': sailing_destination,
                'DESTINATION_KEY': sailing_destination_key,
                'first(DT_POS_UTC)': sailing_first,
                'last(DT_POS_UTC)': sailing_last,
                'count*(SEQ_NO)': sailing_count,
                'filepath_XML': "./xml/" + sailing_mmsi + "_" + str(sailing_destination_key) + ".xml"
            }

            df_sailing = df_sailing.append(data, ignore_index=True)

        # -------------------------------------------------------------------------- 항차별로 YYYY-MM-DD HH feature 추가 ----------------------------------------------------------------------------------

        for i in range(len(df_sailing)):
            df_for_xml = df_new[df_new['DESTINATION_KEY'] == df_sailing.iloc[i]['DESTINATION_KEY']][
                ['SHIP_ID', 'MMSI', 'TRACKING_DATE', 'DT_STATIC_UTC', 'DT_POS_UTC', 'INSERT_DATE', 'LATITUDE',
                 'LONGITUDE', 'DESTINATION']]

            df_for_xml['TRACKING_DATE'] = pd.to_datetime(df_for_xml['TRACKING_DATE'])

            df_for_xml['YYYY-MM-DD HH'] = df_for_xml['TRACKING_DATE'].dt.strftime('%Y-%m-%d %H')

            # ---------------------------- YYYY-MM-DD HH   Mean(LATITUDE)   Mean(LONGITUDE) ----------------------------
            YYYY_MM_DD_list = df_for_xml['YYYY-MM-DD HH'].unique()

            df_final = pd.DataFrame(columns=['YYYY-MM-DD HH', 'Mean(LATITUDE)', 'Mean(LONGITUDE)'])

            for id_name, YYYY in enumerate(YYYY_MM_DD_list):
                df_YYYY = df_for_xml[df_for_xml['YYYY-MM-DD HH'] == YYYY]

                data = {
                    'YYYY-MM-DD HH': YYYY,
                    'Mean(LATITUDE)': str(df_YYYY['LATITUDE'].mean()),
                    'Mean(LONGITUDE)': str(df_YYYY['LONGITUDE'].mean())
                }

                df_final = df_final.append(data, ignore_index=True)
            # -----------------------------------------------------------------------------------------------------------

            # -------------------------- xml 만들기 ------------------------------------
            root = Element("markers")

            for j in range(len(df_final)):
                node1 = Element("marker")
                node1.text = "\n" + "lat='" + str(df_final.iloc[j]['Mean(LATITUDE)']) + "' lng='" + str(
                    df_final.iloc[j]['Mean(LONGITUDE)']) + "'"
                root.append(node1)
            dump(root)

            #             display(root)
            tree = ElementTree(root)

            file_path = df_sailing.iloc[i]['filepath_XML']
            tree.write(file_path)
            # --------------------------------------------------------------------------