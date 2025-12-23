"""
Product model
Demonstrates: Inheritance from BaseEntity
"""
from .base_entity import BaseEntity


class Product(BaseEntity):
    """Product entity"""
    
    def __init__(self, product_id=None, product_code=None, product_name=None, 
                 category=None, price=0.0, stock_quantity=0, unit=None, supplier=None):
        super().__init__(product_id)
        self._product_code = product_code
        self._product_name = product_name
        self._category = category
        self._price = price
        self._stock_quantity = stock_quantity
        self._unit = unit
        self._supplier = supplier
    
    def get_display_info(self):
        """Implementation of abstract method"""
        return (f"Code: {self._product_code} | Name: {self._product_name} | "
                f"Category: {self._category} | Price: {self._price:,.0f} | "
                f"Stock: {self._stock_quantity} {self._unit}")
    
    def get_code(self):
        """Implementation of abstract method"""
        return self._product_code
    
    # Getters and setters
    @property
    def product_code(self):
        return self._product_code
    
    @product_code.setter
    def product_code(self, value):
        self._product_code = value
    
    @property
    def product_name(self):
        return self._product_name
    
    @product_name.setter
    def product_name(self, value):
        self._product_name = value
    
    @property
    def category(self):
        return self._category
    
    @category.setter
    def category(self, value):
        self._category = value
    
    @property
    def price(self):
        return self._price
    
    @price.setter
    def price(self, value):
        self._price = value
    
    @property
    def stock_quantity(self):
        return self._stock_quantity
    
    @stock_quantity.setter
    def stock_quantity(self, value):
        self._stock_quantity = value
    
    @property
    def unit(self):
        return self._unit
    
    @unit.setter
    def unit(self, value):
        self._unit = value
    
    @property
    def supplier(self):
        return self._supplier
    
    @supplier.setter
    def supplier(self, value):
        self._supplier = value
