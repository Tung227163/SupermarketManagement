from repositories.product_repository import ProductRepository
from entities.products import StockEntry, StockEntryType

class InventoryService:
    def __init__(self):
        self.prod_repo = ProductRepository()

    def import_goods(self, entry_code, product_id, quantity):
        """Nhập hàng vào kho"""
        product = self.prod_repo.find_by_id(product_id)
        if not product:
            raise ValueError("Sản phẩm không tồn tại")

        if quantity <= 0:
            raise ValueError("Số lượng nhập phải lớn hơn 0")

        # 1. Cập nhật số lượng tồn kho
        product.stock_qty += quantity
        self.prod_repo.save(product) # Lưu thay đổi vào bảng Products

        # 2. Ghi lịch sử nhập kho
        entry = StockEntry(None, entry_code, StockEntryType.IMPORT, quantity, product_id)
        self.prod_repo.save_stock_entry(entry)
        
        print(f"✅ Đã nhập {quantity} sản phẩm '{product.name}' vào kho.")
        return product

    def check_low_stock(self, threshold=10):
        """Kiểm tra các mặt hàng sắp hết"""
        all_products = self.prod_repo.find_all()
        low_stock_items = [p for p in all_products if p.stock_qty < threshold]
        return low_stock_items