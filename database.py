# database.py
import mysql.connector
from mysql.connector import Error

class DatabaseConfig:
    HOST = 'localhost'
    USER = 'root'
    PASSWORD = 'root'  # <--- HÃY KIỂM TRA KỸ MẬT KHẨU TẠI ĐÂY
    DATABASE = 'supermarket_db'

class Database:
    def __init__(self):
        self.connection = None
        self.cursor = None
        self.connect()

    def connect(self):
        """Tạo kết nối đến database"""
        try:
            self.connection = mysql.connector.connect(
                host=DatabaseConfig.HOST,
                user=DatabaseConfig.USER,
                password=DatabaseConfig.PASSWORD,
                autocommit=True # Tự động commit để đỡ phải gọi lệnh commit nhiều lần
            )
            
            if self.connection.is_connected():
                # Tạo DB nếu chưa có
                temp_cursor = self.connection.cursor()
                temp_cursor.execute(f"CREATE DATABASE IF NOT EXISTS {DatabaseConfig.DATABASE}")
                
                # Kết nối vào DB cụ thể
                self.connection.database = DatabaseConfig.DATABASE
                self.cursor = self.connection.cursor(dictionary=True, buffered=True)
                
                # Tự động tạo bảng
                self.create_tables()
                print("✅ Kết nối MySQL thành công.")
                
        except Error as e:
            print(f"\n❌❌❌ KẾT NỐI DATABASE THẤT BẠI: {e}")
            print("👉 Gợi ý: Kiểm tra xem XAMPP đã bật MySQL chưa? Mật khẩu trong database.py đúng chưa?\n")
            self.cursor = None # Đánh dấu là chưa có cursor

    def close(self):
        if self.connection and self.connection.is_connected():
            self.cursor.close()
            self.connection.close()
            print("MySQL connection closed.")


    def create_tables(self):
        # 1. Users
        t_users = """CREATE TABLE IF NOT EXISTS users (
            id INT AUTO_INCREMENT PRIMARY KEY,
            username VARCHAR(50) UNIQUE NOT NULL,
            password_hash VARCHAR(255) NOT NULL,
            full_name VARCHAR(100),
            email VARCHAR(100),
            phone VARCHAR(20),
            status VARCHAR(20) DEFAULT 'Active',
            role VARCHAR(20) NOT NULL,
            created_at DATETIME DEFAULT CURRENT_TIMESTAMP
        );"""

        # 2. Products (Vẫn giữ stock_qty để hiển thị tổng tồn kho nhanh)
        t_products = """CREATE TABLE IF NOT EXISTS products (
            id INT AUTO_INCREMENT PRIMARY KEY,
            product_code VARCHAR(20) UNIQUE NOT NULL,
            name VARCHAR(100) NOT NULL,
            price DECIMAL(10, 2) NOT NULL,
            stock_qty INT DEFAULT 0, 
            created_at DATETIME DEFAULT CURRENT_TIMESTAMP
        );"""

        # 3. Product Batches (MỚI - Quản lý lô hàng & Hạn sử dụng)
        t_batches = """CREATE TABLE IF NOT EXISTS product_batches (
            id INT AUTO_INCREMENT PRIMARY KEY,
            product_id INT NOT NULL,
            batch_name VARCHAR(50), -- Ví dụ: Lô tháng 10
            quantity INT DEFAULT 0,
            expiry_date DATE NOT NULL,
            received_date DATE DEFAULT (CURRENT_DATE),
            FOREIGN KEY (product_id) REFERENCES products(id) ON DELETE CASCADE
        );"""

        # 4. Customers
        t_customers = """CREATE TABLE IF NOT EXISTS customers (
            id INT AUTO_INCREMENT PRIMARY KEY,
            customer_code VARCHAR(20) UNIQUE NOT NULL,
            name VARCHAR(100) NOT NULL,
            phone VARCHAR(20),
            point INT DEFAULT 0,
            created_at DATETIME DEFAULT CURRENT_TIMESTAMP
        );"""

        # 5. Invoices
        t_invoices = """CREATE TABLE IF NOT EXISTS invoices (
            id INT AUTO_INCREMENT PRIMARY KEY,
            invoice_code VARCHAR(20) UNIQUE NOT NULL,
            invoice_date DATETIME DEFAULT CURRENT_TIMESTAMP,
            total_amount DECIMAL(15, 2) DEFAULT 0,
            customer_id INT,
            cashier_id INT,
            status VARCHAR(20) DEFAULT 'Paid', -- Paid, Cancelled
            FOREIGN KEY (customer_id) REFERENCES customers(id) ON DELETE SET NULL,
            FOREIGN KEY (cashier_id) REFERENCES users(id) ON DELETE SET NULL
        );"""

        # 6. Invoice Items
        t_inv_items = """CREATE TABLE IF NOT EXISTS invoice_items (
            id INT AUTO_INCREMENT PRIMARY KEY,
            invoice_id INT NOT NULL,
            product_id INT NOT NULL,
            quantity INT NOT NULL,
            price DECIMAL(10, 2) NOT NULL,
            FOREIGN KEY (invoice_id) REFERENCES invoices(id) ON DELETE CASCADE,
            FOREIGN KEY (product_id) REFERENCES products(id)
        );"""

        # 7. Stock Entries (Lịch sử nhập kho)
        t_stock = """CREATE TABLE IF NOT EXISTS stock_entries (
            id INT AUTO_INCREMENT PRIMARY KEY,
            entry_code VARCHAR(50) UNIQUE NOT NULL,
            entry_type VARCHAR(20) NOT NULL,
            quantity INT NOT NULL,
            product_id INT NOT NULL,
            expiry_date DATE NULL, -- Lưu lại hạn sử dụng lúc nhập
            entry_date DATETIME DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (product_id) REFERENCES products(id)
        );"""

        for sql in [t_users, t_products, t_batches, t_customers, t_invoices, t_inv_items, t_stock]:
            self.cursor.execute(sql)
        self.connection.commit()

db = Database()