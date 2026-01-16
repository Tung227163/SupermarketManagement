# ui_mocks.py

# =================================================================================
# 1. MÀN HÌNH ĐĂNG NHẬP
# =================================================================================
class MockLoginView:
    def __init__(self):
        self.username_input = ""
        self.password_input = ""

    def get_username(self): return self.username_input
    def get_password(self): return self.password_input
    def show_error(self, msg): print(f"🔴 [UI LOGIN - ERROR]: {msg}")
    def show_success(self, msg): print(f"🟢 [UI LOGIN - SUCCESS]: {msg}")
    def close(self): print("💻 [UI LOGIN]: Cửa sổ đã đóng.")

# =================================================================================
# 2. MÀN HÌNH CHÍNH
# =================================================================================
class MockMainView:
    def update_user_info(self, fullname, role):
        print(f"👤 [UI MAIN]: User: {fullname} | Role: {role}")
    def show_sales_view(self): print("desktop [UI MAIN] -> Tab BÁN HÀNG")
    def show_inventory_view(self): print("📦 [UI MAIN] -> Tab KHO HÀNG")
    def show_manager_view(self): print("👔 [UI MAIN] -> Tab QUẢN TRỊ")
    def show_report_view(self): print("📊 [UI MAIN] -> Tab BÁO CÁO")
    def logout(self): print("👋 [UI MAIN]: Đăng xuất.")

# =================================================================================
# 3. MÀN HÌNH BÁN HÀNG (Cập nhật Tích điểm/Tiêu điểm)
# =================================================================================
class MockSalesView:
    def __init__(self):
        self.product_code_input = "" 
        self.quantity_input = 1
        
        # --- Phần Khách hàng ---
        self.customer_phone_input = "" 
        self.use_points_checkbox = False # Giả lập Checkbox: True = Dùng điểm, False = Không

    # --- INPUTS ---
    def get_product_code(self): return self.product_code_input
    def get_quantity(self): return self.quantity_input
    def get_customer_phone(self): return self.customer_phone_input
    
    def get_use_points_status(self): 
        """Trả về trạng thái Checkbox 'Dùng điểm thanh toán'"""
        return self.use_points_checkbox

    # --- OUTPUTS ---
    def update_customer_info(self, name, current_points):
        """Hiển thị thông tin khách hàng sau khi tìm thấy"""
        print(f"👤 [UI SALES - KHÁCH HÀNG]: {name} | Điểm tích lũy: {current_points} điểm")
        if current_points > 0:
            print(f"   (Có thể giảm tối đa: {current_points * 1000:,.0f} VNĐ)")

    def update_product_preview(self, name, price, stock):
        print(f"ℹ️ [UI SALES - PREVIEW]: SP: {name} | Giá: {price:,.0f} | Kho: {stock}")

    def update_cart_table(self, cart_items):
        print("\n🛒 [UI SALES - GIỎ HÀNG]")
        print(f"{'Mã':<10} | {'Tên SP':<20} | {'SL':<5} | {'Đơn Giá':<10} | {'Thành Tiền'}")
        print("-" * 70)
        for item in cart_items:
            print(f"{item['code']:<10} | {item['name']:<20} | {item['qty']:<5} | {item['price']:<10,.0f} | {item['total']:,.0f}")
        print("-" * 70)

    def update_total_label(self, total_money, discount, final_money):
        """
        Hiển thị tổng tiền. 
        Nếu discount > 0 nghĩa là khách đã dùng điểm để trừ tiền.
        """
        print(f"💰 [UI SALES - THANH TOÁN]")
        print(f"   + Tổng tiền hàng: {total_money:,.0f} VNĐ")
        print(f"   - Giảm giá (Điểm): {discount:,.0f} VNĐ")
        print(f"   = KHÁCH CẦN TRẢ:  {final_money:,.0f} VNĐ")

    def show_error(self, msg): print(f"🔴 [UI SALES - ERROR]: {msg}")
    def show_success(self, msg): print(f"🟢 [UI SALES - SUCCESS]: {msg}")
    
    def clear_product_input(self):
        self.product_code_input = ""
        self.quantity_input = 1
        print("🧹 [UI SALES]: Đã reset ô nhập SP")

    def show_receipt(self, invoice, cart_items, discount_amount, customer_name="Khách lẻ"):
        """In hóa đơn ra màn hình console giả lập máy in nhiệt"""
        print("\n" + "="*40)
        print(f"{'SIÊU THỊ MINI MART':^40}")
        print(f"{'HÓA ĐƠN THANH TOÁN':^40}")
        print("="*40)
        print(f"Mã HĐ    : {invoice.invoice_code}")
        print(f"Ngày     : {invoice.invoice_date.strftime('%d/%m/%Y %H:%M')}")
        print(f"Thu ngân : {invoice.cashier_id}") # Hoặc tên thu ngân nếu có
        print(f"Khách    : {customer_name}")
        print("-" * 40)
        print(f"{'Tên SP':<20} | {'SL':<3} | {'T.Tiền'}")
        print("-" * 40)
        
        raw_total = 0
        for item in cart_items:
            # item là dict từ controller {'name', 'qty', 'total', ...}
            print(f"{item['name']:<20} | {item['qty']:<3} | {item['total']:,.0f}")
            raw_total += item['total']
            
        print("-" * 40)
        print(f"{'Tổng tiền hàng':<25}: {raw_total:,.0f}")
        print(f"{'Giảm giá (Điểm)':<25}: -{discount_amount:,.0f}")
        print(f"{'THÀNH TIỀN':<25}: {invoice.total_amount:,.0f} VNĐ")
        print("="*40)
        print(f"{'Cảm ơn quý khách & Hẹn gặp lại!':^40}")
        print("\n")

