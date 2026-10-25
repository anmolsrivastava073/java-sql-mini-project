package com.carrental;

import com.carrental.model.*;

import java.io.File;
import java.sql.*;
import java.time.LocalDateTime;
import java.time.format.DateTimeFormatter;
import java.util.ArrayList;
import java.util.List;

// Handles SQLite database operations using standard JDBC
public class Database {

    private static final String DB_FILE = "carrental.db";
    private static final String URL = "jdbc:sqlite:" + DB_FILE;

    // Load SQLite JDBC driver
    static {
        try {
            Class.forName("org.sqlite.JDBC");
        } catch (ClassNotFoundException e) {
            System.err.println("SQLite driver not found: " + e.getMessage());
        }
    }

    public static Connection getConnection() throws SQLException {
        Connection conn = DriverManager.getConnection(URL);
        try (Statement stmt = conn.createStatement()) {
            stmt.execute("PRAGMA foreign_keys = ON;");
        }
        return conn;
    }

    // Initialize database tables on startup
    public static void init() {
        try (Connection conn = getConnection();
             Statement stmt = conn.createStatement()) {

            // 1. Cars table
            stmt.execute("""
                CREATE TABLE IF NOT EXISTS cars (
                    car_id INTEGER PRIMARY KEY,
                    brand TEXT NOT NULL,
                    model TEXT NOT NULL,
                    category TEXT NOT NULL CHECK(category IN ('Sedan', 'SUV', 'LuxuryCar')),
                    price_per_day REAL NOT NULL CHECK(price_per_day > 0),
                    available INTEGER NOT NULL DEFAULT 1 CHECK(available IN (0, 1))
                );
            """);

            // 2. Customers table
            stmt.execute("""
                CREATE TABLE IF NOT EXISTS customers (
                    customer_id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL,
                    phone TEXT NOT NULL,
                    driving_license TEXT NOT NULL UNIQUE
                );
            """);

            // 3. Rentals table with foreign keys
            stmt.execute("""
                CREATE TABLE IF NOT EXISTS rentals (
                    rental_id INTEGER PRIMARY KEY AUTOINCREMENT,
                    customer_id INTEGER NOT NULL,
                    car_id INTEGER NOT NULL,
                    days INTEGER NOT NULL CHECK(days > 0),
                    total_amount REAL NOT NULL CHECK(total_amount > 0),
                    active INTEGER NOT NULL DEFAULT 1 CHECK(active IN (0, 1)),
                    rental_date TEXT NOT NULL,
                    return_date TEXT,
                    FOREIGN KEY (customer_id) REFERENCES customers(customer_id),
                    FOREIGN KEY (car_id) REFERENCES cars(car_id)
                );
            """);

            // Seed sample data if cars table is empty
            try (ResultSet rs = stmt.executeQuery("SELECT COUNT(*) FROM cars;")) {
                if (rs.next() && rs.getInt(1) == 0) {
                    seedData(conn);
                }
            }

            System.out.println("SQLite Database connected: " + new File(DB_FILE).getName());
        } catch (SQLException e) {
            System.err.println("Database init error: " + e.getMessage());
        }
    }

    // Insert sample cars and customer
    private static void seedData(Connection conn) throws SQLException {
        String insertCar = "INSERT INTO cars (car_id, brand, model, category, price_per_day, available) VALUES (?, ?, ?, ?, ?, ?);";

        try (PreparedStatement ps = conn.prepareStatement(insertCar)) {
            Object[][] sampleCars = {
                {101, "Honda", "City", "Sedan", 1500.0, 1},
                {102, "Hyundai", "Verna", "Sedan", 1600.0, 1},
                {103, "Hyundai", "Creta", "SUV", 2000.0, 1},
                {104, "Toyota", "Fortuner", "SUV", 3500.0, 1},
                {105, "BMW", "3 Series", "LuxuryCar", 6000.0, 1}
            };

            for (Object[] c : sampleCars) {
                ps.setInt(1, (Integer) c[0]);
                ps.setString(2, (String) c[1]);
                ps.setString(3, (String) c[2]);
                ps.setString(4, (String) c[3]);
                ps.setDouble(5, (Double) c[4]);
                ps.setInt(6, (Integer) c[5]);
                ps.executeUpdate();
            }
        }

        // Add a sample customer
        try (PreparedStatement ps = conn.prepareStatement(
                "INSERT INTO customers (customer_id, name, phone, driving_license) VALUES (201, 'Rahul Sharma', '9876543210', 'DL-04-2022-1122');")) {
            ps.executeUpdate();
        }
    }

