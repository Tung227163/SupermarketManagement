-- Supermarket Management System Database Schema

-- Users table for authentication
CREATE TABLE IF NOT EXISTS users (
    user_id INTEGER PRIMARY KEY AUTOINCREMENT,
    username VARCHAR(50) UNIQUE NOT NULL,
    password VARCHAR(100) NOT NULL,
    full_name VARCHAR(100) NOT NULL,
    role VARCHAR(20) NOT NULL,
    is_active BOOLEAN DEFAULT 1,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Products table
CREATE TABLE IF NOT EXISTS products (
    product_id INTEGER PRIMARY KEY AUTOINCREMENT,
    product_code VARCHAR(50) UNIQUE NOT NULL,
    product_name VARCHAR(200) NOT NULL,
    category VARCHAR(100),
    price DECIMAL(10, 2) NOT NULL,
    stock_quantity INTEGER DEFAULT 0,
    unit VARCHAR(20),
    supplier VARCHAR(200),
    is_active BOOLEAN DEFAULT 1,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Employees table
CREATE TABLE IF NOT EXISTS employees (
    employee_id INTEGER PRIMARY KEY AUTOINCREMENT,
    employee_code VARCHAR(50) UNIQUE NOT NULL,
    full_name VARCHAR(100) NOT NULL,
    phone VARCHAR(20),
    email VARCHAR(100),
    position VARCHAR(50),
    salary DECIMAL(10, 2),
    hire_date DATE,
    is_active BOOLEAN DEFAULT 1,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Customers table
CREATE TABLE IF NOT EXISTS customers (
    customer_id INTEGER PRIMARY KEY AUTOINCREMENT,
    customer_code VARCHAR(50) UNIQUE NOT NULL,
    full_name VARCHAR(100) NOT NULL,
    phone VARCHAR(20),
    email VARCHAR(100),
    address VARCHAR(200),
    is_active BOOLEAN DEFAULT 1,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Sales table
CREATE TABLE IF NOT EXISTS sales (
    sale_id INTEGER PRIMARY KEY AUTOINCREMENT,
    sale_code VARCHAR(50) UNIQUE NOT NULL,
    customer_id INTEGER,
    employee_id INTEGER,
    sale_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    total_amount DECIMAL(10, 2) NOT NULL,
    payment_method VARCHAR(50),
    status VARCHAR(20) DEFAULT 'COMPLETED',
    FOREIGN KEY (customer_id) REFERENCES customers(customer_id),
    FOREIGN KEY (employee_id) REFERENCES employees(employee_id)
);

-- Sale items table
CREATE TABLE IF NOT EXISTS sale_items (
    sale_item_id INTEGER PRIMARY KEY AUTOINCREMENT,
    sale_id INTEGER NOT NULL,
    product_id INTEGER NOT NULL,
    quantity INTEGER NOT NULL,
    unit_price DECIMAL(10, 2) NOT NULL,
    subtotal DECIMAL(10, 2) NOT NULL,
    FOREIGN KEY (sale_id) REFERENCES sales(sale_id),
    FOREIGN KEY (product_id) REFERENCES products(product_id)
);

-- Insert default admin user (password: admin123)
INSERT OR IGNORE INTO users (username, password, full_name, role) 
VALUES ('admin', 'admin123', 'Administrator', 'ADMIN');

-- Insert sample data
INSERT OR IGNORE INTO products (product_code, product_name, category, price, stock_quantity, unit, supplier) VALUES
('P001', 'Gạo Thơm', 'Thực phẩm', 25000, 100, 'kg', 'Nhà cung cấp A'),
('P002', 'Dầu ăn', 'Thực phẩm', 45000, 50, 'lít', 'Nhà cung cấp B'),
('P003', 'Sữa tươi', 'Sữa', 35000, 80, 'hộp', 'Nhà cung cấp C'),
('P004', 'Bánh mì', 'Bánh', 15000, 120, 'ổ', 'Nhà cung cấp D');

INSERT OR IGNORE INTO employees (employee_code, full_name, phone, email, position, salary, hire_date) VALUES
('E001', 'Nguyễn Văn A', '0901234567', 'nva@email.com', 'Quản lý', 15000000, '2023-01-15'),
('E002', 'Trần Thị B', '0912345678', 'ttb@email.com', 'Thu ngân', 8000000, '2023-03-20'),
('E003', 'Lê Văn C', '0923456789', 'lvc@email.com', 'Nhân viên kho', 7000000, '2023-05-10');
