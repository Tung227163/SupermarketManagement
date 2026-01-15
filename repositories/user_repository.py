# repositories/user_repository.py
from repositories.base_repository import BaseRepository
from entities.users import Manager, Cashier, WarehouseKeeper
from entities.base import UserStatus

class UserRepository(BaseRepository):
    
    def _map_row_to_user(self, row):
        """Hàm phụ trợ: Chuyển đổi dữ liệu từ SQL (dict) sang Object Python"""
        if not row:
            return None
        
        role = row['role']
        user_id = row['id']
        # Tạo object tương ứng với Role
        if role == 'Manager':
            user = Manager(user_id, row['username'], row['password_hash'], row['full_name'], row['email'], row['phone'])
        elif role == 'Cashier':
            user = Cashier(user_id, row['username'], row['password_hash'], row['full_name'], row['email'], row['phone'])
        elif role == 'WarehouseKeeper':
            user = WarehouseKeeper(user_id, row['username'], row['password_hash'], row['full_name'], row['email'], row['phone'])
        else:
            return None # Unknown role
        
        # Map thêm các trường base
        user.status = UserStatus(row['status'])
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
        """Lưu mới hoặc cập nhật User"""
        role_name = user.__class__.__name__ # Lấy tên class làm role (Manager, Cashier...)
        
        if user.id is None:
            # INSERT
            query = """
                INSERT INTO users (username, password_hash, full_name, email, phone, status, role)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
            """
            val = (user.username, user.password_hash, user.full_name, user.email, user.phone, user.status.value, role_name)
            self.cursor.execute(query, val)
            self.conn.commit()
            user.id = self.cursor.lastrowid # Cập nhật ID lại cho object
        else:
            # UPDATE
            query = """
                UPDATE users SET full_name=%s, email=%s, phone=%s, status=%s, password_hash=%s
                WHERE id=%s
            """
            val = (user.full_name, user.email, user.phone, user.status.value, user.password_hash, user.id)
            self.cursor.execute(query, val)
            self.conn.commit()
        
        return user

    def delete(self, id):
        query = "DELETE FROM users WHERE id = %s"
        self.cursor.execute(query, (id,))
        self.conn.commit()