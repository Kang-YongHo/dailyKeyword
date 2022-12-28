import datetime
import datetime as dt
from datetime import date, timedelta
import json

import pandas
from sqlalchemy import create_engine
import peewee
from peewee import *

from PyNaver import Naver
from dateutil.relativedelta import relativedelta
from django import forms
from django.conf import settings
from .models import *

# 애플리케이션 인증 정보
client_id = getattr(settings, 'CLIENT_ID', None)
client_secret = getattr(settings, 'CLIENT_SECRET', None)
db_user = getattr(settings, 'DB_USER', None)
db_pass = getattr(settings, 'DB_PASS', None)
# 네이버 API 인스턴스 생성
api = Naver(client_id, client_secret)

# db 설정
db = MySQLDatabase('daily_dev', user=db_user, password=db_pass,
                   host='127.0.0.1', port=3306)
db_connection_str = 'mysql+pymysql://' + db_user + ':' + db_pass + '@127.0.0.1:3306/test'
db_connection = create_engine(db_connection_str)
conn = db_connection.connect()


# 3년치 받아오기
def process(keyword, keyword_id):
    today = dt.datetime.now()
    delta = today + relativedelta(years=-3)
    # 파라미터
    start_date = delta.strftime("%Y-%m-%d")
    end_date = today.strftime("%Y-%m-%d")
    time_unit = "date"
    keyword_groups = [
        {
            "groupName": keyword,
            "keywords": [keyword]
        }
    ]

    # 실행
    df = api.datalab_search(start_date, end_date, time_unit, keyword_groups)
    df.rename(columns={'날짜': 'date'}, inplace=True)
    df.rename(columns={keyword: 'value'}, inplace=True)
    df['keyword_id'] = keyword_id
    df['expect'] = ""
    print(df.head(10))
    df.to_sql(name='search_analysis', con=db_connection
              , if_exists='append', index=False)


# 검색어 테이블 조회 후 최신 한달 분 출력
def find_keyword(subject):
    # keyword 테이블 조회
    try:
        keyword_id = Keyword.objects.get(name=subject).id
        return get_data_from_db(keyword_id)

    except Keyword.DoesNotExist:
        Keyword.objects.create(name=subject)
        keyword_id = Keyword.objects.get(name=subject).id
        process(subject, keyword_id)
        return get_data_from_db(keyword_id)


# 키워드로 한달 분 가져오기
def get_data_from_db(keyword_id):
    today = date.today()
    yearmonth = today.isoformat()

    print(yearmonth[0:7])
    obj = Analysis.objects.filter(keyword_id=keyword_id, date__icontains=yearmonth[0:7]).values()
    df = pandas.DataFrame(obj)
    print(df.head(10))
    return df.to_html()
