import unittest
from datetime import datetime
from entities.base import UserStatus
from entities.users import Manager, Cashier, WarehouseKeeper
from entities.products import Product, StockEntry, StockEntryType
from entities.orders import Customer, Invoice, InvoiceItem
from entities.reports import BusinessReport, CustomerReport

class TestSupermarketEntities(unittest.TestCase):
    """
    Class này dùng để kiểm tra tính đúng đắn của các logic trong folder entities/
    """

    def setUp(self):
        """Hàm này chạy trước mỗi bài test, dùng để khởi tạo dữ liệu mẫu"""
        print("\n" + "="*50)
        
        # Tạo dữ liệu mẫu Product
        self.prod_mi = Product(1, "P001", "Mì Hảo Hảo", 5000.0, 100)
        self.prod_trung = Product(2, "P002", "Trứng gà", 3000.0, 50)

        # Tạo dữ liệu mẫu Customer
        self.customer = Customer(1, "CUST001", "Nguyen Van A", "0901234567")

    # ----------------------------------------------------------------
    # 1. TEST USER LAYER (Manager, Cashier, WarehouseKeeper, BaseUser)
    # ----------------------------------------------------------------
    def test_manager_actions(self):
        print(">> Testing Manager Actions (Login, Assign Role)")
        manager = Manager(1, "admin", "hashed_pass", "Admin User", "admin@store.com", "0909000000")
        
        # Test Login (BaseUser logic)
        is_logged_in = manager.login()
        self.assertTrue(is_logged_in, "Manager login should return True")
        
        # Test Change Password (BaseUser logic)
        manager.change_password("new_hashed_pass")
        self.assertEqual(manager.password_hash, "new_hashed_pass", "Password should be updated")

        # Test Assign Role (Manager logic)
        cashier = Cashier(2, "cashier1", "pass", "Nhan Vien A", "c1@store.com", "0909000001")
        manager.assign_role(cashier, "Senior Cashier") # Chỉ in ra màn hình, không return gì nên không assert

    def test_cashier_actions(self):
        print(">> Testing Cashier Actions")
        cashier = Cashier(2, "cashier1", "pass", "Nhan Vien A", "c1@store.com", "0909000001")
        
        # Test method riêng của Cashier
        cashier.sell_product()
        cashier.create_invoice()
        # Nếu code chạy đến đây không lỗi tức là các hàm đã được gọi thành công

    def test_warehouse_keeper_actions(self):
        print(">> Testing Warehouse Keeper Actions")
        keeper = WarehouseKeeper(3, "kho1", "pass", "Thu Kho", "kho@store.com", "0909000002")
        
        keeper.receive_goods()
        keeper.check_inventory()
        # Kiểm tra trạng thái mặc định
        self.assertEqual(keeper.status, UserStatus.ACTIVE, "Default status should be ACTIVE")

    # ----------------------------------------------------------------
    # 2. TEST PRODUCT LAYER (Product, StockEntry)
    # ----------------------------------------------------------------
    def test_product_display(self):
        print(">> Testing Product String Representation")
        # Kiểm tra hàm __str__
        expected_str = "Mì Hảo Hảo - Qty: 100"
        self.assertEqual(str(self.prod_mi), expected_str)

    def test_stock_entry(self):
        print(">> Testing Stock Entry (Import/Export)")
        # Test phiếu nhập kho
        entry = StockEntry(1, "IMP001", StockEntryType.IMPORT, 500, self.prod_mi.id)
        
        self.assertEqual(entry.type, StockEntryType.IMPORT)
        self.assertEqual(entry.quantity, 500)
        self.assertIsInstance(entry.entry_date, datetime)

    # ----------------------------------------------------------------
    # 3. TEST ORDER LAYER (Invoice, InvoiceItem, Customer) - Quan trọng nhất
    # ----------------------------------------------------------------
    def test_invoice_calculation(self):
        print(">> Testing Invoice Calculation Logic")
        invoice = Invoice(1, "INV-1001", self.customer, cashier_id=2)

        # Mua 2 gói mì (2 * 5000 = 10,000)
        item1 = InvoiceItem(1, self.prod_mi, 2, self.prod_mi.price)
        self.assertEqual(item1.calculate_sub_total(), 10000.0, "Subtotal Item 1 sai")

        # Mua 10 quả trứng (10 * 3000 = 30,000)
        item2 = InvoiceItem(2, self.prod_trung, 10, self.prod_trung.price)
        self.assertEqual(item2.calculate_sub_total(), 30000.0, "Subtotal Item 2 sai")

        # Thêm vào hóa đơn
        invoice.add_item(item1)
        invoice.add_item(item2)

        # Kiểm tra tổng tiền: 10,000 + 30,000 = 40,000
        self.assertEqual(invoice.total_amount, 40000.0, "Tổng tiền hóa đơn tính sai")
        print(f"   [INFO] Invoice Total: {invoice.total_amount} VND (Expected: 40000.0)")

    def test_customer_points(self):
        print(">> Testing Customer Point Accumulation")
        # Giả sử logic là 100,000 VND = 1 điểm (như code ở entities/orders.py)
        
        current_points = self.customer.point
        purchase_amount = 250000.0 # Mong đợi cộng thêm 2 điểm
        
        new_points = self.customer.accumulate_point(purchase_amount)
        
        expected_points = current_points + 2
        self.assertEqual(new_points, expected_points, "Tính điểm tích lũy sai")
        print(f"   [INFO] Points: {new_points} (Expected: {expected_points})")

    # ----------------------------------------------------------------
    # 4. TEST REPORT LAYER
    # ----------------------------------------------------------------
    def test_reports(self):
        print(">> Testing Report Generation")
        # Test Business Report
        biz_report = BusinessReport(1, datetime.now(), total_revenue=5000000, total_invoices=50)
        biz_report.export_pdf() # Chỉ in ra console
        
        self.assertEqual(biz_report.total_revenue, 5000000)

        # Test Customer Report
        cust_report = CustomerReport(1, datetime.now(), total_customers=100, vip_customers=10)
        cust_report.export_pdf()
        
        self.assertEqual(cust_report.vip_customers, 10)

if __name__ == '__main__':
    # Verbosity=2 để hiện chi tiết từng test case pass/fail
    unittest.main(verbosity=2)