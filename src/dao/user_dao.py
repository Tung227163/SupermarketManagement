"""
User DAO implementation
Demonstrates: Implementation of interface, database operations
"""
from typing import List
from .generic_dao import GenericDAO
from ..models.user import User
from ..utils.database import DatabaseUtil


class UserDAO(GenericDAO[User]):
    """User DAO implementation"""
    
    def create(self, user: User) -> User:
        """Create a new user - demonstrates object as parameter and return type"""
        conn = DatabaseUtil.get_connection()
        cursor = conn.cursor()
        
        try:
            cursor.execute("""
                INSERT INTO users (username, password, full_name, role, is_active)
                VALUES (?, ?, ?, ?, ?)
            """, (user.username, user.password, user.full_name, user.role, user.is_active))
            
            conn.commit()
            user.id = cursor.lastrowid
            return user
        except Exception as e:
            print(f"Error creating user: {e}")
            conn.rollback()
            return None
    
    def find_by_id(self, user_id: int) -> User:
        """Find user by ID"""
        conn = DatabaseUtil.get_connection()
        cursor = conn.cursor()
        
        cursor.execute("SELECT * FROM users WHERE user_id = ?", (user_id,))
        row = cursor.fetchone()
        
        if row:
            return self._extract_user_from_row(row)
        return None
    
    def find_by_code(self, username: str) -> User:
        """Find user by username"""
        conn = DatabaseUtil.get_connection()
        cursor = conn.cursor()
        
        cursor.execute("SELECT * FROM users WHERE username = ?", (username,))
        row = cursor.fetchone()
        
        if row:
            return self._extract_user_from_row(row)
        return None
    
    def find_all(self) -> List[User]:
        """Find all active users"""
        conn = DatabaseUtil.get_connection()
        cursor = conn.cursor()
        
        cursor.execute("SELECT * FROM users WHERE is_active = 1 ORDER BY user_id")
        rows = cursor.fetchall()
        
        return [self._extract_user_from_row(row) for row in rows]
    
    def find_by_name(self, name: str) -> List[User]:
        """Find users by name"""
        conn = DatabaseUtil.get_connection()
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT * FROM users WHERE full_name LIKE ? AND is_active = 1
        """, (f"%{name}%",))
        rows = cursor.fetchall()
        
        return [self._extract_user_from_row(row) for row in rows]
    
    def update(self, user: User) -> bool:
        """Update user"""
        conn = DatabaseUtil.get_connection()
        cursor = conn.cursor()
        
        try:
            cursor.execute("""
                UPDATE users SET username = ?, password = ?, full_name = ?, 
                       role = ?, is_active = ?
                WHERE user_id = ?
            """, (user.username, user.password, user.full_name, 
                  user.role, user.is_active, user.id))
            
            conn.commit()
            return cursor.rowcount > 0
        except Exception as e:
            print(f"Error updating user: {e}")
            conn.rollback()
            return False
    
    def delete(self, user_id: int) -> bool:
        """Soft delete user"""
        conn = DatabaseUtil.get_connection()
        cursor = conn.cursor()
        
        try:
            cursor.execute("UPDATE users SET is_active = 0 WHERE user_id = ?", (user_id,))
            conn.commit()
            return cursor.rowcount > 0
        except Exception as e:
            print(f"Error deleting user: {e}")
            conn.rollback()
            return False
    
    def delete_all(self) -> bool:
        """Soft delete all users"""
        conn = DatabaseUtil.get_connection()
        cursor = conn.cursor()
        
        try:
            cursor.execute("UPDATE users SET is_active = 0")
            conn.commit()
            return cursor.rowcount > 0
        except Exception as e:
            print(f"Error deleting all users: {e}")
            conn.rollback()
            return False
    
    def authenticate(self, username: str, password: str) -> User:
        """Authenticate user"""
        conn = DatabaseUtil.get_connection()
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT * FROM users WHERE username = ? AND password = ? AND is_active = 1
        """, (username, password))
        row = cursor.fetchone()
        
        if row:
            return self._extract_user_from_row(row)
        return None
    
    def _extract_user_from_row(self, row) -> User:
        """Extract User object from database row"""
        user = User(
            user_id=row['user_id'],
            username=row['username'],
            password=row['password'],
            full_name=row['full_name'],
            role=row['role']
        )
        user.is_active = bool(row['is_active'])
        user.created_at = row['created_at']
        return user
