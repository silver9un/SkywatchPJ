package com.moon.skywatch;

import android.graphics.Bitmap;

public class CarDataVO {
    private Bitmap imgParking1;
    // private Bitmap imgParking2;
    private Bitmap imgNumPlate;

    private String regulationDate;
    private String regulationTime;
    private String numPlate;
    private String regulationArea;

    public CarDataVO() {

    }

    public CarDataVO(Bitmap imgParking1, /*Bitmap imgParking2,*/ Bitmap imgNumPlate, String regulationDate, String regulationTime, String numPlate, String regulationArea) {
        this.imgParking1 = imgParking1;
        // this.imgParking2 = imgParking2;
        this.imgNumPlate = imgNumPlate;
        this.regulationDate = regulationDate;
        this.regulationTime = regulationTime;
        this.numPlate = numPlate;
        this.regulationArea = regulationArea;
    }

    public Bitmap getImgParking1() {
        return imgParking1;
    }

    public void setImgParking1(Bitmap imgParking1) {
        this.imgParking1 = imgParking1;
    }

    /*public Bitmap getImgParking2() {
        return imgParking2;
    }

    public void setImgParking2(Bitmap imgParking2) {
        this.imgParking2 = imgParking2;
    }*/

    public Bitmap getImgNumPlate() {
        return imgNumPlate;
    }

    public void setImgNumPlate(Bitmap imgNumPlate) {
        this.imgNumPlate = imgNumPlate;
    }

    public String getRegulationDate() {
        return regulationDate;
    }

    public void setRegulationDate(String regulationDate) {
        this.regulationDate = regulationDate;
    }

    public String getRegulationTime() {
        return regulationTime;
    }

    public void setRegulationTime(String regulationTime) {
        this.regulationTime = regulationTime;
    }

    public String getNumPlate() {
        return numPlate;
    }

    public void setNumPlate(String numPlate) {
        this.numPlate = numPlate;
    }

    public String getRegulationArea() {
        return regulationArea;
    }

    public void setRegulationArea(String regulationArea) {
        this.regulationArea = regulationArea;
    }

    @Override
    public String toString() {
        final StringBuffer sb = new StringBuffer("CarDataVO{");
        sb.append("imgParking1=").append(imgParking1);
        // sb.append(", imgParking2=").append(imgParking2);
        sb.append(", imgNumPlate=").append(imgNumPlate);
        sb.append(", regulationDate='").append(regulationDate).append('\'');
        sb.append(", regulationTime='").append(regulationTime).append('\'');
        sb.append(", numPlate='").append(numPlate).append('\'');
        sb.append(", regulationArea='").append(regulationArea).append('\'');
        sb.append('}');
        return sb.toString();
    }
}
