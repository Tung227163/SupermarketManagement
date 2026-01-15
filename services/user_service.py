import hashlib
from repositories.user_repository import UserRepository
from entities.users import Manager, Cashier, WarehouseKeeper
from entities.base import UserStatus

class UserService:
    def __init__(self):
        self.user_repo = UserRepository()

    def create_user(self, username, password, full_name, email, phone, role):
        """Tạo nhân viên mới"""
        # 1. Kiểm tra trùng username
        if self.user_repo.find_by_username(username):
            print(f"❌ Username '{username}' đã tồn tại.")
            return None

        # 2. Hash mật khẩu
        pwd_hash = hashlib.sha256(password.encode()).hexdigest()

        # 3. Khởi tạo đối tượng theo Role
        # ID để None để DB tự sinh
        if role == 'Manager':
            user = Manager(None, username, pwd_hash, full_name, email, phone)
        elif role == 'Cashier':
            user = Cashier(None, username, pwd_hash, full_name, email, phone)
        elif role == 'WarehouseKeeper':
            user = WarehouseKeeper(None, username, pwd_hash, full_name, email, phone)
        else:
            print("❌ Role không hợp lệ.")
            return None

        saved_user = self.user_repo.save(user)
        print(f"✅ Đã tạo nhân viên: {username} - {role}")
        return saved_user

    def update_user_info(self, user_id, full_name, email, phone):
        """Cập nhật thông tin cơ bản"""
        user = self.user_repo.find_by_id(user_id)
        if user:
            user.full_name = full_name
            user.email = email
            user.phone = phone
            self.user_repo.save(user)
            print("✅ Cập nhật thông tin thành công.")
        else:
            print("❌ Không tìm thấy User.")

    def set_user_status(self, user_id, status: UserStatus):
        """Khóa hoặc Mở khóa tài khoản"""
        user = self.user_repo.find_by_id(user_id)
        if user:
            user.status = status
            self.user_repo.save(user)
            print(f"✅ Đã chuyển trạng thái user thành: {status.value}")
        else:
            print("❌ Không tìm thấy User.")

    def reset_password(self, user_id, new_password):
        """Manager cấp lại mật khẩu cho nhân viên"""
        user = self.user_repo.find_by_id(user_id)
        if user:
            user.password_hash = hashlib.sha256(new_password.encode()).hexdigest()
            self.user_repo.save(user)
            print(f"✅ Đã reset mật khẩu cho {user.username}")
        else:
            print("❌ Không tìm thấy User.")
    
    def get_all_users(self):
        return self.user_repo.find_all()