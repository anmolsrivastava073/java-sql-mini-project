package com.carrental.model;

public class SUV extends Car {

    public SUV(int carId, String brand, String model, double pricePerDay) {
        super(carId, brand, model, pricePerDay);
    }

    @Override
    public Double calculateRent(Integer days) {
        // 10% premium rate for SUVs
        return getPricePerDay() * days * 1.10;
    }

    @Override
    public String getCategory() {
        return "SUV";
    }
}
