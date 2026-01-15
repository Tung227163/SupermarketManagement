# entities/products.py
from datetime import datetime, date
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
        return f"{self.name} (Total: {self.stock_qty})"

class ProductBatch(BaseEntity):
    """Class quản lý lô hàng"""
    def __init__(self, id: int, product_id: int, batch_name: str, quantity: int, expiry_date: date):
        super().__init__(id)
        self.product_id = product_id
        self.batch_name = batch_name
        self.quantity = quantity
        self.expiry_date = expiry_date

class StockEntryType(Enum):
    IMPORT = "Import"
    EXPORT = "Export" # Xuất hủy
    ADJUST = "Adjust" # Kiểm kê điều chỉnh

class StockEntry(BaseEntity):
    def __init__(self, id: int, entry_code: str, entry_type: StockEntryType, 
                 quantity: int, product_id: int, expiry_date: date = None):
        super().__init__(id)
        self.entry_code = entry_code
        self.type = entry_type
        self.quantity = quantity
        self.product_id = product_id
        self.expiry_date = expiry_date
        self.entry_date = datetime.now()