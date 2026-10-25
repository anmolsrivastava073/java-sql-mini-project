package com.carrental;

import com.carrental.model.*;

import java.util.List;
import java.util.Scanner;

// Main interactive console application demonstrating Java OOP and SQLite database management
public class CarRentalSystem {

    private static final Scanner sc = new Scanner(System.in);

    private static Integer getIntInput(String prompt) {
        while (true) {
            try {
                System.out.print(prompt);
                String line = sc.nextLine().trim();
                return Integer.valueOf(line);
            } catch (NumberFormatException e) {
                System.out.println("Invalid input. Please enter a valid number.");
            }
        }
    }

    private static void displayAvailableCars() {
        System.out.println("\n--- Available Cars ---");
        List<Car> available = Database.getAvailableCars();
        if (available.isEmpty()) {
            System.out.println("No cars currently available for rent.");
        } else {
            for (Car car : available) {
                car.displayDetails();
            }
        }
    }

    private static Customer registerCustomer() {
        System.out.println("\n--- Customer Details ---");
        System.out.print("Enter Customer Name: ");
        String name = sc.nextLine().trim();

        System.out.print("Enter Phone: ");
        String phone = sc.nextLine().trim();

        System.out.print("Enter Driving License: ");
        String license = sc.nextLine().trim();

        try {
            Customer customer = Database.getOrCreateCustomer(name, phone, license);
            System.out.println("Customer record verified (ID #" + customer.getCustomerId() + ").");
            return customer;
        } catch (CarRentalException e) {
            System.out.println("Error saving customer: " + e.getMessage());
            return null;
        }
    }

    private static void rentCar() {
        displayAvailableCars();
        try {
            Integer carId = getIntInput("\nEnter Car ID to Rent: ");
            Car selectedCar = Database.getCarById(carId);

            if (!selectedCar.isAvailable()) {
                throw new CarRentalException("Selected car is unavailable.");
            }

            Customer customer = registerCustomer();
            if (customer == null) return;

            Integer days = getIntInput("Enter number of rental days: ");
            if (days <= 0) {
                throw new CarRentalException("Rental duration must be at least 1 day.");
            }

            // Polymorphic rent calculation based on vehicle subclass
            Double amount = selectedCar.calculateRent(days);

            System.out.println("\n--- Rental Summary ---");
            System.out.println("Car: " + selectedCar.getBrand() + " " + selectedCar.getModel() + " (" + selectedCar.getCategory() + ")");
            System.out.println("Duration: " + days + " days");
            System.out.println("Total Amount: Rs. " + amount);
            System.out.print("Confirm rental? (Y/N): ");

            String confirm = sc.nextLine().trim();
            if (confirm.equalsIgnoreCase("Y")) {
                Rental rental = Database.rentCar(carId, customer.getName(), customer.getPhone(), customer.getDrivingLicense(), days);
                System.out.println("\nCar rented successfully!");
                rental.displayRental();
            } else {
                System.out.println("Rental cancelled.");
            }

        } catch (CarRentalException e) {
            System.out.println("Error: " + e.getMessage());
        }
    }

    private static void returnCar() {
        try {
            Integer rentalId = getIntInput("\nEnter Rental ID to Return: ");
            Rental returned = Database.returnCar(rentalId);
            System.out.println("\nCar returned successfully!");
            returned.displayRental();
        } catch (CarRentalException e) {
            System.out.println("Error: " + e.getMessage());
        }
    }

    private static void viewRentals() {
        System.out.println("\n--- Rental History ---");
        List<Rental> rentals = Database.getRentals();
        if (rentals.isEmpty()) {
            System.out.println("No rental records found.");
            return;
        }
        for (Rental r : rentals) {
            r.displayRental();
            System.out.println("----------------------------------------");
        }
    }

