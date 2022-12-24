import datetime as dt
import json

from PyNaver import Naver
from dateutil.relativedelta import relativedelta
from django import forms
from django.conf import settings

# 애플리케이션 인증 정보
client_id = getattr(settings, 'CLIENT_ID', None)
client_secret = getattr(settings, 'CLIENT_SECRET', None)

# 네이버 API 인스턴스 생성
api = Naver(client_id, client_secret)

def process(keyword):
    today = dt.datetime.now()
    delta = today + relativedelta(years=-3)
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
    df['예측'] = ""

    return df
def get_json(keyword):
    result = process(keyword).to_json(orient='records')

    return json.loads(result, strict=False)

def get_html(keyword):
    return process(keyword).to_html()


class NameForm(forms.Form):
    your_name = forms.CharField(label='검색어', max_length=100)
