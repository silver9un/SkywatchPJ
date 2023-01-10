package com.moon.skywatch;

import android.graphics.Bitmap;
import android.graphics.BitmapFactory;
import android.os.Build;
import android.os.Bundle;
import android.os.Handler;
import android.util.Log;
import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;
import android.widget.Button;
import android.widget.ImageView;

import androidx.annotation.NonNull;
import androidx.annotation.RequiresApi;
import androidx.fragment.app.Fragment;

import java.io.DataInputStream;
import java.io.DataOutputStream;
import java.io.IOException;
import java.net.Socket;
import java.util.Base64;


public class LiveFragment extends Fragment {

    /*
    * 드론의 실시간 영상
    *
    * 서버는 드론의 영상을 frame 단위로 client 에 이미지로 전송
    * client 는 서버로 부터 받은 이미지 데이터를 받기 때문에 이미지를 연속해서 띄워주는 애니메이션 효과를 사용
    *
    * server client 는 tcp socket 통신을 이용
    * - 네트워크는 전송한 데이터가 목적지에 도달했는지 여부랑
    *   데이터가 자신을 위한 데이터라는 보장을 해주지 않기 때문에 tcp 에서 해주는 처리가 유용
    * - tcp 를 사용하면 네트워크를 통해 데이터 전송시
    *   패킷 손실, 잘못된 순서로 도착 등의 문제에 대해 신경쓸 필요가 없다.
    *
    * client
    * socket --> connect --> send / recv --> close
    *
    * base64 인코딩, 디코딩
    * - 8비트 binary data 를 문자 코드에 영향을 받지 않는
    *   공통 ASCII 영역의 문자들로만 이루어진 일련의 스트링으로 바꾸는 인코딩 방식
    * - ASCII 중 제어문자와 일부 특수문자를 제외한 64개의 안전한 출력 문자만을 이용
    * - 특정 스트링을 서버에 전송했을 때에 #, @ 같은 기호들이 있을시 데이터 전송과 연동에
    *   어려운 부분이 있기 때문에 base64 를 이용하여 인코딩한 후 디코딩 하여 원래의 텍스트로 변환하여 사용
    * - binary data 를 포함해야될 필요가 있을때, binary data 가 시스템 독립적으로
    *   동일하게 전송 또는 저장되는걸 보장하기 위해 사용
    *
    * 1. python server 에서 이미지 byte array 길이 전송
    * 2. server 이미지 byte array 전송
    *   2-1. 서버에서 이미지를 1024byte씩 전송 (이미지 byte 객체가 너무 커서 1024byte씩 잘라서 전송)
    *   2-2. 클라이언트는 1024byte씩 받은 배열을 1에서 받은 길이만크 붙여준다.
    * 3. 전송받은 이미지정보 base64 decodeing
    * 4. 이미지뷰에 적용
   * */

    String ip = ((MainActivity)MainActivity.context_main).ip;
    int flask_port = ((MainActivity)MainActivity.context_main).flask_port;
    int socket_port = ((MainActivity)MainActivity.context_main).socket_port;
    String url;

    // about socket
    private Handler mHandler;
    private Socket socket;
    private DataOutputStream outStream;
    private DataInputStream inStream;
    Thread checkUpdate;

    // 현재 fragment 를 벗어났을때 thread 동작을 제어하는 변수
    private boolean condition;

    View view;
    ImageView iv_droneView;
    Bitmap bmp;
    Button[] btn_drone;
    ImageView[] iv_drone;

    String commend;

    @Override
    public void onResume() {
        super.onResume();

        /*
         * 0 - forward   /   takeoff
         * 1 - back      /   land
         * 2 - left      /   cw (clock wise)
         * 3 - right     /   ccw (counter clock wise)
         * */
        btn_drone = new Button[]{view.findViewById(R.id.btn_droneForward), view.findViewById(R.id.btn_droneBack),
                view.findViewById(R.id.btn_droneLeft), view.findViewById(R.id.btn_droneRight)};

        iv_drone = new ImageView[]{view.findViewById(R.id.iv_droneUp), view.findViewById(R.id.iv_droneDown),
                view.findViewById(R.id.iv_droneCw), view.findViewById(R.id.iv_droneCcw), view.findViewById(R.id.iv_droneTakeOff), view.findViewById(R.id.iv_droneLand), view.findViewById(R.id.iv_droneCap)};

        Log.d("btn1", btn_drone[0] + "");

        for (int i = 0; i < btn_drone.length; i++) {
            final int temp = i;
            btn_drone[i].setOnClickListener(new View.OnClickListener() {
                @Override
                public void onClick(View view) {
                    switch (temp) {
                        case 0:
                            commend = "forward";
                            break;
                        case 1:
                            commend = "back";
                            break;
                        case 2:
                            commend = "Left";
                            break;
                        case 3:
                            commend = "Right";
                            break;
                    }
                }
            });
        }

        for (int i = 0; i < iv_drone.length; i++) {
            int temp = i;
            iv_drone[i].setOnClickListener(new View.OnClickListener() {
                @Override
                public void onClick(View view) {
                    switch (temp) {
                        case 0:
                            commend = "up";
                            break;
                        case 1:
                            commend = "down";
                            break;
                        case 2:
                            commend = "cw";
                            break;
                        case 3:
                            commend = "ccw";
                            break;
                        case 4:
                            commend = "takeOff";
                            break;
                        case 5:
                            commend = "land";
                            break;
                        case 6:
                            commend = "capture";
                            break;
                    }
                }
            });
        }

        // drone 실시간 영상 받아오기
        if(view != null){
            connect();
        }
    }