    // ------------------------------------------------------------------------
    // CAR OPERATIONS
    // ------------------------------------------------------------------------

    public static List<Car> getCars() {
        List<Car> list = new ArrayList<>();
        String sql = "SELECT * FROM cars ORDER BY car_id ASC;";
        try (Connection conn = getConnection();
             PreparedStatement ps = conn.prepareStatement(sql);
             ResultSet rs = ps.executeQuery()) {
            while (rs.next()) {
                list.add(mapCar(rs));
            }
        } catch (SQLException e) {
            System.err.println("Error fetching cars: " + e.getMessage());
        }
        return list;
    }

    public static List<Car> getAvailableCars() {
        List<Car> list = new ArrayList<>();
        String sql = "SELECT * FROM cars WHERE available = 1 ORDER BY car_id ASC;";
        try (Connection conn = getConnection();
             PreparedStatement ps = conn.prepareStatement(sql);
             ResultSet rs = ps.executeQuery()) {
            while (rs.next()) {
                list.add(mapCar(rs));
            }
        } catch (SQLException e) {
            System.err.println("Error fetching available cars: " + e.getMessage());
        }
        return list;
    }

    public static Car getCarById(int carId) throws CarRentalException {
        String sql = "SELECT * FROM cars WHERE car_id = ?;";
        try (Connection conn = getConnection();
             PreparedStatement ps = conn.prepareStatement(sql)) {
            ps.setInt(1, carId);
            try (ResultSet rs = ps.executeQuery()) {
                if (rs.next()) {
                    return mapCar(rs);
                }
            }
        } catch (SQLException e) {
            throw new CarRentalException("Database error: " + e.getMessage());
        }
        throw new CarRentalException("Car with ID #" + carId + " not found.");
    }

    public static void addCar(Car car) throws CarRentalException {
        String insertSql = "INSERT INTO cars (car_id, brand, model, category, price_per_day, available) VALUES (?, ?, ?, ?, ?, ?);";
        try (Connection conn = getConnection();
             PreparedStatement ps = conn.prepareStatement(insertSql)) {
            ps.setInt(1, car.getCarId());
            ps.setString(2, car.getBrand());
            ps.setString(3, car.getModel());
            ps.setString(4, car.getCategory());
            ps.setDouble(5, car.getPricePerDay());
            ps.setInt(6, car.isAvailable() ? 1 : 0);
            ps.executeUpdate();
        } catch (SQLException e) {
            throw new CarRentalException("Failed to add car: " + e.getMessage());
        }
    }

    // ------------------------------------------------------------------------
    // CUSTOMER OPERATIONS
    // ------------------------------------------------------------------------

    public static List<Customer> getCustomers() {
        List<Customer> list = new ArrayList<>();
        String sql = "SELECT * FROM customers ORDER BY customer_id ASC;";
        try (Connection conn = getConnection();
             PreparedStatement ps = conn.prepareStatement(sql);
             ResultSet rs = ps.executeQuery()) {
            while (rs.next()) {
                list.add(new Customer(
                    rs.getInt("customer_id"),
                    rs.getString("name"),
                    rs.getString("phone"),
                    rs.getString("driving_license")
                ));
            }
        } catch (SQLException e) {
            System.err.println("Error fetching customers: " + e.getMessage());
        }
        return list;
    }

    public static Customer getOrCreateCustomer(String name, String phone, String license) throws CarRentalException {
        String findSql = "SELECT * FROM customers WHERE LOWER(driving_license) = LOWER(?);";
        String insertSql = "INSERT INTO customers (name, phone, driving_license) VALUES (?, ?, ?);";

        try (Connection conn = getConnection()) {
            // Check if customer already exists
            try (PreparedStatement ps = conn.prepareStatement(findSql)) {
                ps.setString(1, license.trim());
                try (ResultSet rs = ps.executeQuery()) {
                    if (rs.next()) {
                        return new Customer(
                            rs.getInt("customer_id"),
                            rs.getString("name"),
                            rs.getString("phone"),
                            rs.getString("driving_license")
                        );
                    }
                }
            }

            // Otherwise insert new customer
            try (PreparedStatement ps = conn.prepareStatement(insertSql, Statement.RETURN_GENERATED_KEYS)) {
                ps.setString(1, name.trim());
                ps.setString(2, phone.trim());
                ps.setString(3, license.trim().toUpperCase());
                ps.executeUpdate();

                try (ResultSet keys = ps.getGeneratedKeys()) {
                    int newId = keys.next() ? keys.getInt(1) : 0;
                    return new Customer(newId, name.trim(), phone.trim(), license.trim().toUpperCase());
                }
            }
        } catch (SQLException e) {
            throw new CarRentalException("Database error saving customer: " + e.getMessage());
        }
    }

