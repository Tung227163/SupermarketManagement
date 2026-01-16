-- ====================================================================================
-- SCRIPT KHỞI TẠO DỮ LIỆU MẪU (VERSION 2 - HỖ TRỢ BATCH/FEFO)
-- Chạy script này trên MySQL Workbench để nạp dữ liệu chuẩn bị nộp bài
-- ====================================================================================

USE supermarket_db;

-- 1. TẮT KIỂM TRA KHÓA NGOẠI ĐỂ LÀM SẠCH DỮ LIỆU
SET FOREIGN_KEY_CHECKS = 0;
TRUNCATE TABLE invoice_items;
TRUNCATE TABLE invoices;
TRUNCATE TABLE stock_entries;
TRUNCATE TABLE product_batches;
TRUNCATE TABLE customers;
TRUNCATE TABLE products;
TRUNCATE TABLE users;
SET FOREIGN_KEY_CHECKS = 1;

-- ------------------------------------------------------------------------------------
-- 2. TẠO NHÂN VIÊN (1 Manager, 5 Cashier, 2 WarehouseKeeper)
-- Mật khẩu mặc định cho tất cả là '123456' (Hash SHA256 bên dưới)
-- ------------------------------------------------------------------------------------
INSERT INTO users (username, password_hash, full_name, email, phone, role, status) VALUES 
('admin', '8d969eef6ecad3c29a3a629280e686cf0c3f5d5a86aff3ca12020c923adc6c92', 'Quản Lý Trưởng', 'admin@store.com', '0901000000', 'Manager', 'Active'),
('kho1', '8d969eef6ecad3c29a3a629280e686cf0c3f5d5a86aff3ca12020c923adc6c92', 'Trần Thủ Kho A', 'kho1@store.com', '0902000001', 'WarehouseKeeper', 'Active'),
('kho2', '8d969eef6ecad3c29a3a629280e686cf0c3f5d5a86aff3ca12020c923adc6c92', 'Lê Thủ Kho B', 'kho2@store.com', '0902000002', 'WarehouseKeeper', 'Active'),
('tn1', '8d969eef6ecad3c29a3a629280e686cf0c3f5d5a86aff3ca12020c923adc6c92', 'Phạm Thu Ngân 1', 'tn1@store.com', '0903000001', 'Cashier', 'Active'),
('tn2', '8d969eef6ecad3c29a3a629280e686cf0c3f5d5a86aff3ca12020c923adc6c92', 'Hoàng Thu Ngân 2', 'tn2@store.com', '0903000002', 'Cashier', 'Active'),
('tn3', '8d969eef6ecad3c29a3a629280e686cf0c3f5d5a86aff3ca12020c923adc6c92', 'Vũ Thu Ngân 3', 'tn3@store.com', '0903000003', 'Cashier', 'Active'),
('tn4', '8d969eef6ecad3c29a3a629280e686cf0c3f5d5a86aff3ca12020c923adc6c92', 'Đặng Thu Ngân 4', 'tn4@store.com', '0903000004', 'Cashier', 'Active'),
('tn5', '8d969eef6ecad3c29a3a629280e686cf0c3f5d5a86aff3ca12020c923adc6c92', 'Bùi Thu Ngân 5', 'tn5@store.com', '0903000005', 'Cashier', 'Active');

