import sys
from database import db

# Import Mock Views
from ui_mocks import MockLoginView, MockMainView, MockSalesView, MockInventoryView, MockUserView, MockReportView

# Import Controllers
from controllers.auth_controller import AuthController
from controllers.sales_controller import SalesController
from controllers.inventory_controller import InventoryController
from controllers.user_controller import UserController
from controllers.report_controller import ReportController

def main():
    print("🚀 KHỞI ĐỘNG HỆ THỐNG QUẢN LÝ SIÊU THỊ...")
    
    # ------------------------------------------------------------------
    # 1. ĐĂNG NHẬP
    # ------------------------------------------------------------------
    login_view = MockLoginView()
    auth_ctrl = AuthController(login_view)
    
    current_user = None
    while not current_user:
        print("\n--- ĐĂNG NHẬP ---")
        u = input("Username: ")
        p = input("Password: ")
        
        login_view.username_input = u
        login_view.password_input = p
        
        current_user = auth_ctrl.handle_login()
        if not current_user:
            print("(!) Đăng nhập thất bại. Vui lòng thử lại.")

    # ------------------------------------------------------------------
    # 2. MENU CHÍNH (ĐIỀU HƯỚNG THEO QUYỀN)
    # ------------------------------------------------------------------
    main_view = MockMainView()
    main_view.update_user_info(current_user.full_name, current_user.role)

    while True:
        print(f"\n" + "="*40)
        print(f"   MENU CHÍNH | Xin chào: {current_user.username}")
        print(f"   Vai trò: [{current_user.role}]")
        print("="*40)
        print("1. Bán hàng (Sales)")
        print("2. Kho hàng (Inventory)")
        print("3. Quản lý nhân sự (Manager Only)")
        print("4. Báo cáo & Thống kê (Manager Only)")
        print("0. Đăng xuất / Thoát")
        print("-" * 40)
        
        choice = input("👉 Chọn chức năng: ")

        if choice == '0':
            print("Đã thoát chương trình. Hẹn gặp lại!")
            break
            
        # =================================================================
        # MODULE 1: BÁN HÀNG (Dành cho Cashier & Manager)
        # =================================================================
        elif choice == '1': 
            # --- KIỂM TRA QUYỀN ---
            if current_user.role not in ['Cashier', 'Manager']:
                print(f"⛔ LỖI PHÂN QUYỀN: Bạn là '{current_user.role}', không được phép Bán hàng.")
                continue
            
            sales_view = MockSalesView()
            sales_ctrl = SalesController(sales_view, current_user)
            
            print("\n--- PHÂN HỆ BÁN HÀNG ---")
            phone = input("Nhập SĐT Khách (Enter để bỏ qua): ")
            sales_view.customer_phone_input = phone
            sales_ctrl.handle_search_customer()
            
            while True:
                code = input("Quét mã SP (Nhập 'pay' để thanh toán, 'x' để thoát): ")
                if code == 'x': break
                if code == 'pay':
                    use_p = input("Dùng điểm tích lũy? (y/n): ")
                    sales_view.use_points_checkbox = (use_p.lower() == 'y')
                    sales_ctrl.handle_checkout()
                    break
                
                qty = input("Số lượng: ")
                sales_view.product_code_input = code
                sales_view.quantity_input = int(qty) if qty.isdigit() else 1
                sales_ctrl.handle_scan_product()

        # =================================================================
        # MODULE 2: KHO HÀNG (Dành cho WarehouseKeeper & Manager)
        # =================================================================
        elif choice == '2': 
            # --- KIỂM TRA QUYỀN ---
            if current_user.role not in ['WarehouseKeeper', 'Manager']:
                print(f"⛔ LỖI PHÂN QUYỀN: Bạn là '{current_user.role}', không được phép truy cập Kho.")
                continue

            inv_view = MockInventoryView()
            
            # CẬP NHẬT: Truyền current_user vào Controller
            inv_ctrl = InventoryController(inv_view, current_user) 
            
            while True:
                print("\n--- PHÂN HỆ KHO ---")
                print("1. Xem danh sách tồn kho")
                print("2. Nhập kho (Tạo phiếu nhập)")
                print("3. Kiểm tra hạn sử dụng (Xem lô hàng)")
                print("0. Quay lại Menu chính")
                sub_c = input("Chọn: ")
                
                if sub_c == '0': break
                
                if sub_c == '1':
                    inv_ctrl.load_stock_table()

                elif sub_c == '2':
                    print("\n[NHẬP KHO MỚI]")
                    inv_view.entry_code_in = input("Mã phiếu nhập (VD: PN001): ")
                    inv_view.prod_code_in = input("Mã Sản Phẩm (VD: P001): ")
                    qty = input("Số lượng: ")
                    inv_view.qty_in = int(qty) if qty.isdigit() else 0
                    inv_view.expiry_in = input("Hạn sử dụng (YYYY-MM-DD): ")
                    inv_ctrl.handle_import_goods()

                elif sub_c == '3':
                    p_code = input("Nhập Mã Sản Phẩm cần xem (VD: P001): ")
                    inv_view.selected_product_code = p_code
                    inv_ctrl.handle_view_product_details()

        # =================================================================
        # MODULE 3: QUẢN LÝ NHÂN SỰ (Chỉ Manager)
        # =================================================================
        elif choice == '3': # USER MANAGER
            # Check quyền UI (Lớp bảo vệ 1)
            if current_user.role != 'Manager':
                print(f"⛔ Bạn là '{current_user.role}', không phải Manager.")
                continue
            
            user_view = MockUserView()
            # CẬP NHẬT: Truyền current_user
            user_ctrl = UserController(user_view, current_user)
            
            user_ctrl.load_user_list()
            print("(Chức năng thêm/sửa đang ở chế độ demo danh sách)")
            input("Nhấn Enter để quay lại...")

        # =================================================================
        # MODULE 4: BÁO CÁO (Chỉ Manager)
        # =================================================================
        elif choice == '4': # REPORT
            # Check quyền UI (Lớp bảo vệ 1)
            if current_user.role != 'Manager':
                print(f"⛔ Bạn là '{current_user.role}', không phải Manager.")
                continue
            
            rep_view = MockReportView()
            # CẬP NHẬT: Truyền current_user
            rep_ctrl = ReportController(rep_view, current_user)
            
            rep_ctrl.load_dashboard_data()
            input("Nhấn Enter để quay lại...")

        else:
            print("Lựa chọn không hợp lệ.")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nĐã dừng chương trình.")