    // ------------------------------------------------------------------------
    // RENTAL OPERATIONS (Transactions)
    // ------------------------------------------------------------------------

    public static List<Rental> getRentals() {
        List<Rental> list = new ArrayList<>();
        String sql = """
            SELECT 
                r.rental_id, r.days, r.total_amount, r.active, r.rental_date, r.return_date,
                c.customer_id, c.name, c.phone, c.driving_license,
                cr.car_id, cr.brand, cr.model, cr.category, cr.price_per_day, cr.available
            FROM rentals r
            JOIN customers c ON r.customer_id = c.customer_id
            JOIN cars cr ON r.car_id = cr.car_id
            ORDER BY r.rental_id DESC;
        """;

        try (Connection conn = getConnection();
             PreparedStatement ps = conn.prepareStatement(sql);
             ResultSet rs = ps.executeQuery()) {
            while (rs.next()) {
                Customer customer = new Customer(
                    rs.getInt("customer_id"),
                    rs.getString("name"),
                    rs.getString("phone"),
                    rs.getString("driving_license")
                );

                Car car = mapCar(rs);
                int rentalId = rs.getInt("rental_id");
                int days = rs.getInt("days");
                boolean active = rs.getInt("active") == 1;

                Rental rental = new Rental(rentalId, customer, car, days);
                if (!active) {
                    rental.completeRental();
                }
                list.add(rental);
            }
        } catch (SQLException e) {
            System.err.println("Error fetching rentals: " + e.getMessage());
        }
        return list;
    }

    // Rent car: inserts rental and marks car unavailable inside a transaction
    public static synchronized Rental rentCar(int carId, String name, String phone, String license, int days) throws CarRentalException {
        if (days <= 0) {
            throw new CarRentalException("Rental duration must be at least 1 day.");
        }

        Car car = getCarById(carId);
        if (!car.isAvailable()) {
            throw new CarRentalException("Car " + car.getBrand() + " " + car.getModel() + " is already rented.");
        }

        Customer customer = getOrCreateCustomer(name, phone, license);

        // Polymorphic rent calculation executes inside Rental constructor
        Rental rental = new Rental(0, customer, car, days);

        String insertRentalSql = """
            INSERT INTO rentals (customer_id, car_id, days, total_amount, active, rental_date)
            VALUES (?, ?, ?, ?, 1, ?);
        """;
        String updateCarSql = "UPDATE cars SET available = 0 WHERE car_id = ?;";

        try (Connection conn = getConnection()) {
            conn.setAutoCommit(false); // Start transaction
            try {
                int generatedRentalId;
                try (PreparedStatement ps = conn.prepareStatement(insertRentalSql, Statement.RETURN_GENERATED_KEYS)) {
                    ps.setInt(1, customer.getCustomerId());
                    ps.setInt(2, car.getCarId());
                    ps.setInt(3, days);
                    ps.setDouble(4, rental.getTotalAmount());
                    ps.setString(5, rental.getRentalDate());
                    ps.executeUpdate();

                    try (ResultSet keys = ps.getGeneratedKeys()) {
                        generatedRentalId = keys.next() ? keys.getInt(1) : 1000;
                    }
                }

                // Update car status to unavailable (0)
                try (PreparedStatement ps = conn.prepareStatement(updateCarSql)) {
                    ps.setInt(1, carId);
                    ps.executeUpdate();
                }

                conn.commit(); // Commit transaction
                car.setAvailable(false);
                return new Rental(generatedRentalId, customer, car, days);
            } catch (SQLException e) {
                conn.rollback();
                throw new CarRentalException("Rental transaction failed: " + e.getMessage());
            }
        } catch (SQLException e) {
            throw new CarRentalException("Database connection error: " + e.getMessage());
        }
    }

