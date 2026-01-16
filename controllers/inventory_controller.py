from services.inventory_service import InventoryService

class InventoryController:
    def __init__(self, view, user):
        self.view = view
        self.user = user  # Lưu user đang đăng nhập
        self.inv_service = InventoryService()

    def load_stock_table(self):
        """Lấy dữ liệu tồn kho và hiển thị lên bảng"""
        try:
            # Lấy danh sách sản phẩm từ Service
            products = self.inv_service.get_all_products()
            
            # Lọc theo từ khóa tìm kiếm (nếu có nhập)
            search_text = self.view.get_search_text().lower()
            if search_text:
                products = [p for p in products if search_text in p.name.lower() or search_text in p.product_code.lower()]
            
            self.view.update_stock_table(products)
        except Exception as e:
            self.view.show_error(f"Lỗi tải dữ liệu kho: {e}")

    def handle_import_goods(self):
        data = self.view.get_import_inputs()
        
        if not data['entry_code'] or not data['product_code']:
            self.view.show_error("Thiếu mã phiếu hoặc mã sản phẩm.")
            return

        try:
            product = self.inv_service.find_product_by_code(data['product_code'])
            if not product:
                self.view.show_error(f"Mã sản phẩm '{data['product_code']}' không tồn tại.")
                return

            # CẬP NHẬT GỌI HÀM: Truyền self.user vào đầu tiên
            self.inv_service.import_goods(
                user=self.user,   # <--- QUAN TRỌNG: Truyền user xuống Service
                entry_code=data['entry_code'],
                product_id=product.id,
                quantity=data['quantity'],
                expiry_date_str=data['expiry_date']
            )
            
            self.view.show_success(f"Nhập kho thành công: {product.name}")
            self.load_stock_table()
            
        except PermissionError as pe: # Bắt lỗi bảo mật riêng
            self.view.show_error(str(pe))
        except ValueError as ve:
            self.view.show_error(str(ve))
        except Exception as e:
            self.view.show_error(f"Lỗi: {e}")

    def handle_view_product_details(self):
        """Xem chi tiết hạn sử dụng (Dùng Mã SP)"""
        p_code = self.view.get_selected_product_code() # Lấy code từ UI
        
        if not p_code:
            self.view.show_error("Vui lòng nhập mã sản phẩm.")
            return

        try:
            # 1. Tìm Product từ Code
            product = self.inv_service.find_product_by_code(p_code)
            if not product:
                self.view.show_error(f"Sản phẩm mã '{p_code}' không tồn tại.")
                return

            # 2. Lấy danh sách lô hàng bằng ID
            batches = self.inv_service.get_product_batches(product.id)
            
            # 3. Hiển thị
            self.view.update_batch_details_table(product.name, batches)
            
        except Exception as e:
            self.view.show_error(f"Lỗi xem chi tiết: {e}")