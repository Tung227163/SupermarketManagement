from repositories.customer_repository import CustomerRepository
from entities.orders import Customer
from database import db

class CustomerService:
    def __init__(self):
        self.cust_repo = CustomerRepository()

    def create_customer(self, code, name, phone):
        # Kiểm tra SĐT đã tồn tại chưa
        if self.cust_repo.find_by_phone(phone):
            print("❌ Số điện thoại này đã được đăng ký.")
            return None
        
        cust = Customer(None, code, name, phone)
        return self.cust_repo.save(cust)

    def find_customer_by_phone(self, phone):
        return self.cust_repo.find_by_phone(phone)

    def update_customer(self, cust_id, name, phone):
        cust = self.cust_repo.find_by_id(cust_id)
        if cust:
            cust.name = name
            cust.phone = phone
            self.cust_repo.save(cust)
            print("✅ Cập nhật khách hàng thành công.")
        else:
            print("❌ Khách hàng không tồn tại.")

    def get_purchase_history(self, customer_id):
        """Lấy danh sách các hóa đơn khách đã mua"""
        query = "SELECT * FROM invoices WHERE customer_id = %s ORDER BY invoice_date DESC"
        cursor = db.cursor
        cursor.execute(query, (customer_id,))
        return cursor.fetchall()