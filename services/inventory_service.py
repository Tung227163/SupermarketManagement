from datetime import datetime, date
from repositories.product_repository import ProductRepository
from entities.products import Product, StockEntry, StockEntryType, ProductBatch

class InventoryService:
    def __init__(self):
        self.prod_repo = ProductRepository()

    def get_all_products(self):
        return self.prod_repo.find_all()
    
    def get_product_batches(self, product_id):
        """Lấy danh sách các lô hàng còn tồn của sản phẩm"""
        # Hàm find_batches_by_product_id_sorted đã được viết trong Repo ở các bước trước
        # Nó trả về list ProductBatch, sắp xếp HSD tăng dần
        return self.prod_repo.find_batches_by_product_id_sorted(product_id)

    def add_new_product(self, code, name, price):
        """Tạo sản phẩm mới (chưa có tồn kho)"""
        # Kiểm tra trùng code... (bỏ qua cho ngắn gọn)
        p = Product(None, code, name, price, 0)
        return self.prod_repo.save(p)
    
    def find_product_by_code(self, product_code):
        """Tìm đối tượng Product dựa vào Mã Code"""
        # Cách đơn giản: Query trực tiếp
        query = "SELECT * FROM products WHERE product_code = %s"
        self.prod_repo.cursor.execute(query, (product_code,))
        row = self.prod_repo.cursor.fetchone()
        if row:
            # Map row sang Object Product (Sử dụng hàm có sẵn trong Repo)
            return self.prod_repo._map_row_to_product(row)
        return None

    def import_goods(self, user, entry_code, product_id, quantity, expiry_date_str):
        """
        Nhập kho (Có kiểm tra phân quyền Backend)
        :param user: Đối tượng User đang thực hiện hành động
        """
        # --- LỚP BẢO MẬT BACKEND (SECURITY LAYER) ---
        if user.role not in ['WarehouseKeeper', 'Manager']:
            raise PermissionError(f"⛔ BẢO MẬT: User '{user.username}' ({user.role}) không có quyền Nhập kho!")
        
        """Nhập kho: Tạo Lô mới + Cộng tổng tồn"""
        if quantity <= 0: raise ValueError("Số lượng phải > 0")
        product = self.prod_repo.find_by_id(product_id)
        if not product: raise ValueError("Sản phẩm không tồn tại")

        try:
            exp_date = datetime.strptime(expiry_date_str, "%Y-%m-%d").date()
        except ValueError:
            raise ValueError("Ngày hết hạn phải định dạng YYYY-MM-DD")

        # 1. Tạo Lô mới
        batch_name = f"Lô {datetime.now().strftime('%d%m%y')}"
        new_batch = ProductBatch(None, product_id, batch_name, quantity, exp_date)
        self.prod_repo.save_batch(new_batch)

        # 2. Cộng tổng tồn kho
        product.stock_qty += quantity
        self.prod_repo.save(product)

        # 3. Ghi log
        entry = StockEntry(None, entry_code, StockEntryType.IMPORT, quantity, product_id, exp_date)
        self.prod_repo.save_stock_entry(entry)
        
        print(f"✅ [LOGIC]: Đã nhập {quantity} {product.name} (User: {user.username})")

    def check_low_stock(self, threshold=10):
        """Cảnh báo hàng sắp hết (theo tổng số lượng)"""
        all_prods = self.prod_repo.find_all()
        return [p for p in all_prods if p.stock_qty < threshold]

    def check_expiring_products(self, days=30):
        """Cảnh báo lô hàng sắp hết hạn trong X ngày tới"""
        query = """
            SELECT p.name, b.batch_name, b.quantity, b.expiry_date 
            FROM product_batches b
            JOIN products p ON b.product_id = p.id
            WHERE b.quantity > 0 
            AND b.expiry_date <= DATE_ADD(CURDATE(), INTERVAL %s DAY)
            ORDER BY b.expiry_date ASC
        """
        self.prod_repo.cursor.execute(query, (days,))
        return self.prod_repo.cursor.fetchall()