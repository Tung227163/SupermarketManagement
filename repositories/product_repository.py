from repositories.base_repository import BaseRepository
from entities.products import Product, StockEntry, ProductBatch

class ProductRepository(BaseRepository):
    
    def _map_row_to_product(self, row):
        if not row: return None
        return Product(row['id'], row['product_code'], row['name'], float(row['price']), row['stock_qty'])

    def find_all(self):
        self.cursor.execute("SELECT * FROM products")
        return [self._map_row_to_product(row) for row in self.cursor.fetchall()]

    def find_by_id(self, id):
        self.cursor.execute("SELECT * FROM products WHERE id = %s", (id,))
        return self._map_row_to_product(self.cursor.fetchone())

    def save(self, product: Product):
        if product.id is None:
            query = "INSERT INTO products (product_code, name, price, stock_qty) VALUES (%s, %s, %s, %s)"
            val = (product.product_code, product.name, product.price, product.stock_qty)
            self.cursor.execute(query, val)
            self.conn.commit()
            product.id = self.cursor.lastrowid
        else:
            query = "UPDATE products SET name=%s, price=%s, stock_qty=%s WHERE id=%s"
            val = (product.name, product.price, product.stock_qty, product.id)
            self.cursor.execute(query, val)
            self.conn.commit()
        return product

    # --- BỔ SUNG HÀM DELETE (BẮT BUỘC DO KẾ THỪA BASEREPOSITORY) ---
    def delete(self, id):
        """Xóa sản phẩm (Chỉ xóa được nếu chưa có ràng buộc khóa ngoại)"""
        try:
            self.cursor.execute("DELETE FROM products WHERE id = %s", (id,))
            self.conn.commit()
            return True
        except Exception as e:
            print(f"Error deleting product: {e}")
            return False

    # --- CÁC HÀM XỬ LÝ LÔ HÀNG (BATCH) & STOCK ---
    def save_batch(self, batch: ProductBatch):
        if batch.id is None:
            query = """INSERT INTO product_batches (product_id, batch_name, quantity, expiry_date) 
                       VALUES (%s, %s, %s, %s)"""
            val = (batch.product_id, batch.batch_name, batch.quantity, batch.expiry_date)
            self.cursor.execute(query, val)
            self.conn.commit()
            batch.id = self.cursor.lastrowid
        else:
            query = "UPDATE product_batches SET quantity=%s WHERE id=%s"
            self.cursor.execute(query, (batch.quantity, batch.id))
            self.conn.commit()
        return batch

    def find_batches_by_product_id_sorted(self, product_id):
        query = """SELECT * FROM product_batches 
                   WHERE product_id = %s AND quantity > 0 
                   ORDER BY expiry_date ASC"""
        self.cursor.execute(query, (product_id,))
        rows = self.cursor.fetchall()
        batches = []
        for r in rows:
            batches.append(ProductBatch(r['id'], r['product_id'], r['batch_name'], r['quantity'], r['expiry_date']))
        return batches

    def save_stock_entry(self, entry: StockEntry):
        query = """INSERT INTO stock_entries (entry_code, entry_type, quantity, product_id, expiry_date)
                   VALUES (%s, %s, %s, %s, %s)"""
        val = (entry.entry_code, entry.type.value, entry.quantity, entry.product_id, entry.expiry_date)
        self.cursor.execute(query, val)
        self.conn.commit()
        entry.id = self.cursor.lastrowid
        return entry