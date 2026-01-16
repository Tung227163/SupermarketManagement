from services.auth_service import AuthService

class AuthController:
    def __init__(self, view):
        self.view = view
        self.auth_service = AuthService()

    def handle_login(self):
        """Xử lý sự kiện nhấn nút Đăng nhập"""
        username = self.view.get_username()
        password = self.view.get_password()

        if not username or not password:
            self.view.show_error("Vui lòng nhập tên đăng nhập và mật khẩu.")
            return None

        # Gọi Service kiểm tra
        user = self.auth_service.login(username, password)
        
        if user:
            self.view.show_success(f"Đăng nhập thành công! Xin chào {user.full_name}")
            self.view.close()
            return user # Trả về User object để Main Window biết ai đang dùng
        else:
            self.view.show_error("Sai tên đăng nhập hoặc mật khẩu (hoặc tài khoản bị khóa).")
            return None