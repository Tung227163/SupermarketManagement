from datetime import datetime
from repositories.product_repository import ProductRepository
from repositories.order_repository import InvoiceRepository
from repositories.customer_repository import CustomerRepository
from entities.orders import Invoice, InvoiceItem
from database import db

class SalesService:
    def __init__(self):
        self.prod_repo = ProductRepository()
        self.inv_repo = InvoiceRepository()
        self.cust_repo = CustomerRepository()

    def get_product_price(self, product_code):
        # Hàm tìm nhanh sản phẩm để quét mã vạch
        query = "SELECT * FROM products WHERE product_code = %s"
        db.cursor.execute(query, (product_code,))
        row = db.cursor.fetchone()
        return row # Trả về dict thông tin sản phẩm

    def create_invoice(self, cashier, customer_id, cart_items, use_points=False):
        """Bán hàng: Trừ kho theo lô (FEFO) + Tích điểm"""
        cust = self.cust_repo.find_by_id(customer_id) if customer_id else None
        
        # Tạo mã hóa đơn
        inv_code = f"INV{datetime.now().strftime('%y%m%d%H%M%S')}"
        invoice = Invoice(None, inv_code, cust, cashier_id=cashier.id)
        
        batches_to_update = []
        products_to_update = []
        
        # Duyệt giỏ hàng
        for item in cart_items:
            p_id = item['product_id']
            qty_needed = item['qty']
            
            product = self.prod_repo.find_by_id(p_id)
            if not product: raise ValueError(f"Sản phẩm {p_id} không tồn tại")
            
            # --- LOGIC FEFO ---
            batches = self.prod_repo.find_batches_by_product_id_sorted(p_id)
            total_avail = sum(b.quantity for b in batches)
            if total_avail < qty_needed:
                raise ValueError(f"❌ '{product.name}' chỉ còn {total_avail}, không đủ bán {qty_needed}.")

            qty_remain = qty_needed
            for batch in batches:
                if qty_remain <= 0: break
                take = min(batch.quantity, qty_remain)
                batch.quantity -= take
                qty_remain -= take
                batches_to_update.append(batch)
            
            # Cập nhật tổng tồn kho
            product.stock_qty -= qty_needed
            products_to_update.append(product)
            
            invoice.add_item(InvoiceItem(None, product, qty_needed, product.price))

        # Tính tiền & Điểm
        final_amt = invoice.total_amount
        if cust and use_points and cust.point > 0:
            discount = min(cust.point * 1000, final_amt)
            used_p = int(discount / 1000)
            final_amt -= discount
            cust.point -= used_p
            print(f"   -> Đã dùng {used_p} điểm giảm {discount}đ")

        invoice.total_amount = final_amt
        if cust and final_amt > 0:
            cust.point += int(final_amt / 100000)

        # TRANSACTION
        try:
            saved_inv = self.inv_repo.save(invoice)
            for b in batches_to_update: self.prod_repo.save_batch(b)
            for p in products_to_update: self.prod_repo.save(p)
            if cust: self.cust_repo.save(cust)
            print(f"✅ Hóa đơn {saved_inv.invoice_code} thành công!")
            return saved_inv
        except Exception as e:
            print(f"❌ Lỗi bán hàng: {e}")
            raise e

    def refund_invoice(self, invoice_id):
        """
        Hoàn trả hóa đơn (Refund):
        1. Đổi trạng thái hóa đơn -> Cancelled (cần thêm cột status vào DB hoặc quy ước).
        2. Cộng lại số lượng tồn kho tổng.
        3. (Đơn giản hóa) Cộng lại vào Lô hàng mới nhất hoặc lô mặc định.
        4. Trừ lại điểm đã tích của khách.
        """
        # Lưu ý: Đây là logic phức tạp, ở mức độ đồ án ta sẽ làm đơn giản hóa:
        # Chỉ cộng lại Stock tổng của sản phẩm.
        
        # Lấy thông tin hóa đơn và items
        # (Giả sử repository hỗ trợ lấy full invoice items)
        # Đoạn này cần viết thêm hàm trong Repository để lấy items, ở đây tôi giả lập logic
        
        print("⚠️ Chức năng hoàn trả: Đang xử lý hoàn lại kho tổng...")
        
        query_items = "SELECT * FROM invoice_items WHERE invoice_id = %s"
        db.cursor.execute(query_items, (invoice_id,))
        items = db.cursor.fetchall()
        
        if not items:
            print("❌ Hóa đơn không tồn tại hoặc không có sản phẩm.")
            return

        for item in items:
            p_id = item['product_id']
            qty = item['quantity']
            
            # Cộng lại kho tổng
            product = self.prod_repo.find_by_id(p_id)
            if product:
                product.stock_qty += qty
                self.prod_repo.save(product)
                
                # Update lại lô (Tìm lô nào còn hạn xa nhất để cộng vào - Giả định)
                batches = self.prod_repo.find_batches_by_product_id_sorted(p_id)
                if batches:
                    # Cộng vào lô cuối cùng (lô mới nhất/hạn xa nhất)
                    last_batch = batches[-1]
                    last_batch.quantity += qty
                    self.prod_repo.save_batch(last_batch)
        
        # Cập nhật trạng thái hóa đơn
        sql_update = "UPDATE invoices SET total_amount = 0, invoice_code = CONCAT(invoice_code, '-REFUND') WHERE id = %s"
        db.cursor.execute(sql_update, (invoice_id,))
        db.connection.commit()
        
        print(f"✅ Đã hoàn trả hóa đơn ID {invoice_id}. Kho đã được cập nhật.")