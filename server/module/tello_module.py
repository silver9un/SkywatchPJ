import socket
import time
import threading
import cv2
from threading import Thread
from module.decorators import accepts

# 오픈소스 가져옴

"""
Tello 환경 설정, 동작 또는 조작 클래스
"""
class Tello:
    UDP_IP = '192.168.10.1' #드론 아이피
    UDP_PORT = 8889 #드론 포트
    RESPONSE_TIMEOUT = 0.5 # 응답시간 초과
    TIME_BTW_COMMANDS = 0.5 #명령 사이의 시간
    TIME_BTW_RC_CONTROL_COMMANDS = 0.5 # RC 제어 명령 사이의 시간
    last_received_command = time.time() # 마지막으로 받은 명령

    # 비디오 스트림, 서버 소켓
    VS_UDP_IP = '0.0.0.0'
    VS_UDP_PORT = 11111

    # 비디오캡처 객체
    cap = None
    background_frame_read = None
    stream_on = False

    def __init__(self):
        self.address = (self.UDP_IP, self.UDP_PORT)
        # SOCK_DGRAM은 프롤토콜의 전송방식인 데이터 그램이라고함, AF_INET는 ipv4
        self.clientSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.clientSocket.bind(('',self.UDP_PORT)) #드론으로 연결
        self.response = None
        self.stream_on = False

        thread = threading.Thread(target=self.run_udp_receiver, args=())
        thread.daemon = True # 메인쓰레드가 종료되면 같이 종료되는 쓰레드
        thread.start()

    def run_udp_receiver(self):
        """Setup drone UDP receiver. This method listens for responses of Tello. Must be run from a background thread
                in order to not block the main thread."""
        while True:
            try:
                self.response, _ = self.clientSocket.recvfrom(1024)
            except Exception as e:
                print(e)
                break

    def get_udp_video_address(self):
        return 'udp://@' + self.VS_UDP_IP + ":" + str(self.VS_UDP_PORT)

    def get_video_capture(self):
        # 아 카메라 포트번호 가져와서 cv2.VideoCapture쓰는구나
        if self.cap is None:
            self.cap = cv2.VideoCapture(self.get_udp_video_address())

        if not self.cap.isOpened():
            self.cap.open(self.get_udp_video_address())
        return self.cap

    def get_frame_read(self):
        # 백그라운드 프레임 얻기
        if self.background_frame_read is None:
            self.background_frame_read = BackgroundFrameRead(self, self.get_udp_video_address()).start()
        return self.background_frame_read

    # 비디오 멈추는 함수
    def stop_video_capture(self):
        return self.streamoff()

    # tello에 명령 보내고 응답기다리는 함수
    # true, false 함수임
    @accepts(command=str)
    def send_command_with_return(self, command):
        diff = time.time() * 1000 - self.last_received_command
        if diff < self.TIME_BTW_COMMANDS:
            time.sleep(diff)

        print('Send command: ' + command)
        timestamp = int(time.time() * 1000)

        self.clientSocket.sendto(command.encode('utf-8'), self.address)

        while self.response is None:
            if (time.time() * 1000) - timestamp > self.RESPONSE_TIMEOUT * 1000:
                print('Timeout exceed on command ' + command)
                return False

        print('Response: ' + str(self.response))

        response = self.response.decode('utf-8')
        self.response = None

        self.last_received_command = time.time() * 1000

        return response


    # 응답을 기대하지않고 tello에 명령을 보내는 함수
    @accepts(command=str)
    def send_command_without_return(self,command):
        print('send command (no expect response) : ' + command)
        self.clientSocket.sendto(command.encode('utf-8'), self.address)

    # 이부분은 이해가 안감
    @accepts(command=str)
    def send_control_command(self,command):
        response = self.send_command_with_return(command)

        # 왜? OK 라는게 이해가 안됨 response가..
        # 아 self 부분에서 response있네 그러면 send_command_with_reutnr부분이..?
        # 조작 또는 상태에 따라 반환하는 함수구나
        if response == 'OK' or response == 'ok':
            return True
        else:
            return self.return_error_on_send_command(command, response)

    # tello에 set명령을 보내고 응답을 기다림
    @accepts(command=str)
    def send_read_command(self, command):
        response = self.send_command_with_return(command)

        try:
            response = str(response)
        except TypeError as e:
            print(e)
            pass

        if ('error' not in response) and ('ERROR' not in response) and ('False' not in response):
            if response.isdigit():
                return int(response)
            else:
                return response
        else:
            return self.return_error_on_send_command(command, response)

    @staticmethod
    def return_error_on_send_command(command, response):
        print('Command ' + command + ' was unsuccessful. Message: ' + str(response))
        return False

    def connect(self):
        return self.send_control_command("command")

    def takeoff(self):
        return self.send_control_command("takeoff")

    def land(self):
        return self.send_control_command("land")


    def streamon(self):
        result = self.send_control_command("streamon")
        if result is True:
            self.stream_on = True
        return result


    def streamoff(self):
        result = self.send_control_command("streamoff")
        if result is True:
            self.stream_on = False
        return result

    def emergency(self):
        return self.send_control_command("emergency")

    @accepts(direction=str,x=int)
    def move(self,direction,x):
        return self.send_control_command(direction + ' ' + str(x))

    @accepts(x=int)
    def move_up(self,x):
        return self.move("up",x)

    @accepts(x=int)
    def move_down(self, x):
        return self.move("down",x)

    @accepts(x=int)
    def move_left(self,x):
        return self.move("left",x)

    @accepts(x=int)
    def move_right(self,x):
        return self.move("right",x)

    @accepts(x=int)
    def move_forward(self,x):
        return self.move("forward",x)

    @accepts(x=int)
    def move_back(self,x):
        return self.move("back",x)

    # 재정의 함수하나있었음 똑같은 함수2개임
    @accepts(x=int)
    def move_up(self,x):
        return self.move("up",x)

    # 시계방향으로 회전합니다.
    @accepts(x=int)
    def rotate_clockwise(self,x):
        return self.send_control_command("cw "+str(x))

    @accepts(x=int)
    def rotate_counter_clockwise(self,x):
        return self.send_control_command("ccw "+str(x))

    def flip(self,direction):
        return self.send_control_command("flip "+direction)

    def flip_left(self):
        return self.flip("l")

    def flip_right(self):
        return self.flip("r")

    def flip_forward(self):
        return self.flip("f")

    def flip_back(self):
        return self.flip("b")

    @accepts(x=int, y=int, z=int, speed=int)
    def go_xyz_speed(self,x,y,z,speed):
        return self.send_command_without_return(f'go {x} {y} {z} {speed}')

    @accepts(x1=int,y1=int,z1=int,x2=int,y2=int,z2=int,speed=int)
    def go_xyz_speed(self, x1,y1,z1,x2,y2,z2,speed):
        return self.send_command_without_return(f'curve {x1} {y1} {z1} {x2} {y2} {z2} {speed}')

    @accepts(x=int)
    def set_speed(self,x):
        return self.send_control_command("speed " + str(x))

    last_rc_control_sent = 0

    @accepts(left_right_velocity=int,forward_backward_velocity=int, up_down_velocity=int,yaw_velocity=int)
    def send_rc_control(self,left_right_velocity, forward_backward_velocity, up_down_velocity, yaw_velocity):
        if int(time.time() * 1000) - self.last_rc_control_sent < self.TIME_BTW_RC_CONTROL_COMMANDS:
            pass
        else:
            self.last_rc_control_sent = int(time.time() + 1000)
            return self.send_command_with_return(f'rc {left_right_velocity} {forward_backward_velocity} {up_down_velocity} {yaw_velocity}')

    def set_wifi_with_ssid_password(self):
        return self.send_control_command('wifi ssid pass')

    def get_speed(self):
        return self.send_read_command('speed?')

    def get_battery(self):
        return self.send_read_command("battery?")

    def get_flight_time(self):
        return self.send_read_command('time?')

    def get_height(self):
        return self.send_read_command('height?')

    def get_temperature(self):
        return self.send_read_command('temperature?')

    def get_attitude(self):
        return self.send_read_command('attitude?')

    def get_barometer(self):
        return self.send_read_command('baro?')

    def get_distance_tof(self):
        return self.send_read_command('tof?')

    def get_wifi(self):
        return self.send_read_command('wifi?')

    def end(self):
        if self.stream_on:
            self.streamoff()

        if self.background_frame_read is not None:
            self.background_frame_read.stop()

        if self.cap is not None:
            self.cap.release()


class BackgroundFrameRead:
    def __init__(self, tello, address):
        tello.cap = cv2.VideoCapture(address)
        self.cap = tello.cap

        if not self.cap.isOpened():
            self.cap.open(address)

        self.grabbed, self.frame = self.cap.read()
        self.stopped = False

    def start(self):
        Thread(target=self.update_frame, args=()).start()
        return self

    def update_frame(self):
        while not self.stopped:
            if not self.grabbed or not self.cap.isOpened():
                self.stop()
            else:
                (self.grabbed, self.frame) = self.cap.read()

    def stop(self):
        self.stopped = True











