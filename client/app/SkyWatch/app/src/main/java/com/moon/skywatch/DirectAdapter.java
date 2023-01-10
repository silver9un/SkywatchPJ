package com.moon.skywatch;

import android.content.Context;
import android.content.Intent;
import android.net.Uri;
import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;

import androidx.annotation.NonNull;
import androidx.recyclerview.widget.RecyclerView;

import java.util.ArrayList;

public class DirectAdapter extends RecyclerView.Adapter<DirectViewHolder> {

    private ArrayList<DirectVO> datas;
    private Context context; //activity에서 할 수 있는 일들을 Adapter에서도 수행하려고!

    public DirectAdapter(ArrayList<DirectVO> datas) {
        this.datas = datas;
        this.context = context;
    }

    @NonNull
    @Override
    public DirectViewHolder onCreateViewHolder(@NonNull ViewGroup parent, int viewType) {
        DirectViewHolder holder = new DirectViewHolder(LayoutInflater.from(parent.getContext())
        .inflate(R.layout.templete,parent,false));

        return holder;
    }

    @Override
    public void onBindViewHolder(@NonNull DirectViewHolder holder, int position) {
        final int temp = position;
        holder.tv_title.setText(datas.get(position).getTitle());
        holder.tv_address.setText(datas.get(position).getAddress());
        holder.btn_go.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                Intent intent = new Intent(Intent.ACTION_VIEW, Uri.parse(datas.get(temp).getAddress()));

                intent.addFlags(Intent.FLAG_ACTIVITY_NEW_TASK);
                context.startActivity(intent);

            }
        });
    }

    @Override
    public int getItemCount() {
        return datas.size();
    }
}
