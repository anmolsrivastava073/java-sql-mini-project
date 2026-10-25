# Car Rental Management System (Java OOP & SQLite)

A clean, easy-to-explain Car Rental application built with **Core Java** and a persistent **SQLite Database** using standard **JDBC**.

---

## Features

- **Fleet Inventory:** View available cars or inspect the full fleet from the database.
- **Rental Booking:** Select a car, input customer credentials, choose duration, and compute total rent using category-based polymorphism.
- **Return Processing:** Check in rented cars; updates the rental record and resets vehicle availability to active in SQLite.
- **Admin Panel:** Add new cars and view registered customers and past leases.
- **SQL Console (Viva Tool):** Type and run raw SQL queries directly from the terminal menu (`SELECT * FROM cars;`, `JOIN` queries, etc.) to showcase database skills.
- **ACID Transactions:** Uses `setAutoCommit(false)`, `commit()`, and `rollback()` during car rental and return operations.

---

## OOP Concepts

1. **Abstraction:** `abstract class Car` defines the contract `abstract Double calculateRent(Integer days);`. Child classes supply the implementation.
2. **Encapsulation:** All model fields (`Car`, `Customer`, `Rental`) are `private` with public getter and setter methods.
3. **Inheritance:** `Sedan`, `SUV`, and `LuxuryCar` extend `Car` using `super(...)` to inherit shared vehicle attributes.
4. **Polymorphism (Dynamic Binding):** In `Rental.java`, `this.totalAmount = car.calculateRent(days);` dynamically invokes the overridden method:
   - **Sedan:** `basePrice * days` (1.0x)
   - **SUV:** `basePrice * days * 1.10` (1.10x)
   - **LuxuryCar:** `basePrice * days * 1.20` (1.20x)
5. **Custom Exception Handling:** `CarRentalException extends Exception` validates input parameters (days $\ge 1$, vehicle availability, valid IDs).

---

## Database Schema (SQLite: `carrental.db`)

```sql
-- Cars Table
CREATE TABLE cars (
    car_id INTEGER PRIMARY KEY,
    brand TEXT NOT NULL,
    model TEXT NOT NULL,
    category TEXT NOT NULL CHECK(category IN ('Sedan', 'SUV', 'LuxuryCar')),
    price_per_day REAL NOT NULL CHECK(price_per_day > 0),
    available INTEGER NOT NULL DEFAULT 1 CHECK(available IN (0, 1))
);

-- Customers Table
CREATE TABLE customers (
    customer_id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    phone TEXT NOT NULL,
    driving_license TEXT NOT NULL UNIQUE
);

-- Rentals Table with Foreign Keys
CREATE TABLE rentals (
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
```

---

## Project Structure

```text
├── src/main/java/com/carrental/
│   ├── CarRentalSystem.java        # Main interactive console CLI
│   ├── Database.java               # SQLite JDBC operations, transactions, and SQL runner
│   └── model/
│       ├── Car.java                # Abstract parent class
│       ├── Sedan.java              # Concrete subclass (1.0x rate)
│       ├── SUV.java                # Concrete subclass (1.1x rate)
│       ├── LuxuryCar.java          # Concrete subclass (1.2x rate)
│       ├── Customer.java           # Customer model
│       ├── Rental.java             # Rental model with dynamic polymorphism
│       └── CarRentalException.java # Custom checked exception
├── lib/
│   └── sqlite-jdbc-3.48.0.0.jar    # SQLite JDBC driver
├── carrental.db                    # Relational database file
├── run.sh                          # Compilation and launch script
└── Car_Rental_System_Presentation.pptx # 12-slide presentation for viva
```

---

## How to Run

```bash
cd "/Users/anmolsrivastava073/OOPS Project"

# Compile and run the console application
./run.sh
```
