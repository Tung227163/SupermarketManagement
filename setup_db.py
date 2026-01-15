# setup_db.py
from database import db

print("Đang khởi tạo hệ thống...")

# Khi dòng này chạy, class Database được khởi tạo
# Nó sẽ tự động kết nối và gọi hàm create_tables()
if db.connection.is_connected():
    print("✅ Kết nối thành công!")
    print("✅ Đã tạo (hoặc kiểm tra) Database 'supermarket_db'")
    print("✅ Đã tạo các bảng: users, products, customers, invoices...")
else:
    print("❌ Kết nối thất bại. Kiểm tra lại mật khẩu trong database.py")