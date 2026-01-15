# repositories/order_repository.py
from repositories.base_repository import BaseRepository
from entities.orders import Invoice, InvoiceItem
from repositories.customer_repository import CustomerRepository
from repositories.product_repository import ProductRepository

class InvoiceRepository(BaseRepository):
    def __init__(self):
        super().__init__()
        self.cust_repo = CustomerRepository()
        self.prod_repo = ProductRepository()

    def save(self, invoice: Invoice):
        """
        Lưu hóa đơn và danh sách sản phẩm trong hóa đơn.
        Sử dụng Transaction để đảm bảo tính toàn vẹn dữ liệu.
        """
        try:
            # 1. Lưu Invoice Header
            cust_id = invoice.customer.id if invoice.customer else None
            
            query_inv = """
                INSERT INTO invoices (invoice_code, total_amount, customer_id, cashier_id, invoice_date)
                VALUES (%s, %s, %s, %s, %s)
            """
            val_inv = (invoice.invoice_code, invoice.total_amount, cust_id, invoice.cashier_id, invoice.invoice_date)
            self.cursor.execute(query_inv, val_inv)
            invoice_id = self.cursor.lastrowid
            invoice.id = invoice_id

            # 2. Lưu từng Invoice Item
            query_item = """
                INSERT INTO invoice_items (invoice_id, product_id, quantity, price)
                VALUES (%s, %s, %s, %s)
            """
            for item in invoice.items:
                val_item = (invoice_id, item.product.id, item.quantity, item.price)
                self.cursor.execute(query_item, val_item)

            # Commit transaction
            self.conn.commit()
            return invoice
        
        except Exception as e:
            self.conn.rollback() # Nếu lỗi thì hoàn tác
            print(f"Error saving invoice: {e}")
            raise e

    def find_all(self):
        pass # Có thể implement nếu cần danh sách hóa đơn

    def find_by_id(self, id):
        pass # Có thể implement nếu cần chi tiết hóa đơn

    def delete(self, id):
        pass