package com.moon.skywatch;

import android.view.View;
import android.widget.ImageView;
import android.widget.TextView;

import androidx.annotation.NonNull;
import androidx.recyclerview.widget.RecyclerView;

public class CarDataViewHolder extends RecyclerView.ViewHolder {

    ImageView imgCarParking1;
    ImageView imgCarParking2;
    ImageView imgNumPlate;
    TextView tv_date;
    TextView tv_time;
    TextView tv_carNum;
    TextView tv_area;

    public CarDataViewHolder(@NonNull View itemView) {
        super(itemView);

        imgCarParking1 = (ImageView) itemView.findViewById(R.id.imgCarParking1);
        // imgCarParking2 = (ImageView) itemView.findViewById(R.id.imgCarParking2);
        imgNumPlate = (ImageView) itemView.findViewById(R.id.imgNumPlate);

        tv_date = (TextView) itemView.findViewById(R.id.tv_date);
        tv_time = (TextView) itemView.findViewById(R.id.tv_time);
        tv_carNum = (TextView) itemView.findViewById(R.id.tv_carNum);
        tv_area = (TextView) itemView.findViewById(R.id.tv_area);
    }
}
