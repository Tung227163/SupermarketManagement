"""
Report UI
Handles report generation and display
"""
from ..services.report_service import ReportService


class ReportUI:
    """Report user interface"""
    
    def __init__(self):
        self.report_service = ReportService()
    
    def show_menu(self):
        """Display report menu"""
        while True:
            print("\n" + "="*60)
            print("BÁO CÁO")
            print("="*60)
            print("1. Báo cáo tồn kho")
            print("2. Báo cáo hàng sắp hết")
            print("3. Báo cáo giá trị tồn kho")
            print("4. Báo cáo danh sách nhân viên")
            print("5. Báo cáo nhân viên theo chức vụ")
            print("6. Báo cáo sản phẩm theo danh mục")
            print("0. Quay lại")
            print("="*60)
            
            choice = input("Chọn chức năng: ").strip()
            
            if choice == '1':
                self.inventory_report()
            elif choice == '2':
                self.low_stock_report()
            elif choice == '3':
                self.inventory_value_report()
            elif choice == '4':
                self.employee_report()
            elif choice == '5':
                self.employee_by_position_report()
            elif choice == '6':
                self.product_by_category_report()
            elif choice == '0':
                break
            else:
                print("❌ Lựa chọn không hợp lệ!")
    
    def inventory_report(self):
        """Generate and display inventory report"""
        print("\n" + "="*60)
        print("BÁO CÁO TỒN KHO")
        print("="*60)
        
        products = self.report_service.generate_inventory_report()
        
        if not products:
            print("Không có sản phẩm nào.")
            return
        
        for i, product in enumerate(products, 1):
            print(f"{i}. {product.get_display_info()}")
        
        print(f"\nTổng số sản phẩm: {len(products)}")
    
    def low_stock_report(self):
        """Generate and display low stock report"""
        print("\n" + "="*60)
        print("BÁO CÁO HÀNG SẮP HẾT")
        print("="*60)
        
        try:
            threshold = int(input("Nhập ngưỡng tồn kho (mặc định 50): ").strip() or "50")
        except ValueError:
            threshold = 50
        
        products = self.report_service.generate_low_stock_report(threshold)
        
        if not products:
            print("Không có sản phẩm nào sắp hết.")
            return
        
        for i, product in enumerate(products, 1):
            print(f"{i}. {product.get_display_info()}")
        
        print(f"\n⚠️  Có {len(products)} sản phẩm có số lượng dưới {threshold}")
    
    def inventory_value_report(self):
        """Generate and display inventory value report"""
        print("\n" + "="*60)
        print("BÁO CÁO GIÁ TRỊ TỒN KHO")
        print("="*60)
        
        total_value = self.report_service.calculate_total_inventory_value()
        print(f"\nTổng giá trị tồn kho: {total_value:,.0f} VNĐ")
    
    def employee_report(self):
        """Generate and display employee report"""
        print("\n" + "="*60)
        print("BÁO CÁO DANH SÁCH NHÂN VIÊN")
        print("="*60)
        
        employees = self.report_service.generate_employee_report()
        
        if not employees:
            print("Không có nhân viên nào.")
            return
        
        for i, employee in enumerate(employees, 1):
            print(f"{i}. {employee.get_display_info()}")
        
        print(f"\nTổng số nhân viên: {len(employees)}")
    
    def employee_by_position_report(self):
        """Generate and display employee by position report"""
        print("\n" + "="*60)
        print("BÁO CÁO NHÂN VIÊN THEO CHỨC VỤ")
        print("="*60)
        
        report = self.report_service.generate_employee_by_position_report()
        
        if not report:
            print("Không có nhân viên nào.")
            return
        
        for position, employees in report.items():
            print(f"\n{position}: ({len(employees)} nhân viên)")
            for i, employee in enumerate(employees, 1):
                print(f"  {i}. {employee.get_display_info()}")
    
    def product_by_category_report(self):
        """Generate and display product by category report"""
        print("\n" + "="*60)
        print("BÁO CÁO SẢN PHẨM THEO DANH MỤC")
        print("="*60)
        
        report = self.report_service.generate_product_by_category_report()
        
        if not report:
            print("Không có sản phẩm nào.")
            return
        
        for category, products in report.items():
            print(f"\n{category}: ({len(products)} sản phẩm)")
            for i, product in enumerate(products, 1):
                print(f"  {i}. {product.get_display_info()}")
