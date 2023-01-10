package com.moon.skywatch;

import android.app.AlertDialog;
import android.app.DatePickerDialog;
import android.content.DialogInterface;
import android.content.pm.ActivityInfo;
import android.graphics.Bitmap;
import android.graphics.BitmapFactory;
import android.os.Build;
import android.os.Bundle;
import android.os.Handler;
import android.os.Looper;
import android.util.Log;
import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;
import android.widget.Button;
import android.widget.DatePicker;
import android.widget.EditText;
import android.widget.TextView;
import android.widget.Toast;

import androidx.annotation.NonNull;
import androidx.annotation.Nullable;
import androidx.annotation.RequiresApi;
import androidx.fragment.app.Fragment;
import androidx.recyclerview.widget.LinearLayoutManager;
import androidx.recyclerview.widget.RecyclerView;

import com.android.volley.AuthFailureError;
import com.android.volley.NetworkResponse;
import com.android.volley.ParseError;
import com.android.volley.Request;
import com.android.volley.RequestQueue;
import com.android.volley.Response;
import com.android.volley.VolleyError;
import com.android.volley.toolbox.HttpHeaderParser;
import com.android.volley.toolbox.StringRequest;
import com.android.volley.toolbox.Volley;

import org.json.JSONArray;
import org.json.JSONException;
import org.json.JSONObject;

import java.io.DataInputStream;
import java.io.DataOutputStream;
import java.io.IOException;
import java.io.UnsupportedEncodingException;
import java.net.Socket;
import java.text.SimpleDateFormat;
import java.util.ArrayList;
import java.util.Base64;
import java.util.Calendar;
import java.util.Date;
import java.util.HashMap;
import java.util.Map;


public class NumberFragment extends Fragment {

    /*
    * 날짜 또는 번호판 검색으로 불법주정차 리스트 출력
    * - 사진, 날짜, 시간, 주차 구역, 차량 번호판 출력
    *
    * 웹과 request, response 를 단순화 하기 위해 Volley 라이브러리(Http 통신) 사용
    * 사용법
    * 1. request 객체를 만들고 이 request 객체를 request queue 에 넣어준다.
    * 2. request queue 가 웹서버에 요청하고 응답까지 받아준다.
    * 3. 응답을 받을 수 있도록 메서드를 만들어 두면 응답이 왔을때 자동으로 해당 메서드를 호출
    *
    * 장점
    * 1. thread 사용 불필요
    * 2. request queue 가 내부에서 thread 를 만들어 웹서버에 요청하고 응답받는 과정 진행
    * 3. handler 사용 불필요 <-- 응답을 처리할 수 있는 메서드를 호출할 때는 메인 스레드에서 처리할 수 있도록 만든다.
    *
    * 이미지 주소값을 받으면 Tcp Socket 통신을 이용해서
    * 이미지 정보를 가진 byte 배열 받고 출력
    * */

    static RequestQueue requestQueue;

    private Socket socket;
    private DataOutputStream outStream;
    private DataInputStream inStream;

    String ip = ((MainActivity)MainActivity.context_main).ip;
    int flask_port = ((MainActivity)MainActivity.context_main).flask_port;
    int socket_port = ((MainActivity)MainActivity.context_main).socket_port;
    String url;

    Button btn_date;
    Button btn_carNum;
    TextView editTextDate;
    View view;
    Date nowDate;
    Date setDate;
    SimpleDateFormat simpleDateFormat;
    JSONArray jsonArray;
    JSONObject jsonObject;
    CarDataAdapter carDataAdapter;
    ArrayList<CarDataVO> carDataList;
    RecyclerView rcv;

    String getDate;
    String sendDate;

    String regulation_date;
    String regulation_time;
    String regulation_area;
    String car_num;
    String img_parking1;
//    String img_parking2;
    String img_numPlate;

    Bitmap bmp_parking1;
//    Bitmap bmp_parking2;
    Bitmap bmp_numPlate;

