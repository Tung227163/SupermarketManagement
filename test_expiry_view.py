import unittest
from ui_mocks import MockInventoryView
from controllers.inventory_controller import InventoryController

class TestExpiryFeature(unittest.TestCase):
    
    def test_view_batches(self):
        print("\n" + "="*60)
        print("🧪 TEST CHỨC NĂNG: XEM HẠN SỬ DỤNG CHI TIẾT (BATCHES)")
        print("="*60)
        
        # 1. Khởi tạo
        view = MockInventoryView()
        ctrl = InventoryController(view)
        
        # 2. Giả lập người dùng chọn Sản phẩm ID = 1 (Gạo ST25 từ file Seed Data)
        print("👉 Hành động: Người dùng click vào 'Gạo ST25' (ID: 1)")
        view.selected_product_id = 1
        
        # 3. Gọi Controller xử lý
        ctrl.handle_view_product_details()
        
        # KẾT QUẢ MONG ĐỢI TRÊN MÀN HÌNH:
        # Hệ thống phải in ra bảng chi tiết có 2 dòng (Lô Gần và Lô Xa)
        # Ví dụ:
        # Tên Lô          | Hết Hạn (HSD)   | Số Lượng  
        # ---------------------------------------------
        # Lô Gần 1        | 2024-xx-xx      | 50        
        # Lô Xa 1         | 2025-xx-xx      | 50        

    def test_view_empty_product(self):
        print("\n👉 Hành động: Người dùng click vào SP ID = 999 (Không tồn tại)")
        view = MockInventoryView()
        ctrl = InventoryController(view)
        
        view.selected_product_id = 999
        ctrl.handle_view_product_details()
        # Mong đợi: Báo lỗi đỏ

if __name__ == '__main__':
    unittest.main()