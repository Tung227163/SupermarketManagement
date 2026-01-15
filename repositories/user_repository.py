from repositories.base_repository import BaseRepository
from entities.users import Manager, Cashier, WarehouseKeeper
from entities.base import UserStatus

class UserRepository(BaseRepository):
    
    def _map_row_to_user(self, row):
        if not row: return None
        
        role = row['role']
        user_id = row['id']
        status = UserStatus(row['status']) # Chuyển string sang Enum
        
        # Khởi tạo đúng với __init__ mới (không cần truyền role vào constructor vì class tự định nghĩa)
        if role == 'Manager':
            user = Manager(user_id, row['username'], row['password_hash'], row['full_name'], row['email'], row['phone'], status)
        elif role == 'Cashier':
            user = Cashier(user_id, row['username'], row['password_hash'], row['full_name'], row['email'], row['phone'], status)
        elif role == 'WarehouseKeeper':
            user = WarehouseKeeper(user_id, row['username'], row['password_hash'], row['full_name'], row['email'], row['phone'], status)
        else:
            return None 
        
        # Role đã được set tự động trong __init__ của từng class
        user.created_at = row['created_at']
        return user

    def find_all(self):
        query = "SELECT * FROM users"
        self.cursor.execute(query)
        rows = self.cursor.fetchall()
        return [self._map_row_to_user(row) for row in rows]

    def find_by_id(self, id):
        query = "SELECT * FROM users WHERE id = %s"
        self.cursor.execute(query, (id,))
        row = self.cursor.fetchone()
        return self._map_row_to_user(row)

    def find_by_username(self, username):
        query = "SELECT * FROM users WHERE username = %s"
        self.cursor.execute(query, (username,))
        row = self.cursor.fetchone()
        return self._map_row_to_user(row)

    def save(self, user):
        role_name = user.role # Lấy từ thuộc tính role của object
        
        if user.id is None:
            query = """
                INSERT INTO users (username, password_hash, full_name, email, phone, status, role)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
            """
            val = (user.username, user.password_hash, user.full_name, user.email, user.phone, user.status.value, role_name)
            self.cursor.execute(query, val)
            self.conn.commit()
            user.id = self.cursor.lastrowid
        else:
            query = """
                UPDATE users SET full_name=%s, email=%s, phone=%s, status=%s, password_hash=%s, role=%s
                WHERE id=%s
            """
            val = (user.full_name, user.email, user.phone, user.status.value, user.password_hash, role_name, user.id)
            self.cursor.execute(query, val)
            self.conn.commit()
        return user

    def delete(self, id):
        query = "DELETE FROM users WHERE id = %s"
        self.cursor.execute(query, (id,))
        self.conn.commit()