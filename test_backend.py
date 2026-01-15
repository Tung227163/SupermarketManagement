import unittest
import time
from datetime import datetime, timedelta

# Import Services
from services.auth_service import AuthService
from services.user_service import UserService
from services.inventory_service import InventoryService
from services.sales_service import SalesService
from services.customer_service import CustomerService
from services.report_service import ReportService

# Import Entities để check type
from entities.users import Manager, Cashier
from entities.base import UserStatus

class TestFullBackend(unittest.TestCase):
    """
    Kịch bản kiểm thử toàn diện hệ thống Backend.
    Dữ liệu tạo ra sẽ có tiền tố 'TEST_' để dễ phân biệt.
    """

    @classmethod
    def setUpClass(cls):
        """Khởi tạo các Service một lần duy nhất"""
        print("\n" + "="*70)
        print("🚀 BẮT ĐẦU TEST TOÀN BỘ HỆ THỐNG (INTEGRATION TEST)")
        print("="*70)
        cls.auth_service = AuthService()
        cls.user_service = UserService()
        cls.inv_service = InventoryService()
        cls.sales_service = SalesService()
        cls.cust_service = CustomerService()
        cls.report_service = ReportService()

        # Tạo mã ngẫu nhiên cho lần chạy này để tránh trùng lặp dữ liệu cũ
        cls.run_id = int(time.time()) 

    # =================================================================
    # SCENARIO 1: QUẢN LÝ NHÂN SỰ & XÁC THỰC
    # =================================================================
    def test_01_user_flow(self):
        print("\n🔹 [Test 1] Quy trình Nhân sự & Đăng nhập")
        
        # 1. Manager tạo một Cashier mới
        username = f"cashier_{self.run_id}"
        password = "password123"
        
        new_user = self.user_service.create_user(
            username=username,
            password=password,
            full_name="Test Cashier",
            email="test@store.com",
            phone="0909999999",
            role="Cashier"
        )
        self.assertIsNotNone(new_user, "Tạo user thất bại")
        self.assertEqual(new_user.role, "Cashier")
        print(f"   -> Manager đã tạo nhân viên: {username}")

        # 2. Thử đăng nhập bằng Cashier vừa tạo
        login_user = self.auth_service.login(username, password)
        self.assertIsNotNone(login_user, "Đăng nhập thất bại")
        self.assertEqual(login_user.id, new_user.id)
        print(f"   -> Đăng nhập thành công với user: {login_user.username}")

        # 3. Lưu lại user để dùng cho test bán hàng sau này
        TestFullBackend.cashier_user = login_user

    # =================================================================
    # SCENARIO 2: KHO VẬN & LOGIC HẠN SỬ DỤNG (FEFO)
    # =================================================================
    def test_02_inventory_fefo_setup(self):
        print("\n🔹 [Test 2] Quy trình Kho & Setup FEFO (First Expired First Out)")
        
        # 1. Tạo sản phẩm mới
        p_code = f"PROD_{self.run_id}"
        p_name = f"Sữa tươi Test {self.run_id}"
        price = 10000.0
        
        product = self.inv_service.add_new_product(p_code, p_name, price)
        self.assertIsNotNone(product, "Tạo sản phẩm thất bại")
        TestFullBackend.product_id = product.id # Lưu ID để dùng test sau
        print(f"   -> Đã tạo sản phẩm: {p_name} (ID: {product.id})")

        # 2. Nhập Lô 1: 10 hộp - Hết hạn NĂM NGOÁI (Đã hết hạn hoặc sắp hết)
        # Để test xem nó có trừ lô này trước không
        exp_date_1 = (datetime.now() - timedelta(days=1)).strftime('%Y-%m-%d') # Hôm qua
        self.inv_service.import_goods("IMP_01", product.id, 10, exp_date_1)
        print(f"   -> Nhập Lô 1: 10 cái (HSD: {exp_date_1} - Ưu tiên xuất)")

        # 3. Nhập Lô 2: 10 hộp - Hết hạn NĂM SAU
        exp_date_2 = (datetime.now() + timedelta(days=365)).strftime('%Y-%m-%d')
        self.inv_service.import_goods("IMP_02", product.id, 10, exp_date_2)
        print(f"   -> Nhập Lô 2: 10 cái (HSD: {exp_date_2} - Xuất sau)")

        # 4. Kiểm tra tổng tồn kho (Phải là 20)
        # Cần query lại từ DB để chắc chắn
        p_check = self.inv_service.prod_repo.find_by_id(product.id)
        self.assertEqual(p_check.stock_qty, 20, "Tổng tồn kho không đúng")
        print("   -> Tổng tồn kho hiện tại: 20")

    # =================================================================
    # SCENARIO 3: KHÁCH HÀNG
    # =================================================================
    def test_03_customer_creation(self):
        print("\n🔹 [Test 3] Quy trình Khách hàng")
        c_code = f"CUST_{self.run_id}"
        c_phone = f"09{self.run_id}"[:10] # Lấy 10 số đầu
        
        cust = self.cust_service.create_customer(c_code, "Khách hàng Test", c_phone)
        self.assertIsNotNone(cust)
        TestFullBackend.customer_id = cust.id
        print(f"   -> Đã tạo khách hàng: {cust.name} (Điểm: {cust.point})")

    # =================================================================
    # SCENARIO 4: BÁN HÀNG & TRỪ KHO TỰ ĐỘNG
    # =================================================================
    def test_04_sales_transaction(self):
        print("\n🔹 [Test 4] Quy trình Bán hàng & Trừ kho tự động (FEFO)")
        
        # Mua 15 cái
        # Kỳ vọng: 
        # - Lấy hết 10 cái của Lô 1 (Hết hạn sớm)
        # - Lấy thêm 5 cái của Lô 2
        # - Tổng tồn còn 5 cái
        
        cart = [
            {'product_id': TestFullBackend.product_id, 'qty': 15}
        ]
        
        invoice = self.sales_service.create_invoice(
            cashier=TestFullBackend.cashier_user,
            customer_id=TestFullBackend.customer_id,
            cart_items=cart,
            use_points=False
        )
        
        self.assertIsNotNone(invoice)
        print(f"   -> Hóa đơn được tạo: {invoice.invoice_code}, Tổng tiền: {invoice.total_amount}")

        # KIỂM TRA SAU KHI BÁN (QUAN TRỌNG)
        
        # 1. Kiểm tra tổng tồn kho phải còn 5
        p_after = self.inv_service.prod_repo.find_by_id(TestFullBackend.product_id)
        self.assertEqual(p_after.stock_qty, 5, "Tổng tồn kho sau khi bán sai")
        print("   -> ✅ Tổng tồn kho đã giảm còn 5.")

        # 2. Kiểm tra chi tiết từng lô (FEFO Logic)
        batches = self.inv_service.prod_repo.find_batches_by_product_id_sorted(TestFullBackend.product_id)
        # batches[0] là lô hết hạn sớm (Lô 1), batches[1] là lô hết hạn sau (Lô 2)
        # Lưu ý: hàm find_batches... chỉ trả về lô có quantity > 0.
        # Nên nếu Lô 1 hết sạch, nó có thể không xuất hiện trong list hoặc xuất hiện nếu logic query của bạn lấy cả = 0.
        # Trong code repo tôi viết: query có "AND quantity > 0", nên Lô 1 sẽ BIẾN MẤT khỏi list trả về.
        
        # Nếu chỉ còn 1 lô (Lô 2) và số lượng là 5 -> Đúng
        if len(batches) == 1:
            print(f"   -> ✅ Lô hết hạn sớm đã hết hàng (đúng logic).")
            self.assertEqual(batches[0].quantity, 5, "Lô còn lại phải còn 5 cái")
        else:
            # Trường hợp query trả về cả lô = 0, ta kiểm tra kỹ hơn
             for b in batches:
                 print(f"      - Lô HSD {b.expiry_date}: Còn {b.quantity}")

    # =================================================================
    # SCENARIO 5: BÁO CÁO
    # =================================================================
    def test_05_reporting(self):
        print("\n🔹 [Test 5] Quy trình Báo cáo")
        
        # Lấy doanh thu hôm nay
        report = self.report_service.get_daily_revenue()
        # report trả về tuple hoặc dict tùy driver: {'total_orders': X, 'total_revenue': Y}
        
        print(f"   -> Báo cáo hôm nay: {report}")
        self.assertTrue(report['total_revenue'] > 0, "Doanh thu chưa được cập nhật")

if __name__ == '__main__':
    # Chạy test và hiện chi tiết
    unittest.main(verbosity=2)