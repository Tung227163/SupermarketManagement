"""
Employee management UI
Handles all employee-related user interactions
"""
from ..dao.employee_dao import EmployeeDAO
from ..models.employee import Employee


class EmployeeUI:
    """Employee management user interface"""
    
    def __init__(self):
        self.employee_dao = EmployeeDAO()
    
    def show_menu(self):
        """Display employee management menu"""
        while True:
            print("\n" + "="*60)
            print("QUẢN LÝ NHÂN VIÊN")
            print("="*60)
            print("1. Thêm mới nhân viên")
            print("2. Duyệt danh sách nhân viên")
            print("3. Tìm kiếm nhân viên")
            print("4. Cập nhật nhân viên")
            print("5. Xóa nhân viên")
            print("6. Xóa tất cả nhân viên")
            print("7. Sắp xếp nhân viên")
            print("0. Quay lại")
            print("="*60)
            
            choice = input("Chọn chức năng: ").strip()
            
            if choice == '1':
                self.add_employee()
            elif choice == '2':
                self.browse_employees()
            elif choice == '3':
                self.search_employees()
            elif choice == '4':
                self.update_employee()
            elif choice == '5':
                self.delete_employee()
            elif choice == '6':
                self.delete_all_employees()
            elif choice == '7':
                self.sort_employees()
            elif choice == '0':
                break
            else:
                print("❌ Lựa chọn không hợp lệ!")
    
    def add_employee(self):
        """Add new employee"""
        print("\n--- THÊM MỚI NHÂN VIÊN ---")
        
        code = input("Mã nhân viên: ").strip()
        if self.employee_dao.find_by_code(code):
            print("❌ Mã nhân viên đã tồn tại!")
            return
        
        name = input("Họ tên: ").strip()
        phone = input("Số điện thoại: ").strip()
        email = input("Email: ").strip()
        position = input("Chức vụ: ").strip()
        
        try:
            salary = float(input("Lương: ").strip())
        except ValueError:
            print("❌ Lương không hợp lệ!")
            return
        
        hire_date = input("Ngày vào làm (YYYY-MM-DD): ").strip()
        
        employee = Employee(
            employee_code=code,
            full_name=name,
            phone=phone,
            email=email,
            position=position,
            salary=salary,
            hire_date=hire_date
        )
        
        if self.employee_dao.create(employee):
            print("✓ Thêm nhân viên thành công!")
        else:
            print("❌ Không thể thêm nhân viên!")
    
    def browse_employees(self):
        """Browse all employees"""
        print("\n--- DANH SÁCH NHÂN VIÊN ---")
        employees = self.employee_dao.find_all()
        
        if not employees:
            print("Không có nhân viên nào.")
            return
        
        for i, employee in enumerate(employees, 1):
            print(f"{i}. {employee.get_display_info()}")
    
    def search_employees(self):
        """Search employees submenu"""
        print("\n--- TÌM KIẾM NHÂN VIÊN ---")
        print("1. Tìm theo mã")
        print("2. Tìm theo tên")
        print("3. Tìm theo chức vụ")
        
        choice = input("Chọn: ").strip()
        
        if choice == '1':
            code = input("Nhập mã nhân viên: ").strip()
            employee = self.employee_dao.find_by_code(code)
            if employee:
                print(f"\n✓ {employee.get_display_info()}")
            else:
                print("❌ Không tìm thấy nhân viên!")
        
        elif choice == '2':
            name = input("Nhập tên nhân viên: ").strip()
            employees = self.employee_dao.find_by_name(name)
            if employees:
                for i, e in enumerate(employees, 1):
                    print(f"{i}. {e.get_display_info()}")
            else:
                print("❌ Không tìm thấy nhân viên!")
        
        elif choice == '3':
            position = input("Nhập chức vụ: ").strip()
            employees = self.employee_dao.find_by_position(position)
            if employees:
                for i, e in enumerate(employees, 1):
                    print(f"{i}. {e.get_display_info()}")
            else:
                print("❌ Không tìm thấy nhân viên!")
    
    def update_employee(self):
        """Update employee"""
        print("\n--- CẬP NHẬT NHÂN VIÊN ---")
        code = input("Nhập mã nhân viên cần cập nhật: ").strip()
        employee = self.employee_dao.find_by_code(code)
        
        if not employee:
            print("❌ Không tìm thấy nhân viên!")
            return
        
        print(f"\nThông tin hiện tại: {employee.get_display_info()}")
        print("\nNhập thông tin mới (Enter để giữ nguyên):")
        
        name = input(f"Họ tên [{employee.full_name}]: ").strip()
        if name:
            employee.full_name = name
        
        phone = input(f"Số điện thoại [{employee.phone}]: ").strip()
        if phone:
            employee.phone = phone
        
        email = input(f"Email [{employee.email}]: ").strip()
        if email:
            employee.email = email
        
        position = input(f"Chức vụ [{employee.position}]: ").strip()
        if position:
            employee.position = position
        
        salary_str = input(f"Lương [{employee.salary}]: ").strip()
        if salary_str:
            try:
                employee.salary = float(salary_str)
            except ValueError:
                print("❌ Lương không hợp lệ, giữ nguyên!")
        
        if self.employee_dao.update(employee):
            print("✓ Cập nhật nhân viên thành công!")
        else:
            print("❌ Không thể cập nhật nhân viên!")
    
    def delete_employee(self):
        """Delete an employee"""
        print("\n--- XÓA NHÂN VIÊN ---")
        code = input("Nhập mã nhân viên cần xóa: ").strip()
        employee = self.employee_dao.find_by_code(code)
        
        if not employee:
            print("❌ Không tìm thấy nhân viên!")
            return
        
        confirm = input(f"Bạn có chắc muốn xóa '{employee.full_name}'? (y/n): ").strip().lower()
        if confirm == 'y':
            if self.employee_dao.delete(employee.id):
                print("✓ Xóa nhân viên thành công!")
            else:
                print("❌ Không thể xóa nhân viên!")
    
    def delete_all_employees(self):
        """Delete all employees"""
        print("\n--- XÓA TẤT CẢ NHÂN VIÊN ---")
        confirm = input("Bạn có chắc muốn xóa TẤT CẢ nhân viên? (y/n): ").strip().lower()
        if confirm == 'y':
            if self.employee_dao.delete_all():
                print("✓ Xóa tất cả nhân viên thành công!")
            else:
                print("❌ Không thể xóa nhân viên!")
    
    def sort_employees(self):
        """Sort employees submenu"""
        print("\n--- SẮP XẾP NHÂN VIÊN ---")
        print("1. Sắp xếp theo lương (tăng dần)")
        print("2. Sắp xếp theo lương (giảm dần)")
        
        choice = input("Chọn: ").strip()
        employees = []
        
        if choice == '1':
            employees = self.employee_dao.sort_by_salary(ascending=True)
        elif choice == '2':
            employees = self.employee_dao.sort_by_salary(ascending=False)
        else:
            print("❌ Lựa chọn không hợp lệ!")
            return
        
        if employees:
            print("\n--- KẾT QUẢ SẮP XẾP ---")
            for i, e in enumerate(employees, 1):
                print(f"{i}. {e.get_display_info()}")
        else:
            print("Không có nhân viên nào.")
