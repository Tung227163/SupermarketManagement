"""
Demo script - Demonstrates the supermarket management system
"""
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from src.utils.database import DatabaseUtil
from src.dao.product_dao import ProductDAO
from src.dao.employee_dao import EmployeeDAO
from src.services.auth_service import AuthService
from src.services.report_service import ReportService


def demo_oop_concepts():
    """Demonstrate OOP concepts used in the project"""
    
    print("="*60)
    print("DEMO: OOP CONCEPTS IN SUPERMARKET MANAGEMENT SYSTEM")
    print("="*60)
    
    # Initialize database
    DatabaseUtil.initialize_database()
    
    # 1. Abstract Class & Inheritance
    print("\n1. ABSTRACT CLASS & INHERITANCE")
    print("-" * 40)
    product_dao = ProductDAO()
    products = product_dao.find_all()
    if products:
        product = products[0]
        print(f"Product object (inherits from BaseEntity):")
        print(f"  - {product.get_display_info()}")
        print(f"  - Code: {product.get_code()}")
    
    # 2. Polymorphism
    print("\n2. POLYMORPHISM")
    print("-" * 40)
    employee_dao = EmployeeDAO()
    employees = employee_dao.find_all()
    if employees:
        employee = employees[0]
        print(f"Employee object (same methods, different implementation):")
        print(f"  - {employee.get_display_info()}")
        print(f"  - Code: {employee.get_code()}")
    
    # 3. Encapsulation
    print("\n3. ENCAPSULATION")
    print("-" * 40)
    if products:
        product = products[0]
        print(f"Using properties (getters/setters):")
        print(f"  - Original price: {product.price}")
        product.price = 30000
        print(f"  - New price: {product.price}")
    
    # 4. Object as Parameter/Return Type
    print("\n4. OBJECT AS PARAMETER & RETURN TYPE")
    print("-" * 40)
    auth_service = AuthService()
    user = auth_service.login("admin", "admin123")
    if user:
        print(f"Login returns User object:")
        print(f"  - {user.get_display_info()}")
    
    # 5. Service Layer with Objects
    print("\n5. SERVICE LAYER WORKING WITH OBJECTS")
    print("-" * 40)
    report_service = ReportService()
    total_value = report_service.calculate_total_inventory_value()
    print(f"Total inventory value: {total_value:,.0f} VNĐ")
    
    low_stock = report_service.generate_low_stock_report(60)
    print(f"Low stock products (< 60): {len(low_stock)}")
    
    # 6. Constructor
    print("\n6. CONSTRUCTOR")
    print("-" * 40)
    print("All classes use __init__ constructor:")
    print("  - ProductDAO(), EmployeeDAO(), AuthService()")
    print("  - Models: Product(...), Employee(...), User(...)")
    
    print("\n" + "="*60)
    print("Demo completed successfully!")
    print("="*60)
    
    # Cleanup
    DatabaseUtil.close_connection()


if __name__ == "__main__":
    demo_oop_concepts()
