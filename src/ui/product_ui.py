"""
Product management UI
Handles all product-related user interactions
"""
from ..dao.product_dao import ProductDAO
from ..models.product import Product


class ProductUI:
    """Product management user interface"""
    
    def __init__(self):
        self.product_dao = ProductDAO()
    
    def show_menu(self):
        """Display product management menu"""
        while True:
            print("\n" + "="*60)
            print("QUẢN LÝ SẢN PHẨM")
            print("="*60)
            print("1. Thêm mới sản phẩm")
            print("2. Duyệt danh sách sản phẩm")
            print("3. Tìm kiếm sản phẩm")
            print("4. Cập nhật sản phẩm")
            print("5. Xóa sản phẩm")
            print("6. Xóa tất cả sản phẩm")
            print("7. Sắp xếp sản phẩm")
            print("0. Quay lại")
            print("="*60)
            
            choice = input("Chọn chức năng: ").strip()
            
            if choice == '1':
                self.add_product()
            elif choice == '2':
                self.browse_products()
            elif choice == '3':
                self.search_products()
            elif choice == '4':
                self.update_product()
            elif choice == '5':
                self.delete_product()
            elif choice == '6':
                self.delete_all_products()
            elif choice == '7':
                self.sort_products()
            elif choice == '0':
                break
            else:
                print("❌ Lựa chọn không hợp lệ!")
    
    def add_product(self):
        """Add new product"""
        print("\n--- THÊM MỚI SẢN PHẨM ---")
        
        code = input("Mã sản phẩm: ").strip()
        if self.product_dao.find_by_code(code):
            print("❌ Mã sản phẩm đã tồn tại!")
            return
        
        name = input("Tên sản phẩm: ").strip()
        category = input("Danh mục: ").strip()
        
        try:
            price = float(input("Giá: ").strip())
            stock = int(input("Số lượng: ").strip())
        except ValueError:
            print("❌ Giá hoặc số lượng không hợp lệ!")
            return
        
        unit = input("Đơn vị: ").strip()
        supplier = input("Nhà cung cấp: ").strip()
        
        product = Product(
            product_code=code,
            product_name=name,
            category=category,
            price=price,
            stock_quantity=stock,
            unit=unit,
            supplier=supplier
        )
        
        if self.product_dao.create(product):
            print("✓ Thêm sản phẩm thành công!")
        else:
            print("❌ Không thể thêm sản phẩm!")
    
    def browse_products(self):
        """Browse all products"""
        print("\n--- DANH SÁCH SẢN PHẨM ---")
        products = self.product_dao.find_all()
        
        if not products:
            print("Không có sản phẩm nào.")
            return
        
        for i, product in enumerate(products, 1):
            print(f"{i}. {product.get_display_info()}")
    
    def search_products(self):
        """Search products submenu"""
        print("\n--- TÌM KIẾM SẢN PHẨM ---")
        print("1. Tìm theo mã")
        print("2. Tìm theo tên")
        print("3. Tìm theo danh mục")
        
        choice = input("Chọn: ").strip()
        
        if choice == '1':
            code = input("Nhập mã sản phẩm: ").strip()
            product = self.product_dao.find_by_code(code)
            if product:
                print(f"\n✓ {product.get_display_info()}")
            else:
                print("❌ Không tìm thấy sản phẩm!")
        
        elif choice == '2':
            name = input("Nhập tên sản phẩm: ").strip()
            products = self.product_dao.find_by_name(name)
            if products:
                for i, p in enumerate(products, 1):
                    print(f"{i}. {p.get_display_info()}")
            else:
                print("❌ Không tìm thấy sản phẩm!")
        
        elif choice == '3':
            category = input("Nhập danh mục: ").strip()
            products = self.product_dao.find_by_category(category)
            if products:
                for i, p in enumerate(products, 1):
                    print(f"{i}. {p.get_display_info()}")
            else:
                print("❌ Không tìm thấy sản phẩm!")
    
    def update_product(self):
        """Update product"""
        print("\n--- CẬP NHẬT SẢN PHẨM ---")
        code = input("Nhập mã sản phẩm cần cập nhật: ").strip()
        product = self.product_dao.find_by_code(code)
        
        if not product:
            print("❌ Không tìm thấy sản phẩm!")
            return
        
        print(f"\nThông tin hiện tại: {product.get_display_info()}")
        print("\nNhập thông tin mới (Enter để giữ nguyên):")
        
        name = input(f"Tên [{product.product_name}]: ").strip()
        if name:
            product.product_name = name
        
        category = input(f"Danh mục [{product.category}]: ").strip()
        if category:
            product.category = category
        
        price_str = input(f"Giá [{product.price}]: ").strip()
        if price_str:
            try:
                product.price = float(price_str)
            except ValueError:
                print("❌ Giá không hợp lệ, giữ nguyên!")
        
        stock_str = input(f"Số lượng [{product.stock_quantity}]: ").strip()
        if stock_str:
            try:
                product.stock_quantity = int(stock_str)
            except ValueError:
                print("❌ Số lượng không hợp lệ, giữ nguyên!")
        
        unit = input(f"Đơn vị [{product.unit}]: ").strip()
        if unit:
            product.unit = unit
        
        supplier = input(f"Nhà cung cấp [{product.supplier}]: ").strip()
        if supplier:
            product.supplier = supplier
        
        if self.product_dao.update(product):
            print("✓ Cập nhật sản phẩm thành công!")
        else:
            print("❌ Không thể cập nhật sản phẩm!")
    
    def delete_product(self):
        """Delete a product"""
        print("\n--- XÓA SẢN PHẨM ---")
        code = input("Nhập mã sản phẩm cần xóa: ").strip()
        product = self.product_dao.find_by_code(code)
        
        if not product:
            print("❌ Không tìm thấy sản phẩm!")
            return
        
        confirm = input(f"Bạn có chắc muốn xóa '{product.product_name}'? (y/n): ").strip().lower()
        if confirm == 'y':
            if self.product_dao.delete(product.id):
                print("✓ Xóa sản phẩm thành công!")
            else:
                print("❌ Không thể xóa sản phẩm!")
    
    def delete_all_products(self):
        """Delete all products"""
        print("\n--- XÓA TẤT CẢ SẢN PHẨM ---")
        confirm = input("Bạn có chắc muốn xóa TẤT CẢ sản phẩm? (y/n): ").strip().lower()
        if confirm == 'y':
            if self.product_dao.delete_all():
                print("✓ Xóa tất cả sản phẩm thành công!")
            else:
                print("❌ Không thể xóa sản phẩm!")
    
    def sort_products(self):
        """Sort products submenu"""
        print("\n--- SẮP XẾP SẢN PHẨM ---")
        print("1. Sắp xếp theo giá (tăng dần)")
        print("2. Sắp xếp theo giá (giảm dần)")
        print("3. Sắp xếp theo tên (A-Z)")
        print("4. Sắp xếp theo tên (Z-A)")
        
        choice = input("Chọn: ").strip()
        products = []
        
        if choice == '1':
            products = self.product_dao.sort_by_price(ascending=True)
        elif choice == '2':
            products = self.product_dao.sort_by_price(ascending=False)
        elif choice == '3':
            products = self.product_dao.sort_by_name(ascending=True)
        elif choice == '4':
            products = self.product_dao.sort_by_name(ascending=False)
        else:
            print("❌ Lựa chọn không hợp lệ!")
            return
        
        if products:
            print("\n--- KẾT QUẢ SẮP XẾP ---")
            for i, p in enumerate(products, 1):
                print(f"{i}. {p.get_display_info()}")
        else:
            print("Không có sản phẩm nào.")
