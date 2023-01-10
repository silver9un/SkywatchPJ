package com.moon.joystick1;

import android.content.Context;
import android.content.res.Resources;
import android.content.res.TypedArray;
import android.graphics.Canvas;
import android.graphics.Paint;
import android.util.AttributeSet;
import android.view.MotionEvent;
import android.view.View;

import org.jetbrains.annotations.NotNull;
import org.jetbrains.annotations.Nullable;

import kotlin.Metadata;
import kotlin.jvm.internal.DefaultConstructorMarker;
import kotlin.jvm.internal.Intrinsics;
import kotlin.ranges.RangesKt;

public class JoystickView extends View implements Runnable{
    private final Paint basePaint = new Paint();
    private final Paint stickPaint = new Paint();
    private int baseColor;
    private int stickColor;
    private OnMoveListener moveListener;
    private boolean useSpring = true;
    private Thread mThread = new Thread((Runnable)this);
    private int moveUpdateInterval = 50;
    private float mPosX;
    private float mPosY;
    private float mCenterX;
    private float mCenterY;
    private float stickRatio;
    private float baseRatio;
    private float stickRadius;
    private float baseRadius;
    private static final String TAG = JoystickView.class.getSimpleName();
    private static final int DEFAULT_SIZE = 200;
    private static final int DEFAULT_UPDATE_INTERVAL = 50;
    @NotNull
    public static final JoystickView.Companion Companion = new Companion((DefaultConstructorMarker)null);

    protected void onSizeChanged(int w, int h, int oldw, int oldh) {
        super.onSizeChanged(w, h, oldw, oldh);
        this.mPosX = (float)(this.getWidth() / 2);
        this.mPosY = (float)(this.getWidth() / 2);
        this.mCenterX = this.mPosX;
        this.mCenterY = this.mPosY;
        int d = RangesKt.coerceAtMost(w, h);
        this.stickRadius = (float)(d / 2) * this.stickRatio;
        this.baseRadius = (float)(d / 2) * this.baseRatio;
    }

    public boolean onTouchEvent(@Nullable MotionEvent event) {
        Intrinsics.checkNotNull(event);
        this.mPosX = event.getX();
        this.mPosY = event.getY();
        OnMoveListener var10000;
        switch(event.getAction()) {
            case 0:
                if (this.mThread.isAlive()) {
                    this.mThread.interrupt();
                }

                this.mThread = new Thread((Runnable)this);
                this.mThread.start();
                var10000 = this.moveListener;
                if (var10000 != null) {
                    var10000.onMove(this.getAngle(), this.getStrength());
                }
                break;
            case 1:
                this.mThread.interrupt();
                if (this.useSpring) {
                    this.mPosX = this.mCenterX;
                    this.mPosY = this.mCenterY;
                    var10000 = this.moveListener;
                    if (var10000 != null) {
                        var10000.onMove(this.getAngle(), this.getStrength());
                    }
                }
        }

        float var3 = this.mPosX - this.mCenterX;
        byte var4 = 2;
        float var5 = (float)Math.pow((double)var3, (double)var4);
        var3 = this.mPosY - this.mCenterY;
        var4 = 2;
        var3 = var5 + (float)Math.pow((double)var3, (double)var4);
        float length = (float)Math.sqrt((double)var3);
        if (length > this.baseRadius) {
            this.mPosX = (this.mPosX - this.mCenterX) * this.baseRadius / length + this.mCenterX;
            this.mPosY = (this.mPosY - this.mCenterY) * this.baseRadius / length + this.mCenterY;
        }

        this.invalidate();
        return true;
    }

    protected void onDraw(@Nullable Canvas canvas) {
        if (canvas != null) {
            canvas.drawCircle((float)(this.getWidth() / 2), (float)(this.getWidth() / 2), this.baseRadius, this.basePaint);
        }

        if (canvas != null) {
            canvas.drawCircle(this.mPosX, this.mPosY, this.stickRadius, this.stickPaint);
        }

    }

    protected void onMeasure(int widthMeasureSpec, int heightMeasureSpec) {
        int d = RangesKt.coerceAtMost(this.measure(widthMeasureSpec), this.measure(heightMeasureSpec));
        this.setMeasuredDimension(d, d);
    }

    private final int measure(int measureSpec) {
        return MeasureSpec.getMode(measureSpec) == 0 ? 200 : MeasureSpec.getSize(measureSpec);
    }

    private final int getAngle() {
        float xx = this.mPosX - this.mCenterX;
        float yy = this.mCenterY - this.mPosY;
        int angle = (int)Math.toDegrees((double)((float)Math.atan2((double)yy, (double)xx)));
        return angle < 0 ? angle + 360 : angle;
    }

    private final int getStrength() {
        float var2 = this.mPosX - this.mCenterX;
        byte var3 = 2;
        float var10000 = (float)Math.pow((double)var2, (double)var3);
        var2 = this.mPosY - this.mCenterY;
        var3 = 2;
        var2 = var10000 + (float)Math.pow((double)var2, (double)var3);
        float length = (float)Math.sqrt((double)var2);
        return (int)(length / this.baseRadius * (float)100);
    }

