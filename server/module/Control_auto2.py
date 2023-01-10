import os
import pandas as pd
import numpy as np
from djitellopy import Tello
from time import sleep
import cv2
from keras.models import load_model
from tensorflow.keras.preprocessing import image
from tensorflow.keras.applications.imagenet_utils import preprocess_input
import PIL
from PIL import Image

from datetime import datetime
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'


class drone_control:
    def __init__(self):
        #드론 캡쳐 데이터 경로
        self.dcap_dir = "./Skywatch/server/drone_img/parking"
        self.save_cap = "./Skywatch/server/drone_img/parking/cap_sector"
        self.num_cap = "./Skywatch/server/drone_img/numPlate"

        # self.dcap_dir = "data/drone_img/parking"
        # self.save_cap = "data/drone_img/parking/d_sector"
        # self.num_cap = "data/drone_img/numPlate"

        # 학습된 모델 불러오기 (VGG + Dense 확장)
        #(Tr 0:1 - 1272:528, Val 92:40, Te 106:31)
        self.loaded_model = load_model('./module/CNN_VGG_Vol9.h5')
        self.move_A()


    def cap_cnn(self, img, cap_time):
        img = img[int(img.shape[0] // 1.7):, :]
        size_x = img.shape[0]
        size_y = img.shape[1]

        div_x = 3  # 3행
        div_y = 6  # 6열 로 이미지 분할 선

        rois = []
        for y in range(div_y):
            for x in range(div_x):
                rois.append(img[(size_x // div_x) * x: (size_x // div_x) * (x + 1),
                            (size_y // div_y) * y: (size_y // div_y) * (y + 1)])

        cnt = 0
        for roi in rois:
            cnt += 1
            cv2.imwrite(f'{self.save_cap}/cap{cap_time}--{cnt}.png', roi,
                        params=[cv2.IMWRITE_JPEG_PROGRESSIVE, 0])
        roi_class = []
        for i in range(div_x * div_y):
            # 평가용 이미지 하나
            test_img = cv2.imread(f'{self.save_cap}/cap{cap_time}--{i + 1}.png', cv2.IMREAD_COLOR)
            test_img = cv2.resize(test_img, (150, 150))

            # 가져온 이미지 nparray 형식으로 변환
            np_img = image.img_to_array(test_img)
            np_img.shape

            # 모델 분석키 위해 4차원 변환(이해가 필요함)
            img_batch = np.expand_dims(np_img, axis=0)
            img_batch.shape

            # 이미지 정규화
            pre_processed = preprocess_input(img_batch)

            # 분류 결과 값 출력
            y_preds = self.loaded_model.predict(pre_processed)
            road = y_preds[0][0]
            car = y_preds[0][1]
            if road > car:
                roi_class.append(f'cap{i + 1} > road')
            else:
                roi_class.append(f'cap{i + 1} > car')

        # 분할된 이미지들의 도로/차량 분류 결과를 조건에 따라 드론 촬영 섹터 저장
        sectors = pd.DataFrame({'roi_class': roi_class})

        cond1 = sectors.loc[3, 'roi_class'] == 'cap4 > car'
        cond2 = sectors.loc[6, 'roi_class'] == 'cap7 > car'

        cond3 = sectors.loc[4, 'roi_class'] == 'cap5 > car'
        cond4 = sectors.loc[8, 'roi_class'] == 'cap8 > car'

        cond5 = sectors.loc[2, 'roi_class'] == 'cap3 > car'
        cond6 = sectors.loc[5, 'roi_class'] == 'cap6 > car'

        cond7 = sectors.loc[9, 'roi_class'] == 'cap10 > car'
        cond8 = sectors.loc[12, 'roi_class'] == 'cap13 > car'

        cond9 = sectors.loc[10, 'roi_class'] == 'cap11 > car'
        cond10 = sectors.loc[13, 'roi_class'] == 'cap14 > car'

        cond11 = sectors.loc[14, 'roi_class'] == 'cap15 > car'
        cond12 = sectors.loc[15, 'roi_class'] == 'cap16 > car'

        patrol_area = []

        if cond1 or cond2:
            print('sector1 불법차량 발견')
            patrol_area.append(1)
        if cond3 or cond4:
            print('sector2 불법차량 발견')
            patrol_area.append(2)
        if cond5 or cond6:
            print('sector3 불법차량 발견')
            patrol_area.append(3)
        if cond7 or cond8:
            print('sector4 불법차량 발견')
            patrol_area.append(4)
        if cond9 or cond10:
            print('sector5 불법차량 발견')
            patrol_area.append(5)
        if cond11 or cond12:
            print('sector6 불법차량 발견')
            patrol_area.append(6)

        # print(sectors)
        # print(f'정찰섹터 순서 >> {patrol_area}')

        return(patrol_area)

    #A 구역 정찰 움직임
    def move_A(self):
        
        self.drone = Tello()
        
        if not self.drone.connect():
            print(self.drone.get_battery())

        print(self.drone.get_battery())
        # self.drone.connect()
        # print(self.drone.get_battery())
        # self.drone.streamon()

        for i in range(0, 1):
            print('이륙')
            self.drone.takeoff()
            self.drone.send_rc_control(0, 0, 0, 0)
            sleep(2)

            # [left_right, front_back, up_down, clock_counter]
            # print('전진')

            self.drone.move_forward(40)
            sleep(2)

            print('좌행')

            self.drone.move_left(160)
            sleep(2)

            print('전진')

            self.drone.move_forward(110)
            sleep(2)

            print('우회전')

            self.drone.rotate_clockwise(90)
            sleep(2)

            print('하강')

            self.drone.move_down(20)
            sleep(1)

            print('지역 캡쳐 시작')

            cap_time = datetime.now().date()

            img = self.drone.get_frame_read().frame
            cv2.imwrite(f'{self.dcap_dir}/{cap_time}_parking.png', img,
                        params=[cv2.IMWRITE_JPEG_PROGRESSIVE, 0])
            print(f"지역 캡쳐 완료__{cap_time}")

            # cv2.imshow("Image", image)
            # cv2.waitKey(1)
            # cv2.destroyAllWindows()

            img = cv2.imread(f'{self.dcap_dir}/{cap_time}_parking.png')

            #분할된 섹터 이미지 cnn 분류 결과 -> 2차 비행 경로
            result = self.cap_cnn(img, cap_time)
            print(result)

            # cnn 분류 결과에 따른 드론 제어
            for i in result:
     
                if i == 1:
                    self.drone.move_forward(120)
                    self.drone.move_left(20)
                    self.drone.move_down(20)
                    sleep(1)

                    print(f'{i}섹터 차량 캡쳐 시작')

                    img = self.drone.get_frame_read().frame
                    cv2.imwrite(f'{self.num_cap}/{cap_time}--{i}sector_car.png', img,
                                params=[cv2.IMWRITE_JPEG_PROGRESSIVE, 0])
                    print(f"{i}섹터 차량 캡쳐 완료")

                    self.drone.move_up(20)
                    self.drone.move_right(20)
                    self.drone.move_back(120)
                    sleep(1)

                if i == 2:
                    self.drone.move_forward(90)
                    self.drone.move_left(20)
                    self.drone.move_down(20)
                    sleep(1)

                    print(f'{i}섹터 차량 캡쳐 시작')
                    img = self.drone.get_frame_read().frame
                    cv2.imwrite(f'{self.num_cap}/{cap_time}--{i}sector_car.png', img,
                                params=[cv2.IMWRITE_JPEG_PROGRESSIVE, 0])
                    print(f"{i}섹터 차량 캡쳐 완료")

                    self.drone.move_up(20)
                    self.drone.move_right(20)
                    self.drone.move_back(90)
                    sleep(1)

                if i == 3:
                    self.drone.move_forward(60)
                    self.drone.move_left(20)
                    self.drone.move_down(20)
                    sleep(1)

                    print(f'{i}섹터 차량 캡쳐 시작')
                    img = self.drone.get_frame_read().frame
                    cv2.imwrite(f'{self.num_cap}/{cap_time}--{i}sector_car.png', img,
                                params=[cv2.IMWRITE_JPEG_PROGRESSIVE, 0])
                    print(f"{i}섹터 차량 캡쳐 완료")

                    self.drone.move_up(20)
                    self.drone.move_right(20)
                    self.drone.move_back(60)
                    sleep(1)

                if i == 4:
                    self.drone.move_forward(120)
                    self.drone.move_right(20)
                    self.drone.move_down(20)
                    sleep(1)

                    print(f'{i}섹터 차량 캡쳐 시작')
                    img = self.drone.get_frame_read().frame
                    cv2.imwrite(f'{self.num_cap}/{cap_time}--{i}sector_car.png', img,
                                params=[cv2.IMWRITE_JPEG_PROGRESSIVE, 0])
                    print(f"{i}섹터 차량 캡쳐 완료")

                    self.drone.move_up(20)
                    self.drone.move_left(20)
                    self.drone.move_back(120)
                    sleep(1)

                if i == 5:
                    self.drone.move_forward(90)
                    self.drone.move_right(20)
                    self.drone.move_down(20)
                    sleep(1)

                    print(f'{i}섹터 차량 캡쳐 시작')
                    img = self.drone.get_frame_read().frame
                    cv2.imwrite(f'{self.num_cap}/{cap_time}--{i}sector_car.png', img,
                                params=[cv2.IMWRITE_JPEG_PROGRESSIVE, 0])
                    print(f"{i}섹터 차량 캡쳐 완료")

                    self.drone.move_up(20)
                    self.drone.move_left(20)
                    self.drone.move_back(90)
                    sleep(1)               

                if i == 6:
                    self.drone.move_forward(60)
                    self.drone.move_right(20)
                    self.drone.move_down(20)
                    sleep(1)

                    print(f'{i}섹터 차량 캡쳐 시작')
                    img = self.drone.get_frame_read().frame
                    cv2.imwrite(f'{self.num_cap}/{cap_time}--{i}sector_car.png', img,
                                params=[cv2.IMWRITE_JPEG_PROGRESSIVE, 0])
                    print(f"{i}섹터 차량 캡쳐 완료")

                    self.drone.move_up(20)
                    self.drone.move_left(20)
                    self.drone.move_back(60)
                    sleep(1)

            # print(f'정찰섹터 순서 >> {patrol_area}')
            self.drone.send_rc_control(0, 0, 0, 0)
            sleep(2)
            print('전진')

            self.drone.move_forward(200)
            sleep(2)
            print('착륙')

            sleep(2)
            self.drone.land()
            sleep(2)
            print(self.drone.get_battery())
            break
        self.drone.end()
        

# 별도 테스트용
# drone = tello.Tello()
# drone.connect()
# print(drone.get_battery())
# drone.streamon()

# control = drone_control()
# control.move_A(drone)


