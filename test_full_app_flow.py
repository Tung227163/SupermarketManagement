# test_full_app_flow.py
from ui_mocks import MockLoginView, MockSalesView, MockInventoryView, MockReportView, MockUserView
from controllers.auth_controller import AuthController
from controllers.sales_controller import SalesController
from controllers.inventory_controller import InventoryController
from controllers.report_controller import ReportController
from controllers.user_controller import UserController

print("\n🚀 KỊCH BẢN: MỘT NGÀY HOẠT ĐỘNG SIÊU THỊ")
print("="*60)

# ---------------------------------------------------------
# 1. ĐĂNG NHẬP (QUẢN LÝ)
# ---------------------------------------------------------
print("\n🔹 [BƯỚC 1] ADMIN ĐĂNG NHẬP")
login_view = MockLoginView()
auth_ctrl = AuthController(login_view)

login_view.username_input = "admin"
login_view.password_input = "123456" # Pass mặc định từ seed data
current_user = auth_ctrl.handle_login()

if not current_user:
    print("❌ Đăng nhập thất bại. Dừng test.")
    exit()

# ---------------------------------------------------------
# 2. QUẢN LÝ NHÂN SỰ (Tạo nhân viên mới)
# ---------------------------------------------------------
print("\n🔹 [BƯỚC 2] ADMIN TẠO NHÂN VIÊN MỚI")
user_view = MockUserView()
user_ctrl = UserController(user_view)

# Admin xem danh sách trước
user_ctrl.load_user_list()

# Admin tạo thu ngân mới
user_view.username_in = "thungan_moi2"
user_view.password_in = "123"
user_view.fullname_in = "Nhân Viên Mới"
user_view.role_in = "Cashier"
user_ctrl.handle_create_user()

# ---------------------------------------------------------
# 3. NHẬP KHO (Thủ kho làm việc)
# ---------------------------------------------------------
print("\n🔹 [BƯỚC 3] NHẬP KHO HÀNG HÓA")
inv_view = MockInventoryView()
inv_ctrl = InventoryController(inv_view)

# Xem tồn kho hiện tại
inv_ctrl.load_stock_table()

# Nhập thêm 100 chai nước suối (ID giả định là 1 - Gạo ST25 hoặc gì đó có sẵn trong DB)
inv_view.entry_code_in = "PN_TEST_002"
inv_view.prod_id_in = 1 
inv_view.qty_in = 100
inv_view.expiry_in = "2025-12-31" # Date xa
inv_ctrl.handle_import_goods()

# ---------------------------------------------------------
# 4. BÁN HÀNG (Thu ngân bán cho khách)
# ---------------------------------------------------------
print("\n🔹 [BƯỚC 4] THU NGÂN BÁN HÀNG")
sales_view = MockSalesView()
sales_ctrl = SalesController(sales_view, current_user) # Dùng user admin bán luôn cho nhanh

# Tìm khách hàng VIP (SĐT có trong seed data)
# Bạn hãy thay số này bằng số thật trong DB của bạn nếu báo lỗi
sales_view.customer_phone_input = "0904541166" 
sales_ctrl.handle_search_customer()

# Mua hàng (ID 1 vừa nhập ở trên)
sales_view.product_code_input = "P001" # Mã Gạo ST25 (trong seed data)
sales_view.quantity_input = 2
sales_ctrl.handle_scan_product()

# Thanh toán
sales_ctrl.handle_checkout()

# ---------------------------------------------------------
# 5. XEM BÁO CÁO (Cuối ngày)
# ---------------------------------------------------------
print("\n🔹 [BƯỚC 5] ADMIN XEM DOANH THU CUỐI NGÀY")
report_view = MockReportView()
report_ctrl = ReportController(report_view)

report_ctrl.load_dashboard_data()

print("\n✅ KỊCH BẢN HOÀN TẤT!")