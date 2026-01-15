from repositories.user_repository import UserRepository
from entities.base import UserStatus
import hashlib

class UserService:
    def __init__(self):
        self.user_repo = UserRepository()

    def create_user(self, user_obj):
        """Tạo nhân viên mới"""
        # Kiểm tra trùng username
        existing = self.user_repo.find_by_username(user_obj.username)
        if existing:
            raise ValueError("Username đã tồn tại!")
        
        # Hash password trước khi lưu
        user_obj.password_hash = hashlib.sha256(user_obj.password_hash.encode()).hexdigest()
        
        return self.user_repo.save(user_obj)

    def lock_user(self, user_id):
        """Khóa tài khoản nhân viên (Thay vì xóa)"""
        user = self.user_repo.find_by_id(user_id)
        if user:
            user.status = UserStatus.LOCKED
            self.user_repo.save(user)
            print(f"🔒 Đã khóa tài khoản {user.username}")
        else:
            print("Không tìm thấy user.")

    def delete_user(self, user_id):
        """Xóa hẳn nhân viên (Chức năng admin mạnh)"""
        # Cần cẩn trọng vì nếu user đã lập hóa đơn, khóa ngoại (FK) sẽ báo lỗi
        # Ở đây ta giả định xóa được
        self.user_repo.delete(user_id)
        print(f"🗑️ Đã xóa user ID {user_id}")