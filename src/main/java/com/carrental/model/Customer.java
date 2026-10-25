package com.carrental.model;

// Customer class holding personal and license details
public class Customer {
    private Integer customerId;
    private String name;
    private String phone;
    private String drivingLicense;

    public Customer(int customerId, String name, String phone, String drivingLicense) {
        this.customerId = customerId;
        this.name = name;
        this.phone = phone;
        this.drivingLicense = drivingLicense;
    }

    public Integer getCustomerId() {
        return customerId;
    }

    public String getName() {
        return name;
    }

    public String getPhone() {
        return phone;
    }

    public String getDrivingLicense() {
        return drivingLicense;
    }

    public void displayCustomer() {
        System.out.println(
                "Customer ID: " + customerId +
                        " | Name: " + name +
                        " | Phone: " + phone +
                        " | License: " + drivingLicense
        );
    }
}
