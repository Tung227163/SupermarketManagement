# test_sales_flow.py
from ui_mocks import MockSalesView
from controllers.sales_controller import SalesController
from entities.users import Cashier

# 1. Giả lập 1 thu ngân đang đăng nhập
cashier = Cashier(1, "thu_ngan1", "pass", "Nguyễn Văn A", "email", "0909")

# 2. Khởi tạo
view = MockSalesView()
controller = SalesController(view, cashier)

print("=== BƯỚC 1: TÌM KHÁCH HÀNG (để tích điểm) ===")
view.customer_phone_input = "0904541166" # (Số ĐT này phải có trong DB seed_data của bạn nhé, nếu ko sẽ báo lỗi)
# Hoặc bạn tự tạo khách mới trong DB trước khi chạy test này
controller.handle_search_customer()
# KẾT QUẢ MONG ĐỢI: Hiện tên khách và số điểm

print("\n=== BƯỚC 2: QUÉT SẢN PHẨM ===")
view.product_code_input = "P001"
view.quantity_input = 2
controller.handle_scan_product()
# KẾT QUẢ MONG ĐỢI: Giỏ hàng hiện 2 món P001

print("\n=== BƯỚC 3: DÙNG ĐIỂM GIẢM GIÁ ===")
view.use_points_checkbox = True # Khách muốn dùng điểm
controller.calculate_totals()
# KẾT QUẢ MONG ĐỢI: Tổng tiền giảm đi

print("\n=== BƯỚC 4: THANH TOÁN ===")
controller.handle_checkout()
# KẾT QUẢ MONG ĐỢI: Báo thành công, Reset giỏ hàng