package com.carrental.model;

// Abstract base class representing a car
public abstract class Car {
    private Integer carId;
    private String brand;
    private String model;
    private Double pricePerDay;
    private Boolean available;

    public Car(int carId, String brand, String model, double pricePerDay) {
        this.carId = carId;
        this.brand = brand;
        this.model = model;
        this.pricePerDay = pricePerDay;
        this.available = true;
    }

    // Abstract method implemented differently by subclasses (Polymorphism)
    public abstract Double calculateRent(Integer days);

    public abstract String getCategory();

    public Integer getCarId() {
        return carId;
    }

    public String getBrand() {
        return brand;
    }

    public String getModel() {
        return model;
    }

    public Double getPricePerDay() {
        return pricePerDay;
    }

    public void setPricePerDay(Double pricePerDay) {
        this.pricePerDay = pricePerDay;
    }

    public Boolean isAvailable() {
        return available;
    }

    public void setAvailable(Boolean available) {
        this.available = available;
    }

    public void displayDetails() {
        System.out.println(
                "ID: " + carId +
                        " | " + brand + " " + model +
                        " | Type: " + getCategory() +
                        " | Price: Rs." + pricePerDay + "/day" +
                        " | Status: " + (available ? "Available" : "Rented")
        );
    }
}
