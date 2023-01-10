from flask import Blueprint, redirect, flash, Flask,url_for,request,render_template, Response
from module import dbmodule, Control_auto2
from socket import *
import time
import os
import datetime
from module.tello_module import Tello
import cv2


features  = Blueprint('features',__name__,url_prefix='/features')


# 단속구역 자율주행
# get, post
# @features.route('/autonomous driving')
# def autonomous_driving():
#     return redirect('main.index')

# ----------------
# 정보 수집 및 저장
def getDate(now):
    year = str(now.tm_year)
    month = str(now.tm_mon)
    day = str(now.tm_mday)
    
    if len(month) == 1:
        month = '0' + month
    if len(day) == 1:
        day = '0' + day
    
    return (year + '-' + month + '-' + day)
    
def getTime(now):
    return (str(now.tm_hour) + '.' + str(now.tm_min) + '.' + str(now.tm_sec))

@features.route("/setinfo")
def setInfo_car():
    data = ''
    
    now = time.localtime()
    
    regulation_date = getDate(now)
    regulation_time = getTime(now)
    car_num = str("123가4568", "utf-8")
    regulation_area = str("abc abc", "utf-8")

    os.chdir("../")
    imgdir_parking = "/drone_img/parking/" + "2022-12-03_15.09.00" + ".png"
    imgdir_numPlate = "/drone_img/numPlate/" + "2022-12-03_15.09.00" + ".jpg"
    
    db_tbareatest = dbmodule.Database()
    query_insert = f"insert into tb_area_test values ('{regulation_date}', '{regulation_time}', '{car_num}', '{regulation_area}', '{imgdir_parking}', '{imgdir_numPlate})"
    db_tbareatest.execute(query_insert)
    db_tbareatest.commit()
    

@features.route("/getDate_android", methods=['POST'])
def getDate_car():
    data = ''
    
    getDate = request.form["sendDate"]
    print("getDate: ", getDate)
    
    db_tbArea = dbmodule.Database()
    sql = f"select * from tb_area where regulation_date = '{getDate}'"
    row = db_tbArea.executeAll(sql)
    
    print("row len", len(row))
    print(type(row))
    print(row)
    
    if len(row) == 0:
        data = "none"
    else :
        for i in range(len(row)):
            # print(type(i))
            if row[i]['imgdir_parking'] == None:
                row[i]['imgdir_parking'] = "\drone_img\parking\\no_image.png"
                print("check imgdir_parking")
            # if row[i]['imgdir_parking2'] == None:
            #     row[i]['imgdir_parking2'] = "\drone_img\parking\\no_image.png"
            #     print("check imgdir_parking2")
            if row[i]['imgdir_numplate'] == None:
                row[i]['imgdir_numplate'] = "\drone_img\parking\\no_image.png"
                print("check img_dir_numplate")
    
        data = row

    return data

@features.route("/getCarNum_android", methods=['POST'])
def getNum_car():
    data = ''
    
    getCarNum = request.form["carNum"]
    print("getCarNum: ", getCarNum)
    
    db_tbArea = dbmodule.Database()
    sql = f"select * from tb_area_test where car_num = '{getCarNum}'"
    row = db_tbArea.executeAll(sql)
    
    print("row len", len(row))
    print(type(row))
    print(row)

    if len(row) == 0:
        data = "none"
    else :
        for i in range(len(row)):
            # print(type(i))
            if row[i]['imgdir_parking'] == None:
                row[i]['imgdir_parking'] = "\drone_img\parking\\no_image.png"
                print("check imgdir_parking")
            """ if row[i]['imgdir_parking2'] == None:
                row[i]['imgdir_parking2'] = "\drone_img\parking\\no_image.png"
                print("check imgdir_parking2") """
            if row[i]['imgdir_numplate'] == None:
                row[i]['imgdir_numplate'] = "\drone_img\parking\\no_image.png"
                print("check img_dir_numplate")
    
        data = row

    return data

@features.route("/getArea_android", methods=["POST"])
def getArea():
    msg = ''
    
    getData = request.form["sendArea"]
    print(getData)
    
    msg = "success"
    
    video_stream()
    Control_auto2.drone_control.move_A(video_camera)


    return msg

"""
    플라스크-드론 실시간 영상, 동작 조작 기능
    
    
    # 텔로포트 소켓 오류 난 경우에는 텔로 포트 죽이고나서 수동으로 해야함
    # 텔로포트 찾게해줌
    netstat -ano|findstr 8889
    # 텔로포트 죽어야함
    taskkill /f /pid 
"""





video_camera = None
global_frame = None
camera_frame = None
# tello = None
# tello = Tello()

# FPS
FPS = 25

