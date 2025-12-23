"""
Main application entry point
Supermarket Management System

Demonstrates:
- OOP concepts: classes, objects, inheritance, polymorphism, abstract classes
- Menu-driven interface with submenus
- User authentication
- Database persistence with SQL
- Service layer architecture
"""
import sys
import os

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from src.utils.database import DatabaseUtil
from src.services.auth_service import AuthService
from src.ui.product_ui import ProductUI
from src.ui.employee_ui import EmployeeUI
from src.ui.report_ui import ReportUI


class SupermarketApp:
    """
    Main application class
    Demonstrates: Class, constructor, methods
    """
    
    def __init__(self):
        """Constructor - demonstrates constructor concept"""
        self.auth_service = AuthService()
        self.product_ui = ProductUI()
        self.employee_ui = EmployeeUI()
        self.report_ui = ReportUI()
    
    def run(self):
        """
        Main application loop
        Runs until user chooses to exit
        """
        print("\n" + "="*60)
        print("HỆ THỐNG QUẢN LÝ SIÊU THỊ")
        print("="*60)
        
        # Initialize database
        DatabaseUtil.initialize_database()
        
        # User login required
        if not self.login():
            print("❌ Đăng nhập thất bại!")
            return
        
        # Main menu loop - runs until user exits
        while True:
            if not self.show_main_menu():
                break
        
        # Cleanup
        DatabaseUtil.close_connection()
        print("\n✓ Đã thoát chương trình. Tạm biệt!")
    
    def login(self):
        """
        User authentication
        Demonstrates: object as return type
        """
        print("\n--- ĐĂNG NHẬP ---")
        max_attempts = 3
        attempts = 0
        
        while attempts < max_attempts:
            username = input("Tên đăng nhập: ").strip()
            password = input("Mật khẩu: ").strip()
            
            # Demonstrates: method returning object
            user = self.auth_service.login(username, password)
            
            if user:
                print(f"\n✓ Xin chào, {user.full_name}!")
                return True
            else:
                attempts += 1
                remaining = max_attempts - attempts
                if remaining > 0:
                    print(f"❌ Sai tên đăng nhập hoặc mật khẩu! Còn {remaining} lần thử.")
                else:
                    print("❌ Đã hết số lần thử!")
        
        return False
    
    def show_main_menu(self):
        """
        Display main menu with submenus
        Demonstrates: menu navigation
        Returns: True to continue, False to exit
        """
        current_user = self.auth_service.get_current_user()
        
        print("\n" + "="*60)
        print(f"MENU CHÍNH - Người dùng: {current_user.full_name}")
        print("="*60)
        print("1. Quản lý sản phẩm")
        print("2. Quản lý nhân viên")
        print("3. Báo cáo")
        print("4. Đăng xuất")
        print("0. Thoát chương trình")
        print("="*60)
        
        choice = input("Chọn chức năng: ").strip()
        
        if choice == '1':
            # Product management submenu
            self.product_ui.show_menu()
        elif choice == '2':
            # Employee management submenu
            self.employee_ui.show_menu()
        elif choice == '3':
            # Reports submenu
            self.report_ui.show_menu()
        elif choice == '4':
            # Logout and require login again
            self.auth_service.logout()
            print("\n✓ Đã đăng xuất!")
            if not self.login():
                return False
        elif choice == '0':
            # Exit program
            confirm = input("Bạn có chắc muốn thoát? (y/n): ").strip().lower()
            if confirm == 'y':
                return False
        else:
            print("❌ Lựa chọn không hợp lệ!")
        
        return True


def main():
    """Application entry point"""
    app = SupermarketApp()
    app.run()


if __name__ == "__main__":
    main()