-- ------------------------------------------------------------------------------------
-- 3. TẠO SẢN PHẨM (20 Món) - Ban đầu set stock_qty = 0, sẽ update sau khi nhập Batch
-- ------------------------------------------------------------------------------------
INSERT INTO products (product_code, name, price, stock_qty) VALUES
('P001', 'Gạo ST25 Ông Cua 5kg', 180000, 0),
('P002', 'Mì Hảo Hảo Tôm Chua Cay', 4500, 0),
('P003', 'Dầu Ăn Neptune 1L', 48000, 0),
('P004', 'Nước Mắm Nam Ngư', 35000, 0),
('P005', 'Bột Giặt OMO Matic 3kg', 120000, 0),
('P006', 'Nước Rửa Chén Sunlight', 28000, 0),
('P007', 'Thùng Bia Tiger 24 lon', 340000, 0),
('P008', 'Lốc 4 Hộp Sữa Vinamilk', 30000, 0),
('P009', 'Dầu Gội Head & Shoulders', 110000, 0),
('P010', 'Sữa Tắm Lifebuoy', 95000, 0),
('P011', 'Snack Khoai Tây Lays', 15000, 0),
('P012', 'Bánh ChocoPie Hộp 12 cái', 50000, 0),
('P013', 'Xúc Xích Vissan Gói 5 cây', 20000, 0),
('P014', 'Nước Ngọt CocaCola 1.5L', 18000, 0),
('P015', 'Giấy Vệ Sinh Cuộn Emos', 35000, 0),
('P016', 'Kem Đánh Răng PS', 25000, 0),
('P017', 'Bàn Chải Đánh Răng', 12000, 0),
('P018', 'Trứng Gà Ba Huân (vỉ 10)', 32000, 0),
('P019', 'Cà Phê G7 Trung Nguyên', 45000, 0),
('P020', 'Tương Ớt Chin-su', 15000, 0);

-- ------------------------------------------------------------------------------------
-- 4. NHẬP KHO & TẠO LÔ HÀNG (QUAN TRỌNG CHO FEFO)
-- Mỗi sản phẩm sẽ có 2 Lô:
--   Lô A: 50 cái, Hết hạn sau 30 ngày (Dùng để bán trước)
--   Lô B: 50 cái, Hết hạn sau 1 năm (Dùng để bán sau)
-- ------------------------------------------------------------------------------------

-- Tạo Procedure để loop insert batch cho gọn
DELIMITER //
CREATE PROCEDURE SeedBatches()
BEGIN
    DECLARE i INT DEFAULT 1;
    DECLARE total_prods INT DEFAULT 20;
    
    WHILE i <= total_prods DO
        -- Lô 1: Date gần (Hôm nay + 30 ngày)
        INSERT INTO product_batches (product_id, batch_name, quantity, expiry_date, received_date)
        VALUES (i, CONCAT('Lô Gần ', i), 50, DATE_ADD(CURDATE(), INTERVAL 30 DAY), CURDATE());
        
        INSERT INTO stock_entries (entry_code, entry_type, quantity, product_id, expiry_date)
        VALUES (CONCAT('IMP_SHORT_', i), 'Import', 50, i, DATE_ADD(CURDATE(), INTERVAL 30 DAY));

        -- Lô 2: Date xa (Hôm nay + 365 ngày)
        INSERT INTO product_batches (product_id, batch_name, quantity, expiry_date, received_date)
        VALUES (i, CONCAT('Lô Xa ', i), 50, DATE_ADD(CURDATE(), INTERVAL 365 DAY), CURDATE());
        
        INSERT INTO stock_entries (entry_code, entry_type, quantity, product_id, expiry_date)
        VALUES (CONCAT('IMP_LONG_', i), 'Import', 50, i, DATE_ADD(CURDATE(), INTERVAL 365 DAY));

        -- Cập nhật tổng tồn kho trong bảng Products (50 + 50 = 100)
        UPDATE products SET stock_qty = 100 WHERE id = i;
        
        SET i = i + 1;
    END WHILE;
END //
DELIMITER ;

CALL SeedBatches();
DROP PROCEDURE IF EXISTS SeedBatches;

-- ------------------------------------------------------------------------------------
-- 5. TẠO 50 KHÁCH HÀNG (Dùng Loop)
-- ------------------------------------------------------------------------------------
DELIMITER //
CREATE PROCEDURE SeedCustomers()
BEGIN
    DECLARE i INT DEFAULT 1;
    WHILE i <= 50 DO
        INSERT INTO customers (customer_code, name, phone, point)
        VALUES (
            CONCAT('KH', LPAD(i, 3, '0')), 
            CONCAT('Khách Hàng ', i), 
            CONCAT('090', FLOOR(1000000 + RAND() * 8999999)), 
            FLOOR(RAND() * 200) -- Điểm ngẫu nhiên 0-200
        );
        SET i = i + 1;
    END WHILE;
END //
DELIMITER ;

CALL SeedCustomers();
DROP PROCEDURE IF EXISTS SeedCustomers;

