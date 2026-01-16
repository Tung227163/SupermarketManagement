from services.sales_service import SalesService
from services.customer_service import CustomerService

class SalesController:
    def __init__(self, view, cashier_user):
        """
        view: MockSalesView (hoặc GUI thật sau này)
        cashier_user: Object User đang đăng nhập
        """
        self.view = view
        self.cashier = cashier_user
        
        self.sales_service = SalesService()
        self.cust_service = CustomerService()
        
        # Dữ liệu tạm trong phiên bán hàng
        self.current_cart = []    # List các món hàng
        self.current_customer = None # Object Customer (nếu khách có thành viên)

    def handle_search_customer(self):
        """
        Bước 1: Nhập SĐT -> Tìm khách -> Hiện tên & Điểm
        """
        phone = self.view.get_customer_phone()
        if not phone:
            return # Không nhập gì thì thôi

        customer = self.cust_service.find_customer_by_phone(phone)
        
        if customer:
            self.current_customer = customer
            # Cập nhật lên UI: Tên và Điểm
            self.view.update_customer_info(customer.name, customer.point)
            self.view.show_success(f"Đã chọn khách: {customer.name}")
        else:
            self.current_customer = None
            self.view.show_error("Khách hàng không tồn tại (Có thể cần tạo mới).")

    def handle_scan_product(self):
        """
        Bước 2: Nhập mã SP -> Thêm vào giỏ
        """
        code = self.view.get_product_code()
        qty = self.view.get_quantity()

        if not code:
            self.view.show_error("Vui lòng nhập mã sản phẩm")
            return

        # Gọi Service lấy thông tin giá (Giả sử service có hàm này)
        # Lưu ý: Cần đảm bảo SalesService hoặc ProductRepo có hàm tìm theo code
        product_info = self.sales_service.get_product_price(code) 
        
        if not product_info:
            self.view.show_error(f"Không tìm thấy mã {code}")
            return

        # Tính thành tiền
        price = float(product_info['price'])
        total_line = price * qty
        
        # Thêm vào giỏ hàng (Logic cộng dồn nếu trùng mã)
        found = False
        for item in self.current_cart:
            if item['code'] == code:
                item['qty'] += qty
                item['total'] = item['qty'] * item['price']
                found = True
                break
        
        if not found:
            new_item = {
                'product_id': product_info['id'],
                'code': product_info['product_code'],
                'name': product_info['name'],
                'price': price,
                'qty': qty,
                'total': total_line
            }
            self.current_cart.append(new_item)

        # Cập nhật UI
        self.view.update_cart_table(self.current_cart)
        self.view.clear_product_input()
        
        # Tính lại tổng tiền ngay
        self.calculate_totals()

    def calculate_totals(self):
        """
        Bước 3: Tính toán tổng tiền, trừ điểm (nếu có)
        """
        total_money = sum(item['total'] for item in self.current_cart)
        
        discount = 0
        use_points = self.view.get_use_points_status() # Kiểm tra checkbox
        
        # Logic tính giảm giá từ điểm
        if self.current_customer and use_points:
            # 1 điểm = 1000 VNĐ (Ví dụ)
            max_discount_by_points = self.current_customer.point * 1000
            
            # Không được giảm quá tổng tiền
            discount = min(total_money, max_discount_by_points)
        
        final_money = total_money - discount
        
        # Cập nhật UI
        self.view.update_total_label(total_money, discount, final_money)
        return final_money

    def handle_checkout(self):
        """
        Bước 4: Thanh toán & Lưu xuống DB & IN HÓA ĐƠN
        """
        if not self.current_cart:
            self.view.show_error("Giỏ hàng đang trống!")
            return

        try:
            # 1. Tính toán lại số liệu để in hóa đơn (trước khi gọi service)
            total_money = sum(item['total'] for item in self.current_cart)
            discount = 0
            use_points = self.view.get_use_points_status()
            
            if self.current_customer and use_points:
                max_discount = self.current_customer.point * 1000
                discount = min(total_money, max_discount)

            # 2. Chuẩn bị dữ liệu cho Service
            cart_data_for_service = [
                {'product_id': item['product_id'], 'qty': item['qty']} 
                for item in self.current_cart
            ]

            # 3. GỌI SERVICE (Lưu DB)
            invoice = self.sales_service.create_invoice(
                cashier=self.cashier,
                customer_id=self.current_customer.id if self.current_customer else None,
                cart_items=cart_data_for_service,
                use_points=use_points
            )
            
            self.view.show_success(f"Giao dịch thành công! Đang in hóa đơn...")

            # 4. IN HÓA ĐƠN (Gọi hàm mới thêm bên View)
            cust_name = self.current_customer.name if self.current_customer else "Khách lẻ"
            self.view.show_receipt(invoice, self.current_cart, discount, cust_name)
            
            # 5. DỌN DẸP (Reset để bán đơn mới)
            self.current_cart = []
            self.current_customer = None
            self.view.update_cart_table([])
            self.view.update_total_label(0, 0, 0)
            
        except ValueError as ve:
            self.view.show_error(f"Lỗi bán hàng: {ve}")
        except Exception as e:
            self.view.show_error(f"Lỗi hệ thống: {e}")
            import traceback
            traceback.print_exc()