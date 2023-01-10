package com.moon.skywatch;

import android.content.Intent;
import android.os.Bundle;
import android.view.View;
import android.widget.Button;
import android.widget.EditText;

import androidx.appcompat.app.AppCompatActivity;

public class AddActivity extends AppCompatActivity {

    EditText edt_title;
    EditText edt_addres;
    Button btn_ok;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_add);

        edt_title = findViewById(R.id.edt_title);
        edt_addres = findViewById(R.id.edt_addres);
        btn_ok = findViewById(R.id.btn_ok);



        btn_ok.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                Intent intent = new Intent();
                intent.putExtra("title",edt_title.getText().toString());
                intent.putExtra("addres",edt_addres.getText().toString());

                setResult(RESULT_OK,intent);
                finish();

            }
        });
    }
}