# repositories/product_repository.py
from repositories.base_repository import BaseRepository
from entities.products import Product, StockEntry, StockEntryType

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

    def delete(self, id):
        self.cursor.execute("DELETE FROM products WHERE id = %s", (id,))
        self.conn.commit()

    # --- Phần xử lý Stock Entry ---
    def save_stock_entry(self, entry: StockEntry):
        query = """
            INSERT INTO stock_entries (entry_code, entry_type, quantity, product_id, entry_date)
            VALUES (%s, %s, %s, %s, %s)
        """
        val = (entry.entry_code, entry.type.value, entry.quantity, entry.product_id, entry.entry_date)
        self.cursor.execute(query, val)
        self.conn.commit()
        entry.id = self.cursor.lastrowid
        return entry