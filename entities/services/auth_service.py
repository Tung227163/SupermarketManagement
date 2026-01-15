import hashlib
from repositories.user_repository import UserRepository

class AuthService:
    def __init__(self):
        self.user_repo = UserRepository()

    def hash_password(self, password: str) -> str:
        """Mã hóa mật khẩu sử dụng SHA-256 (Built-in Python)"""
        return hashlib.sha256(password.encode()).hexdigest()

    def login(self, username, password):
        """
        Kiểm tra đăng nhập.
        Trả về User object nếu thành công, None nếu thất bại.
        """
        user = self.user_repo.find_by_username(username)
        if not user:
            print("❌ User không tồn tại.")
            return None
        
        # Kiểm tra mật khẩu (hash password nhập vào rồi so sánh)
        hashed_input = self.hash_password(password)
        if hashed_input == user.password_hash:
            if user.status.value != "Active":
                print("❌ Tài khoản đang bị khóa.")
                return None
            print(f"✅ Đăng nhập thành công: {user.full_name} ({user.__class__.__name__})")
            return user
        else:
            print("❌ Sai mật khẩu.")
            return None