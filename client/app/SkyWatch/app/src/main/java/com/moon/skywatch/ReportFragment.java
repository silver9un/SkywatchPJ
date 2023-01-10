package com.moon.skywatch;

import android.app.AlertDialog;
import android.content.DialogInterface;
import android.content.Intent;
import android.content.pm.ActivityInfo;
import android.net.Uri;
import android.os.Bundle;
import android.util.Log;
import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;
import android.widget.Toast;

import androidx.annotation.NonNull;
import androidx.fragment.app.Fragment;

import com.google.android.gms.maps.CameraUpdateFactory;
import com.google.android.gms.maps.GoogleMap;
import com.google.android.gms.maps.MapView;
import com.google.android.gms.maps.OnMapReadyCallback;
import com.google.android.gms.maps.model.LatLng;
import com.google.android.gms.maps.model.Marker;
import com.google.android.gms.maps.model.MarkerOptions;
import com.moon.skywatch.databinding.FragmentReportBinding;

import java.util.Iterator;


public class ReportFragment extends Fragment implements OnMapReadyCallback{

    /*
    * 현재 위치 또는 단속 구역 인근의 경찰서에
    * 신고할 수 있는 fragment
    *
    * google map 활용
    * 해당 마커에 해당하는 경찰서에 전화
    * */

    private GoogleMap gmap;
    private MapView mmapView;
    private FragmentReportBinding binding;

    public View onCreateView(@NonNull LayoutInflater inflater,
                             ViewGroup container, Bundle savedInstanceState) {

        binding = FragmentReportBinding.inflate(inflater, container, false);
        View root = binding.getRoot();
        getActivity().setRequestedOrientation(ActivityInfo.SCREEN_ORIENTATION_PORTRAIT);

        mmapView = (MapView) root.findViewById(R.id.reportmap);
        mmapView.onCreate(savedInstanceState);
        mmapView.getMapAsync(new OnMapReadyCallback() {
            @Override
            public void onMapReady(@NonNull GoogleMap googleMap) {
                gmap = googleMap;

                LatLng latLng = new LatLng(35.149796202004325, 126.91992834014);
                googleMap.addMarker(new MarkerOptions().position(latLng).title("스마트인재개발원"));
                latLng = new LatLng(35.14926434318328 , 126.91984381043518 );
                gmap.addMarker(new MarkerOptions().position(latLng).title("광주동부경찰서"));

                latLng = new LatLng(35.149521034504936 , 126.91954725211693 );
                gmap.addMarker(new MarkerOptions().position(latLng).title("금남지구대"));


                gmap.moveCamera(CameraUpdateFactory.newLatLngZoom(latLng,19));

                gmap.setOnInfoWindowClickListener(new GoogleMap.OnInfoWindowClickListener() {
                    @Override
                    public void onInfoWindowClick(@NonNull Marker marker) {
                        android.app.AlertDialog.Builder builder = new android.app.AlertDialog.Builder(getContext());
                        String markerArea = marker.getTitle();
                        builder.setTitle(markerArea);
                        builder.setMessage("관할 지역으로 신고 하시겠습니까?");

                        builder.setPositiveButton("확인", new DialogInterface.OnClickListener() {
                            @Override
                            public void onClick(DialogInterface dialogInterface, int i) {
                                Intent intent = new Intent(Intent.ACTION_DIAL);
                                intent.setData(Uri.parse("tel:01021628994"));
                                if(intent.resolveActivity(getActivity().getPackageManager()) != null){
                                    startActivity(intent);

                                }
                            }
                        });

                        builder.setNegativeButton("취소", new DialogInterface.OnClickListener() {
                            @Override
                            public void onClick(DialogInterface dialogInterface, int i) {

                            }
                        });

                        AlertDialog alertDialog = builder.create();
                        alertDialog.show();
                    }
                });
            }
        });




        return root;
    }

    @Override
    public void onDestroyView() {
        super.onDestroyView();
        binding = null;
    }
    @Override
    public void onMapReady(@NonNull GoogleMap googleMap) {
        googleMap.addMarker(new MarkerOptions()
                .position(new LatLng(0, 0))
                .title("Marker"));

    }
    @Override
    public void onResume() {
        super.onResume();
        mmapView.onResume();
    }
    @Override
    public void onPause() {
        super.onPause();
        mmapView.onPause();
    }
    @Override
    public void onLowMemory() {
        super.onLowMemory();
        mmapView.onLowMemory();
    }
    @Override
    public void onDestroy() {
        mmapView.onDestroy();
        super.onDestroy();
    }
}