# entities/orders.py
from datetime import datetime
from typing import List
from entities.base import BaseEntity
from entities.products import Product

class Customer(BaseEntity):
    def __init__(self, id: int, customer_code: str, name: str, phone: str, point: int = 0):
        super().__init__(id)
        self.customer_code = customer_code
        self.name = name
        self.phone = phone
        self.point = point

    def accumulate_point(self, amount: float):
        # Giả sử 100k = 1 điểm
        points_earned = int(amount / 100000)
        self.point += points_earned
        return self.point

class InvoiceItem(BaseEntity):
    def __init__(self, id: int, product: Product, quantity: int, price: float):
        super().__init__(id)
        self.product = product
        self.quantity = quantity
        self.price = price # Giá tại thời điểm bán (có thể khác giá product hiện tại)

    def calculate_sub_total(self) -> float:
        return self.quantity * self.price

class Invoice(BaseEntity):
    def __init__(self, id: int, invoice_code: str, customer: Customer = None, cashier_id: int = None):
        super().__init__(id)
        self.invoice_code = invoice_code
        self.invoice_date = datetime.now()
        self.customer = customer
        self.cashier_id = cashier_id
        self.items: List[InvoiceItem] = [] # Composition: Invoice chứa nhiều InvoiceItem
        self.total_amount = 0.0

    def add_item(self, item: InvoiceItem):
        self.items.append(item)
        self.calculate_total()

    def calculate_total(self):
        self.total_amount = sum(item.calculate_sub_total() for item in self.items)
        return self.total_amount