    // Return car: marks rental completed and sets car available again
    public static synchronized Rental returnCar(int rentalId) throws CarRentalException {
        String findRentalSql = """
            SELECT r.*, c.name, c.phone, c.driving_license
            FROM rentals r
            JOIN customers c ON r.customer_id = c.customer_id
            WHERE r.rental_id = ?;
        """;

        String updateRentalSql = "UPDATE rentals SET active = 0, return_date = ? WHERE rental_id = ?;";
        String updateCarSql = "UPDATE cars SET available = 1 WHERE car_id = ?;";

        try (Connection conn = getConnection()) {
            int carId;
            int days;
            Customer customer;
            Car car;

            try (PreparedStatement ps = conn.prepareStatement(findRentalSql)) {
                ps.setInt(1, rentalId);
                try (ResultSet rs = ps.executeQuery()) {
                    if (!rs.next()) {
                        throw new CarRentalException("Rental record #" + rentalId + " not found.");
                    }
                    if (rs.getInt("active") == 0) {
                        throw new CarRentalException("Rental #" + rentalId + " is already completed.");
                    }
                    carId = rs.getInt("car_id");
                    days = rs.getInt("days");
                    customer = new Customer(rs.getInt("customer_id"), rs.getString("name"), rs.getString("phone"), rs.getString("driving_license"));
                    car = getCarById(carId);
                }
            }

            conn.setAutoCommit(false); // Start transaction
            try {
                String returnDate = LocalDateTime.now().format(DateTimeFormatter.ofPattern("yyyy-MM-dd HH:mm"));

                try (PreparedStatement ps = conn.prepareStatement(updateRentalSql)) {
                    ps.setString(1, returnDate);
                    ps.setInt(2, rentalId);
                    ps.executeUpdate();
                }

                try (PreparedStatement ps = conn.prepareStatement(updateCarSql)) {
                    ps.setInt(1, carId);
                    ps.executeUpdate();
                }

                conn.commit(); // Commit transaction
                car.setAvailable(true);
                Rental completed = new Rental(rentalId, customer, car, days);
                completed.completeRental();
                return completed;
            } catch (SQLException e) {
                conn.rollback();
                throw new CarRentalException("Return transaction failed: " + e.getMessage());
            }
        } catch (SQLException e) {
            throw new CarRentalException("Database error: " + e.getMessage());
        }
    }

    // ------------------------------------------------------------------------
    // CONSOLE SQL QUERY RUNNER (To demonstrate SQL directly during Viva)
    // ------------------------------------------------------------------------

    public static void runConsoleQuery(String sql) {
        if (sql == null || sql.trim().isEmpty()) {
            System.out.println("Query cannot be empty.");
            return;
        }

        try (Connection conn = getConnection();
             Statement stmt = conn.createStatement()) {

            String trimmed = sql.trim();
            boolean isSelect = trimmed.regionMatches(true, 0, "SELECT", 0, 6)
                    || trimmed.regionMatches(true, 0, "PRAGMA", 0, 6);

            if (isSelect) {
                try (ResultSet rs = stmt.executeQuery(trimmed)) {
                    ResultSetMetaData md = rs.getMetaData();
                    int count = md.getColumnCount();

                    // Print header
                    System.out.println("\n-------------------------------------------------------------");
                    for (int i = 1; i <= count; i++) {
                        System.out.printf("%-18s", md.getColumnLabel(i));
                    }
                    System.out.println("\n-------------------------------------------------------------");

                    int rows = 0;
                    while (rs.next()) {
                        rows++;
                        for (int i = 1; i <= count; i++) {
                            Object val = rs.getObject(i);
                            System.out.printf("%-18s", val != null ? val.toString() : "NULL");
                        }
                        System.out.println();
                    }
                    System.out.println("-------------------------------------------------------------");
                    System.out.println("Rows returned: " + rows);
                }
            } else {
                int affected = stmt.executeUpdate(trimmed);
                System.out.println("Query executed successfully. Rows affected: " + affected);
            }
        } catch (SQLException e) {
            System.out.println("SQL Error: " + e.getMessage());
        }
    }

    // Maps database row to Sedan, SUV, or LuxuryCar based on category column
    private static Car mapCar(ResultSet rs) throws SQLException {
        int id = rs.getInt("car_id");
        String brand = rs.getString("brand");
        String model = rs.getString("model");
        String category = rs.getString("category");
        double price = rs.getDouble("price_per_day");
        boolean available = rs.getInt("available") == 1;

        Car car;
        if ("SUV".equalsIgnoreCase(category)) {
            car = new SUV(id, brand, model, price);
        } else if ("LuxuryCar".equalsIgnoreCase(category)) {
            car = new LuxuryCar(id, brand, model, price);
        } else {
            car = new Sedan(id, brand, model, price);
        }
        car.setAvailable(available);
        return car;
    }
}
