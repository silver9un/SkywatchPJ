package com.moon.skywatch;

public class MapPointVO {
    private String pointName;
    private Double latitude;
    private Double longitude;

    public MapPointVO() {
    }

    public MapPointVO(String pointName, Double latitude, Double longitude) {
        this.pointName = pointName;
        this.latitude = latitude;
        this.longitude = longitude;
    }

    public String getPointName() {
        return pointName;
    }

    public void setPointName(String pointName) {
        this.pointName = pointName;
    }

    public Double getLatitude() {
        return latitude;
    }

    public void setLatitude(Double latitude) {
        this.latitude = latitude;
    }

    public Double getLongitude() {
        return longitude;
    }

    public void setLongitude(Double longitude) {
        this.longitude = longitude;
    }

    @Override
    public String toString() {
        final StringBuffer sb = new StringBuffer("MapPointVO{");
        sb.append("pointName='").append(pointName).append('\'');
        sb.append(", latitude=").append(latitude);
        sb.append(", longitude=").append(longitude);
        sb.append('}');
        return sb.toString();
    }
}
