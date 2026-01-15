# entities/products.py
from datetime import datetime
from enum import Enum
from entities.base import BaseEntity

class Product(BaseEntity):
    def __init__(self, id: int, product_code: str, name: str, price: float, stock_qty: int):
        super().__init__(id)
        self.product_code = product_code
        self.name = name
        self.price = price
        self.stock_qty = stock_qty

    def __str__(self):
        return f"{self.name} - Qty: {self.stock_qty}"

class StockEntryType(Enum):
    IMPORT = "Import" # Nhập kho
    EXPORT = "Export" # Xuất kho (hủy, trả hàng NCC)

class StockEntry(BaseEntity):
    def __init__(self, id: int, entry_code: str, entry_type: StockEntryType, 
                 quantity: int, product_id: int):
        super().__init__(id)
        self.entry_code = entry_code
        self.type = entry_type
        self.quantity = quantity
        self.product_id = product_id # Foreign Key tới Product
        self.entry_date = datetime.now()

class InventorySnapshot(BaseEntity):
    """Lưu trữ trạng thái kho tại một thời điểm (dùng cho báo cáo)"""
    def __init__(self, id: int, total_products: int, total_stock_value: float):
        super().__init__(id)
        self.snapshot_date = datetime.now()
        self.total_products = total_products
        self.total_stock_value = total_stock_value