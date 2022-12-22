import datetime
import os
import environ
import datetime as dt
from dateutil.relativedelta import relativedelta
from django import forms
from PyNaver import Naver

from main.dailyKeyword.settings import BASE_DIR

env = environ.Env(DEBUG=(bool, True))
environ.Env.read_env(
    env_file=os.path.join(BASE_DIR, '.env')
)

# 애플리케이션 인증 정보
client_id = env('client_id')
client_secret = env('client_secret')

# 네이버 API 인스턴스 생성
api = Naver(client_id, client_secret)


def trend(keyword):
    today = dt.datetime.now()
    delta = today+relativedelta(years= -3)
    # 파라미터
    startDate = delta.strftime("%Y-%m-%d")
    endDate = today.strftime("%Y-%m-%d")
    timeUnit = "date"
    keywordGroups = [
        {
            "groupName": keyword,
            "keywords": [keyword]
        }
    ]

    # 실행
    df = api.datalab_search(startDate, endDate, timeUnit, keywordGroups)

    print(df)
    return df.transpose().to_html()


class NameForm(forms.Form):
    your_name = forms.CharField(label='검색어', max_length=100)





