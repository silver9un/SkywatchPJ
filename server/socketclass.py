import socket
import cv2
import numpy
import base64
import time
import sys
import os
from datetime import datetime
from djitellopy import Tello
from module import Control_auto2
import threading

""" 
    opencv를 통해 드론 영상을 frame 단위로 받기 때문에
    서버는 클라이언트에 frame 단위로 이미지 전송
    
    server client 는 tcp socket 통신을 이용
    - 네트워크는 전송한 데이터가 목적지에 도달했는지 여부랑
      데이터가 자신을 위한 데이터라는 보장을 해주지 않기 때문에 tcp 에서 해주는 처리가 유용
    - tcp 를 사용하면 네트워크를 통해 데이터 전송시
      패킷 손실, 잘못된 순서로 도착 등의 문제에 대해 신경쓸 필요가 없다.
      
    server
    socket --> bind --> listen --> accept --> recv / send --> close
    
    base64 인코딩, 디코딩
    - 8비트 binary data 를 문자 코드에 영향을 받지 않는
      공통 ASCII 영역의 문자들로만 이루어진 일련의 스트링으로 바꾸는 인코딩 방식
    - ASCII 중 제어문자와 일부 특수문자를 제외한 64개의 안전한 출력 문자만을 이용
    - 특정 스트링을 서버에 전송했을 때에 #, @ 같은 기호들이 있을시 데이터 전송과 연동에
      어려운 부분이 있기 때문에 base64 를 이용하여 인코딩한 후 디코딩 하여 원래의 텍스트로 변환하여 사용
    - binary data 를 포함해야될 필요가 있을때, binary data 가 시스템 독립적으로
      동일하게 전송 또는 저장되는걸 보장하기 위해 사용
      
    1. 전송할 이미지 base64 인코딩
    1. 이미지 byte array 길이 전송
    2. 이미지 byte array 전송
      2-1. 서버에서 이미지를 1024byte씩 전송
           (이미지 byte 객체가 너무 커서 1024byte씩 잘라서 전송)
"""