-- ------------------------------------------------------------------------------------
-- 6. TẠO 50 HÓA ĐƠN LỊCH SỬ (Giả lập bán hàng)
-- Lưu ý: Để đơn giản cho script SQL, ta sẽ chỉ trừ số lượng ở 'Lô Gần'
-- ------------------------------------------------------------------------------------
DELIMITER //
CREATE PROCEDURE SeedInvoices()
BEGIN
    DECLARE i INT DEFAULT 1;
    DECLARE rand_cust INT;
    DECLARE rand_cashier INT;
    DECLARE new_inv_id INT;
    DECLARE total_bill DECIMAL(15,2);
    
    WHILE i <= 50 DO
        -- Chọn ngẫu nhiên
        SET rand_cust = FLOOR(1 + RAND() * 50);
        -- Cashier ID từ 4 đến 8 (theo thứ tự insert ở trên)
        SET rand_cashier = FLOOR(4 + RAND() * 5);
        
        -- Tạo Invoice Header
        INSERT INTO invoices (invoice_code, invoice_date, total_amount, customer_id, cashier_id, status)
        VALUES (
            CONCAT('INV-', YEAR(CURDATE()), '-', LPAD(i, 4, '0')),
            DATE_SUB(CURDATE(), INTERVAL FLOOR(RAND() * 60) DAY), -- Random trong 60 ngày qua
            0, -- Sẽ update sau
            rand_cust,
            rand_cashier,
            'Paid'
        );
        
        SET new_inv_id = LAST_INSERT_ID();
        SET total_bill = 0;
        
        -- Mỗi hóa đơn mua 2 sản phẩm ngẫu nhiên
        -- Món 1
        BEGIN
            DECLARE p_id INT;
            DECLARE p_price DECIMAL(10,2);
            DECLARE qty INT DEFAULT 2; -- Mua 2 cái
            
            SET p_id = FLOOR(1 + RAND() * 20);
            SELECT price INTO p_price FROM products WHERE id = p_id;
            
            INSERT INTO invoice_items (invoice_id, product_id, quantity, price)
            VALUES (new_inv_id, p_id, qty, p_price);
            
            SET total_bill = total_bill + (p_price * qty);
            
            -- TRỪ KHO (Giả lập logic FEFO: Trừ vào Lô Gần trước)
            -- 1. Trừ bảng Products
            UPDATE products SET stock_qty = stock_qty - qty WHERE id = p_id;
            -- 2. Trừ bảng Product_Batches (Tìm lô gần nhất của sp đó)
            UPDATE product_batches 
            SET quantity = quantity - qty 
            WHERE product_id = p_id 
            ORDER BY expiry_date ASC LIMIT 1;
        END;

        -- Món 2 (Logic tương tự)
        BEGIN
            DECLARE p_id INT;
            DECLARE p_price DECIMAL(10,2);
            DECLARE qty INT DEFAULT 1; -- Mua 1 cái
            
            SET p_id = FLOOR(1 + RAND() * 20); -- Có thể trùng món 1, kệ nó
            SELECT price INTO p_price FROM products WHERE id = p_id;
            
            INSERT INTO invoice_items (invoice_id, product_id, quantity, price)
            VALUES (new_inv_id, p_id, qty, p_price);
            
            SET total_bill = total_bill + (p_price * qty);
            
            UPDATE products SET stock_qty = stock_qty - qty WHERE id = p_id;
            UPDATE product_batches SET quantity = quantity - qty WHERE product_id = p_id ORDER BY expiry_date ASC LIMIT 1;
        END;
        
        -- Update tổng tiền hóa đơn
        UPDATE invoices SET total_amount = total_bill WHERE id = new_inv_id;
        
        SET i = i + 1;
    END WHILE;
END //
DELIMITER ;

CALL SeedInvoices();
DROP PROCEDURE IF EXISTS SeedInvoices;

-- ====================================================================================
-- KẾT THÚC KHỞI TẠO
-- ====================================================================================
SELECT '✅ SUCCESS: Database has been populated!' AS Status;
SELECT * FROM users;
SELECT * FROM product_batches LIMIT 10;
SELECT COUNT(*) AS total_invoices FROM invoices;