    byte[][] img_list;

    int check;

    CarDataVO cvo;

    public View onCreateView(@NonNull LayoutInflater inflater,
                             ViewGroup container, Bundle savedInstanceState) {

        getActivity().setRequestedOrientation(ActivityInfo.SCREEN_ORIENTATION_PORTRAIT);
        view = inflater.inflate(R.layout.fragment_number, container, false);

        btn_date = view.findViewById(R.id.btn_date);
        btn_carNum = view.findViewById(R.id.btn_carNum);
        editTextDate = view.findViewById(R.id.editTextDate);
        rcv = view.findViewById(R.id.recyclerview);

        simpleDateFormat = new SimpleDateFormat("yyyy-MM-dd");
        nowDate = Calendar.getInstance().getTime();
        getDate = simpleDateFormat.format(nowDate);
        editTextDate.setText(getDate);

        carDataList = new ArrayList<>();
        carDataAdapter = new CarDataAdapter(getContext(), carDataList);
        rcv.setAdapter(carDataAdapter);
        rcv.setLayoutManager(new LinearLayoutManager(this.getContext()));

        // 날짜 검색시 스피너 형태의 날짜 선택 화면 띄워주기
        // 초기 화면에서는 현재 날짜를 기본으로 띄워준다.
        final Calendar date = Calendar.getInstance();

        DatePickerDialog datePickerDialog = new DatePickerDialog(
                view.getContext(), new DatePickerDialog.OnDateSetListener() {
            @Override
            public void onDateSet(DatePicker datePicker, int year, int month, int dayOfMonth) {
                Calendar updateDate = Calendar.getInstance();
                updateDate.set(year, month, dayOfMonth);

                setDate = updateDate.getTime();
                getDate = simpleDateFormat.format(setDate);
                editTextDate.setText(getDate);

                // 날짜 설정을 하고 확인 버튼을 누르면 해당 날짜를 서버에 request
                makeRequestDate(getDate);
            }
        }, date.get(Calendar.YEAR), date.get(Calendar.MONTH), date.get(Calendar.DAY_OF_MONTH));

        datePickerDialog.getDatePicker().setSpinnersShown(true);

        // 날짜 검색 버튼 누를 시
        btn_date.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View view) {
                datePickerDialog.show();
                sendDate = editTextDate.getText().toString();
                Log.d("sendDate", sendDate);

            }
        });

        // 차량번호 검색시 입력 dialog 띄우기
        btn_carNum.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View view) {
                final EditText et_carNum = new EditText(view.getContext());
                AlertDialog.Builder builder = new AlertDialog.Builder(view.getContext());
                builder.setTitle("차량번호를 입력해주세요");
                builder.setView(et_carNum);
                builder.setPositiveButton("입력", new DialogInterface.OnClickListener() {
                    @Override
                    public void onClick(DialogInterface dialogInterface, int i) {
                        editTextDate.setText(et_carNum.getText().toString());

                        // 차량번호 서버에 request
                        makeRequestCarNum(et_carNum.getText().toString());
                    }
                });
                builder.show();
            }
        });


        if (requestQueue == null) {
            requestQueue = Volley.newRequestQueue(view.getContext());
        }


        return view;
    }

    @Override
    public void onDestroyView() {
        super.onDestroyView();
        view = null;
    }

    // 서버로 부터 response 받은 데이터를 json 객체화
    public void getResponseData(String response) {
        try {
            carDataList.clear();
            jsonArray = new JSONArray(response);
            Log.d("jsonArray Length", jsonArray.length() + "");

            for (int i = 0; i < jsonArray.length(); i++) {
                jsonObject = jsonArray.getJSONObject(i);

                regulation_date = (String) jsonObject.get("regulation_date");
                regulation_time = (String) jsonObject.get("regulation_time");
                regulation_area = (String) jsonObject.get("regulation_area");
                car_num = (String) jsonObject.get("car_num");

                img_parking1 = (String) jsonObject.get("imgdir_parking");
//                img_parking2 = (String) jsonObject.get("imgdir_parking2");
                img_numPlate = (String) jsonObject.get("imgdir_numplate");

                String[] car_data = new String[]{regulation_date, regulation_time, regulation_area, car_num};
                String[] imgDir = new String[]{img_parking1, /*img_parking2,*/ img_numPlate};

                if (imgDir.length != 0) {
                    connect(imgDir);
                }

                if (check == 1) {
                    // 받은 결과값을 vo 객체에 담고 Arraylist에 담아주기
                    carDataList.add(setResult(car_data, img_list));
                    Log.d("carDataList add", "add");
                }

                Thread.sleep(100);
            }

            Log.d("carDataList size", carDataList.size() + "");
            carDataAdapter.notifyDataSetChanged();

        } catch (JSONException e) {
            e.printStackTrace();
        } catch (InterruptedException e) {
            e.printStackTrace();
        }
    }

    public void makeRequestDate(String sendDate) {
        check = 0;

        String url = "http://" + ip + ":" + flask_port + "/features/getDate_android";

        StringRequest request = new StringRequest(Request.Method.POST, url,
                new Response.Listener<String>() {
                    @Override
                    public void onResponse(String response) {
                        Log.d("response", response);
                        if (response.equals("none")) {
                            Toast.makeText(view.getContext(), "검색 결과가 존재하지 않습니다.", Toast.LENGTH_SHORT).show();
                        } else {
                            // 서버로 부터 response 받은 데이터 --> json object
                            getResponseData(response);
                        }
                    }
                }, new Response.ErrorListener() {
            @Override
            public void onErrorResponse(VolleyError error) {
                Log.d("Response Error", "" + error.getMessage());
            }
        }) {
            @Override //response를 UTF8로 변경해주는 소스코드
            protected Response<String> parseNetworkResponse(NetworkResponse response) {
                try {
                    String utf8String = new String(response.data, "UTF-8");
                    Log.d("utf8string", utf8String);
                    return Response.success(utf8String, HttpHeaderParser.parseCacheHeaders(response));
                } catch (UnsupportedEncodingException e) {
                    // log error
                    return Response.error(new ParseError(e));
                } catch (Exception e) {
                    // log error
                    return Response.error(new ParseError(e));
                }
            }
            @Nullable
            @Override
            protected Map<String, String> getParams() throws AuthFailureError {
                HashMap<String, String> param = new HashMap<>();
                // 서버로 전송해줄 데이터
                param.put("sendDate", sendDate);

                return param;
            }
        };

        request.setShouldCache(false);
        requestQueue.add(request);
    }

    public void makeRequestCarNum(String carNum) {
        check = 0;

        String url = "http://" + ip + ":" + flask_port + "/features/getCarNum_android";

        StringRequest request = new StringRequest(Request.Method.POST, url,
                new Response.Listener<String>() {
                    @Override
                    public void onResponse(String response) {
                        Log.d("response", response);
                        if (response.equals("none")) {
                            Toast.makeText(view.getContext(), "검색 결과가 존재하지 않습니다.", Toast.LENGTH_SHORT).show();
                        } else {
                            getResponseData(response);
                            Log.d("response", response);
                        }
                    }
                }, new Response.ErrorListener() {
            @Override
            public void onErrorResponse(VolleyError error) {
                Log.d("Response Error", "" + error.getMessage());
            }
        }) {
            @Override //response를 UTF8로 변경해주는 소스코드
            protected Response<String> parseNetworkResponse(NetworkResponse response) {
                try {
                    String utf8String = new String(response.data, "UTF-8");
                    Log.d("utf8string", utf8String);
                    return Response.success(utf8String, HttpHeaderParser.parseCacheHeaders(response));
                } catch (UnsupportedEncodingException e) {
                    // log error
                    return Response.error(new ParseError(e));
                } catch (Exception e) {
                    // log error
                    return Response.error(new ParseError(e));
                }
            }
            @Nullable
            @Override
            protected Map<String, String> getParams() throws AuthFailureError {
                HashMap<String, String> param = new HashMap<>();
                param.put("carNum", carNum);

                return param;
            }
        };

        request.setShouldCache(false);
        requestQueue.add(request);
    }

    // 서버로부터 받는 이미지 스트림을 byte array 로 변환해주는 함수
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
            //Log.w("get image", "get image");
        } catch (IOException e) {
            e.printStackTrace();
        }

        return resbytes;
    }

    // 이미지가 저장되어있는 서버에 주소값을 보내주고 이미지 정보를 받는 함수 (tcp socket 이용)
    void connect(String[] imgDir) {
        Handler mHandler = new Handler(Looper.getMainLooper());
        Log.w("connect", "connecting...");
        Log.d("imgDir len", imgDir.length + "");

        Bitmap bmp;

        Thread checkUpdate = new Thread() {
            @RequiresApi(api = Build.VERSION_CODES.O)
            public void run() {

                try{
                    socket = new Socket(ip, socket_port);
                    Log.w("서버 접속", "서버 접속 성공");
                } catch (IOException e1) {
                    Log.w("서버 접속 실패", "서버 접속 실패");
                    e1.printStackTrace();
                }

                try {
                    outStream = new DataOutputStream(socket.getOutputStream());
                    inStream = new DataInputStream(socket.getInputStream());
                    outStream.writeUTF("/image");
                    outStream.flush();
                    inStream.readInt();
                } catch (IOException e) {
                    e.printStackTrace();
                    Log.w("버퍼 생성 실패", "버퍼 생성 실패");
                }

                Log.w("버퍼 생성 성공", "버퍼 생성 성공");

                int img_len = 0;

                img_list = new byte[imgDir.length][];

                for (int i = 0; i < imgDir.length; i++) {
                    try {
                        Log.d("imgDir", i + " : " + imgDir[i]);
                        outStream.writeUTF(imgDir[i]);
                        outStream.flush();
                        Log.d("send img dir", "send img dir");

                        img_len = inStream.readInt();
                        Log.d("get img len", img_len + "");
                    } catch (IOException e) {
                        Log.d("send img dir error", "send img dir error");
                    }

                    img_list[i] = InPutStreamToByteArray(img_len, inStream);
                    Log.d("img receive", (i + 1) + "img receive");
                }

                try {
                    socket.close();
                } catch (IOException e) {

                }
            }
        };
        checkUpdate.start();

        try {
            checkUpdate.join();
        }catch (InterruptedException e){

        }
        check = 1;
        Log.d("Thread terminated", "Thread terminated");
    }

    // json object vo에 담기
    public CarDataVO setResult(String[] car_data, byte[][] img_list) {

        CarDataVO vo = new CarDataVO();

        vo.setRegulationDate(car_data[0]);
        vo.setRegulationTime(car_data[1]);
        vo.setRegulationArea(car_data[2]);
        vo.setNumPlate(car_data[3]);

        for (int i = 0; i < img_list.length; i++) {
            Base64.Decoder decoder = null;
            if (android.os.Build.VERSION.SDK_INT >= android.os.Build.VERSION_CODES.O) {
                decoder = Base64.getDecoder();

                byte[] decodedBytes = decoder.decode(img_list[i]);
                Bitmap bmp = BitmapFactory.decodeByteArray(decodedBytes, 0, decodedBytes.length);

                switch (i) {
                    case 0:
                        bmp_parking1 = bmp;
                        break;
                    /*case 1:
                        bmp_parking2 = bmp;
                        break;*/
                    case 1:
                        bmp_numPlate = bmp;
                        break;
                }
            }
            Log.d("setResult", i + "");
        }

        vo.setImgParking1(bmp_parking1);
        vo.setImgNumPlate(bmp_numPlate);

        return vo;
    }


}

