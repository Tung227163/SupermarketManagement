"""
Report service for generating various reports
"""
from typing import List, Dict
from ..dao.product_dao import ProductDAO
from ..dao.employee_dao import EmployeeDAO
from ..models.product import Product
from ..models.employee import Employee


class ReportService:
    """Report service for generating various reports"""
    
    def __init__(self):
        self.product_dao = ProductDAO()
        self.employee_dao = EmployeeDAO()
    
    def generate_inventory_report(self) -> List[Product]:
        """Generate full inventory report"""
        return self.product_dao.find_all()
    
    def generate_low_stock_report(self, threshold: int = 50) -> List[Product]:
        """Generate low stock report"""
        all_products = self.product_dao.find_all()
        return [p for p in all_products if p.stock_quantity < threshold]
    
    def generate_employee_report(self) -> List[Employee]:
        """Generate employee list report"""
        return self.employee_dao.find_all()
    
    def generate_employee_by_position_report(self) -> Dict[str, List[Employee]]:
        """Generate employee report grouped by position"""
        all_employees = self.employee_dao.find_all()
        report = {}
        
        for employee in all_employees:
            position = employee.position
            if position not in report:
                report[position] = []
            report[position].append(employee)
        
        return report
    
    def generate_product_by_category_report(self) -> Dict[str, List[Product]]:
        """Generate product report grouped by category"""
        all_products = self.product_dao.find_all()
        report = {}
        
        for product in all_products:
            category = product.category
            if category not in report:
                report[category] = []
            report[category].append(product)
        
        return report
    
    def calculate_total_inventory_value(self) -> float:
        """Calculate total inventory value"""
        all_products = self.product_dao.find_all()
        total = sum(p.price * p.stock_quantity for p in all_products)
        return total