    public void run() {
        while(true) {
            if (!Thread.interrupted()) {
                this.post((Runnable)(new Runnable() {
                    public final void run() {
                        OnMoveListener var10000 = JoystickView.this.moveListener;
                        if (var10000 != null) {
                            var10000.onMove(JoystickView.this.getAngle(), JoystickView.this.getStrength());
                        }

                    }
                }));

                try {
                    Thread.sleep((long)this.moveUpdateInterval);
                    continue;
                } catch (InterruptedException var2) {
                }
            }

            return;
        }
    }

    public final void setOnMoveListener(@NotNull OnMoveListener listener, int intervalMs) {
        Intrinsics.checkNotNullParameter(listener, "listener");
        this.moveListener = listener;
        this.moveUpdateInterval = intervalMs;
    }

    public final void setOnMoveListener(@NotNull OnMoveListener listener) {
        Intrinsics.checkNotNullParameter(listener, "listener");
        this.setOnMoveListener(listener, 50);
    }

    public JoystickView(@Nullable Context context, @Nullable AttributeSet attrs) {
        super(context, attrs);
        if (context != null) {
            Resources.Theme var10000 = context.getTheme();
            if (var10000 != null) {
                TypedArray var9 = var10000.obtainStyledAttributes(attrs, R.styleable.Joystick, 0, 0);
                if (var9 != null) {
                    TypedArray var3 = var9;
                    TypedArray $this$apply = var3;
                    boolean var5 = false;

                    try {
                        this.baseColor = $this$apply.getColor(R.styleable.Joystick_joystickBaseColor, -256);
                        this.stickColor = $this$apply.getColor(R.styleable.Joystick_joystickStickColor, -16776961);
                        this.stickRatio = $this$apply.getFraction(R.styleable.Joystick_joystickStickRatio, 1, 1, 0.25F);
                        this.baseRatio = $this$apply.getFraction(R.styleable.Joystick_joystickBaseRatio, 1, 1, 0.75F);
                        this.useSpring = $this$apply.getBoolean(R.styleable.Joystick_joystickUseSpring, true);
                    } finally {
                        var3.recycle();
                    }

                    this.basePaint.setAntiAlias(true);
                    this.basePaint.setColor(this.baseColor);
                    this.basePaint.setStyle(Paint.Style.FILL);
                    this.stickPaint.setAntiAlias(true);
                    this.stickPaint.setColor(this.stickColor);
                    this.stickPaint.setStyle(Paint.Style.FILL);
                }
            }
        }

    }

    // $FF: synthetic method
    public static final void access$setMoveListener$p(JoystickView $this, OnMoveListener var1) {
        $this.moveListener = var1;
    }

    @Metadata(
            mv = {1, 7, 1},
            k = 1,
            d1 = {"\u0000\u0018\n\u0002\u0018\u0002\n\u0002\u0010\u0000\n\u0000\n\u0002\u0010\u0002\n\u0000\n\u0002\u0010\b\n\u0002\b\u0002\bæ\u0080\u0001\u0018\u00002\u00020\u0001J\u0018\u0010\u0002\u001a\u00020\u00032\u0006\u0010\u0004\u001a\u00020\u00052\u0006\u0010\u0006\u001a\u00020\u0005H&¨\u0006\u0007"},
            d2 = {"Lcom/moon/joystick/JoystickView$OnMoveListener;", "", "onMove", "", "x", "", "y", "Testjoystick.joystick.main"}
    )
    public interface OnMoveListener {
        void onMove(int var1, int var2);
    }

    @Metadata(
            mv = {1, 7, 1},
            k = 1,
            d1 = {"\u0000\u001c\n\u0002\u0018\u0002\n\u0002\u0010\u0000\n\u0002\b\u0002\n\u0002\u0010\b\n\u0002\b\u0002\n\u0002\u0010\u000e\n\u0002\b\u0002\b\u0086\u0003\u0018\u00002\u00020\u0001B\u0007\b\u0002¢\u0006\u0002\u0010\u0002R\u000e\u0010\u0003\u001a\u00020\u0004X\u0082T¢\u0006\u0002\n\u0000R\u000e\u0010\u0005\u001a\u00020\u0004X\u0082T¢\u0006\u0002\n\u0000R\u0016\u0010\u0006\u001a\n \b*\u0004\u0018\u00010\u00070\u0007X\u0082\u0004¢\u0006\u0002\n\u0000¨\u0006\t"},
            d2 = {"Lcom/moon/joystick/JoystickView$Companion;", "", "()V", "DEFAULT_SIZE", "", "DEFAULT_UPDATE_INTERVAL", "TAG", "", "kotlin.jvm.PlatformType", "Testjoystick.joystick.main"}
    )
    public static final class Companion {
        private Companion() {
        }

        // $FF: synthetic method
        public Companion(DefaultConstructorMarker $constructor_marker) {
            this();
        }
    }
}
