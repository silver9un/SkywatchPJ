import torch
import cv2
import easyocr
import pymysql
import dbmodule
import datetime
import time
import os
from views import features

#import RRDBNet_arch as arch
#import numpy as np
db = pymysql.connect(
    user='sky',
    passwd='1q2w3e',
    port=3307,
    host='project-db-stu.ddns.net',
    db='sky',
    charset='utf8'
)


# list => string
def listToString(str_list):
    result = ""
    for s in str_list:
        result += s.replace(' ','')
    return result

#def yolo(video):
# 커스텀 데이터 load
def yolo(img=None,vid=None):
    # 커스텀 데이터 load
    model = torch.hub.load('ultralytics/yolov5', 'custom', path='v5s_b64_e150.pt',
                           force_reload=True)
    str_list=''
    count = 1

    if vid != None:
        cap = cv2.VideoCapture(f'{vid}')

        while cap.isOpened():
            # 이미지 읽어옴

            ret, frame = cap.read()
            if not ret:  # ret이 False일때 동작
                print('이미지를 불러오지 못했습니다')
                cap.release()  # 비디오 객체 종료
                cv2.destroyAllWindows()
                break

            # 불러온 모델에 캡쳐한 frame을 넣고 detection 진행
            results = model(frame)

            # detection이 진행된 results에서 어떤 라벨이 뽑혔는지와, 그 라벨의 bounding box에 대한 정보를 labels와 cord에 담음
            labels, cord = results.xyxyn[0][:, -1], results.xyxyn[0][:, :-1]

            # detection된 수를 뽑음
            number_detection = len(labels)

            x_shape, y_shape = frame.shape[1], frame.shape[0]

            # 발견된 detection 수만큼 loop를 돌며,
            for i in range(number_detection):
                row = cord[i]
                conf = row[4]  # 검출된 객체 cord[i]의 confidence 깂

                if conf >= 0.5:  # conf 이상으로 확신하는 경우만 바운딩 박스를 그림
                    x1, y1, x2, y2 = int(row[0] * x_shape), int(row[1] * y_shape), int(row[2] * x_shape), int(
                        row[3] * y_shape)
                    bgr = (0, 255, 0)
                    cv2.rectangle(frame, (x1, y1), (x2, y2), bgr, 2)
                    # 번호판부분 잘라오기
                    roi_img = frame[y1:y2,x1:x2]
                    cv2.imshow('yolo', frame)
                    # 캡처 1
                    if cv2.waitKey(5) == 49:
                        # 흑백전환
                        gray = cv2.cvtColor(roi_img, cv2.COLOR_BGR2GRAY)

                        # 한국어 설정
                        reader = easyocr.Reader(['ko'], gpu=True)

                        # roi_img사진 넣기
                        result = reader.readtext(gray)

                        # 잘린 사진 저장
                        cv2.imwrite(f'../drone_img/numPlate/1.jpg', roi_img)
                        # 원본 이미지 0.5배 만들고 경로에 저장
                        img = cv2.resize(img, dsize=(0, 0), fx=0.5, fy=0.5, interpolation=cv2.INTER_LINEAR)
                        cv2.imwrite(f'../drone_img/parking/1.jp', img)
                        chars = result[0][1]

                        # str 변환
                        str_list = listToString(chars)

                        # 번호판 리스트 형태에 최소 8개들어가있음
                        print(str_list)
                        count += 1


                    if cv2.waitKey(5) & 0xFF == ord('q'):
                        break

    # ocr 적용 2
    elif img!=None:
        # 사진경로
        img=cv2.imread(img)
        results = model(img)

        labels, cord = results.xyxyn[0][:, -1], results.xyxyn[0][:, :-1]

        number_detection = len(labels)

        x_shape, y_shape = img.shape[1], img.shape[0]

        for i in range(number_detection):
            row = cord[i]
            if row[4] >= 0.4:  # threshold 조절해서 분류

                x1, y1, x2, y2 = int(row[0] * x_shape), int(row[1] * y_shape), int(row[2] * x_shape), int(
                    row[3] * y_shape)  # 모델 인식부분 바운딩 박스

                # 번호판 사각형 표기
                cv2.rectangle(img, (x1, y1), (x2, y2), (0, 255, 0), 2)
                roi_img = img[y1:y2, x1:x2]


                while True:
                    cv2.imshow('result',roi_img)
                    if cv2.waitKey(5) == 49:
                        # 흑백전환
                        gray = cv2.cvtColor(roi_img, cv2.COLOR_BGR2GRAY)

                        # 한국어 설정
                        reader = easyocr.Reader(['ko'], gpu=True)


                        # roi_img사진 넣기
                        result = reader.readtext(gray)

                        # 잘린 사진 경로에 저장
                        cv2.imwrite(f'../drone_img/numPlate/{count}.jpg', roi_img)
                        # 원본 이미지 0.5배 만들고 경로에 저장
                        img = cv2.resize(img, dsize=(0, 0), fx=0.5, fy=0.5, interpolation=cv2.INTER_LINEAR)
                        cv2.imwrite(f'../drone_img/parking/{count}.jpg', img)
                        chars=result[0][1]

                        # str 변환
                        str_list = listToString(chars)

                        # 번호판 리스트 형태에 최소 8개들어가있음
                        print(str_list)

                        now = time.localtime()

                        regulation_date = features.getDate(now)
                        regulation_time = features.getTime(now)

                        os.chdir("../")
                        imgdir_parking = f"/drone_img/numPlate/{count}.jpg"
                        imgdir_numPlate = f"/drone_img/parking/{count}.jpg"


                        regulation_area = str("황금동")

                        # db_tbareatest = dbmodule.Database()
                        # query_insert = f"insert into tb_area_test values ('{regulation_date}', '{regulation_time}', '{str_list}', '{regulation_area}', '{imgdir_parking}', '{imgdir_numPlate})"
                        # db_tbareatest.execute(query_insert,)
                        cur = db.cursor()
                        sql = "insert into tb_area(car_num,regulation_area,regulation_date,regulation_time,imgdir_parking,imgdir_numPlate) values (%s,%s,%s,%s,%s,%s)"
                        cur.execute(sql,(str_list,regulation_area,regulation_date,regulation_time,imgdir_parking,imgdir_numPlate))
                        db.commit()
                        count += 1
                    if cv2.waitKey(5) & 0xFF == ord('q'):
                        break
    # # cur = db.cursor()
    # #번호판 insert문
    # # sql = "insert into tb_area_test(car_num,regulation_area,regulation_date,regulation_time) values (%s,%s,%s,%s)"
    # # cur.execute(sql,(str_list,'지역','날짜','시간'))
    #
    # #번호판 update문
    # # sql = "update tb_area_test set car_num = %s where regulation_time = %s"
    # # cur.execute(sql,str_list,'지역')
    # # db.commit()
    # # db.close()



yolo(img="../drone_img/regulation_img/")

