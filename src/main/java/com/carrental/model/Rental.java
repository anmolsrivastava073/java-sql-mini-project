package com.carrental.model;

import java.time.LocalDateTime;
import java.time.format.DateTimeFormatter;

// Represents a rental record linking customer, car, and days
public class Rental {
    private Integer rentalId;
    private Customer customer;
    private Car car;
    private Integer days;
    private Double totalAmount;
    private Boolean active;
    private String rentalDate;
    private String returnDate;

    public Rental(int rentalId, Customer customer, Car car, int days) {
        this.rentalId = rentalId;
        this.customer = customer;
        this.car = car;
        this.days = days;
        // Calls the overridden calculateRent method based on actual car type
        this.totalAmount = car.calculateRent(days);
        this.active = true;
        this.rentalDate = LocalDateTime.now().format(DateTimeFormatter.ofPattern("yyyy-MM-dd HH:mm"));
        this.returnDate = null;
    }

    public Integer getRentalId() {
        return rentalId;
    }

    public Customer getCustomer() {
        return customer;
    }

    public Car getCar() {
        return car;
    }

    public Integer getDays() {
        return days;
    }

    public Double getTotalAmount() {
        return totalAmount;
    }

    public Boolean isActive() {
        return active;
    }

    public String getRentalDate() {
        return rentalDate;
    }

    public String getReturnDate() {
        return returnDate;
    }

    public void completeRental() {
        this.active = false;
        this.returnDate = LocalDateTime.now().format(DateTimeFormatter.ofPattern("yyyy-MM-dd HH:mm"));
        this.car.setAvailable(true);
    }

    public void displayRental() {
        System.out.println("Rental ID: " + rentalId);
        System.out.println("Customer: " + customer.getName());
        System.out.println("Car: " + car.getBrand() + " " + car.getModel());
        System.out.println("Days: "  + days);
        System.out.println("Total Amount: Rs." + totalAmount);
        System.out.println("Status: " + (active ? "Active" : "Completed"));
        if (rentalDate != null) System.out.println("Rented On: " + rentalDate);
        if (returnDate != null) System.out.println("Returned On: " + returnDate);
    }
}
