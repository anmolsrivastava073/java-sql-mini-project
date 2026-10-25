package com.carrental.model;

// Custom exception for car rental validation errors
public class CarRentalException extends Exception {
    public CarRentalException(String message) {
        super(message);
    }
}
