import hashlib
from repositories.user_repository import UserRepository
from entities.base import UserStatus

class AuthService:
    def __init__(self):
        self.user_repo = UserRepository()

    def hash_password(self, password: str) -> str:
        """Mã hóa mật khẩu bằng SHA-256"""
        return hashlib.sha256(password.encode()).hexdigest()

    def login(self, username, password):
        """
        Xử lý đăng nhập.
        Return: User object nếu thành công, None nếu thất bại.
        """
        user = self.user_repo.find_by_username(username)
        
        if not user:
            print("❌ Tên đăng nhập không tồn tại.")
            return None
        
        if user.status == UserStatus.LOCKED or user.status.value == "Locked":
            print("❌ Tài khoản này đã bị KHÓA. Vui lòng liên hệ quản lý.")
            return None

        hashed_input = self.hash_password(password)
        if hashed_input == user.password_hash:
            print(f"✅ Xin chào, {user.full_name} ({user.role})!")
            return user
        else:
            print("❌ Mật khẩu không đúng.")
            return None

    def change_password(self, user_id, old_pass, new_pass):
        """Người dùng tự đổi mật khẩu"""
        user = self.user_repo.find_by_id(user_id)
        if not user: return False

        # Kiểm tra pass cũ
        if user.password_hash != self.hash_password(old_pass):
            print("❌ Mật khẩu cũ không khớp.")
            return False

        # Cập nhật pass mới
        user.password_hash = self.hash_password(new_pass)
        self.user_repo.save(user)
        print("✅ Đổi mật khẩu thành công!")
        return True