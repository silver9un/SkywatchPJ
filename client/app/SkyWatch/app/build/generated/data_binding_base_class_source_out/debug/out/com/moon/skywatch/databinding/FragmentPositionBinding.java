// Generated by view binder compiler. Do not edit!
package com.moon.skywatch.databinding;

import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;
import android.widget.Button;
import android.widget.ToggleButton;
import androidx.annotation.NonNull;
import androidx.annotation.Nullable;
import androidx.constraintlayout.widget.ConstraintLayout;
import androidx.viewbinding.ViewBinding;
import androidx.viewbinding.ViewBindings;
import com.google.android.gms.maps.MapView;
import com.moon.skywatch.R;
import java.lang.NullPointerException;
import java.lang.Override;
import java.lang.String;

public final class FragmentPositionBinding implements ViewBinding {
  @NonNull
  private final ConstraintLayout rootView;

  @NonNull
  public final Button btnSendArea;

  @NonNull
  public final ToggleButton btnSetArea;

  @NonNull
  public final MapView mapView;

  private FragmentPositionBinding(@NonNull ConstraintLayout rootView, @NonNull Button btnSendArea,
      @NonNull ToggleButton btnSetArea, @NonNull MapView mapView) {
    this.rootView = rootView;
    this.btnSendArea = btnSendArea;
    this.btnSetArea = btnSetArea;
    this.mapView = mapView;
  }

  @Override
  @NonNull
  public ConstraintLayout getRoot() {
    return rootView;
  }

  @NonNull
  public static FragmentPositionBinding inflate(@NonNull LayoutInflater inflater) {
    return inflate(inflater, null, false);
  }

  @NonNull
  public static FragmentPositionBinding inflate(@NonNull LayoutInflater inflater,
      @Nullable ViewGroup parent, boolean attachToParent) {
    View root = inflater.inflate(R.layout.fragment_position, parent, false);
    if (attachToParent) {
      parent.addView(root);
    }
    return bind(root);
  }

  @NonNull
  public static FragmentPositionBinding bind(@NonNull View rootView) {
    // The body of this method is generated in a way you would not otherwise write.
    // This is done to optimize the compiled bytecode for size and performance.
    int id;
    missingId: {
      id = R.id.btn_sendArea;
      Button btnSendArea = ViewBindings.findChildViewById(rootView, id);
      if (btnSendArea == null) {
        break missingId;
      }

      id = R.id.btn_setArea;
      ToggleButton btnSetArea = ViewBindings.findChildViewById(rootView, id);
      if (btnSetArea == null) {
        break missingId;
      }

      id = R.id.mapView;
      MapView mapView = ViewBindings.findChildViewById(rootView, id);
      if (mapView == null) {
        break missingId;
      }

      return new FragmentPositionBinding((ConstraintLayout) rootView, btnSendArea, btnSetArea,
          mapView);
    }
    String missingId = rootView.getResources().getResourceName(id);
    throw new NullPointerException("Missing required view with ID: ".concat(missingId));
  }
}
