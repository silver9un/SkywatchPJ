package com.moon.skywatch;

import android.view.View;
import android.widget.Button;
import android.widget.TextView;

import androidx.annotation.NonNull;
import androidx.recyclerview.widget.RecyclerView;

public class DirectViewHolder extends RecyclerView.ViewHolder {
    // 생성자란 ?
    // 객체를 생성할 때 호출되는 메소드!
    // 생성자의 첫줄에는 super(); 생략되어 있음...
    // 상위클래스의 생성자를 호출하는 명령! => 무조건 생성자의 첫줄에만 작성가능!
    // 만약 상위클래스의 생성자에 매개변수가 있다면????
    // 하위클래스에서 반드시 생성자를 설계해서 super() 호출해줘야함

     TextView tv_title;
     TextView tv_address;
     Button btn_go;
     Button btn_add;



    public DirectViewHolder(@NonNull View itemView) {
        super(itemView);

        tv_title = itemView.findViewById(R.id.tv_title);
        tv_address = itemView.findViewById(R.id.tv_address);
        btn_go = itemView.findViewById(R.id.btn_go);
        btn_add = itemView.findViewById(R.id.btn_add);

    }





}