# 실시간 영상 찍을수있는 함수
def video_stream():
    content = ''
    global video_camera
    global global_frame
    global camera_frame
    # video_camera = tello
    if video_camera == None:

        """
        이것은 파이참 환경에서 실행했을경우에는 자동적으로 돌아가는데 
        터미널에서 하면 아예 못 돌아간다는 단점이다.
        """
        # if not video_camera.connect():
        #     print("Tello not connected")
        #     return video_camera.connect()
        #
        # if not video_camera.set_speed(10):
        #     print("Not set speed to lowest possible")
        #     return video_camera.set_speed(10)
        #
        # # In case streaming is on. This happens when we quit this program without the escape key.
        # if not video_camera.streamoff():
        #     print("Could not stop video stream")
        #     return video_camera.streamoff()
        #
        # if not video_camera.streamon():
        #     print("Could not start video stream")
        #     return video_camera.streamon()

        """
        따라서 터미널환경 실행할꺼면 이거하는게 좋다.
        """
        video_camera = Tello()
        video_camera.connect()
        video_camera.set_speed(10)
        video_camera.streamoff()
        video_camera.streamon()
    while True:
        frame_read = video_camera.get_frame_read()
        print(frame_read)
        should_stop = False
        video_camera.get_battery()

        if True:
            print("디버그모드 활성화함")
        while not should_stop:
            if frame_read.stopped:
                frame_read.stop()
                break

            ori_frame = frame_read.frame
            frame = ori_frame
            if ori_frame.any():
                success, jpeg = cv2.imencode('.jpg',ori_frame)
                if success:
                    frame = jpeg.tobytes()

            if frame != None:
                global_frame = frame
                yield (b'--frame\r\n'b'Conetent-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')
            else:
                yield (b'--frame\r\n'b'Conetent-Type: image/jpeg\r\n\r\n' + global_frame + b'\r\n\r\n')


#영상 프레임 얻게하는것
@staticmethod
def get_frame(self):
    ret, frame = self.cap.read()

    if ret:
        ret, jpeg = cv2.imenocde('.jpg',frame)

        if self.is_record:
            if self.out == None:
                fourcc = cv2.VideoWriter_fourcc(*'MJPG')
                self.out = cv2.VideoWriter('./static/video.avi',fourcc,20.0,(640,480))
            ret,frame = self.cap.read()
            if ret:
                self.out.write(frame)
        else:
            if self.out != None:
                self.out.release()
                self.out = None

        return jpeg.tobytes()

# 실시간 영상
@features.route('/video_feed')
def video_feed():
    return Response(video_stream(),mimetype="multipart/x-mixed-replace; boundary=frame")

@features.route('/takeOff')
def takeOff():
    drone_terbang = video_camera
    drone_state = 'Drone Takeoff'
    if not drone_terbang.takeoff():
        print(drone_state)
        return render_template("area/features.html",drone_state=drone_state)
    return render_template("area/features.html")

@features.route('/Land')
def Land():
    drone_terbang = video_camera
    drone_state = 'Drone Landing'
    if not drone_terbang.land():
        print(drone_state)
        return render_template("area/features.html",drone_state=drone_state)
    return render_template("area/features.html")

@features.route('/Right')
def Right():
    drone_terbang = video_camera
    drone_state = 'Drone move right'
    if not drone_terbang.move_right(100):
        print(drone_state)
        return render_template("area/features.html",drone_state=drone_state)
    return render_template("area/features.html")
@features.route('/Left')
def Left():
    drone_terbang = video_camera
    drone_state = 'Drone move left'
    if not drone_terbang.move_left(100):
        print(drone_state)
        return render_template("area/features.html",drone_state=drone_state)
    return render_template("area/features.html")

@features.route('/forward')
def Forward():
    drone_terbang = video_camera
    drone_state = 'Drone move forward'
    if not drone_terbang.move_forward(100):
        print(drone_state)
        return render_template("area/features.html",drone_state=drone_state)
    return render_template("area/features.html")

@features.route('/back')
def Back():
    drone_terbange = video_camera
    drone_state = 'Drone move back'
    if not drone_terbange.move_back(100):
        print(drone_state)
        return render_template("area/features.html",drone_state=drone_state)
    return render_template("area/features.html")


@features.route('/cw')
def Rotate_clockwise():
    drone_terbange = video_camera
    drone_state = 'Drone rotate_clockwise'
    if not drone_terbange.rotate_clockwise(100):
        print(drone_state)
        return render_template("area/features.html",drone_state=drone_state)
    return render_template("area/features.html")

@features.route('/ccw')
def Rotate_counter_clockwise():
    drone_terbange = video_camera
    drone_state = 'Drone rotate_counter_clockwise'
    if not drone_terbange.rotate_counter_clockwise(100):
        print(drone_state)
        return render_template("area/features.html", drone_state=drone_state)
    return render_template("area/features.html")


@features.route('/flip')
def Flip():
    drone_terbange = video_camera
    drone_state = 'Drone flip'
    if not drone_terbange.flip("l"):
        print(drone_state)
        return render_template("area/features.html", drone_state=drone_state)
    return render_template("area/features.html")

@features.route('/flip_left')
def Flip_left():
    drone_terbange = video_camera
    drone_state = 'Drone move flip_left'
    if not drone_terbange.flip_left():
        print(drone_state)
        return render_template("area/features.html", drone_state=drone_state)
    return render_template("area/features.html")


@features.route('/flip_right')
def Flip_right():
    drone_terbange = video_camera
    drone_state = 'Drone move flip_right'
    if not drone_terbange.flip_right():
        print(drone_state)
        return render_template("area/features.html", drone_state=drone_state)
    return render_template("area/features.html")

@features.route('/flip_forward')
def Flip_forward():
    drone_terbange = video_camera
    drone_state = 'Drone move flip_forward'
    if not drone_terbange.flip_forward():
        print(drone_state)
        return render_template("area/features.html", drone_state=drone_state)
    return render_template("area/features.html")
@features.route('/flip_back')
def Flip_back():
    drone_terbange = video_camera
    drone_state = 'Drone move flip_back'
    if not drone_terbange.flip_back():
        print(drone_state)
        return render_template("area/features.html", drone_state=drone_state)
    return render_template("area/features.html")


@features.route('/move_A')
def drone_move_A():
    drone_state = 'Drone move A'
    Control_auto2.drone_control.move_A_flask(video_camera)
    print(drone_state)
    return render_template("area/features.html", drone_state=drone_state)