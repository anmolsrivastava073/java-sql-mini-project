package com.carrental.model;

public class Sedan extends Car {

    public Sedan(int carId, String brand, String model, double pricePerDay) {
        super(carId, brand, model, pricePerDay);
    }

    @Override
    public Double calculateRent(Integer days) {
        // Base rate for Sedans
        return getPricePerDay() * days;
    }

    @Override
    public String getCategory() {
        return "Sedan";
    }
}