    public View onCreateView(@NonNull LayoutInflater inflater,
                             ViewGroup container, Bundle savedInstanceState) {

        view = inflater.inflate(R.layout.fragment_live, container, false);

        mHandler = new Handler();
        iv_droneView = view.findViewById(R.id.iv_droneView);
        condition = true;

    return view;
    }


    @Override
    public void onDestroyView() {
        super.onDestroyView();
        condition = false;
        view = null;
    }

    void connect() {
        Log.w("connect", "connecting...");
        commend = null;

        checkUpdate = new Thread(new Runnable() {
            @RequiresApi(api = Build.VERSION_CODES.O)
            @Override
            public void run() {

                try{
                    // 소켓 선언
                    socket = new Socket(ip, socket_port);

                    Log.w("서버 접속", "서버 접속 성공");
                } catch (IOException e1) {
                    Log.w("서버 접속 실패", "서버 접속 실패");
                    e1.printStackTrace();
                }

                try {
                    // 소켓 접속후 inputstream, ouputstream 받기
                    outStream = new DataOutputStream(socket.getOutputStream());
                    inStream = new DataInputStream(socket.getInputStream());
                    // 드론 영상을 받기위한 문자열 전송
                    outStream.writeUTF("/drone");
                    // 버퍼 비워주기
                    outStream.flush();
                } catch (IOException e) {
                    e.printStackTrace();
                    Log.w("버퍼 생성 실패", "버퍼 생성 실패");
                }

                // fragment를 종료하기 전까지 thread 열어두고 데이터 받기
                while (condition) {
                    try {

                        // 이미지 길이 받기
                        int length = inStream.readInt();
                        Log.d("data length: ",  length + "---");

                        // 전송받은 길이만큼 이미지 정보 받기
                        byte[] buffer = InPutStreamToByteArray(length, inStream);
                        Log.d("buffer", new String(buffer));

                        // 전송받은 이미지 정보 base64 디코딩
                        Base64.Decoder decoder = Base64.getDecoder();
                        byte[] decodedBytes = decoder.decode(buffer);

                        // Bitmap 저장
                        bmp = BitmapFactory.decodeByteArray(decodedBytes, 0, decodedBytes.length);

                        if (commend != null) {
                            Log.d("commend", commend);
                            outStream.writeUTF(commend);
                            outStream.flush();
                            commend = null;
                        }

                    } catch (Exception e) {
                        Log.d("sdafas", "asdfsadf");
                        break;
                    }

                    // ui 작업은 메인스레드에서만 가능
                    // socket 을 통해 받은 정보를 UI에 적용하기위해 handler를 통해 접근
                    mHandler.post(new Runnable() {
                        @Override
                        public void run() {
                            Log.d("bmp", bmp + "");
                            iv_droneView.setImageBitmap(Bitmap.createScaledBitmap(bmp, bmp.getWidth(), bmp.getHeight(), false));
                            Log.d("img 불러오기", "success");
                        }
                    });

                    try {
                        // 이미지가 순차적을 잘 재생되기 위해 sleep
                        Thread.sleep(10);
                    } catch (InterruptedException e) {
                        e.printStackTrace();
                    }
                }

                try {
                    socket.close();
                    Log.d("socket close", "socket close()");
                    // connect();
                } catch (IOException e) {
                    e.printStackTrace();
                }
            }
        });
        checkUpdate.start();
    }

    /*
    * 서버에서 1024byte씩 전송해주기 때문에
    * 이미지 길이 맞추어 전송받은 스트림을 이어 붙여주는 함수
    * */
    public byte[] InPutStreamToByteArray(int data_len, DataInputStream in) {
        int loop = (int)(data_len / 1024);
        Log.w("loop: ", Integer.toString(loop));
        byte[] resbytes = new byte[data_len];
        int offset = 0;

        try {
            for (int i = 0; i < loop; i++) {
                in.readFully(resbytes, offset, 1024);
                offset += 1024;
            }
            in.readFully(resbytes, offset, data_len-(loop*1024));
            Log.d("inStream", new String(resbytes));
            Log.w("resbytes len: ", Integer.toString(resbytes.length));
            Log.w("resbytes: ", new String(resbytes));
        } catch (IOException e) {
            e.printStackTrace();
        }

        return resbytes;
    }
}