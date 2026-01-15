# database.py
import mysql.connector
from mysql.connector import Error

class DatabaseConfig:
    """Cấu hình thông số kết nối MySQL"""
    HOST = 'localhost'
    USER = 'root'          # Thay bằng user MySQL của bạn
    PASSWORD = 'root'          # Thay bằng password MySQL của bạn
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
                password=DatabaseConfig.PASSWORD
            )
            
            # Tạo database nếu chưa tồn tại
            if self.connection.is_connected():
                cursor = self.connection.cursor()
                cursor.execute(f"CREATE DATABASE IF NOT EXISTS {DatabaseConfig.DATABASE}")
                self.connection.database = DatabaseConfig.DATABASE
                self.cursor = self.connection.cursor(dictionary=True) # dictionary=True để kết quả trả về dạng dict
                print("Connected to MySQL Database successfully.")
                
                # Tự động tạo bảng khi kết nối lần đầu
                self.create_tables()
        except Error as e:
            print(f"Error connecting to MySQL: {e}")

    def get_connection(self):
        return self.connection

    def close(self):
        if self.connection and self.connection.is_connected():
            self.cursor.close()
            self.connection.close()
            print("MySQL connection closed.")

    def create_tables(self):
        """Tạo các bảng dữ liệu khớp với Entity Class"""
        
        # 1. Bảng Users (Lưu chung Manager, Cashier, WarehouseKeeper)
        # Cột 'role' sẽ phân biệt loại user
        table_users = """
        CREATE TABLE IF NOT EXISTS users (
            id INT AUTO_INCREMENT PRIMARY KEY,
            username VARCHAR(50) UNIQUE NOT NULL,
            password_hash VARCHAR(255) NOT NULL,
            full_name VARCHAR(100),
            email VARCHAR(100),
            phone VARCHAR(20),
            status VARCHAR(20) DEFAULT 'Active',
            role VARCHAR(20) NOT NULL,
            created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
            updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
        );
        """

        # 2. Bảng Products
        table_products = """
        CREATE TABLE IF NOT EXISTS products (
            id INT AUTO_INCREMENT PRIMARY KEY,
            product_code VARCHAR(20) UNIQUE NOT NULL,
            name VARCHAR(100) NOT NULL,
            price DECIMAL(10, 2) NOT NULL,
            stock_qty INT DEFAULT 0,
            created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
            updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
        );
        """

        # 3. Bảng Customers
        table_customers = """
        CREATE TABLE IF NOT EXISTS customers (
            id INT AUTO_INCREMENT PRIMARY KEY,
            customer_code VARCHAR(20) UNIQUE NOT NULL,
            name VARCHAR(100) NOT NULL,
            phone VARCHAR(20),
            point INT DEFAULT 0,
            created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
            updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
        );
        """

        # 4. Bảng Invoices (Hóa đơn)
        table_invoices = """
        CREATE TABLE IF NOT EXISTS invoices (
            id INT AUTO_INCREMENT PRIMARY KEY,
            invoice_code VARCHAR(20) UNIQUE NOT NULL,
            invoice_date DATETIME DEFAULT CURRENT_TIMESTAMP,
            total_amount DECIMAL(15, 2) DEFAULT 0,
            customer_id INT,
            cashier_id INT,
            created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
            updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
            FOREIGN KEY (customer_id) REFERENCES customers(id) ON DELETE SET NULL,
            FOREIGN KEY (cashier_id) REFERENCES users(id) ON DELETE SET NULL
        );
        """

        # 5. Bảng InvoiceItems (Chi tiết hóa đơn)
        table_invoice_items = """
        CREATE TABLE IF NOT EXISTS invoice_items (
            id INT AUTO_INCREMENT PRIMARY KEY,
            invoice_id INT NOT NULL,
            product_id INT NOT NULL,
            quantity INT NOT NULL,
            price DECIMAL(10, 2) NOT NULL,
            created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
            updated_at DATETIME DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (invoice_id) REFERENCES invoices(id) ON DELETE CASCADE,
            FOREIGN KEY (product_id) REFERENCES products(id)
        );
        """

        # 6. Bảng StockEntries (Nhập/Xuất kho)
        table_stock_entries = """
        CREATE TABLE IF NOT EXISTS stock_entries (
            id INT AUTO_INCREMENT PRIMARY KEY,
            entry_code VARCHAR(20) UNIQUE NOT NULL,
            entry_type VARCHAR(20) NOT NULL,
            quantity INT NOT NULL,
            product_id INT NOT NULL,
            entry_date DATETIME DEFAULT CURRENT_TIMESTAMP,
            created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
            updated_at DATETIME DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (product_id) REFERENCES products(id)
        );
        """

        tables = [table_users, table_products, table_customers, table_invoices, table_invoice_items, table_stock_entries]
        
        try:
            for table_sql in tables:
                self.cursor.execute(table_sql)
            self.connection.commit()
            # print("All tables checked/created successfully.")
        except Error as e:
            print(f"Failed to create tables: {e}")

# Singleton instance để dùng chung toàn app
db = Database()