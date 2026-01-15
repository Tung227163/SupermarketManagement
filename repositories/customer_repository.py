# repositories/customer_repository.py
from repositories.base_repository import BaseRepository
from entities.orders import Customer

class CustomerRepository(BaseRepository):
    
    def _map_row(self, row):
        if not row: return None
        return Customer(row['id'], row['customer_code'], row['name'], row['phone'], row['point'])

    def find_all(self):
        self.cursor.execute("SELECT * FROM customers")
        return [self._map_row(row) for row in self.cursor.fetchall()]

    def find_by_id(self, id):
        self.cursor.execute("SELECT * FROM customers WHERE id = %s", (id,))
        return self._map_row(self.cursor.fetchone())
    
    def find_by_phone(self, phone):
        self.cursor.execute("SELECT * FROM customers WHERE phone = %s", (phone,))
        return self._map_row(self.cursor.fetchone())

    def save(self, customer: Customer):
        if customer.id is None:
            query = "INSERT INTO customers (customer_code, name, phone, point) VALUES (%s, %s, %s, %s)"
            val = (customer.customer_code, customer.name, customer.phone, customer.point)
            self.cursor.execute(query, val)
            self.conn.commit()
            customer.id = self.cursor.lastrowid
        else:
            query = "UPDATE customers SET name=%s, phone=%s, point=%s WHERE id=%s"
            val = (customer.name, customer.phone, customer.point, customer.id)
            self.cursor.execute(query, val)
            self.conn.commit()
        return customer

    def delete(self, id):
        self.cursor.execute("DELETE FROM customers WHERE id = %s", (id,))
        self.conn.commit()