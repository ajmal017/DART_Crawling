# 35d444d5a2ca8c271de34c8d296baf7474c37035 my API key
# pip install dart-fss
import dart_fss as dart
import pandas as pd
import sqlite3
import pymysql

def get_dart():
    api_key='35d444d5a2ca8c271de34c8d296baf7474c37035' 
    dart.set_api_key(api_key=api_key)

    # 코스피 시총 상위 50개 기업 가져오기
    kospi = pd.read_excel('./kospi top 50.xlsx')
    print(kospi['corp'])

    corps = kospi['corp']

    # DART 에 공시된 회사 리스트 불러오기
    corp_list = dart.get_corp_list()

    # corp_df = pd.DataFrame()

    con = sqlite3.connect("./kospi.db")


    # for co in corps:
    #     try:
    #         print(co)
    #         corp = corp_list.find_by_corp_name(co, exactly=True)[0]
    #         corp_name = corp.info['corp_name']
    #         corp_code = corp.info['corp_code']
    #         stock_code = corp.info['stock_code']
    #         sector = corp.info['sector']

    #         corp_df['Corp'] =  corp_name
    #         corp_df['corp_code'] =  corp_code
    #         corp_df['Stock_code'] = stock_code
    #         corp_df['Sector'] = sector

    #         try:
    #             # 2012년부터 분기별 연결재무제표 불러오기
    #             fs = corp.extract_fs(bgn_de='19870101', report_tp='quarter') # fs_tp = bs, is, cis, cf
                
    #             for num in range(0,4):
    #                 fs[num]['Code'] = stock_code
    #                 fs[num]['Corp'] = corp_name
    #                 print('add code & name')
    #                 if num == 0:
    #                     fs[num].to_sql('financial_statement{}'.format(corp_code), con)
    #                     print('financial_statement done')

    #                 elif num == 1:
    #                     fs[num].to_sql('income_statement{}'.format(corp_code), con)
    #                     print('income_statement done')

    #                 elif num == 2:
    #                     fs[num].to_sql('Comprehensive_income_statement{}'.format(corp_code), con)
    #                     print('Comprehensive_income_statement done')

    #                 else:
    #                     fs[num].to_sql('cashflow{}'.format(corp_code), con)
    #                     print('cashflow done')

    #             #annual semiannual quarter 순으로 뽑는데 안나오는 경우 그냥 업보고서 or 분기 보고서 쓰기??
    #         except:
    #             print('DB err')

    #     except:
    #         print('corp info err')
    # print(corp_df.head())
    # corp_df.to_sql('Company', con)


    


if __name__ == "__main__":
    get_dart()
    





