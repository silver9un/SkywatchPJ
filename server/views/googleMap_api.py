from flask import Flask, Blueprint, request, render_template
from flask_googlemaps import GoogleMaps, Map,icons,get_address,get_coordinates
from socket import *

google = Blueprint('googleMap',__name__,'/googleMap')

"""
이거는 flask_googlemap 라이브러리에서 있는 gmapjs.html 있는데
수정 안하면 구글 맵 지도 아예 안뜬다. 따라서 수정해야한다.
임시적으로 메모장에다가 적을예정이니 참고하세요
"""

# 테스트
results = []
print(len(results))
message_results = []
print(message_results)
print(len(message_results))
msg = '안녕하세요?'
print(msg)


@google.route('/googleMap_api')
def googlemap():
    # 뷰에서 지도생성
    clickmap = Map(
        zoom=18,
        identifier="clickmap",
        varname="clickmap",
        lat=35.149796202004325,
        lng=126.91992834014,
        language="ko",
        style="height:600px;width:1050px;margin:0;",
        # collapsible=True, # 지도를 접을 수 있게 만든 변수
        # cluster=True, # 마커표시 수 지도 줌 아웃하면 자동적으로 숫자 나타남
        report_clickpos=True, # 클릭 포스 신고(보니까 클릭하면 post 날라옴)
        clickpos_uri="/clickpost", # report_clickpos 같이해야함
        markers={
            icons.dots.blue: [s for s in results]
        },
        # center_on_user_location=True, #(현재 위치 말하는 듯)사용자 위치를 중심으로

    )
    print(message_results)
    print(len(message_results))

    return render_template("information/crackdown_inquiry.html",clickmap = clickmap,msg=msg,message_results=message_results)
#

# 클릭시 함수 호출
@google.route('/clickpost',methods = ["POST"])
def clickpost():
    lat = request.form["lat"] #위도
    lng = request.form["lng"] # 경도
    if len(results) < 4:
        results.append((lat,lng))
        print(len(results))
        print(results)
    elif len(results) == 4:
        a = '최대 4개 마커 찍을 수 있습니다.'
        print(a)
        print(" ".join([msg,a]))
        if len(message_results) < 1:
            message_results.append(" ".join([msg, a]))

    return "ok"