class ServerSocket:
    def __init__(self, ip, port):
        self.TCP_IP = ip
        self.TCP_PORT = port
        self.drone = Tello()
        self.commend = ''
        self.socketOpen()
        # self.receiveThread = threading.Thread(target=self.receive)
        # self.receiveThread.start()
        
        
    def socketClose(self):
        self.sock.close()
        print(f"Server Socket [ TCP_IP: {self.TCP_IP}, TCP_PORT: {self.TCP_PORT} ] is close")
        
    def socketOpen(self):
        # 소켓 객체 생성
        # AF_INET (IPv4) / SOCK_STREAM (TCP)
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # WinError10048 해결 (포트 사용중라 연결할 수 없다는 에러)
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        # 소켓을 특정 네트워크 인터페이스와 포트 번호에 연결
        self.sock.bind((self.TCP_IP, self.TCP_PORT))
        # 서버가 클라이언트의 접속을 허용(99 : 접속허용수)
        self.sock.listen(99)
        print(f"Server Socket [ TCP_IP: {self.TCP_IP}, TCP_PORT: {self.TCP_PORT} ] is open")

        # accept() 함수에더 대기하다가 클라이어트가 접속하면 새로운 소켓을 리턴
        self.client_conn, self.addr = self.sock.accept()
        print(f"Server Socket [ TCP_IP: {self.TCP_IP}, TCP_PORT: {self.TCP_PORT} ] is connected with client")
        
        # self.receive()
        
        self.receiveThread = threading.Thread(target=self.receive)
        self.sendVideoThread = threading.Thread(target=self.sendVideo)
        # self.autoMoveThread = threading.Thread(target=Control_auto2.drone_control)
        self.receiveThread.start()
        # self.receiveThread.join()
        
             
    def receive(self):
        
        try:
            
            while True:
                if not self.drone.connect():
                    print(self.drone.get_battery())

                # 이미지전송과 라이브전송을 구분하기 위한 변수
                # 첫 2byte는 쓰레기값이 들어있다.
                getMsg = bytearray(self.client_conn.recv(1024))[2:]
                msg = getMsg.decode("utf-8")
                print(len(msg), msg)
                
                if len(msg) != 0:
                    if msg == "/image":
                        print("sendImage()")
                        self.sendImage()
                    elif msg == "/drone":
                        print("sendVideo()")
                        if not self.drone.streamoff():
                            print("drone stream off()")
                        
                        # self.sendVideo()  
                        self.sendVideoThread.start()
                        # self.sendVideoThread.join()
                        
                    elif msg == "/sendArea":
                        print("/sendArea")
                        Control_auto2.drone_control()
                        # self.autoMoveThread.start()
                        time.sleep(1)
                        self.socketClose()
                        time.sleep(0.1)
                        self.socketOpen()
                    else :
                        print("===" + msg + "===")
                        self.commend = msg
                    
        except Exception as e:
            print(e)
            # self.drone.streamoff()
            self.socketClose()
            time.sleep(0.1)
            self.socketOpen()
            

    def sendVideo(self):
        
        cnt = 0
        self.drone.streamon()
        # capture = cv2.VideoCapture("big_buck_bunny_720p_10mb.mp4")

        try:
            # while capture.isOpened():
            while True:
                now = time.localtime()
                # result, frame = capture.read()
                frame = self.drone.get_frame_read().frame
                frame = cv2.resize(frame, (1280, 720))
                
                # cv2.imshow("drone", frame)
                result, frame = cv2.imencode('.jpg', frame, [cv2.IMWRITE_JPEG_QUALITY, 90])
                
                data = numpy.array(frame)
                stringData = base64.b64encode(data)
                length = len(stringData)
                
                self.client_conn.sendall(length.to_bytes(4, byteorder="big"))
            
                while len(stringData):
                    if len(stringData) < 1024:
                        self.client_conn.sendall(stringData)
                        stringData = []
                    else:
                        self.client_conn.sendall(stringData[:1024])
                        stringData = stringData[1024:]
                
                # print(f"send image {cnt} : {length}bytes")
                
                cv2.waitKey(33)
                
                if self.commend != '':
                    print(self.commend)
                    print(len(self.commend))
                    
                    if self.commend == "takeOff":
                        # self.drone.takeoff()
                        print("takeoff")
                        # self.drone.send_rc_control(0, 0, 0, 0)
                    elif self.commend == "land":
                        self.drone.land()
                    elif self.commend == "cw":
                        self.drone.rotate_clockwise(90)
                    elif self.commend == "ccw":
                        self.drone.rotate_counter_clockwise(90)
                    elif self.commend == "forward":
                        self.drone.move_forward(30)
                    elif self.commend == "back":
                        self.drone.move_back(30)
                    elif self.commend == "Left":
                        self.drone.move_left(30)
                    elif self.commend == "Right":
                        self.drone.move_right(30)
                    elif self.commend == "up":
                        self.drone.move_up(30)
                    elif self.commend == "down":
                        self.drone.move_down(30)
                    elif self.commend == "capture":
                        t_day = self.getDate(now)
                        t_time = self.getTime(now)
                        cv2.imwrite(os.getcwd() + f"/drone_img/{t_day}_{t_time}.png", frame)

                    time.sleep(0.01)
                    self.commend = ''
                    
                time.sleep(0.001)
                cnt += 1
        except Exception as e:
            print(e)
            self.drone.streamoff()
            self.socketClose()
            time.sleep(0.1)
            self.socketOpen()
            
        self.client_conn.close()
            
    def sendImage(self):
        length = 10
        self.client_conn.sendall(length.to_bytes(4, byteorder="big"))
        for i in range(3):
            getDir = bytearray(self.client_conn.recv(1024))[2:].decode("utf-8")

            print(os.getcwd() + getDir)
            # img = cv2.imread(getDir, cv2.IMREAD_COLOR)
            img = cv2.imread(os.getcwd() + getDir)
            
            result, img = cv2.imencode('.jpg', img, [cv2.IMWRITE_JPEG_QUALITY, 90])
            
            data = numpy.array(img)
            stringData = base64.b64encode(data)
            length = len(stringData)
            
            print(length)
            
            self.client_conn.sendall(length.to_bytes(4, byteorder="big"))
            
            while len(stringData):
                if len(stringData) < 1024:
                    self.client_conn.sendall(stringData)
                    stringData = []
                else:
                    self.client_conn.sendall(stringData[:1024])
                    stringData = stringData[1024:]
                    
        self.socketClose()
        time.sleep(0.01)
        self.socketOpen()
        
    def getDate(self, now):
        year = str(now.tm_year)
        month = str(now.tm_mon)
        day = str(now.tm_mday)
        
        if len(month) == 1:
            month = '0' + month
        if len(day) == 1:
            day = '0' + day
        
        return (year + '-' + month + '-' + day)
        
    def getTime(self, now):
        return (str(now.tm_hour) + '.' + str(now.tm_min) + '.' + str(now.tm_sec))