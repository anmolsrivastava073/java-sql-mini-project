package com.carrental.model;

public class LuxuryCar extends Car {

    public LuxuryCar(int carId, String brand, String model, double pricePerDay) {
        super(carId, brand, model, pricePerDay);
    }

    @Override
    public Double calculateRent(Integer days) {
        // 20% premium rate for Luxury Cars
        return getPricePerDay() * days * 1.20;
    }

    @Override
    public String getCategory() {
        return "LuxuryCar";
    }
}
