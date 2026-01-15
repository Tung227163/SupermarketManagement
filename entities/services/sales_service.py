from repositories.product_repository import ProductRepository
from repositories.order_repository import InvoiceRepository
from repositories.customer_repository import CustomerRepository
from entities.orders import Invoice, InvoiceItem

class SalesService:
    def __init__(self):
        self.prod_repo = ProductRepository()
        self.inv_repo = InvoiceRepository()
        self.cust_repo = CustomerRepository()

    def create_invoice(self, cashier, customer_id, cart_items, use_points=False):
        """
        Tạo hóa đơn bán hàng.
        :param cashier: Object User (Thu ngân)
        :param customer_id: ID khách hàng (có thể None)
        :param cart_items: List các dict [{'product_id': 1, 'qty': 2}, ...]
        :param use_points: Có dùng điểm tích lũy để giảm giá không?
        """
        # 1. Khởi tạo hóa đơn
        customer = None
        if customer_id:
            customer = self.cust_repo.find_by_id(customer_id)
        
        # Tạo mã hóa đơn tạm (thực tế nên sinh tự động xịn hơn)
        import datetime
        invoice_code = f"INV-{datetime.datetime.now().strftime('%Y%m%d%H%M%S')}"
        invoice = Invoice(None, invoice_code, customer, cashier_id=cashier.id)

        # 2. Duyệt giỏ hàng và kiểm tra tồn kho
        for item in cart_items:
            p_id = item['product_id']
            qty = item['qty']
            
            product = self.prod_repo.find_by_id(p_id)
            if not product:
                raise ValueError(f"Sản phẩm ID {p_id} không tồn tại")
            
            # --- KIỂM TRA TỒN KHO (BLOCK NẾU KHÔNG ĐỦ) ---
            if product.stock_qty < qty:
                raise ValueError(f"❌ Không đủ hàng! '{product.name}' chỉ còn {product.stock_qty}, khách mua {qty}.")
            
            # Trừ kho tạm thời trong object (chưa lưu DB)
            product.stock_qty -= qty
            
            # Thêm vào hóa đơn
            inv_item = InvoiceItem(None, product, qty, product.price)
            invoice.add_item(inv_item)

        # 3. Tính toán tiền và điểm
        final_amount = invoice.total_amount
        
        # Xử lý Tiêu điểm (Nếu khách có thẻ và muốn dùng)
        discount_amount = 0
        points_used = 0
        
        if customer and use_points and customer.point > 0:
            # Quy đổi: 1 điểm = 1000 VNĐ
            max_discount = customer.point * 1000
            
            if max_discount >= final_amount:
                # Điểm dư sức trả hết hóa đơn
                points_used = int(final_amount / 1000)
                discount_amount = points_used * 1000
                final_amount = 0
            else:
                # Dùng hết sạch điểm để giảm giá một phần
                points_used = customer.point
                discount_amount = max_discount
                final_amount -= discount_amount
            
            # Trừ điểm khách hàng
            customer.point -= points_used
            print(f"   -> Khách dùng {points_used} điểm để giảm {discount_amount} VNĐ")

        # Cập nhật tổng tiền cuối cùng vào hóa đơn
        invoice.total_amount = final_amount

        # Xử lý Tích điểm (Cộng điểm mới dựa trên số tiền thực trả)
        if customer and final_amount > 0:
            # 100k = 1 điểm
            points_earned = int(final_amount / 100000)
            customer.point += points_earned
            print(f"   -> Khách được cộng thêm {points_earned} điểm.")

        # 4. LƯU TẤT CẢ XUỐNG DB (Transaction an toàn)
        try:
            # Lưu hóa đơn
            self.inv_repo.save(invoice)
            
            # Cập nhật lại kho cho từng sản phẩm
            for item in invoice.items:
                self.prod_repo.save(item.product) # Lưu số lượng tồn kho mới
            
            # Cập nhật điểm khách hàng
            if customer:
                self.cust_repo.save(customer)
                
            print(f"✅ Bán hàng thành công! Mã: {invoice.invoice_code}. Tổng tiền: {invoice.total_amount}")
            return invoice
            
        except Exception as e:
            print(f"❌ Lỗi khi lưu hóa đơn: {e}")
            raise e