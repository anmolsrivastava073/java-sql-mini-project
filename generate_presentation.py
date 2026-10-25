import sys
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.enum.shapes import MSO_SHAPE

def create_presentation(output_path):
    prs = Presentation()
    # 16:9 widescreen
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)

    blank_layout = prs.slide_layouts[6]

    # Colors
    BG_DARK = RGBColor(15, 23, 42)      # Slate 900
    CARD_BG = RGBColor(30, 41, 59)      # Slate 800
    CARD_BORDER = RGBColor(51, 65, 85)  # Slate 700
    GOLD = RGBColor(245, 158, 11)       # Amber 500
    CYAN = RGBColor(56, 189, 248)       # Sky 400
    WHITE = RGBColor(248, 250, 252)     # Slate 50
    GRAY = RGBColor(148, 163, 184)      # Slate 400
    EMERALD = RGBColor(52, 211, 153)    # Emerald 400

    def add_background(slide):
        bg = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0), Inches(0), prs.slide_width, prs.slide_height)
        bg.fill.solid()
        bg.fill.fore_color.rgb = BG_DARK
        bg.line.fill.background()
        return bg

    def add_header(slide, title_text, category_text="JAVA OOP & SQL DATABASE PROJECT"):
        tb = slide.shapes.add_textbox(Inches(0.8), Inches(0.5), Inches(11.7), Inches(1.1))
        tf = tb.text_frame
        tf.word_wrap = True
        tf.margin_left = tf.margin_top = tf.margin_right = tf.margin_bottom = 0

        p0 = tf.paragraphs[0]
        p0.text = category_text.upper()
        p0.font.size = Pt(11)
        p0.font.bold = True
        p0.font.color.rgb = GOLD
        p0.font.name = "Calibri"

        p1 = tf.add_paragraph()
        p1.text = title_text
        p1.font.size = Pt(24)
        p1.font.bold = True
        p1.font.color.rgb = WHITE
        p1.font.name = "Arial"
        p1.space_before = Pt(4)

    # =========================================================================
    # SLIDE 1: Title Slide
    # =========================================================================
    s1 = prs.slides.add_slide(blank_layout)
    add_background(s1)

    card = s1.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(1.2), Inches(1.2), Inches(10.9), Inches(5.1))
    card.fill.solid()
    card.fill.fore_color.rgb = CARD_BG
    card.line.color.rgb = CARD_BORDER

    tb1 = s1.shapes.add_textbox(Inches(1.8), Inches(1.8), Inches(9.7), Inches(3.9))
    tf1 = tb1.text_frame
    tf1.word_wrap = True

    p = tf1.paragraphs[0]
    p.text = "CAR RENTAL MANAGEMENT SYSTEM"
    p.font.size = Pt(32)
    p.font.bold = True
    p.font.color.rgb = GOLD
    p.font.name = "Arial"

    p = tf1.add_paragraph()
    p.text = "Core Java Object-Oriented Programming & Relational SQLite Database"
    p.font.size = Pt(18)
    p.font.color.rgb = WHITE
    p.font.name = "Calibri"
    p.space_before = Pt(10)

    p = tf1.add_paragraph()
    p.text = "\nKey Focus Areas: Abstraction | Encapsulation | Inheritance | Polymorphism | JDBC & SQLite\nTechnology Stack: Java 21+ • SQLite 3 JDBC • Transaction Safety • CLI Console"
    p.font.size = Pt(13)
    p.font.color.rgb = GRAY
    p.font.name = "Calibri"

    # =========================================================================
    # SLIDE 2: Project Overview & Motivation
    # =========================================================================
    s2 = prs.slides.add_slide(blank_layout)
    add_background(s2)
    add_header(s2, "Project Overview & Problem Statement")

    cards_data = [
        ("The Problem Statement", 
         "• In-memory programs lose all data when the application terminates.\n• Manual record keeping leads to calculation mistakes and double-booking.\n• Hardcoded pricing lacks flexibility across vehicle categories.\n• Need for persistent, relational data management in Java.",
         GOLD),
        ("Our Solution", 
         "• Strict Object-Oriented design with robust domain modeling.\n• Dynamic polymorphic rent calculation (Sedan, SUV, LuxuryCar).\n• Persistent SQLite database storing cars, customers, and active leases.\n• Direct SQL Console for live evaluation and verification.",
         CYAN),
        ("Core Functionalities", 
         "• Fleet Inventory: Inspect and dynamically add vehicles.\n• Rental Desk: Register customers and calculate rental rates.\n• Vehicle Return: Process check-ins with automatic availability updates.\n• SQL Query Runner: Execute queries directly via JDBC in the terminal.",
         EMERALD)
    ]

    for i, (ctitle, cdesc, ccolor) in enumerate(cards_data):
        c = s2.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8 + i * 4.0), Inches(2.0), Inches(3.7), Inches(4.7))
        c.fill.solid()
        c.fill.fore_color.rgb = CARD_BG
        c.line.color.rgb = CARD_BORDER

        tb = s2.shapes.add_textbox(Inches(1.0 + i * 4.0), Inches(2.2), Inches(3.3), Inches(4.3))
        tf = tb.text_frame
        tf.word_wrap = True

        p = tf.paragraphs[0]
        p.text = ctitle
        p.font.size = Pt(16)
        p.font.bold = True
        p.font.color.rgb = ccolor

        p = tf.add_paragraph()
        p.text = cdesc
        p.font.size = Pt(13)
        p.font.color.rgb = WHITE
        p.space_before = Pt(14)

    # =========================================================================
    # SLIDE 3: System Architecture
    # =========================================================================
    s3 = prs.slides.add_slide(blank_layout)
    add_background(s3)
    add_header(s3, "System Architecture: 3-Tier Layered Design")

    layers = [
        ("1. Presentation Layer (Interactive Terminal Interface)", 
         "Provides a clean, intuitive text console interface:\n• Interactive menu for renting, returning, adding cars, and viewing history.\n• Live SQL query console enabling the evaluator to test raw queries on SQLite.",
         CYAN),
        ("2. Business Logic Layer (Java OOP Domain Models)", 
         "Enforces core domain rules, pricing calculations, and constraints:\n• Domain Models: Car (abstract), Sedan, SUV, LuxuryCar, Customer, Rental.\n• Custom Exception: CarRentalException thrown on business rule violations.",
         GOLD),
        ("3. Persistence Layer (SQLite Database via JDBC)", 
         "Ensures ACID relational persistence across application restarts:\n• Database.java: Centralized JDBC connection with Foreign Keys enforced.\n• Transaction Safety: Commit/Rollback protection for rental and return operations.",
         EMERALD)
    ]

    for i, (ltitle, ldesc, lcolor) in enumerate(layers):
        c = s3.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(2.0 + i * 1.6), Inches(11.7), Inches(1.35))
        c.fill.solid()
        c.fill.fore_color.rgb = CARD_BG
        c.line.color.rgb = CARD_BORDER

        tb = s3.shapes.add_textbox(Inches(1.1), Inches(2.1 + i * 1.6), Inches(11.1), Inches(1.15))
        tf = tb.text_frame
        tf.word_wrap = True

        p = tf.paragraphs[0]
        p.text = ltitle
        p.font.size = Pt(15)
        p.font.bold = True
        p.font.color.rgb = lcolor

        p = tf.add_paragraph()
        p.text = ldesc
        p.font.size = Pt(12)
        p.font.color.rgb = WHITE
        p.space_before = Pt(4)

    # =========================================================================
    # SLIDE 4: OOP Pillar 1 - Abstraction
    # =========================================================================
    s4 = prs.slides.add_slide(blank_layout)
    add_background(s4)
    add_header(s4, "OOP Pillar 1: Abstraction", "CORE OOP CONCEPTS")

    c_left = s4.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(2.0), Inches(5.7), Inches(4.7))
    c_left.fill.solid()
    c_left.fill.fore_color.rgb = CARD_BG
    c_left.line.color.rgb = CARD_BORDER

    tb_l = s4.shapes.add_textbox(Inches(1.1), Inches(2.2), Inches(5.1), Inches(4.3))
    tf_l = tb_l.text_frame
    tf_l.word_wrap = True
    p = tf_l.paragraphs[0]
    p.text = "Concept & Practical Purpose"
    p.font.size = Pt(16)
    p.font.bold = True
    p.font.color.rgb = GOLD

    p = tf_l.add_paragraph()
    p.text = "• Definition: Hiding complex internal calculations while presenting only essential features to the outside world.\n\n• Abstract Class: 'public abstract class Car' acts as a base blueprint. A Car cannot be instantiated on its own because rental calculation depends on the car's specific category.\n\n• Abstract Method:\n'public abstract Double calculateRent(Integer days);'\nForces every concrete subclass (Sedan, SUV, LuxuryCar) to supply its own rental calculation logic."
    p.font.size = Pt(13)
    p.font.color.rgb = WHITE
    p.space_before = Pt(10)

    c_right = s4.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(6.8), Inches(2.0), Inches(5.7), Inches(4.7))
    c_right.fill.solid()
    c_right.fill.fore_color.rgb = RGBColor(10, 15, 29)
    c_right.line.color.rgb = CARD_BORDER

    tb_r = s4.shapes.add_textbox(Inches(7.1), Inches(2.2), Inches(5.1), Inches(4.3))
    tf_r = tb_r.text_frame
    tf_r.word_wrap = True
    p = tf_r.paragraphs[0]
    p.text = "Code Evidence: Car.java"
    p.font.size = Pt(14)
    p.font.bold = True
    p.font.color.rgb = CYAN

    p = tf_r.add_paragraph()
    p.text = "public abstract class Car {\n    private Integer carId;\n    private String brand;\n    private String model;\n    private Double pricePerDay;\n    private Boolean available;\n\n    // Abstract method defining the contract\n    public abstract Double calculateRent(Integer days);\n\n    public abstract String getCategory();\n}"
    p.font.size = Pt(12)
    p.font.name = "Courier New"
    p.font.color.rgb = WHITE
    p.space_before = Pt(10)

    # =========================================================================
    # SLIDE 5: OOP Pillar 2 - Encapsulation
    # =========================================================================
    s5 = prs.slides.add_slide(blank_layout)
    add_background(s5)
    add_header(s5, "OOP Pillar 2: Encapsulation & Data Hiding", "CORE OOP CONCEPTS")

    c_left = s5.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(2.0), Inches(5.7), Inches(4.7))
    c_left.fill.solid()
    c_left.fill.fore_color.rgb = CARD_BG
    c_left.line.color.rgb = CARD_BORDER

    tb_l = s5.shapes.add_textbox(Inches(1.1), Inches(2.2), Inches(5.1), Inches(4.3))
    tf_l = tb_l.text_frame
    tf_l.word_wrap = True
    p = tf_l.paragraphs[0]
    p.text = "Concept & Practical Purpose"
    p.font.size = Pt(16)
    p.font.bold = True
    p.font.color.rgb = GOLD

    p = tf_l.add_paragraph()
    p.text = "• Definition: Bundling data and methods into a single unit while restricting direct access to object attributes.\n\n• Private Fields: All fields in Car, Customer, and Rental are declared 'private'.\n\n• Controlled Access: Access is mediated through public getter and setter methods.\n\n• Integrity Protection: Direct tampering with critical values (e.g. price, totalAmount, availability) is prohibited, maintaining valid business state."
    p.font.size = Pt(13)
    p.font.color.rgb = WHITE
    p.space_before = Pt(10)

    c_right = s5.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(6.8), Inches(2.0), Inches(5.7), Inches(4.7))
    c_right.fill.solid()
    c_right.fill.fore_color.rgb = RGBColor(10, 15, 29)
    c_right.line.color.rgb = CARD_BORDER

    tb_r = s5.shapes.add_textbox(Inches(7.1), Inches(2.2), Inches(5.1), Inches(4.3))
    tf_r = tb_r.text_frame
    tf_r.word_wrap = True
    p = tf_r.paragraphs[0]
    p.text = "Code Evidence: Customer.java & Car.java"
    p.font.size = Pt(14)
    p.font.bold = True
    p.font.color.rgb = CYAN

    p = tf_r.add_paragraph()
    p.text = "public class Customer {\n    // Private fields: protected against direct access\n    private Integer customerId;\n    private String name;\n    private String phone;\n    private String drivingLicense;\n\n    // Controlled read access\n    public Integer getCustomerId() { return customerId; }\n    public String getName() { return name; }\n    public String getDrivingLicense() { return drivingLicense; }\n}"
    p.font.size = Pt(11)
    p.font.name = "Courier New"
    p.font.color.rgb = WHITE
    p.space_before = Pt(10)

    # =========================================================================
    # SLIDE 6: OOP Pillar 3 - Inheritance
    # =========================================================================
    s6 = prs.slides.add_slide(blank_layout)
    add_background(s6)
    add_header(s6, "OOP Pillar 3: Inheritance & Code Reusability", "CORE OOP CONCEPTS")

    c_left = s6.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(2.0), Inches(5.7), Inches(4.7))
    c_left.fill.solid()
    c_left.fill.fore_color.rgb = CARD_BG
    c_left.line.color.rgb = CARD_BORDER

    tb_l = s6.shapes.add_textbox(Inches(1.1), Inches(2.2), Inches(5.1), Inches(4.3))
    tf_l = tb_l.text_frame
    tf_l.word_wrap = True
    p = tf_l.paragraphs[0]
    p.text = "Concept & Practical Purpose"
    p.font.size = Pt(16)
    p.font.bold = True
    p.font.color.rgb = GOLD

    p = tf_l.add_paragraph()
    p.text = "• Definition: Mechanism where a child class acquires all properties and behaviors of a parent class.\n\n• Code Reusability: Sedan, SUV, and LuxuryCar extend Car, inheriting brand, model, pricePerDay, and availability.\n\n• 'super' Keyword: Child constructors invoke the parent constructor via 'super(carId, brand, model, pricePerDay)' to reuse initialization logic without duplicating code.\n\n• Extensibility: Adding a new vehicle class (e.g., ElectricCar) requires zero modifications to existing classes."
    p.font.size = Pt(13)
    p.font.color.rgb = WHITE
    p.space_before = Pt(10)

    c_right = s6.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(6.8), Inches(2.0), Inches(5.7), Inches(4.7))
    c_right.fill.solid()
    c_right.fill.fore_color.rgb = RGBColor(10, 15, 29)
    c_right.line.color.rgb = CARD_BORDER

    tb_r = s6.shapes.add_textbox(Inches(7.1), Inches(2.2), Inches(5.1), Inches(4.3))
    tf_r = tb_r.text_frame
    tf_r.word_wrap = True
    p = tf_r.paragraphs[0]
    p.text = "Code Evidence: Sedan.java & SUV.java"
    p.font.size = Pt(14)
    p.font.bold = True
    p.font.color.rgb = CYAN

    p = tf_r.add_paragraph()
    p.text = "public class SUV extends Car {\n    public SUV(int carId, String brand, String model, double price) {\n        // Reusing parent constructor\n        super(carId, brand, model, price);\n    }\n\n    @Override\n    public Double calculateRent(Integer days) {\n        return getPricePerDay() * days * 1.10;\n    }\n}"
    p.font.size = Pt(11)
    p.font.name = "Courier New"
    p.font.color.rgb = WHITE
    p.space_before = Pt(10)

    # =========================================================================
    # SLIDE 7: OOP Pillar 4 - Polymorphism
    # =========================================================================
    s7 = prs.slides.add_slide(blank_layout)
    add_background(s7)
    add_header(s7, "OOP Pillar 4: Polymorphism & Dynamic Method Dispatch", "CORE OOP CONCEPTS")

    c_left = s7.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(2.0), Inches(5.7), Inches(4.7))
    c_left.fill.solid()
    c_left.fill.fore_color.rgb = CARD_BG
    c_left.line.color.rgb = CARD_BORDER

    tb_l = s7.shapes.add_textbox(Inches(1.1), Inches(2.2), Inches(5.1), Inches(4.3))
    tf_l = tb_l.text_frame
    tf_l.word_wrap = True
    p = tf_l.paragraphs[0]
    p.text = "Runtime Dynamic Binding"
    p.font.size = Pt(16)
    p.font.bold = True
    p.font.color.rgb = GOLD

    p = tf_l.add_paragraph()
    p.text = "• Definition: The ability of a message or method call to be processed in more than one form at runtime.\n\n• Overridden Method: Subclasses override calculateRent(days):\n  - Sedan: base rate (1.0x)\n  - SUV: 10% premium (1.10x)\n  - LuxuryCar: 20% premium (1.20x)\n\n• Dynamic Binding: In Rental.java constructor, 'this.totalAmount = car.calculateRent(days)' is called on a reference of type Car. The JVM determines at runtime which subclass method to execute based on the concrete object."
    p.font.size = Pt(13)
    p.font.color.rgb = WHITE
    p.space_before = Pt(10)

    c_right = s7.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(6.8), Inches(2.0), Inches(5.7), Inches(4.7))
    c_right.fill.solid()
    c_right.fill.fore_color.rgb = RGBColor(10, 15, 29)
    c_right.line.color.rgb = CARD_BORDER

    tb_r = s7.shapes.add_textbox(Inches(7.1), Inches(2.2), Inches(5.1), Inches(4.3))
    tf_r = tb_r.text_frame
    tf_r.word_wrap = True
    p = tf_r.paragraphs[0]
    p.text = "Code Evidence: Rental.java"
    p.font.size = Pt(14)
    p.font.bold = True
    p.font.color.rgb = CYAN

    p = tf_r.add_paragraph()
    p.text = "public class Rental {\n    private Car car; // Superclass reference\n    private Double totalAmount;\n\n    public Rental(int id, Customer cust, Car car, int days) {\n        this.car = car;\n        // Polymorphic invocation at runtime\n        this.totalAmount = car.calculateRent(days);\n    }\n}"
    p.font.size = Pt(12)
    p.font.name = "Courier New"
    p.font.color.rgb = WHITE
    p.space_before = Pt(10)

    # =========================================================================
    # SLIDE 8: Custom Exception Handling
    # =========================================================================
    s8 = prs.slides.add_slide(blank_layout)
    add_background(s8)
    add_header(s8, "Robust Exception Handling: CarRentalException", "SYSTEM RELIABILITY")

    c_left = s8.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(2.0), Inches(5.7), Inches(4.7))
    c_left.fill.solid()
    c_left.fill.fore_color.rgb = CARD_BG
    c_left.line.color.rgb = CARD_BORDER

    tb_l = s8.shapes.add_textbox(Inches(1.1), Inches(2.2), Inches(5.1), Inches(4.3))
    tf_l = tb_l.text_frame
    tf_l.word_wrap = True
    p = tf_l.paragraphs[0]
    p.text = "Custom Checked Exception"
    p.font.size = Pt(16)
    p.font.bold = True
    p.font.color.rgb = GOLD

    p = tf_l.add_paragraph()
    p.text = "• Class Definition: 'public class CarRentalException extends Exception' defines a checked exception.\n\n• Validation Scenarios:\n  - Invalid or non-existent Car ID\n  - Attempting to rent an already rented car\n  - Non-positive rental duration (<= 0 days)\n  - Returning an already completed rental\n  - Database transaction failures\n\n• Graceful Recovery: Thrown exceptions are caught in try-catch blocks to display clear error messages without application crashes."
    p.font.size = Pt(13)
    p.font.color.rgb = WHITE
    p.space_before = Pt(10)

    c_right = s8.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(6.8), Inches(2.0), Inches(5.7), Inches(4.7))
    c_right.fill.solid()
    c_right.fill.fore_color.rgb = RGBColor(10, 15, 29)
    c_right.line.color.rgb = CARD_BORDER

    tb_r = s8.shapes.add_textbox(Inches(7.1), Inches(2.2), Inches(5.1), Inches(4.3))
    tf_r = tb_r.text_frame
    tf_r.word_wrap = True
    p = tf_r.paragraphs[0]
    p.text = "Code Evidence: CarRentalException.java"
    p.font.size = Pt(14)
    p.font.bold = True
    p.font.color.rgb = CYAN

    p = tf_r.add_paragraph()
    p.text = "public class CarRentalException extends Exception {\n    public CarRentalException(String message) {\n        super(message);\n    }\n}\n\n// Usage in Business Logic:\nif (days <= 0) {\n    throw new CarRentalException(\"Rental duration must be at least 1 day.\");\n}"
    p.font.size = Pt(12)
    p.font.name = "Courier New"
    p.font.color.rgb = WHITE
    p.space_before = Pt(10)

    # =========================================================================
    # SLIDE 9: Relational Database Schema & SQL
    # =========================================================================
    s9 = prs.slides.add_slide(blank_layout)
    add_background(s9)
    add_header(s9, "Relational Database Schema: SQLite Database", "DATABASE MANAGEMENT")

    db_tables = [
        ("Table: cars", 
         "• car_id (INT, PK)\n• brand (TEXT NOT NULL)\n• model (TEXT NOT NULL)\n• category (TEXT CHECK IN ('Sedan', 'SUV', 'LuxuryCar'))\n• price_per_day (REAL > 0)\n• available (INT CHECK IN (0, 1))",
         GOLD),
        ("Table: customers", 
         "• customer_id (INT, PK AUTOINCREMENT)\n• name (TEXT NOT NULL)\n• phone (TEXT NOT NULL)\n• driving_license (TEXT UNIQUE NOT NULL)",
         CYAN),
        ("Table: rentals", 
         "• rental_id (INT, PK AUTOINCREMENT)\n• customer_id (INT, FK -> customers)\n• car_id (INT, FK -> cars)\n• days (INT > 0)\n• total_amount (REAL > 0)\n• active (INT CHECK IN (0, 1))\n• rental_date (TEXT NOT NULL)\n• return_date (TEXT)",
         EMERALD)
    ]

    for i, (ttitle, tcols, tcolor) in enumerate(db_tables):
        c = s9.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8 + i * 4.0), Inches(2.0), Inches(3.7), Inches(4.7))
        c.fill.solid()
        c.fill.fore_color.rgb = CARD_BG
        c.line.color.rgb = CARD_BORDER

        tb = s9.shapes.add_textbox(Inches(1.0 + i * 4.0), Inches(2.2), Inches(3.3), Inches(4.3))
        tf = tb.text_frame
        tf.word_wrap = True

        p = tf.paragraphs[0]
        p.text = ttitle
        p.font.size = Pt(16)
        p.font.bold = True
        p.font.color.rgb = tcolor

        p = tf.add_paragraph()
        p.text = tcols
        p.font.size = Pt(12)
        p.font.color.rgb = WHITE
        p.space_before = Pt(14)

    # =========================================================================
    # SLIDE 10: JDBC Connectivity & Architecture
    # =========================================================================
    s10 = prs.slides.add_slide(blank_layout)
    add_background(s10)
    add_header(s10, "JDBC Connectivity & Database Architecture", "DATABASE MANAGEMENT")

    c_left = s10.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(2.0), Inches(5.7), Inches(4.7))
    c_left.fill.solid()
    c_left.fill.fore_color.rgb = CARD_BG
    c_left.line.color.rgb = CARD_BORDER

    tb_l = s10.shapes.add_textbox(Inches(1.1), Inches(2.2), Inches(5.1), Inches(4.3))
    tf_l = tb_l.text_frame
    tf_l.word_wrap = True
    p = tf_l.paragraphs[0]
    p.text = "JDBC Architecture & Security"
    p.font.size = Pt(16)
    p.font.bold = True
    p.font.color.rgb = GOLD

    p = tf_l.add_paragraph()
    p.text = "• Connection: Managed via DriverManager.getConnection(\"jdbc:sqlite:carrental.db\").\n\n• Foreign Keys Enforced: PRAGMA foreign_keys = ON;\n\n• SQL Injection Prevention: All user queries use PreparedStatement with parameterized '?' placeholders.\n\n• Polymorphic Entity Hydration: mapCar(ResultSet rs) reads the category column and instantiates new Sedan(), new SUV(), or new LuxuryCar().\n\n• Transaction Safety: conn.setAutoCommit(false), conn.commit(), and conn.rollback() ensure ACID compliance during booking and return."
    p.font.size = Pt(12)
    p.font.color.rgb = WHITE
    p.space_before = Pt(10)

    c_right = s10.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(6.8), Inches(2.0), Inches(5.7), Inches(4.7))
    c_right.fill.solid()
    c_right.fill.fore_color.rgb = RGBColor(10, 15, 29)
    c_right.line.color.rgb = CARD_BORDER

    tb_r = s10.shapes.add_textbox(Inches(7.1), Inches(2.2), Inches(5.1), Inches(4.3))
    tf_r = tb_r.text_frame
    tf_r.word_wrap = True
    p = tf_r.paragraphs[0]
    p.text = "Code Evidence: Transaction in Database.java"
    p.font.size = Pt(14)
    p.font.bold = True
    p.font.color.rgb = CYAN

    p = tf_r.add_paragraph()
    p.text = "conn.setAutoCommit(false); // Begin transaction\ntry {\n    // 1. Insert into rentals table\n    psRental.executeUpdate();\n\n    // 2. Mark car as unavailable in cars table\n    psCar.executeUpdate();\n\n    conn.commit(); // Success\n} catch (SQLException e) {\n    conn.rollback(); // Rollback on error\n    throw new CarRentalException(\"Transaction failed\");\n}"
    p.font.size = Pt(11)
    p.font.name = "Courier New"
    p.font.color.rgb = WHITE
    p.space_before = Pt(8)

    # =========================================================================
    # SLIDE 11: Viva Q&A Reference Guide
    # =========================================================================
    s11 = prs.slides.add_slide(blank_layout)
    add_background(s11)
    add_header(s11, "Viva & Evaluation Q&A Cheat Sheet", "PREPARATION REFERENCE")

    viva_cards = [
        ("Q1: Why use an Abstract Class instead of an Interface for Car?",
         "Answer: Car holds shared state (carId, brand, model, pricePerDay, available) and concrete getters/setters, while enforcing that child classes implement calculateRent(). Interfaces cannot hold non-static instance state.",
         CYAN),
        ("Q2: Where exactly does Dynamic Binding happen?",
         "Answer: In Rental.java constructor on: car.calculateRent(days). The variable is of type Car, but the runtime JVM resolves whether Sedan, SUV, or LuxuryCar executes based on the concrete object passed.",
         GOLD),
        ("Q3: How did you ensure SQL security & relational integrity?",
         "Answer: 1) Used PreparedStatement placeholders to prevent SQL injection. 2) Foreign keys link rentals to customers and cars. 3) PRAGMA foreign_keys = ON enforces relational constraints.",
         EMERALD)
    ]

    for i, (qtitle, qdesc, qcolor) in enumerate(viva_cards):
        c = s11.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(2.0 + i * 1.6), Inches(11.7), Inches(1.35))
        c.fill.solid()
        c.fill.fore_color.rgb = CARD_BG
        c.line.color.rgb = CARD_BORDER

        tb = s11.shapes.add_textbox(Inches(1.1), Inches(2.1 + i * 1.6), Inches(11.1), Inches(1.15))
        tf = tb.text_frame
        tf.word_wrap = True

        p = tf.paragraphs[0]
        p.text = qtitle
        p.font.size = Pt(14)
        p.font.bold = True
        p.font.color.rgb = qcolor

        p = tf.add_paragraph()
        p.text = qdesc
        p.font.size = Pt(12)
        p.font.color.rgb = WHITE
        p.space_before = Pt(4)

    # =========================================================================
    # SLIDE 12: Conclusion & Summary
    # =========================================================================
    s12 = prs.slides.add_slide(blank_layout)
    add_background(s12)
    add_header(s12, "Summary & Conclusion", "PROJECT WRAP-UP")

    card = s12.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(1.5), Inches(2.0), Inches(10.3), Inches(4.7))
    card.fill.solid()
    card.fill.fore_color.rgb = CARD_BG
    card.line.color.rgb = CARD_BORDER

    tb = s12.shapes.add_textbox(Inches(1.9), Inches(2.3), Inches(9.5), Inches(4.1))
    tf = tb.text_frame
    tf.word_wrap = True

    p = tf.paragraphs[0]
    p.text = "Key Takeaways & Technical Highlights"
    p.font.size = Pt(20)
    p.font.bold = True
    p.font.color.rgb = GOLD

    p = tf.add_paragraph()
    p.text = "✅ 100% Core Java OOP Principles applied cleanly (Abstraction, Encapsulation, Inheritance, Polymorphism).\n\n✅ Persistent SQLite Database with verified Relational Foreign Keys (cars, customers, rentals).\n\n✅ Robust Database.java architecture with Parameterized PreparedStatement queries preventing SQL Injection.\n\n✅ Direct Console SQL Query Tool allowing live query execution during project viva.\n\n✅ Robust Exception Handling with custom checked exception CarRentalException."
    p.font.size = Pt(14)
    p.font.color.rgb = WHITE
    p.space_before = Pt(14)

    prs.save(output_path)
    print(f"Presentation saved successfully to {output_path}")

if __name__ == "__main__":
    out = "/Users/anmolsrivastava073/OOPS Project/Car_Rental_System_Presentation.pptx"
    create_presentation(out)