    private static void addNewCarPrompt() {
        try {
            System.out.println("\n--- Add New Vehicle to Database ---");
            System.out.print("Car Type (Sedan / SUV / LuxuryCar): ");
            String type = sc.nextLine().trim();

            Integer id = getIntInput("Enter Car ID: ");
            System.out.print("Brand: ");
            String brand = sc.nextLine().trim();
            System.out.print("Model: ");
            String model = sc.nextLine().trim();
            System.out.print("Price Per Day: ");
            double price = Double.parseDouble(sc.nextLine().trim());

            Car car;
            if ("SUV".equalsIgnoreCase(type)) {
                car = new SUV(id, brand, model, price);
            } else if ("LuxuryCar".equalsIgnoreCase(type)) {
                car = new LuxuryCar(id, brand, model, price);
            } else {
                car = new Sedan(id, brand, model, price);
            }

            Database.addCar(car);
            System.out.println("Car #" + id + " (" + brand + " " + model + ") saved to SQLite database successfully.");
        } catch (Exception e) {
            System.out.println("Error adding car: " + e.getMessage());
        }
    }

    private static void adminMenu() {
        while (true) {
            System.out.println("\n--- Admin Menu ---");
            System.out.println("1. View All Fleet Cars");
            System.out.println("2. View Registered Customers");
            System.out.println("3. View All Rentals");
            System.out.println("4. Add New Car");
            System.out.println("5. Back to Main Menu");

            Integer choice = getIntInput("Enter choice (1-5): ");
            switch (choice) {
                case 1:
                    System.out.println("\n--- All Fleet Vehicles ---");
                    for (Car c : Database.getCars()) {
                        c.displayDetails();
                    }
                    break;
                case 2:
                    System.out.println("\n--- Registered Customers ---");
                    var customers = Database.getCustomers();
                    if (customers.isEmpty()) {
                        System.out.println("No customers registered yet.");
                    } else {
                        for (Customer c : customers) {
                            c.displayCustomer();
                        }
                    }
                    break;
                case 3:
                    viewRentals();
                    break;
                case 4:
                    addNewCarPrompt();
                    break;
                case 5:
                    return;
                default:
                    System.out.println("Invalid option. Please enter 1 to 5.");
            }
        }
    }

    private static void sqlQueryConsole() {
        System.out.println("\n--- SQL Query Console (Direct SQLite JDBC) ---");
        System.out.println("Examples:");
        System.out.println("  SELECT * FROM cars;");
        System.out.println("  SELECT * FROM customers;");
        System.out.println("  SELECT r.rental_id, c.name, cr.model, r.days, r.total_amount FROM rentals r JOIN customers c ON r.customer_id=c.customer_id JOIN cars cr ON r.car_id=cr.car_id;");
        System.out.print("\nEnter SQL query (or type 'back' to return): ");

        String query = sc.nextLine().trim();
        if (query.equalsIgnoreCase("back") || query.isEmpty()) {
            return;
        }

        Database.runConsoleQuery(query);
    }

    public static void main(String[] args) {
        // Initialize SQLite database schema and sample records
        Database.init();

        while (true) {
            System.out.println("\n=================================");
            System.out.println("  CAR RENTAL MANAGEMENT SYSTEM   ");
            System.out.println("  (Java OOP & SQLite Database)   ");
            System.out.println("=================================");
            System.out.println("1. View Available Cars");
            System.out.println("2. Rent a Car");
            System.out.println("3. Return a Car");
            System.out.println("4. View Rental History");
            System.out.println("5. Admin Menu");
            System.out.println("6. Run SQL Query Directly (Viva Demo)");
            System.out.println("7. Exit");

            Integer choice = getIntInput("\nEnter your choice (1-7): ");

            switch (choice) {
                case 1:
                    displayAvailableCars();
                    break;
                case 2:
                    rentCar();
                    break;
                case 3:
                    returnCar();
                    break;
                case 4:
                    viewRentals();
                    break;
                case 5:
                    adminMenu();
                    break;
                case 6:
                    sqlQueryConsole();
                    break;
                case 7:
                    System.out.println("\nThank you for using Car Rental Management System. Goodbye!");
                    sc.close();
                    return;
                default:
                    System.out.println("Invalid choice. Please select between 1 and 7.");
            }
        }
    }
}