# =================================================================================
# 4. MÀN HÌNH KHO
# =================================================================================
class MockInventoryView:
    def __init__(self):
        self.entry_code_in = ""
        
        # SỬA: Thay vì prod_id_in, dùng prod_code_in
        self.prod_code_in = "" 
        self.qty_in = 0
        self.expiry_in = "" 
        self.search_text = ""
        
        # SỬA: Thay vì selected_product_id, dùng selected_product_code
        self.selected_product_code = ""

    def get_import_inputs(self):
        return {
            'entry_code': self.entry_code_in,
            'product_code': self.prod_code_in, # <--- Sửa ở đây
            'quantity': self.qty_in,
            'expiry_date': self.expiry_in
        }

    def get_selected_product_code(self):
        return self.selected_product_code

    def get_search_text(self): 
        return self.search_text

    # --- CÁC HÀM HIỂN THỊ (OUTPUT) ---
    def update_stock_table(self, products):
        print("\n📦 [UI KHO - TỒN KHO]")
        print(f"{'ID':<5} | {'Tên SP':<20} | {'Tổng Tồn':<10} | {'Giá Bán'}")
        print("-" * 55)
        for p in products:
            print(f"{p.id:<5} | {p.name:<20} | {p.stock_qty:<10} | {p.price:,.0f}")
        print("-" * 55)

    def update_batch_details_table(self, product_name, batches):
        """Hiển thị chi tiết các lô hàng của 1 sản phẩm"""
        print(f"\n📅 [UI KHO - CHI TIẾT HẠN SỬ DỤNG]: {product_name}")
        if not batches:
            print("   (Sản phẩm này hiện không có lô hàng nào trong kho)")
            return

        print(f"   {'Tên Lô':<15} | {'Hết Hạn (HSD)':<15} | {'Số Lượng':<10}")
        print("   " + "-" * 45)
        for b in batches:
            # Kiểm tra nếu date là string hay object date để in cho đúng
            hsd = str(b.expiry_date) 
            print(f"   {b.batch_name:<15} | {hsd:<15} | {b.quantity:<10}")
        print("   " + "-" * 45)

    def show_success(self, msg): print(f"🟢 [UI KHO - SUCCESS]: {msg}")
    def show_error(self, msg): print(f"🔴 [UI KHO - ERROR]: {msg}")
    def show_alert(self, msg): print(f"⚠️ [UI KHO - CẢNH BÁO]: {msg}")

# =================================================================================
# 5. MÀN HÌNH QUẢN LÝ NHÂN SỰ (Cập nhật Phân Quyền)
# =================================================================================
class MockUserView:
    def __init__(self):
        # Input tạo mới
        self.username_in = ""
        self.password_in = ""
        self.fullname_in = ""
        self.role_in = "Cashier"
        
        # Input cập nhật phân quyền (Giả lập việc chọn 1 dòng trên bảng rồi sửa)
        self.selected_user_id = None 
        self.edit_role_input = "Manager" 

    def get_create_inputs(self):
        return {'username': self.username_in, 'password': self.password_in, 'fullname': self.fullname_in, 'role': self.role_in}

    def get_role_update_inputs(self):
        """Lấy ID user đang được chọn và Role mới muốn gán"""
        return {
            'user_id': self.selected_user_id,
            'new_role': self.edit_role_input
        }

    def update_user_table(self, users):
        print("\n👥 [UI USER - DANH SÁCH NHÂN VIÊN]")
        print(f"{'ID':<5} | {'User':<15} | {'Họ Tên':<20} | {'Vai Trò':<15} | {'Trạng Thái'}")
        print("-" * 75)
        for u in users:
            print(f"{u.id:<5} | {u.username:<15} | {u.full_name:<20} | {u.role:<15} | {u.status.value}")

    def show_success(self, msg): print(f"🟢 [UI USER - SUCCESS]: {msg}")
    def show_error(self, msg): print(f"🔴 [UI USER - ERROR]: {msg}")

# =================================================================================
# 6. MÀN HÌNH BÁO CÁO
# =================================================================================
class MockReportView:
    def update_daily_revenue(self, data):
        print(f"\n📊 [UI REPORT - DOANH THU]: {data['total_revenue']:,.0f} VNĐ ({data['total_orders']} đơn)")
    
    def update_top_products(self, products):
        print(f"\n🏆 [UI REPORT - TOP BÁN CHẠY]")
        for p in products: print(f"   - {p['name']}: {p['total_sold']}")