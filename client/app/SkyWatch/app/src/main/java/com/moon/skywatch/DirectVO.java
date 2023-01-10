package com.moon.skywatch;

public class DirectVO {
    private String title;
    private String address;






    public DirectVO(String title, String address) {
        this.title = title;
        this.address = address;
    }

    public String getTitle() {
        return title;
    }
    public void setTitle(String title) {
        this.title = title;
    }
    public String getAddress() {
        return address;
    }
    public void setAddress(String address) {
        this.address = address;
    }


    @Override
    public String toString() {
        // String 을 + 연산하게되면 메모리낭비가 심함!
        // StringBuffer => 고급

        StringBuffer temp = new StringBuffer();
        temp.append("DirectVO");
        temp.append("title='");
        temp.append(title);
        temp.append(", address='");
        temp.append(address);
        temp.append("}");

        return temp.toString();
    }
}
